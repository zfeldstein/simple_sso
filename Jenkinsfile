pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}


 docker run --name jenkins-docker --rm -d --group-add $(stat -c '%g' /var/run/docker.sock) -p 8080:8080 -p 50000:50000  -v jenkins_home:/var/jenkins_home  -v /var/run/docker.sock:/var/run/docker.sock -P jenkins-docker
sudo docker run --name jenkins -d -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts'