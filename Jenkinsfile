pipeline {
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Docker Hub credentials stored in Jenkins
        DOCKER_IMAGE = "ujjwalk20/cust_seg_app"
        DOCKER_TAG = "latest"
        REPO_URL = "https://github.com/ujjwalk20/Customer_Segmentation.git"
        MINIKUBE_PATH ="\"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe\""  // Use the absolute path of Minikube

    }

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
                    def dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Use credentials for Docker Hub login
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                            // Push the Docker image to Docker Hub
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes via Minikube') {
            steps {
                script {
                    kubernetesDeploy(
                        configs: 'streamlit-deployment.yaml',  // Deployment YAML file for Kubernetes
                        kubeconfigId: 'minikube-kubeconfig',    // Jenkins kubeconfig ID for accessing Minikube
                        enableConfigSubstitution: true
                    )
                    
                    kubernetesDeploy(
                        configs: 'streamlit-service.yaml',  // Service YAML file for Kubernetes
                        kubeconfigId: 'minikube-kubeconfig',
                        enableConfigSubstitution: true
                    )
                }
            }
        }
          stage('Get Minikube Service URL') {
            steps {
                script {
                    // Capture and print the service URL
                    def minikubeServiceUrl = bat(script: "${env.MINIKUBE_PATH} service streamlit-service --url", returnStdout: true).trim()
                    echo "Minikube Service URL: ${serviceUrl}"
                }
            }
          }
    }
}
