FROM jenkins/jenkins:lts

# Switch to root user to install additional tools
USER root

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    vim \
    inotify-tools

RUN apt install -y python3-poetry

# Switch back to the Jenkins user
USER jenkins

# Skip initial setup wizard and Allow local checkout (INSECURE SETTING APPLIED)
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true

# Set initial admin password
COPY security.groovy /usr/share/jenkins/ref/init.groovy.d/

# Install plugins
RUN jenkins-plugin-cli --plugins "blueocean:latest workflow-aggregator:latest pipeline-stage-view:latest configuration-as-code:latest job-dsl:latest git:latest"

# # Expose the Groovy init scripts directory as a volume
# VOLUME /usr/share/jenkins/ref/init.groovy.d

COPY jenkins.yaml /var/lib/jenkins/jenkins.yaml
COPY seedJob.groovy /var/lib/jenkins/seedJob.groovy

ENV CASC_JENKINS_CONFIG=/var/lib/jenkins/jenkins.yaml
