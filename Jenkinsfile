pipeline {
    agent any

    environment {
        IMAGE_NAME = "adjemiangerman/api-notes:latest"
        DEPLOYMENT_NAME = "notes-deployment"
        NAMESPACE = "default"
    }

    stages {

        stage('Push Image') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push ${IMAGE_NAME}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying API to Kubernetes..."
                // Si el deployment existe, actualiza la imagen. Si no, aplica el yaml
                sh """
                    kubectl get deployment ${DEPLOYMENT_NAME} -n ${NAMESPACE} && \
                    kubectl set image deployment/${DEPLOYMENT_NAME} notes=${IMAGE_NAME} -n ${NAMESPACE} || \
                    kubectl apply -f k8s/deployment.yaml
                """
            }
        }

        stage('Test API') {
            steps {
                echo "Testing API availability..."
                sh """
                    kubectl run temp-test --rm -i --tty --image=curlimages/curl --restart=Never -- \
                    curl -f http://notes-service.default.svc.cluster.local:80 || exit 1
                """
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
