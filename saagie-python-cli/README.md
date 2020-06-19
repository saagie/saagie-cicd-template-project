# Quick Start

saagie-python-cli let you use 2 functions : createProject and addJob.
The createProject function creates for the user all the necessary base folders and files to be able to :
* Add jobs following the gradle-cicd-template
* Use the gradle plugin locally to deploy WIP tests
* Init a git project if necessary with some CI-CD (.gitignore file and .gitlab-ci.yml)
* Use some local folders outside of the git project to put some local project files ('00-Inputs', '01-Data', '02-Pilotage')

To use those functions, one will have to create a 'saagie-properties.json' file at project's root. This file must have the following structure and contain the following information :

	{
	    "url": "https://....io",
	    "platform_id": "1",
	    "saagie_user_env_name": "BUT_SAAGIE_LOGIN",
	    "saagie_pwd_env_name": "BUT_SAAGIE_PWD",
	    "project_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
	}

with :
* url: the platform url
* platform_id: the platforme id
* saagie_user_env_name: the name of an environment variable defined on the machine one use to launch the script and with value the user login on Saagie
* saagie_pwd_env_name: the name of an environment variable defined on the machine one use to launch the script and with value the user password on Saagie
* project_id: the Saagie's project id one want to link the local project to

Usage :
* Clone the saagie-python-cli folder
* cd at folder root and call **python3 saagie-cli.py** with proper arguments

Requirements :
* Python 3.6 (f-strings used in code)
* Having the querySaagieApi package installed (or having the package cloned in saagie-python-cli root) (https://gitlab.com/saagie-group/service/internal/api-saagie)

The command arguments (see python3 saagie-cli.py -h for latest documentation) :

	user@HOST:~/saagie-project$ python3 saagieProject.py -h
	usage: saagieProject.py [-h] [-p PROJECTPATH] [-t {python,pyspark}]
	                        [-c {Extraction,Processing,Smart App}] [--cicd]
	                        [--ide {ST}]
	                        {createProject,addJob} name

	Create base project or add job

	positional arguments:
	  {createProject,addJob}
	                        action to realise : <createProject|addJob>
	  name                  name of the job or project to create

	optional arguments:
	  -h, --help            show this help message and exit
	  -p PROJECTPATH, --projectPath PROJECTPATH
	                        project base path (unix style) to create project or
	                        add job into. Default to current python location
	  -t {python,pyspark}, --technology {python,pyspark}
	                        Job'technology (python, pyspark, ...). Only for
	                        'addJob'
	  -c {Extraction,Processing,Smart App}, --category {Extraction,Processing,Smart App}
	                        Job's category in Saagie ('Extraction', 'Processing'
	                        or 'Smart App')
	  --cicd                If present, add this job to the ci-cd jobs dealt with
	                        the .gitlab-ci.yml file
	  --ide {ST}            Add specific files for the mentioned IDE. Currently
	                        only support 'ST' value. Only for createProject

### createProject

Usage : python3 saagie-cli.py createProject projectName -p /path/to/project 

Create the folder structure and initial files necessary to use the gradle plugin.

### addJob

Usage : python3 saagie-cli.py addJob jobName -p /path/to/project -t <python|pyspark> -c <Extraction|Processing|Smart App> [--cicd --ide ST]

Create the necessary local code files for a new job (a simple HelloWorld file), create a corresponding job in Saagie with the HelloWorld file uploaded, get the job id, create the local gradle file to be able to use the gradle plugin to upload code modification and run the job, create the gradle call in the gitlab-ci.yml file if the --cicd option is passed.
