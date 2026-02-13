pipeline {
    agent any

    environment {
        IMAGE_NAME = "adjemiangerman/api-notes:latest"
        DEPLOYMENT_NAME = "notes-deployment"
        NAMESPACE = "default"
    }

    stages {
        stage('Create Build Pod') {
            steps {
                echo "Creating temporary build pod..."
                sh "kubectl apply -f k8s/build-pod.yaml"
                sh "kubectl wait --for=condition=Ready pod/temp-build --timeout=60s"
            }
        }

        stage('Build and Push Image') {
            steps {
                echo "Building and pushing Docker image..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                        kubectl exec temp-build -- sh -c 'docker build -t ${IMAGE_NAME} /var/jenkins_home/workspace/Actividad_1_develop/api-notes'
                        kubectl exec temp-build -- sh -c 'echo $PASS | docker login -u $USER --password-stdin'
                        kubectl exec temp-build -- docker push ${IMAGE_NAME}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying updated image..."
                sh "kubectl set image deployment/${DEPLOYMENT_NAME} notes=${IMAGE_NAME} -n ${NAMESPACE}"
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
                echo "Deleting temporary build pod..."
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
