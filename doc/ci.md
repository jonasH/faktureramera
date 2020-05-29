# CI description

When time is given this should be in code instead of in docs

## Setup docker

podman volume create jenkins-data

podman build -t jenkins/fm .

podman container run \
  --name jenkins \
  --rm \
  --detach \
  --privileged \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  jenkins/fm
podman exec jenkins bash -c 'cat $JENKINS_HOME/secrets/initialAdminPassword'

podman stop jenkins


## Run tests

QT_QPA_PLATFORM=minimal
export QT_QPA_PLATFORM
make test


Publish JUNIT results with following glob:

build/*_test_result.xml

Publish coverage reports  with following file:

build/coverage.xml