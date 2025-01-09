pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gabriel1502affonso/task-manager-api'
        KUBECONFIG = credentials('docker-desktop-kubeconfig')
    }

    stages {
        stage('Verify Tools') {
            steps {
                container('docker') {
                    sh 'docker --version'
                }
                container('kubectl') {
                    sh 'kubectl version --client'
                }
                container('kubectl') {
                    sh 'helm version'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                    git branch: 'main', url: 'https://github.com/Inutilismo/task-manager-api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.build("${DOCKER_IMAGE}:latest")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub') {
                            docker.image("${DOCKER_IMAGE}:latest").push()
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'docker-desktop-kubeconfig']) {
                    container('kubectl') {
                        sh 'helm upgrade --install task-manager-api ./task-manager-api --namespace task-manager-api'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
