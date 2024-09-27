pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository from your version control system
                git 'https://your-repo-url-here.git'  // Replace with your repository URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile
                    sh 'docker build -t customer-clustering-app:latest .'
                }
            }
        }

        stage('Run Unit Tests in Docker') {
            steps {
                script {
                    // Run unit tests inside a Docker container
                    sh '''
                    docker run --rm customer-clustering-app:latest pytest test_pytest.py
                    '''
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    // Stop and remove any existing container, then deploy the new one
                    sh '''
                    docker stop customer-clustering-app || true
                    docker rm customer-clustering-app || true
                    docker run -d --name customer-clustering-app -p 8501:8501 customer-clustering-app:latest
                    '''
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
