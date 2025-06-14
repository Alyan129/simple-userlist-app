pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13'
        CHROME_VERSION = 'latest'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    # Install Python dependencies
                    python -m pip install --upgrade pip
                    pip install -r app/requirements.txt
                    
                    # Install Chrome and ChromeDriver
                    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
                    apt-get update
                    apt-get install -y google-chrome-stable
                    
                    # Install ChromeDriver
                    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
                    wget -N "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}"
                    CHROMEDRIVER_VERSION=$(cat "LATEST_RELEASE_${CHROME_VERSION}")
                    wget -N "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
                    unzip chromedriver_linux64.zip
                    chmod +x chromedriver
                    mv chromedriver /usr/local/bin/
                '''
            }
        }
        
        stage('Start Flask Application') {
            steps {
                sh '''
                    cd app
                    python app.py &
                    sleep 5  # Wait for the application to start
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    cd app
                    python -m unittest tests/test_selenium.py
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                sh '''
                    # Kill the Flask application
                    pkill -f "python app.py"
                '''
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
} 