node {
  git '…' // checks out Dockerfile & Makefile
  def myEnv = docker.build 'my-environment:snapshot'
  myEnv.inside {
    sh 'make test'
  }
}