pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Use Maven to build the project
                echo 'Build...'
                sh ("cp -r /mnt/cicd-django-demo/* .")

            }
        }

        stage('Static Analysis') {
            steps {
                sh ("./cicd2.sh flake8")
            }
        }

        stage("Unit Tests") {
            steps{
                sh("./cicd2.sh unittest")
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
