pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gabriel1502affonso/task-manager-api'
        KUBECONFIG = credentials('docker-desktop-kubeconfig')
    }

    stages {
        stage('Verify Tools') {
            parallel {
                stage('Check Docker') {
                    steps {
                        container('docker') {
                            sh 'docker --version'
                        }
                    }
                }
                stage('Check Kubectl') {
                    steps {
                        container('kubectl') {
                            sh 'kubectl version --client'
                        }
                    }
                }
                stage('Check Helm') {
                    steps {
                        container('kubectl') {
                            sh 'helm version'
                        }
                    }
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
                        docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub') {
                            docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'docker-desktop-kubeconfig']) {
                    container('kubectl') {
                        sh """
                        helm upgrade --install task-manager-api ./task-manager-api \
                        --namespace task-manager-api \
                        --set image.tag=${BUILD_NUMBER}
                        """
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
