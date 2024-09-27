pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository from GitHub
                checkout scm // Assumes GitHub repo is configured in Jenkins
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile
                    docker.build('customer-clustering-app:latest')
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // // Stop and remove any existing container if it is running
                    // def existingContainer = docker ps().find { it.name == 'customer-clustering-app' }
                    // if (existingContainer) {
                    //     docker.stop('customer-clustering-app')
                    //     docker.rm('customer-clustering-app')
                    // }

                    // Run the new container in detached mode and expose the port
                    docker.run('customer-clustering-app:latest', '-d -p 8501:8501 --name customer-clustering-app')
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after the pipeline runs
            cleanWs()
        }

        success {
            // Notify that the pipeline completed successfully
            echo 'Application successfully built and deployed!'
        }

        failure {
            // Notify that the pipeline failed
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
