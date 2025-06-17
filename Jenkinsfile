pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t selenium-tests-app .'
            }
        }
        
        stage('Run Tests in Docker') {
            steps {
                sh 'docker run --rm selenium-tests-app'
            }
        }
    }
    
    post {
        always {
            cleanWs() // Clean up workspace after build
        }
        success {
            echo 'Pipeline completed successfully: All tests passed in Docker!'
        }
        failure {
            echo 'Pipeline failed: Check logs for Docker build or test execution errors.'
        }
    }
} 