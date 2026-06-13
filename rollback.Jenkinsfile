pipeline {
    agent any

    stages {
        stage('Switch Traffic to Stable (Green)') {
            steps {
                sh '''
                    kubectl patch service sentiment-api-service -p '{"spec":{"selector":{"app":"sentiment-api","slot":"green"}}}'
                    kubectl get service sentiment-api-service -o yaml | grep -A4 selector
                '''
            }
        }
    }
}
