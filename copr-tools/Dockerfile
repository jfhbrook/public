FROM jfhbrook/coprctl:0.3.0

RUN dnf install -y copr-rpmbuild fedora-packager gcc go2rpm pyp2spec rpmdevtools rust2rpm tito

VOLUME /root

WORKDIR /workspace
VOLUME /workspace

ENV PS1='[\u@copr-tools \W]\$ '

CMD ["/bin/bash"]
