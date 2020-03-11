node {
    stage('Setup Env') {
    sh '''
       echo "Setting up Python Environment"
       # TODO(zf) Make venv off BUILDID
       echo "Creating VirtualEnv"
       virtualenv -p python3 venv
       ./venv/bin/pip3 install -r "./requirements.txt"
    '''
    }
    stage('Unit Test'){
     sh './venv/bin/pytest'
    }
    stage('Build Container') {
      sh 'docker build -t sso-api .'
    }
    stage('Integration Tests')
      sh 'sudo docker run --name sso-api-test -d -p 5000:5000 sso-api'
      sh 'curl localhost:5000/api/users'
}
