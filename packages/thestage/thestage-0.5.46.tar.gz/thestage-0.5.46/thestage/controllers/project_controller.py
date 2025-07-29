import time
from pathlib import Path
from typing import Optional, List

import re

import typer
from typing_extensions import Annotated

from thestage.controllers.utils_controller import validate_config_and_get_service_factory, get_current_directory
from thestage.entities.project_inference_simulator import ProjectInferenceSimulatorEntity
from thestage.entities.project_inference_simulator_model import ProjectInferenceSimulatorModelEntity
from thestage.entities.project_task import ProjectTaskEntity
from thestage.helpers.logger.app_logger import app_logger
from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.enums.inference_model_status import InferenceModelStatus
from thestage.services.clients.thestage_api.dtos.enums.inference_simulator_status import InferenceSimulatorStatus
from thestage.services.clients.thestage_api.dtos.inference_controller.get_inference_simulator_response import \
    GetInferenceSimulatorResponse
from thestage.services.logging.logging_service import LoggingService
from thestage.services.project.dto.project_config import ProjectConfig
from thestage.services.project.mapper.project_inference_simulator_mapper import ProjectInferenceSimulatorMapper
from thestage.services.project.mapper.project_inference_simulator_model_mapper import \
    ProjectInferenceSimulatorModelMapper
from thestage.services.project.mapper.project_task_mapper import ProjectTaskMapper
from thestage.services.project.project_service import ProjectService
from thestage.services.task.dto.task_dto import TaskDto

app = typer.Typer(no_args_is_help=True, help=__("Manage projects"))
inference_simulators_app = typer.Typer(no_args_is_help=True, help="Manage project inference simulators")
app.add_typer(inference_simulators_app, name="inference-simulator")
inference_simulator_model_app = typer.Typer(no_args_is_help=True, help="Manage project inference simulator models")
app.add_typer(inference_simulator_model_app, name="model")
task_app = typer.Typer(no_args_is_help=True, help=__("Manage project tasks"))
config_app = typer.Typer(no_args_is_help=True, help=__("Manage project config"))
app.add_typer(task_app, name="task")
app.add_typer(config_app, name="config")


@app.command(name='clone', no_args_is_help=True, help=__("Clone project repository to empty directory"))
def clone(
        project_uid: str = typer.Argument(
            help=__("Project unique ID"),
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to the working directory: current directory used by default"),
            is_eager=False,
        ),
):
    """
        Clones project to current working directory
    """
    app_logger.info(f'Start project clone from {get_current_directory()}')
    if not working_directory:
        working_directory = get_current_directory().joinpath(project_uid)

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.clone_project(
        config=config,
        project_slug=project_uid,
    )

    typer.echo(__("Project successfully cloned to %path%", {"path": config.runtime.working_directory}))
    raise typer.Exit(0)


@app.command(name='init', no_args_is_help=True, help=__("Initialize project repository with existing files"))
def init(
        project_uid: Optional[str] = typer.Argument(
            help=__("Project unique ID"),
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Initializes project in current working directory
    """
    app_logger.info(f'Start project init from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()
    project_config = service_factory.get_config_provider().read_project_config()

    if project_config:
        typer.echo(__("Directory is initialized and already contains working project"))
        raise typer.Exit(1)

    project_service.init_project(
        project_slug=project_uid,
        config=config,
    )

    typer.echo(__("Project successfully initialized at %path%", {"path": config.runtime.working_directory}))
    raise typer.Exit(0)


@app.command(name='run', no_args_is_help=True, help=__("Run a task within the project. By default, it uses the latest commit from the main branch and streams real-time task logs."))
def run(
        command: Annotated[List[str], typer.Argument(
            help=__("Command to run (required)"),
        )],
        commit_hash: Optional[str] = typer.Option(
            None,
            '--commit-hash',
            '-hash',
            help=__("Commit hash to use. By default, the current HEAD commit is used."),
            is_eager=False,
        ),
        docker_container_slug: Optional[str] = typer.Option(
            None,
            '--container-uid',
            '-cid',
            help=__("Docker container unique ID"),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            show_default=False,
            is_eager=False,
        ),
        enable_log_stream: Optional[bool] = typer.Option(
            True,
            " /--no-logs",
            " /-nl",
            help=__("Disable real-time log streaming"),
            is_eager=False,
        ),
        task_title: Optional[str] = typer.Option(
            None,
            "--title",
            "-t",
            help=__("Provide a custom task title. Git commit message is used by default."),
            is_eager=False,
        ),
):
    """
        Runs a task within a project
    """
    app_logger.info(f'Start project run from {get_current_directory()}')

    if not command:
        typer.echo(__('Command is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    task: Optional[TaskDto] = project_service.project_run_task(
        config=config,
        run_command=" ".join(command),
        commit_hash=commit_hash,
        docker_container_slug=docker_container_slug,
        task_title=task_title,
    )

    if enable_log_stream:
        logging_service: LoggingService = service_factory.get_logging_service()

        logging_service.stream_task_logs_with_controls(
            config=config,
            task_id=task.id
        )

    raise typer.Exit(0)


@task_app.command(name='cancel', no_args_is_help=True, help=__("Cancel a task by ID"))
def cancel_task(
        task_id: Annotated[int, typer.Argument(
            help=__("Task ID (required)"),
        )],
):
    """
        Cancels a task
    """
    app_logger.info(f'Start cancel task from {get_current_directory()}')

    if not task_id:
        typer.echo(__('Task ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.cancel_task(
        config=config,
        task_id=task_id
    )

    raise typer.Exit(0)


@task_app.command("ls", help=__("List tasks"))
def list_runs(
        project_uid: Annotated[str, typer.Argument(help=__("Project unique ID. By default, project info is taken from the current directory"), metavar="OPTIONAL")] = None,
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Set number of rows displayed per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Set starting page for displaying output"),
            is_eager=False,
        ),
):
    """
        Lists tasks for a project
    """
    app_logger.info(f'Start project list-runs from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()
    project_service: ProjectService = service_factory.get_project_service()

    project_service.print_task_list(config, project_uid, row, page)

    typer.echo(__("Tasks listing complete"))
    raise typer.Exit(0)


@task_app.command(name="logs", no_args_is_help=True, help=__("Stream real-time task logs or view last logs for a task"))
def task_logs(
        task_id: Optional[int] = typer.Argument(help=__("Task ID"),),
        logs_number: Optional[int] = typer.Option(
            None,
            '--number',
            '-n',
            help=__("Display a number of latest log entries. No real-time stream if provided."),
            is_eager=False,
        ),
):
    """
        Streams real-time task logs
    """
    app_logger.info(f'View task logs')

    if not task_id:
        typer.echo(__('Task ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    logging_service: LoggingService = service_factory.get_logging_service()

    if logs_number is None:
        logging_service.stream_task_logs_with_controls(
            config=config,
            task_id=task_id
        )
    else:
        logging_service.print_last_task_logs(config=config, task_id=task_id, logs_number=logs_number)

    app_logger.info(f'Task logs - end')
    raise typer.Exit(0)


@app.command(name='checkout', no_args_is_help=True, help=__("Checkout project repository to a specific reference"))
def checkout_project(
        reference: Optional[str] = typer.Argument(
            help=__("Task ID or branch name to checkout. '/' will try to identify the main branch."),
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Checkout project in current working directory
    """
    app_logger.info(f'Start project checkout from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    task_id: Optional[int] = None
    branch_name: Optional[str] = None

    if reference == "/":
        pass
    elif reference.isdigit():
        task_id = int(reference)
    else:
        branch_name = reference

    project_service.checkout_project(
        config=config,
        task_id=task_id,
        branch_name=branch_name
    )

    raise typer.Exit(0)


@app.command(name='pull', help=__("Pulls the changes from the remote project repository. Equivalent to 'git pull'."))
def pull_project(
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Pull project in current working directory
    """
    app_logger.info(f'Start project pull from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.pull_project(
        config=config,
    )

    raise typer.Exit(0)


@app.command(name='reset', help=__("Resets the current project branch to remote counterpart. All working tree changes will be lost. Equivalent to 'git fetch && git reset --hard origin/{ref}'."))
def reset_project(
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Pull project in current working directory
    """
    app_logger.info(f'Start project pull from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.reset_project(
        config=config
    )

    raise typer.Exit(0)


@config_app.command(name='set-default-container', no_args_is_help=True, help=__("Set default docker container for a project installation"))
def set_default_container(
        container_uid: Annotated[Optional[str], typer.Argument(
            help=__("Unique ID of the container to use by default for running tasks"),
        )] = None,
        unset_default_container: Optional[bool] = typer.Option(
            False,
            "--unset",
            "-u",
            help=__("Unsets the default docker container"),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Initializes project in current working directory
    """
    app_logger.info(f'Start project init from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    if unset_default_container and container_uid:
        typer.echo("Container unique ID is provided along with unset flag. Please pick one.")
        raise typer.Exit(1)

    if not unset_default_container and not container_uid:
        typer.echo("Provide container unique ID or use '--unset' flag")
        raise typer.Exit(1)

    project_service = service_factory.get_project_service()

    project_service.set_default_container(
        config=config,
        container_uid=container_uid,
    )

    raise typer.Exit(0)


@config_app.command(name='get', no_args_is_help=False, help=__("View config for a local project installation"))
def get_project_config(
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Initializes project in current working directory
    """
    app_logger.info(f'Start project init from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.print_project_config(
        config=config,
    )

    raise typer.Exit(0)


@inference_simulators_app.command(name='run', no_args_is_help=True, help="Run an inference simulator within the project")
def run_inference_simulator(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator unique ID"), ),
        rented_instance_unique_id: Optional[str] = typer.Option(
            None,
            '--rented-instance-unique-id',
            '-ruid',
            help=__("The rented instance unique ID on which the inference simulator will run"),
            is_eager=False,
        ),
        self_hosted_instance_unique_id: Optional[str] = typer.Option(
            None,
            '--self-hosted-instance-unique-id',
            '-suid',
            help=__("The self-hosted instance unique ID on which the inference simulator will run"),
            is_eager=False,
        ),
        commit_hash: Optional[str] = typer.Option(
            None,
            '--commit-hash',
            '-hash',
            help=__("Commit hash to use. By default, the current HEAD commit is used."),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory. By default, the current directory is used"),
            show_default=False,
            is_eager=False,
        ),
        enable_log_stream: Optional[bool] = typer.Option(
            True,
            " /--no-logs",
            " /-nl",
            help=__("Disable real-time log streaming"),
            is_eager=False,
        ),
        is_skip_installation: Optional[bool] = typer.Option(
            False,
            "--skip-installation",
            "-si",
            help=__("Skip installing dependencies from requirements.txt and install.sh"),
            is_eager=False,
        ),
):
    """
        Run an inference simulator within a project
    """

    if unique_id and not re.match(r"^[a-zA-Z0-9-]+$", unique_id):
        raise typer.BadParameter(__("Invalid UID format. The UID can only contain letters, numbers, and hyphens."))

    app_logger.info(f'Running an inference simulator from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    working_dir_path = Path(working_directory) if working_directory else Path(config.runtime.working_directory)
    inference_files = list(working_dir_path.rglob("inference.py"))
    if not inference_files:
        typer.echo("No inference.py file found in the project directory.")
        raise typer.Exit(1)
    elif len(inference_files) == 1:
        selected_inference = inference_files[0]
    else:
        choices = [str(path.relative_to(working_dir_path)) for path in inference_files]
        typer.echo("Multiple inference.py files found:")
        for idx, choice in enumerate(choices, start=1):
            typer.echo(f"{idx}) {choice}")
        choice_str = typer.prompt("Choose which inference.py to use")
        try:
            choice_index = int(choice_str)
        except ValueError:
            raise typer.BadParameter("Invalid input. Please enter a number.")
        if not (1 <= choice_index <= len(choices)):
            raise typer.BadParameter("Choice out of range.")
        selected_inference = inference_files[choice_index - 1]

    relative_inference = selected_inference.relative_to(working_dir_path)
    parent_dir = relative_inference.parent
    if parent_dir == Path("."):
        inference_dir = "/"
    else:
        inference_dir = f"{parent_dir.as_posix()}/"
    typer.echo(f"Selected inference file relative path: {inference_dir}")

    project_service = service_factory.get_project_service()

    project_service.project_run_inference_simulator(
        config=config,
        commit_hash=commit_hash,
        slug=unique_id,
        rented_instance_unique_id=rented_instance_unique_id,
        self_hosted_instance_unique_id=self_hosted_instance_unique_id,
        inference_dir=inference_dir,
        is_skip_installation=is_skip_installation,
    )

    if enable_log_stream:
        logging_service: LoggingService = service_factory.get_logging_service()

        logging_service.stream_inference_simulator_logs_with_controls(
            config=config,
            slug=unique_id
        )
    raise typer.Exit(0)


@inference_simulators_app.command(name='save-metadata', no_args_is_help=True, help="Get and save inference simulator metadata")
def get_and_save_inference_simulator_metadata(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator unique ID"),),
        file_path: Optional[str] = typer.Option(
            None,
            "--file-path",
            "-fp",
            help=__("Full path to a new file. By default metadata is saved to the current directory as metadata.json"),
            show_default=False,
            is_eager=False,
        ),
):
    """
        Get and save inference simulator metadata
    """

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.project_get_and_save_inference_simulator_metadata(
        config=config,
        file_path=file_path,
        slug=unique_id,
    )

    raise typer.Exit(0)


@inference_simulators_app.command(name='push', no_args_is_help=True, help="Push an inference simulator within the project to model registry")
def push_inference_simulator(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator unique ID"),),
):
    """
        Push an inference simulator within a project to AWS
    """
    app_logger.info(f'Pushing an inference simulator')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.project_push_inference_simulator(
        config=config,
        slug=unique_id,
    )

    raise typer.Exit(0)


@inference_simulators_app.command("ls", help=__("List inference simulators"))
def list_inference_simulators(
        project_uid: Annotated[str, typer.Argument(help=__("Project unique ID. By default, project info is taken from the current directory"), metavar="OPTIONAL")] = None,
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Set number of rows displayed per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Set starting page for displaying output"),
            is_eager=False,
        ),
        statuses: List[str] = typer.Option(
            None,
            '--status',
            '-s',
            help=__("Filter by status, use --status all to list all inference simulators"),
            is_eager=False,
        ),
):
    """
        Lists inference simulators for a project
    """
    app_logger.info(f'Start project list inference simulators from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()
    project_service: ProjectService = service_factory.get_project_service()

    project_service.print_inference_simulator_list(config, project_uid, statuses, row, page)

    typer.echo(__("Inference simulators listing complete"))
    raise typer.Exit(0)


@inference_simulator_model_app.command("ls", help=__("List inference simulator models"))
def list_inference_simulator_models(
        project_uid: Annotated[str, typer.Argument(help=__("Project unique ID. By default, project info is taken from the current directory"), metavar="OPTIONAL")] = None,
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Set number of rows displayed per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Set starting page for displaying output"),
            is_eager=False,
        ),
        statuses: List[str] = typer.Option(
            None,
            '--status',
            '-s',
            help=__("Filter by status, use --status all to list all inference simulator models"),
            is_eager=False,
        ),
):
    """
        Lists inference simulator models for a project
    """
    app_logger.info(f'Start project list inference simulator models from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()
    project_service: ProjectService = service_factory.get_project_service()

    project_service.print_inference_simulator_model_list(config, project_uid, statuses, row, page)

    typer.echo(__("Inference simulator models listing complete"))
    raise typer.Exit(0)


@inference_simulators_app.command(name="logs", no_args_is_help=True, help=__("Stream real-time task logs or view last logs for an inference simulator"))
def inference_simulator_logs(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator unique ID"),),
        logs_number: Optional[int] = typer.Option(
            None,
            '--number',
            '-n',
            help=__("Display a number of latest log entries. No real-time stream if provided."),
            is_eager=False,
        ),
):
    """
        Streams real-time inference simulator logs
    """
    app_logger.info(f'View inference simulator logs')

    if not unique_id:
        typer.echo(__('Inference simulator UID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    logging_service: LoggingService = service_factory.get_logging_service()

    if logs_number is None:
        logging_service.stream_inference_simulator_logs_with_controls(
            config=config,
            slug=unique_id
        )
    else:
        get_inference_simulator_response: Optional[GetInferenceSimulatorResponse] = service_factory.get_thestage_api_client().get_inference_simulator(
            token=config.main.thestage_auth_token,
            slug=unique_id,
        )
        if not get_inference_simulator_response:
            typer.echo(__("Inference simulator with UID %uid% not found", {"uid": unique_id}))
            raise typer.Exit(1)
        else:
            inference_simulator_id = get_inference_simulator_response.inferenceSimulator.id
            logging_service.print_last_inference_simulator_logs(config=config, inference_simulator_id=inference_simulator_id, logs_number=logs_number)

    app_logger.info(f'Inference simulator logs - end')
    raise typer.Exit(0)


@inference_simulator_model_app.command("deploy-instance", no_args_is_help=True, help=__("Deploy an inference simulator model to an instance"))
def deploy_inference_simulator_model_to_instance(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator model unique ID"), ),
        rented_instance_unique_id: Optional[str] = typer.Option(
            None,
            '--rented-instance-unique-id',
            '-ruid',
            help=__("The rented instance unique ID on which the inference simulator model will be deployed"),
            is_eager=False,
        ),
        self_hosted_instance_unique_id: Optional[str] = typer.Option(
            None,
            '--self-hosted-instance-unique-id',
            '-suid',
            help=__("The self-hosted instance unique ID on which the inference simulator model will be deployed"),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory. By default, the current directory is used"),
            show_default=False,
            is_eager=False,
        ),
        enable_log_stream: Optional[bool] = typer.Option(
            True,
            " /--no-logs",
            " /-nl",
            help=__("Disable real-time log streaming"),
            is_eager=False,
        ),
):
    """
        Deploy an inference simulator model to an instance
    """

    if unique_id and not re.match(r"^[a-zA-Z0-9-]+$", unique_id):
        raise typer.BadParameter(__("Invalid UID format. The UID can only contain letters, numbers, and hyphens."))

    unique_id_with_timestamp = f"{unique_id}-{int(time.time())}"

    app_logger.info(f'Deploying an inference simulator model')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.project_deploy_inference_simulator_model_to_instance(
        config=config,
        unique_id=unique_id,
        unique_id_with_timestamp=unique_id_with_timestamp,
        rented_instance_unique_id=rented_instance_unique_id,
        self_hosted_instance_unique_id=self_hosted_instance_unique_id,
    )

    if enable_log_stream:
        logging_service: LoggingService = service_factory.get_logging_service()

        logging_service.stream_inference_simulator_logs_with_controls(
            config=config,
            slug=unique_id_with_timestamp
        )
    raise typer.Exit(0)


@inference_simulator_model_app.command("deploy-sagemaker", no_args_is_help=True, help=__("Deploy an inference simulator model to SageMaker"))
def deploy_inference_simulator_model_to_sagemaker(
        unique_id: Optional[str] = typer.Argument(help=__("Inference simulator model unique ID"), ),
        arn: Optional[str] = typer.Option(
            None,
            '--amazon-resource-name',
            '-arn',
            help=__("The Amazon Resource Name of the IAM Role to use, e.g., arn:aws:iam::{aws_account_id}:role/{role}"),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory. By default, the current directory is used"),
            show_default=False,
            is_eager=False,
        ),
        instance_type: Optional[str] = typer.Option(
            None,
            '--instance-type',
            '-it',
            help=__("Instance type on which the inference simulator model will be deployed"),
            is_eager=False,
        ),
        initial_variant_weight: Optional[float] = typer.Option(
            None,
            "--initial-variant-weight",
            "-ivw",
            help=__("Initial Variant Weight. By default 1.0"),
            show_default=False,
            is_eager=False,
        ),
        initial_instance_count: Optional[int] = typer.Option(
            None,
            "--initial-instance-count",
            "-iic",
            help=__("Initial Instance Count"),
            show_default=False,
            is_eager=False,
        ),

):
    """
        Deploy an inference simulator model to SageMaker
    """

    if unique_id and not re.match(r"^[a-zA-Z0-9-]+$", unique_id):
        raise typer.BadParameter(__("Invalid UID format. The UID can only contain letters, numbers, and hyphens."))

    app_logger.info(f'Deploying an inference simulator model')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()

    project_service.project_deploy_inference_simulator_model_to_sagemaker(
        config=config,
        unique_id=unique_id,
        arn=arn,
        instance_type=instance_type,
        initial_variant_weight=initial_variant_weight,
        initial_instance_count=initial_instance_count,
    )
