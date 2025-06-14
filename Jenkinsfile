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
                sh 'docker build -t selenium-tests .'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'docker run --rm selenium-tests'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
} 