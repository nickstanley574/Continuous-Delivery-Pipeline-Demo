theScript = new File('/mnt/cicd-django-demo/Jenkinsfile').getText("UTF-8")
pipelineJob('cicd-demo-local') {
  definition {
    cps {
      script(theScript)
      sandbox()
    }
  }
}