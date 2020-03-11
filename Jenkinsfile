node {
    stage('Setup Env') {
    sh '''
       echo "Setting up Python Environment"
       # TODO(zf) Make venv off BUILDID
       echo "Creating VirtualEnv"
       virtualenv -p python3 venv
       source ./venv/bin/activate
       pip install -r "./requirements.txt"
    '''
    }
    stage('Unit Test'){
     sh '''
     source ./venv/bin/activate
     ./venv/bin/pytest
     
     '''
    }
    stage('Build Container') {
      sh 'docker build -t sso-api .'
    }
    stage('Integration Tests')
      sh 'sudo docker run --name sso-api-test -d -p 5000:5000 sso-api'
      sh 'curl localhost:5000/api/users'
}
