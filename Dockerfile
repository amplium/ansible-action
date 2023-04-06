FROM docker.io/python:3.11.3-alpine

COPY requirements.txt /requirements.txt

RUN set -e \
	&& apk --update --no-cache add git gnupg openssh-client sshpass rsync openssl \
	&& pip install --no-cache-dir --upgrade -r /requirements.txt \
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf \
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -rf \
	&& rm -f requirements.txt

LABEL maintainer="scheatkode <scheatkode@amplium.io>" \
	org.opencontainers.image.authors="scheatkode <scheatkode@amplium.io>" \
	org.opencontainers.image.vendor="amplium" \
	org.opencontainers.image.licenses="MIT" \
	org.opencontainers.image.url="https://github.com/amplium/ansible-action" \
	org.opencontainers.image.documentation="https://github.com/amplium/ansible-action" \
	org.opencontainers.image.source="https://github.com/amplium/ansible-action" \
	org.opencontainers.image.ref.name="Ansible Playbook Action" \
	org.opencontainers.image.title="Ansible Playbook Action" \
	org.opencontainers.image.description="Ansible Playbook Action"

COPY ansible.cfg /etc/ansible/ansible.cfg
COPY main.py     /main.py

ENTRYPOINT ["python", "/main.py"]
