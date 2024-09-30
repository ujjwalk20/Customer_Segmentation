pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using Docker plugin
                    dockerImage = docker.build("test_streamlit_app")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    
                    
                    // Run the new container using Docker plugin
                    docker.image("test_streamlit_app").run('-p 8501:8501 ')
                }
            }
        }
    }
}
