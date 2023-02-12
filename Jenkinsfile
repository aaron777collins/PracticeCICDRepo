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
                sh 'docker build -t practicecicdrepo .' // Build docker image
            }
        }
    }
}
