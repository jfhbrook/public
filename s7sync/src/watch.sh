set -euo pipefail

export ACCEPT_EULA="${ACCEPT_EULA:-}"

function log-debug {
  s7sync internal log --level debug --pid "$$" "$@"
}

function log-info {
  s7sync internal log --level info --pid "$$" "$@"
  echo -e "($$) \e[36minfo\e[0m:" "$@"
}

function log-warn {
  s7sync internal log --level warn --pid "$$" "$@"
  echo -e "($$) \e[1;33mwarn\e[0m:" "$@"
}

function log-error {
  s7sync internal log --level error --pid "$$" "$@"
}

function log-output {
  sed "s/^/($$) /"
}

export PLATFORM="${PLATFORM:-$(s7sync internal platform)}"

if [ "${PLATFORM}" == windows ]; then
  # TODO: figure out what the windows config path should be - possibly with
  # %USERPROFILE% ?
  log-error "don't know where windows config goes (yet)"
  exit 1
else
  DEFAULT_CONFIG_HOME="${HOME}/.config/s7sync"
fi


# initialize config vars, respecting any values already set in env vars
# TODO: set these entirely in rust
CONFIG_HOME="${CONFIG_HOME:-${DEFAULT_CONFIG_HOME}}"
REPOSITORY_PATH="${REPOSITORY_PATH:-$(pwd)}"
REMOTE=""
BRANCH=""
MIN_POLL_WAIT="${MIN_POLL_WAIT:-1}"  # 1s
MIN_COMMIT_WAIT="${MIN_COMMIT_WAIT:-15}"  # 15s
MIN_PULL_WAIT="${MIN_PULL_WAIT:-600}"  # 10 minutes
MAX_PULL_WAIT="${MAX_PULL_WAIT:-7200}"  # 2 hours
MIN_PUSH_WAIT="${MIN_PUSH_WAIT:-600}"  # 10 minutes
IDLE_TIMEOUT="${IDLE_TIMEOUT:-600}"  # 10 minutes
SESSION_TIMEOUT="${SESSION_TIMEOUT:-1800}"  # 30 minutes
COMMIT_MESSAGE="${COMMIT_MESSAGE:-"automatic commit by s7sync"}"

# in macos, we can use ioreg to get the OS's idle time. things are more
# complicated in other OS's and need tools that - afaik - don't exist yet.
# TODO: push this logic into rust

function get-idle-time {
  case "${PLATFORM}" in
    linux)
      # TODO: the answer isn't so straightforward in linux. wayland has the
      # KDE idle protocol, so we could write a tool that calls that API for
      # us. alternately, swayidle will call actions when it goes idle, and we
      # may prefer to solve the problem from that angle.
      echo -1
      ;;
    macos)
      # see: http://hints.macworld.com/article.php?story=20040330161158532
      echo $(($(ioreg -c IOHIDSystem | sed -e '/HIDIdleTime/ !{ d' -e 't' -e '}' -e 's/.* = //g' -e 'q') / 1000000000))
      ;;
    windows)
      # TODO: write a rust cli wrapping the win32 api bindings + use it here
      # see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getlastinputinfo
      echo -1
      ;;
    *)
      echo -1
      ;;
  esac
}

# The meat and potatoes - this beefy boi procedure watches an individual
# repository!

timestamp=0
session_created_at=0
last_commit_at=0
last_pull_at=0
last_push_at=0
commit_wait=0
pull_wait=0
push_wait=0
session_age=86400  # 1 day
completed_at=0
is_idle=''
took=0
added_files=''
# TODO: get git to say whether or not there are unpushed commits
unpushed_commits=''
# always pull on first start
remote_stale=1

log-debug "MIN_POLL_WAIT='${MIN_POLL_WAIT}'"
log-debug "MIN_COMMIT_WAIT='${MIN_COMMIT_WAIT}'"
log-debug "MIN_PULL_WAIT='${MIN_PULL_WAIT}'"
log-debug "MAX_PULL_WAIT='${MAX_PULL_WAIT}'"
log-debug "MIN_PUSH_WAIT='${MIN_PUSH_WAIT}'"
log-debug "IDLE_TIMEOUT='${IDLE_TIMEOUT}'"
log-debug "SESSION_TIMEOUT='${SESSION_TIMEOUT}'"
log-debug "REPOSITORY_PATH='${REPOSITORY_PATH}'"
log-debug "COMMIT_MESSAGE='${COMMIT_MESSAGE}'"

cd "${REPOSITORY_PATH}"

if [ ! -d .git ]; then
  log-error "TODO: implement auto-init"
  exit 1
fi

if [ -z "${BRANCH}" ]; then
  BRANCH="$(git rev-parse --abbrev-ref HEAD)"
fi

if [ -z "${REMOTE}" ]; then
  REMOTE="$(git branch --list latest --format '%(upstream)' | cut -d / -f 3)"
fi
REMOTE="${REMOTE:-origin}"

log-debug "branch: ${BRANCH}"
log-debug "remote: ${REMOTE}"

git checkout "${BRANCH}" 2>&1 | log-output

while true; do
  timestamp="$(date +%s)"
  commit_wait="$((timestamp - last_commit_at))"
  pull_wait="$((timestamp - last_pull_at))"
  push_wait="$((timestamp - last_push_at))"
  session_age="$((timestamp - session_created_at))"
  idle_time="$(get-idle-time)"

  if [ "${idle_time}" -gt "${IDLE_TIMEOUT}" ]; then
    log-debug "user has been inactive for ${idle_time} seconds and is idle"
    is_idle=1
  elif [ "${idle_time}" -gt 0 ]; then
    log-debug "user was active as of ${idle_time} seconds ago"
    is_idle=''
  fi

  # modified files
  git ls-files -m | while read -r file; do
    if [ -f "${file}" ]; then
      log-debug "adding ${file}"
      git add "${file}" 2>&1 | log-output
    else
      log-debug "removing ${file}"
      git rm "${file}" 2>&1 | log-output
    fi
  done

  # untracked files
  git ls-files --others --exclude-standard | while read -r file; do
    # TODO: include/exclude paths logic
    log-debug "adding ${file}"
    git add "${file}" 2>&1 | log-output
  done

  # files added but not committed
  added_files="$(git diff --cached --name-only --diff-filter=M)"
  if [ -n "${added_files}" ] && [ "${commit_wait}" -gt "${MIN_COMMIT_WAIT}" ]; then
    # TODO: dynamic messages?
    git commit -m "${COMMIT_MESSAGE}" 2>&1 | log-output
    added_files=''
    unpushed_commits=1
    last_commit_at="${timestamp}"
    log-info "$(pwd) committed at: $(date)"
  elif [ "${commit_wait}" -gt "${MIN_COMMIT_WAIT}" ]; then
    log-debug "$(pwd) will commit as soon as there are staged files"
  else
    log-debug "$(pwd) will be committed in $((MIN_COMMIT_WAIT - commit_wait)) seconds"
  fi

  # remote is considered stale if there are unpushed commits *and* we've waited
  # the minimum amount of time
  if [ -n "${unpushed_commits}" ]; then
    # if the session is (probably) unlocked then always consider the remote stale, but
    # otherwise make sure we've waited a sensible amount of time
    if [ "${pull_wait}" -gt "${MIN_PULL_WAIT}" ] || [ "${session_age}" -lt "${SESSION_TIMEOUT}" ]; then
      remote_stale=1
    else
      log-debug "fetch and rebase ${REMOTE}/${BRANCH} in $((MIN_PULL_WAIT - pull_wait)) seconds"
    fi
  elif [ "${pull_wait}" -gt "${MIN_PULL_WAIT}" ]; then
    log-debug "fetch ${REMOTE}/${BRANCH} as soon as there are unpushed commits"
  fi

  if [ -z "${is_idle}" ]; then
     
    # it's *also* considered stale if we haven't pulled since the max wait
    if [ "${pull_wait}" -gt "${MAX_PULL_WAIT}" ]; then
      remote_stale=1
    else
      log-debug "fetch and fast-forward ${REMOTE}/${BRANCH} in $((MAX_PULL_WAIT - pull_wait)) seconds"
    fi

    if [ -n "${remote_stale}" ]; then
      log-info "pulling $(pwd)"
      git pull --rebase 2>&1 | log-output
      last_pull_at="${timestamp}"
      remote_stale=''

      # if the session had expired, assume we made a new one
      if [ "${session_age}" -gt "${SESSION_TIMEOUT}" ]; then
        session_created_at="${timestamp}"
      fi
      log-info "$(pwd) pulled at: $(date)"
    fi

    if [ -n "${unpushed_commits}" ]; then
      # if we've waited before pushing *or* the session is (probably) unlocked, push
      if [ "${push_wait}" -gt "${MIN_PUSH_WAIT}" ] || [ "${session_age}" -lt "${SESSION_TIMEOUT}" ]; then
        log-info "pushing $(pwd)"
        git push 2>&1 | log-output
        unpushed_commits=''
        last_push_at="${timestamp}"

        # if the session had expired, assume we made a new one
        if [ "${session_age}" -gt "${SESSION_TIMEOUT}" ]; then
          session_created_at="${timestamp}"
        fi
      else
        log-debug "push new commits in $((MIN_PUSH_WAIT - timestamp + last_push_at)) seconds"
      fi
    fi
  else
    log-debug "user is idle"
  fi

  completed_at="$(date +%s)"
  took="$((completed_at - timestamp))"

  if [ "${took}" -lt "${MIN_POLL_WAIT}" ]; then
    wait=$((MIN_POLL_WAIT - took))
    sleep "${wait}"
  fi
done
}

function init-repository {
  local repo_path="$1"
  local repo_remote="$2"

  if [ ! -d "${repo_path}" ]; then
    if [ -z "${repo_remote}" ]; then
      # TODO: lazily create the repo + generate the remote using gh
      log-warn "could not find ${repo_path} and don't have a remote to clone from"
    else
      log-info "cloning ${repo_path} from ${repo_remote}"
      git clone "${repo_remote}" "${repo_path}"
    fi
  else
    log-debug "${repo_path} found"
  fi
}
