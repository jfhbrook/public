FROM fedora:latest

RUN dnf install -y copr-cli yq
COPY bin/coprctl /usr/bin/coprctl
RUN chmod +x /usr/bin/coprctl

COPY example/config.yml /root/.config/coprctl/config.yml
VOLUME /root/.config/coprctl

RUN mkdir /workspace
WORKDIR /workspace
VOLUME /workspace

CMD ["/usr/bin/coprctl"]
