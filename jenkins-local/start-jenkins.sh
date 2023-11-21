#!/bin/bash

# Run Jenkins in the background
/usr/local/bin/jenkins.sh &

# Store the process ID (PID) of the last background command
jenkins_pid=$!

# Wait for Jenkins to be accessible at http://localhost:8080/
echo "Waiting for Jenkins to be accessible..."
while ! curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ | grep -q "200"; do
    sleep 1
done

cd /tmp
curl -Os http://localhost:8080/jnlpJars/jenkins-cli.jar 
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:password123 reload-jcasc-configuration

echo http://localhost:8080/
# Wait for Jenkins to finish
wait $jenkins_pid
