# Saagie project

This is a template project with Gradle plugin and Gitlab CI/CD configured.
This fake Python project is made of 2 fake python jobs (Collect and Process), a pipeline associating both of them, and a third pyspark job (spark_job).
 

### Usage

In order to work, you need to update the saagie/jobs and saagie/pipeline configuration.
For that, you'll need to specifiy the URL or your Saagie platform along with the credentials inside environment variables : 
* SAAGIE_LOGIN
* SAAGIE_PWD

#### For the jobs
Under the `saagie/jobs` directory : 

`gradle packageCode -PjobName=<collect|process|spark_job> -Penv=<dev|prod>` to zip your Python code

`gradle projectsUpdateJob -PjobName=<jobname> -Penv=<dev|prod>` to update your job on Saagie (will first package your code)

`gradle projectsRunJob -PjobName=<jobname> -Penv=<dev|prod>` to run your job on Saagie (will first update your job on Saagie)

#### For the pipeline
Under the `saagie/pipeline` directory : 

`gradle projectsUpdatePipeline -PenvironmentName=<dev|prod>` to update your pipeline on Saagie

`gradle projectsRunPipeline -PenvironmentName=<dev|prod>` to run your pipeline on Saagie (will first update your pipeline on Saagie)
### CI/CD
The CI/CD pipeline is configured to work in Gitlab on works that way : 
* every time a commit is pushed to the `develop` branch, a CI pipeline is triggered, which will run unit tests and then update the jobs and pipelines on your Saagie DEV environment
* every time a commit is pushed to the `master` branch, a CI pipeline is triggered, which will run unit tests and then update the jobs and pipelines on your Saagie PROD environment

To update this behavior, simply update the `.gitlab-ci.yml` file

### Release note
The release note is automatically set based on the latest commit message and the commit id.
To update this behavior, simply update the `build.gradle` files