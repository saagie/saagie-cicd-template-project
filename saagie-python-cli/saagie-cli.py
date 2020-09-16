from querySaagieApi import QuerySaagieApiProject
import argparse
from pathlib import Path
import json
import shutil
import os


def main():
    desc = "Create base project or add job"

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("action",
                        help="action to realise : <createProject|addJob>",
                        choices=['createProject', 'addJob'])

    parser.add_argument("name",
                        help="name of the job or project to create")

    parser.add_argument("-p", "--projectPath",
                        help=("project base path (unix style) to create "
                              "project or add job into. Default to current "
                              "python location"))

    parser.add_argument("-m", "--module",
                        help=("Saagie module to choose for the project or "
                              "the job: 'projects' (v2), 'manager' (v1) (or "
                              "'both' for createProject operation only). "
                              "Default to 'projects'"),
                        choices=['projects', 'manager', 'both'],
                        default='projects')

    parser.add_argument("-t", "--technology",
                        help=("Job'technology (python, pyspark, ...). "
                              "Only for 'addJob'"),
                        choices=['python', 'pyspark'])

    parser.add_argument("-c", "--category",
                        help=("Job's category in Saagie ('Extraction', "
                              "'Processing' or 'Smart App')"),
                        choices=['Extraction', 'Processing', 'Smart App'])

    parser.add_argument("--cicd",
                        help=("If present, add this job to the ci-cd jobs "
                              "dealt with the .gitlab-ci.yml file"),
                        action="store_true")

    parser.add_argument("--ide",
                        help=("Add specific files for the mentioned IDE. "
                              "Currently only support 'ST' value. Only "
                              "for createProject"),
                        choices=['ST'])

    args = parser.parse_args()

    if args.action == 'addJob' and (not args.technology or not args.category):
        parser.error("addJob requires --technology (-t) and --category (-c)")

    # Manage options
    if args.action == 'createProject':
        createProject(name=args.name,
                      path=args.projectPath,
                      module=args.module,
                      ide=args.ide)

    if args.action == 'addJob':
        addJob(name=args.name, path=args.projectPath,
               technology=args.technology, category=args.category,
               ide=args.ide, cicd=args.cicd)


def createProject(name, path=None, module='projects', ide=None):
    if not path:
        path = './'

    path = Path(path)

    # Check for existence of path
    if not path.exists():
        raise ValueError(f"'{path}' is not a valid path.")

    # Check for existence of saagie-properties.json file in path
    if not path.joinpath('saagie-properties.json').exists():
        raise FileNotFoundError("There is no 'saagie-properties.json' file in "
                                f"'{path}'. Such a file must exist at the "
                                "project root path, otherwise, information is "
                                "missing. Add it if missing or check the "
                                "'path' parameter provided")

    if ide == 'ST' and not path.joinpath(f"{name}.sublime-project").exists():
        raise FileNotFoundError(f"There is no '{name}.sublime-project' file "
                                f"in '{path}'. Such a file must exist at the "
                                "project root path, otherwise, information is "
                                "missing. Add it if missing or check the "
                                "'path' parameter provided")

    # Create folders
    path_to_copy = Path(__file__).parent.joinpath('project-base')

    for p in path_to_copy.iterdir():
        if p.is_dir():
            shutil.copytree(str(p),
                            str(path.joinpath(p.name)),
                            copy_function=shutil.copy,
                            ignore=lambda scr, names: ['.gitkeep'])
        elif p.is_file():
            shutil.copy(str(p), str(path))
        else:
            print('An element in project-base is neither a file nor a '
                  f'directory : {str(p)}. Not supposed to happen')

    # Create Git specific files
    path_to_copy = Path(__file__).parent.joinpath('project-git')

    for p in path_to_copy.iterdir():
        shutil.copy(str(p), str(path))

    # Load project properties
    with path.joinpath('saagie-properties.json').open() as f:
        saagie_prop = json.load(f)

    # Create template files
    path_to_copy = Path(__file__).parent.joinpath('project-template-files')

    for file in path_to_copy.iterdir():
        # Build.gradle (build v2)
        if (file.name == 'build.gradle') and (module in ['projects', 'both']):
            write_path = path.joinpath('saagie/jobs').joinpath(file.name)

            with file.open(mode='r', encoding='utf-8') as f:
                content = f.read()

            with write_path.open(mode='w', encoding='utf-8') as f:
                f.write(content.format(saagie_prop['url'],
                                       saagie_prop['saagie_user_env_name'],
                                       saagie_prop['saagie_pwd_env_name'],
                                       saagie_prop['platform_id']))

        # Build_manager.gradle (build v1)
        elif (file.name == 'build_manager.gradle') and (module in ['manager', 'both']):
            write_path = path.joinpath('saagie/jobs').joinpath(file.name)

            with file.open(mode='r', encoding='utf-8') as f:
                content = f.read()

            with write_path.open(mode='w', encoding='utf-8') as f:
                f.write(content.format(saagie_prop['url_manager'],
                                       saagie_prop['saagie_user_env_name'],
                                       saagie_prop['saagie_pwd_env_name'],
                                       saagie_prop['platform_id']))

        # Gradle.properties
        elif file.name == 'gradle.properties':
            write_path = path.joinpath('saagie/jobs').joinpath(file.name)
            shutil.copy(str(file), str(write_path))

        # Settings.gradle
        elif file.name == 'settings.gradle':
            write_path = path.joinpath('saagie/jobs').joinpath(file.name)

            with file.open(mode='r', encoding='utf-8') as f:
                content = f.read()

            with write_path.open(mode='w', encoding='utf-8') as f:
                f.write(content.format(name))

    # Add project name to project properties
    saagie_prop['project_name'] = name

    with path.joinpath('saagie-properties.json').open(mode='w') as f:
        json.dump(saagie_prop, f, indent=4)

    # Specific SublimeText
    if ide == 'ST':
        path_to_copy = Path(__file__).parent.joinpath('project-specific-st3')

        for file in path_to_copy.iterdir():
            # Sublime project file
            if file.name == 'project_name.sublime-project':
                with file.open(mode='r', encoding='utf-8') as f:
                    content = json.load(f)

                # Filter to keep only the necessary build systems
                if module == 'projects':
                    content['build_systems'] = [content['build_systems'][0]]

                if module == 'manager':
                    content['build_systems'] = [content['build_systems'][1]]

                write_path = path.joinpath(f"{name}.sublime-project")
                with write_path.open(mode='w', encoding='utf-8') as f:
                    json.dump(content, f, indent="\t")

            # Interpreter docker files
            elif file.name in ('python-docker-launch.ps1',
                               'pyspark-docker-launch.ps1'):
                write_path = path.joinpath(file.name)
                shutil.copy(str(file), str(write_path))

            else:
                print("Not supposed to happen ! A file was added in "
                      "'project-specific-st3' that is not dealt with in this "
                      f"code: {str(file)}")

    print(f'Create Project {name}')


def addJob(name, path=None, technology='python', category='Processing',
           ide=None, cicd=False):
    print(f'Add {technology} Job {name}')

    if not path:
        path = './'

    path = Path(path)

    # Check for existence of path
    if not path.exists():
        raise ValueError(f"'{path}' is not a valid path.")

    # Check for existence of saagie-properties.json file in path
    if not path.joinpath('saagie-properties.json').exists():
        raise FileNotFoundError("There is no 'saagie-properties.json' file in "
                                f"'{path}'. Such a file must exist at the "
                                "project root path, otherwise, information is "
                                "missing. Add it if missing or check the "
                                "'path' parameter provided")

    if not path.joinpath("app").exists():
        raise FileNotFoundError(f"There is no 'app' folder in '{path}'."
                                f"Such a folder must exist at the "
                                "project root path. Run createProject to "
                                "create the right folder structure")

    if not path.joinpath("saagie/jobs").exists():
        raise FileNotFoundError("There is no 'saagie/jobs' folder in "
                                f"'{path}'. Such a folder must exist at the "
                                "project root path. Run createProject to "
                                "create the right folder structure")

    if path.joinpath("app/name").exists():
        raise ValueError("There is already a job '{name}' in '{path}/app/'")

    # Load project properties
    with path.joinpath('saagie-properties.json').open() as f:
        saagie_prop = json.load(f)

    # Create Job in Saagie
    user = os.environ[saagie_prop['saagie_user_env_name']]
    password = os.environ[saagie_prop['saagie_pwd_env_name']]
    saagie = QuerySaagieApiProject(url_saagie=saagie_prop['url'],
                                   id_plateform=saagie_prop['platform_id'],
                                   user=user,
                                   password=password)

    file = Path(__file__).parent.joinpath(f'job-base/{technology}/__main__.py')

    if technology == "python":
        runtime_version = '3.6'
        command_line = 'python {file}'
        release_note = ''
        extra_technology = ''
        extra_technology_version = ''

    elif technology == "pyspark":
        technology = 'spark'
        runtime_version = '2.4'
        command_line = 'spark-submit --py-files={file} __main__.py'
        release_note = ''
        extra_technology = 'Python'
        extra_technology_version = '3.6'

    job = saagie.create_job(job_name=name,
                            project_id=saagie_prop['project_id'],
                            file=str(file),
                            description='desc',
                            category=category,
                            technology=technology,
                            runtime_version=runtime_version,
                            command_line=command_line,
                            release_note=release_note,
                            extra_technology=extra_technology,
                            extra_technology_version=extra_technology_version)

    job_id = job['data']['createJob']['id']

    # Create job folder in 'app'
    path_to_copy = Path(__file__).parent.joinpath(f'job-base/{technology}')
    write_path = path.joinpath(f"app/{name}")

    shutil.copytree(str(path_to_copy), str(write_path),
                    copy_function=shutil.copy)

    # Create specific files
    path_to_copy = Path(__file__).parent.joinpath('job-template-files/')

    for file in path_to_copy.iterdir():
        # gradle-job_name.properties
        if file.name == 'gradle-job_name.properties':
            write_path = path.joinpath(f'saagie/jobs/gradle-{name}.properties')

            with file.open(mode='r', encoding='utf-8') as f:
                content = f.read()

            with write_path.open(mode='w', encoding='utf-8') as f:
                f.write(content.format(job_id,
                                       saagie_prop['project_id'],
                                       name,
                                       'desc',
                                       runtime_version,
                                       command_line,
                                       name,
                                       technology,
                                       extra_technology,
                                       extra_technology_version))

        else:
            print("Not supposed to happen ! A file was added in "
                  "'job-template-files' that is not dealt with in this "
                  f"code: {str(file)}")

    # Update gitlab ci-cd file
    if cicd:
        file_to_modify = path.joinpath('.gitlab-ci.yml')

        with file_to_modify.open(mode='r', encoding='utf-8') as f:
            content = f.read()

        just_after = '  only:\n    - develop\n\ndeploy job to prod'
        gradle_call = ('    - gradle -b saagie/jobs/build.gradle '
                       f'projectsUpdateJob -PjobName={name} -Penv=dev\n')
        content = content.replace(just_after, gradle_call + just_after)

        with file_to_modify.open(mode='w', encoding='utf-8') as f:
            f.write(content)

    # ST3 specificities
    if ide == 'ST':
        # Adding pathmap for job to sublime-project file
        file = path.joinpath(f"{saagie_prop['project_name']}.sublime-project")

        with file.open() as f:
            content = json.load(f)

        interpreter = content['settings']['python_interpreter']

        if technology == 'python':
            docker_path = '/sandbox'
        elif technology == 'spark':
            docker_path = '/opt/spark/work-dir'

        local_path = '${folder}\\app'

        if name != 'utils':
            pathmap = f'pathmap={local_path}\\{name}\\,{docker_path}/'
        else:
            pathmap = f'pathmap={local_path}\\{name}\\,{docker_path}/utils/'

        if interpreter[-1] == '9':
            interpreter += f"?{pathmap}"
        else:
            interpreter += f"&{pathmap}"

        content['settings']['python_interpreter'] = interpreter

        with file.open(mode='w') as f:
            json.dump(content, f, indent="\t")


if __name__ == '__main__':
    main()
