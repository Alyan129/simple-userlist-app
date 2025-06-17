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
                # It's good practice to run Flask in the background for tests if it's part of the Docker image's CMD
                # However, since the Dockerfile CMD runs tests directly, ensure Flask is part of the image.
                # For this setup, we're assuming the Flask app is simple enough that it's just the 'tests' that are run.
                # If the tests need the Flask app running as a service, the Dockerfile or Jenkinsfile might need more orchestration (e.g. docker-compose).
                # For now, this assumes the 'CMD' in Dockerfile is the complete test execution.
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