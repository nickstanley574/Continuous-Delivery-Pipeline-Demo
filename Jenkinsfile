def checkForDeprecation(){
    return True
}



pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        TAG = "${env.JOB_NAME}-jenkins-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build...'
                sh("cp -r /mnt/cicd-django-demo/* .")
                sh("docker build -t cicd-demo-webapp:${env.TAG} . ")
            }
        }

        stage('Style') {
            steps {
              sh(
                    label: "black",
                    script: "docker run -t --rm --name cicd-demo-webapp-local cicd-demo-webapp:${env.TAG} ./cicd.sh black"
                )
            }
        }

        stage("Security") {
            steps{
                echo("####################################################################")
                // sh("docker run -t --rm --name cicd-demo-webapp-local cicd-demo-webapp:${env.TAG} ./cicd.sh security")
                // sh("docker run -v /run/user/1000/docker.sock:/var/run/docker.sock aquasec/trivy image --no-progress --exit-code 1 --exit-on-eol 1 cicd-demo-webapp:${env.TAG}")
            }
        }

        stage("Compliance") {
            steps{
                sh("echo TODO")
            }
        }

        stage("Unit") {
            steps{
                sh("docker run -t --rm --name cicd-demo-webapp-local cicd-demo-webapp:${env.TAG} ./cicd.sh unittest")
            }
        }

        stage("Selenium") {
            agent {
                docker {
                    image 'docker:dind'
                    // Run the container on the node specified at the
                    // top-level of the Pipeline, in the same workspace,
                    // rather than on a new node entirely:
                    reuseNode true
                    args '-u root:root'
                }
            }
            steps{
                sh("ls -al")
                sh("whoami")

                sh("docker run -t --rm -d --name cicd-demo-webapp-local cicd-demo-webapp:${env.TAG} python app.py")
                sh("ifconfig")

                sh("apk add python3 py3-pip")
                sh("pip install selenium docker")
                sh("./cicd.sh selenium")

            }
        }

        stage('Deploy') {
            steps {
                // Deployment steps (e.g., deploy to a server or artifact repository)
                // You may need to customize this based on your deployment process
                echo 'Deploying...'
            }
        }
    }

    post {
        success {
            // Actions to perform when the build is successful
            echo 'Build successful!'

            // You can trigger additional downstream jobs or notifications here
        }
        failure {
            // Actions to perform when the build fails
            echo 'Build failed!'

            // You can trigger additional actions or notifications for failure here
        }
    }
}
