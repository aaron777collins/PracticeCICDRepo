pipeline {
    agent any

    stages {
        stage('Init') {
            steps {
                echo 'Initializing..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
                docker build -t ghcr.io/aaron777collins/practicecicdrepo:latest .
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying.....'
                docker push ghcr.io/aaron777collins/practicecicdrepo:latest .
            }
        }
    }
}
