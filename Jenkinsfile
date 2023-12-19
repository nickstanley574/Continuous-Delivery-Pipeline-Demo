def checkForDeprecation(){
    return True
}



pipeline {
    agent {
        docker {
            image 'docker:dind'
            reuseNode true
            args '-u root:root'
        }
    }
    // agent any
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
                sh("docker build --no-cache -t cicd-demo-webapp:${env.TAG} . ")
            }
        }
        stage("Selenium") {
            steps{
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
