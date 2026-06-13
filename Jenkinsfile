pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'ashesdock'
        IMAGE_NAME = 'sentiment-api'
    }

    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run') {
            steps {
                sh '''
                    docker rm -f sentiment-test || true
                    mkdir -p logs

                    docker build --pull=false -t ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable .

                    docker run -d --name sentiment-test -p 5000:5000 -v "$PWD/logs:/app/logs" ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable

                    for i in $(seq 1 30); do
                        curl -fs http://127.0.0.1:5000/health && exit 0
                        sleep 1
                    done

                    echo "App did not become healthy in time"
                    docker logs sentiment-test
                    exit 1
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    docker run --rm --network host -e BASE_URL=http://127.0.0.1:5000 ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable pytest tests/test_api.py -q
                '''
            }
        }

        stage('UI Test') {
            steps {
                sh '''
                    docker run --rm --network host -e BASE_URL=http://127.0.0.1:5000 ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable pytest tests/test_ui.py -q
                '''
            }
        }

        stage('Build and Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable

                        rm -rf stable-build
                        git clone --branch stable-fallback https://github.com/blackwatermelon0000/selfhealing-mlops-FA23-BAI-010.git stable-build

                        docker build --pull=false -t ${DOCKERHUB_USER}/${IMAGE_NAME}:stable stable-build
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:stable
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/pvc.yaml
                    kubectl apply -f k8s/blue-deployment.yaml
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl get pods
                    kubectl get svc sentiment-api-service
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f sentiment-test || true
                rm -rf stable-build || true
            '''
        }
    }
}
