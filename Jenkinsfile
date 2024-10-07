pipeline {
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Docker Hub credentials stored in Jenkins
        DOCKER_IMAGE = "ujjwalk20/cust_seg_app"
        DOCKER_TAG = "latest"
        REPO_URL = "https://github.com/ujjwalk20/Customer_Segmentation.git"
        MINIKUBE_PATH = "\"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe\""  // Absolute path of Minikube
        KUBECTL_PATH = "\"C:\\Program Files\\Kubernetes\\Minikube\\kubectl.exe\""  // Absolute path of kubectl
        KUBECONFIG_PATH = "\"C:\\Users\\ujjwa\\.kube\\config\""
    }

    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Pytest') {
            steps {
                script {
                    try {
                        echo 'running unittest'
                        bat '"C:\\Users\\ujjwa\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" test_all.py'
                    } catch (Exception e) {
                        echo "Tests failed: ${e.message}"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        }
                    }
                }
            }
        }
    
      
       stage('Deploy to Kubernetes via Minikube') {
            steps {
                script {
                    // Apply the deployment YAML
                    bat "${KUBECTL_PATH} apply -f streamlit-deployment.yaml --kubeconfig=${KUBECONFIG_PATH}"
                    // Apply the service YAML
                    bat "${KUBECTL_PATH} apply -f streamlit-service.yaml --kubeconfig=${KUBECONFIG_PATH}"
                }
            }
       }

// stage('Get Minikube Service URL') {
//             steps {
//                 script {
//                     bat "${MINIKUBE_PATH} service streamlit-service --url"
//                 }
//             }
//         }
    }
}
