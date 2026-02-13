pipeline {
    agent any

    environment {
        IMAGE_NAME = "adjemiangerman/api-notes:latest"
        DEPLOYMENT_NAME = "notes-deployment"
        NAMESPACE = "default"
    }

    stages {
        stage('Build Image') {
            steps {
                echo "Building Docker image..."
                script {
                    sh "docker build -t ${IMAGE_NAME} ./api-notes"
                }
            }
        }

        stage('Push Image') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker push ${IMAGE_NAME}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                sh """
                kubectl set image deployment/${DEPLOYMENT_NAME} notes=${IMAGE_NAME} -n ${NAMESPACE} || \
                kubectl apply -f k8s/deployment.yaml
                """
            }
        }

        stage('Test API') {
            steps {
                echo "Testing API..."
                sh "kubectl port-forward svc/notes-service 8080:80 & sleep 5"
                sh "curl -f http://localhost:8080 || exit 1"
            }
        }

        stage('Cleanup Build Pod') {
            steps {
                echo "Removing temporary build pod (if any)..."
                sh "kubectl delete pod temp-build || true"
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
