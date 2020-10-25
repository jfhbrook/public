while :; do
  inotifywait ./build.py ./themes/* ./base.yml
  python ./build.py
done
