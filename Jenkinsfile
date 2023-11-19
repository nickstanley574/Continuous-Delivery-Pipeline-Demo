pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Use Maven to build the project
                echo 'Build...'

            }
        }

        stage('Test') {
            steps {
                // Run tests (customize according to your testing framework)
                echo 'Testing...'
                sh ("./testing.sh")
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
