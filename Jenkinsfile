pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Build...'
                sh("cp -r /mnt/cicd-django-demo/* .")
                sh("docker build -t cicd-demo-webapp:local-${env.BUILD_NUMBER} . ")
            }
        }

        stage('Style Checks') {
            steps {
                sh("docker run -it --rm --name cicd-demo-webapp-local cicd-demo-webapp:local ./cicd.sh flake8")
                sh("./cicd.sh black")
            }
        }

        stage("Security") {
            steps{
                sh("./cicd.sh security")
            }
        }

        stage("Unit Tests") {
            steps{
                sh("./cicd.sh unittest")
            }
        }

        stage("Selenium") {
            steps{
                echo "TODO"
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
