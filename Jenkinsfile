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
                    // Build the Docker image using Docker plugin// 
                    dockerImage = docker.build("customer_segmentation_app1")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    
                    
                    // Run the new container using Docker plugin 
                    // add -d to run in detached mode
                    docker.image("customer_segementation_app1").run('-p 8501:8501')
                }
            }
        }
    }
}
