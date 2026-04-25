pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gokulggowdabits/aceest-fitness"
        DOCKER_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/gokulggowda-bits/aceest-fitness-devops.git',
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Lint') {
            steps {
                sh "docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} flake8 app.py --max-line-length=120"
            }
        }

        stage('Test') {
            steps {
                sh "docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} pytest tests/ -v"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl set image deployment/aceest-fitness aceest-fitness=${DOCKER_IMAGE}:${DOCKER_TAG} --kubeconfig=${KUBECONFIG}"
                sh "kubectl rollout status deployment/aceest-fitness --kubeconfig=${KUBECONFIG}"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Build #${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline failed. Rolling back..."
            sh "kubectl rollout undo deployment/aceest-fitness --kubeconfig=${KUBECONFIG} || true"
        }
    }
}