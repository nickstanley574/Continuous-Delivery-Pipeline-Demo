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
        IMAGE = "simple-task-app"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build...'
                sh("cp -r /mnt/cicd-django-demo/* .")
                sh("cp -r /mnt/cicd-django-demo/.trivyignore .")
                sh("cp -r /mnt/cicd-django-demo/.approved-dep.csv .")

                // Create all dependencies test code
                sh("docker build --no-cache --target builder -t ${IMAGE}:${env.TAG}-builder . ")
                
                // Final App Image
                sh("docker build --target app -t ${IMAGE}:${env.TAG} . ")
            }
        }

        stage("Selenium") {
            steps{
                sh("""
                cd app/
                # python -m unittest test_selenium.SeleniumTestCase.test_task_order  --verbose
                python -m unittest test_selenium.py --verbose
                """)    
            }
        }

        stage('ClamAV') {
            steps {
                sh("docker build --build-arg base_image=${IMAGE}:${env.TAG} -f Dockerfile-clamav.dockerfile -t ${env.TAG}-temp-clamav  .")
                sh("docker build --build-arg base_image=${IMAGE}:${env.TAG}-builder -f Dockerfile-clamav.dockerfile -t ${env.TAG}-temp-clamav  .")
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
