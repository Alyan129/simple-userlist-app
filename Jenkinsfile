pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
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
                    # Install Python
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip
                    
                    # Install Python dependencies
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r app/requirements.txt
                    
                    # Install Chrome and ChromeDriver
                    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
                    sudo apt-get update
                    sudo apt-get install -y google-chrome-stable
                    
                    # Install ChromeDriver
                    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
                    wget -N "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}"
                    CHROMEDRIVER_VERSION=$(cat "LATEST_RELEASE_${CHROME_VERSION}")
                    wget -N "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
                    unzip chromedriver_linux64.zip
                    chmod +x chromedriver
                    sudo mv chromedriver /usr/local/bin/
                '''
            }
        }
        
        stage('Start Flask Application') {
            steps {
                sh '''
                    cd app
                    python3 app.py &
                    sleep 5  # Wait for the application to start
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    cd app
                    python3 -m unittest tests/test_selenium.py
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                sh '''
                    # Kill the Flask application
                    pkill -f "python3 app.py"
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