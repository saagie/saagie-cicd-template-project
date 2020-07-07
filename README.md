Repository Organization:  
Master Branch: Python Gradle and gitlab CI/CD template  
template_project_scala Branch: Spark Scala Gradle and gitlab CI/CD template  

# Saagie project

This is a template project with Gradle plugin and Gitlab CI/CD configured.
This fake Scala / Spark project is made of 2 fake scala jobs. 

### Usage

In order to work, you need to update the saagie gradle configuration (`saagie/build.gradle` and `gradle-<dev|prod>.properties`).
Configuration of the `saagie/build.gradle` file:
- fileName: change the filename with the correct jar path (e.g. "../target/scala-<scala_version>/<name>-<version>.jar")
<br>

Configuration of the `gradle-<dev|prod>.properties` file:
- URL of the platform (e.g. https://saagie-manager.prod.saagie.io/manager)
- ID of the platform (https://saagie-manager.prod.saagie.io/manager/platform/6 => ID of platform is 6)
- ID of jobs (Findable in the URL (https://saagie-manager.prod.saagie.io/manager/platform/6/#/manager/6/job/1 => ID of job is 1))
- Command of the jobs (e.g. HADOOP_USER_NAME=hdfs spark-submit --executor-memory 4G --executor-cores 2 --driver-memory 2G --total-executor-cores 4 --class=io.saagie.spark.template_test {file})
- The credentials inside environment variables : 
    * SAAGIE_LOGIN
    * SAAGIE_PWD

#### For the jobs
Under the `saagie` directory : 

`gradlew packageCode -Penv=<dev|prod>` to zip your Python code

`gradlew UpdateJob -Penv=<dev|prod>` to update your job on Saagie (will first package your code)

`gradlew RunJob -Penv=<dev|prod>` to run your job on Saagie (will first update your job on Saagie)

### CI/CD
The CI/CD pipeline is configured to work in Gitlab on works that way : 
* every time a commit is pushed to the `develop` branch, a CI pipeline is triggered, which will run unit tests and then update the jobs and pipelines on your Saagie DEV environment
* every time a commit is pushed to the `master` branch, a CI pipeline is triggered, which will run unit tests and then update the jobs and pipelines on your Saagie PROD environment

To update this behavior, simply update the `.gitlab-ci.yml` file

For more information on CI / CD in Gitlab, you can go [here](https://docs.gitlab.com/ee/ci/).

### Release note
The release note is automatically set based on the latest commit message and the commit id.
To update this behavior, simply update the `build.gradle` files