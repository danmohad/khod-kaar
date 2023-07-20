# TODO Add a Dockerfile for just running the containerized application, not VSCode

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3-bullseye, 3.10-bullseye, 3-buster, 3.10-buster
ARG VARIANT=3-bullseye
FROM python:3.10

ARG OPENAI_API_KEY
ARG OPENAI_ORG_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV OPENAI_ORG_KEY=$OPENAI_ORG_KEY

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
# Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
&& apt-get purge -y imagemagick imagemagick-6-common

# Temporary: Upgrade python packages due to https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40897
# They are installed by the base image (python) which does not have the patch.
RUN python3 -m pip install --upgrade setuptools

# Install Chromium for web browsing
RUN apt-get install -y chromium-driver

# Install vim for command-line file editing
RUN apt-get install -y vim

# Install java and graphviz for PlantUML
RUN apt-get install -y default-jre graphviz

# Get PlantUML .jar
RUN wget -O plantuml.jar http://sourceforge.net/projects/plantuml/files/plantuml.jar/download
RUN mkdir /usr/local/plantuml
RUN mv plantuml.jar /usr/local/plantuml/plantuml.jar

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY ../requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1
