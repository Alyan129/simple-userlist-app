pipeline {
    agent any
    stages {
        stage('Clean DevOps directory') {
            steps {
                sh '''
                if [ -d "/var/lib/jenkins/DevOps/" ]; then
                    find "/var/lib/jenkins/DevOps/" -mindepth 1 -delete
                    echo "Cleaned DevOps directory."
                fi
                '''
            }
        }

        stage('Clone from GitHub') {
            steps {
                sh 'git clone https://github.com/Alyan129/simple-userlist-app.git /var/lib/jenkins/DevOps/app/'
            }
        }

        stage('Run Docker Compose') {
            steps {
                dir('/var/lib/jenkins/DevOps/app/') {
                    sh 'docker-compose -p myapp up -d'
                }
            }
        }
    }
}
