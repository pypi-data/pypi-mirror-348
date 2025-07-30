import time
from typing import Annotated, Optional
from uuid import UUID

import typer
from rich.progress import SpinnerColumn, Progress, TextColumn

from pcli import PerianTyper
from pcli.api.instance_type import (
    get_by_id as get_instance_type_by_id,
    get_by_requirements as get_instance_type_by_requirements,
)
from pcli.api.job import (
    get_by_id as get_job_by_id,
    get_all,
    cancel_job,
    create_job as api_create_job,
)
from pcli.colors import PERIAN_PURPLE_LIGHT
from pcli.responses import (
    InstanceTypeApiException,
    InvalidFilterCriteriaException,
    handle_exception,
    ExceptionLevel,
    JobNotFoundException,
    DefaultApiException,
    JobAPIException,
    InvalidJobIdException,
    NoOrganizationException,
    success,
    JobAlreadyDoneException,
    InvalidWorkloadManifestException,
    InvalidParametersException,
    InvalidInstanceTypeIdException,
    InsufficientQuotaException,
    InstanceTypeNotFoundException,
    warning,
)
from pcli.util import load_instance_type_filter_from_values, load_workload_manifest_from_json
from pcli.util.formatter import (
    print_jobs_list,
    print_job_description,
    format_instance_type_query,
)
from pcli.util.string_similarity import validate_billing_granularity
from perian import InstanceTyperQueryView, CreateJobRequest
from pcli import db
from urllib.parse import urlparse
from perian.models import DockerRegistryCredentials

job_command = PerianTyper(
    no_args_is_help=True, rich_markup_mode="rich", help="Create and manage jobs"
)


def _parse_container_image_name(image_name) -> tuple[str, Optional[str]]:
    if not ":" in image_name:
        return image_name, None
    split_image = image_name.rsplit(":", 1)
    return split_image[0], split_image[1]


def _validate_job_description(job_description: dict):
    if not "instance_type_id" in job_description:
        raise InvalidInstanceTypeIdException()

    if (
        not "docker_run_parameters" in job_description
        or not "image_name" in job_description["docker_run_parameters"]
    ):
        raise InvalidParametersException("Please provide a valid container image name.")

    if "requirements" in job_description:
        job_description["requirements"] = format_instance_type_query(
            job_description["requirements"]
        )

    return job_description


def _inject_stored_registry(job_description: dict):
    # getting already stored registry data
    registry_data = db.get("registry")

    image_url = urlparse(
        "https://" + job_description["docker_run_parameters"]["image_name"]
    )

    if registry_data:
        for registry_name in registry_data:
            registry_url = urlparse(registry_data[registry_name]["url"])

            if registry_url.netloc == image_url.netloc:
                job_description["docker_registry_credentials"] = (
                    DockerRegistryCredentials(
                        url=registry_data[registry_name]["url"],
                        username=registry_data[registry_name]["username"],
                        password=registry_data[registry_name]["password"],
                    )
                )
    return job_description


def _parse_duration(duration_str: str) -> int:
    """
    Parse a duration string into seconds.
    Supports formats like: '30s', '5m', '2h', '7d', '1h30m', etc.
    
    Args:
        duration_str: String in format like '1h30m' or '30s'
        
    Returns:
        Total number of seconds
        
    Raises:
        ValueError: If the duration string format is invalid
    """
    if not duration_str:
        raise ValueError("Duration string cannot be empty")
        
    # Time unit multipliers in seconds
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }
    
    total_seconds = 0
    current_number = ''
    
    for char in duration_str:
        if char.isdigit():
            current_number += char
        elif char in units:
            if not current_number:
                raise ValueError(f"Invalid duration format: {duration_str}")
            total_seconds += int(current_number) * units[char]
            current_number = ''
        else:
            raise ValueError(f"Invalid character in duration: {char}")
    
    if current_number:
        raise ValueError(f"Invalid duration format: {duration_str}")
    
    if total_seconds == 0:
        raise ValueError("Duration must be greater than 0 seconds")
    
    return total_seconds


JOB_COMMAND_FLAG_HELP = (
    "Specify the shell command to be executed inside the Docker container. "
    + " Examples: "
    + "--command '/bin/sh -c cat /etc/hosts'"
)


@job_command.command("create", help="Create a job")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InstanceTypeApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(
    InstanceTypeNotFoundException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(InsufficientQuotaException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InvalidWorkloadManifestException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(
    InvalidFilterCriteriaException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(
    InvalidInstanceTypeIdException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(InvalidParametersException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(JobAPIException, exit=True, level=ExceptionLevel.ERROR)
def create_job(
    image: Annotated[Optional[str], typer.Option(help="Container image name")] = None,
    command: Annotated[Optional[str], typer.Option(help=JOB_COMMAND_FLAG_HELP)] = None,
    instance_type_id: Annotated[
        Optional[str], typer.Option(help="ID of instance type")
    ] = None,
    cores: Annotated[Optional[int], typer.Option(help="Number of cpu cores")] = None,
    memory: Annotated[Optional[int], typer.Option(help="Gigabyte of RAM")] = None,
    accelerators: Annotated[
        Optional[int], typer.Option(help="Number of Accelerators")
    ] = None,
    accelerator_type: Annotated[
        Optional[str],
        typer.Option(
            help="Name of accelerator type. See accelerator-type command for a list of all supported ones"
        ),
    ] = None,
    country_code: Annotated[
        Optional[str], typer.Option(help="Country code (e.g. DE)")
    ] = None,
    billing_granularity: Annotated[
        Optional[str], typer.Option(help="Billing granularity (PER_SECOND, PER_MINUTE, PER_HOUR, PER_10_MINUTES)")
    ] = None,
    timeout: Annotated[
        Optional[str],
        typer.Option(
            help="Job timeout duration (e.g. '30s', '5m', '2h', '7d', '1h30m'). After this duration, the job will be cancelled"
        ),
    ] = None,
    manifest: Annotated[
        Optional[str],
        typer.Option(
            help="Job description manifest. A JSON string or the path to a JSON file is expected here"
        ),
    ] = None,
):
    job_description = {}

    with Progress(
        SpinnerColumn(style=PERIAN_PURPLE_LIGHT),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # we can load the entire job description from file
        if manifest:
            job_description = load_workload_manifest_from_json(manifest)
        elif not manifest:
            if not image:
                raise InvalidParametersException(
                    "Please provide a valid container image name."
                )

            # handling container image
            _image_name, _tag = _parse_container_image_name(image)
            job_description["docker_run_parameters"] = {"image_name": _image_name}
            if _tag:
                job_description["docker_run_parameters"]["image_tag"] = _tag
            if command:
                job_description["docker_run_parameters"]["command"] = command

            # Add timeout if specified
            if timeout:
                try:
                    timeout_seconds = _parse_duration(timeout)
                    job_description["timeout_seconds"] = timeout_seconds
                except ValueError as e:
                    raise InvalidParametersException(str(e))

            # handling instance type for job
            # user has provided a specific instance type id
            if instance_type_id:
                try:
                    instance_type_id = UUID(instance_type_id)
                except Exception:
                    raise InvalidInstanceTypeIdException()
                job_description["instance_type_id"] = str(instance_type_id)

            # no specific instance type id, we need to find a suitable one first
            else:
                if billing_granularity:
                    validated_granularity = validate_billing_granularity(billing_granularity)
                    if not validated_granularity:
                        warning(f"Invalid billing granularity: '{billing_granularity}'. Valid options are: PER_SECOND, PER_MINUTE, PER_HOUR, PER_10_MINUTES")
                        return
                    billing_granularity = validated_granularity

                instance_type_filters = load_instance_type_filter_from_values(
                    cores=cores,
                    memory=memory,
                    accelerators=accelerators,
                    accelerator_type=accelerator_type,
                    country_code=country_code,
                    billing_granularity=billing_granularity,
                )

                # storing filters for later usage
                job_description["requirements"] = instance_type_filters

                selecting_instance_type_task = progress.add_task(
                    description="Selecting optimal instance type", total=None
                )

                # creating instance type query
                instance_type_query = InstanceTyperQueryView(**instance_type_filters)

                # querying for instance type
                instance_types = get_instance_type_by_requirements(
                    instance_type_query, 1
                )
                if len(instance_types) == 0:
                    raise InstanceTypeNotFoundException()

                job_description["instance_type_id"] = instance_types[0].id

                # this is just for the user experience and the progress spinner
                time.sleep(0.3)
                progress.remove_task(selecting_instance_type_task)

        # validating input before calling API
        job_description = _validate_job_description(job_description)

        # inject private registry previously saved via the CLI
        job_description = _inject_stored_registry(job_description)

        # creating job request and calling API
        create_job_task = progress.add_task(
            description="Submitting job to Sky Platform", total=None
        )
        create_job_request = CreateJobRequest(**job_description)
        created_job = api_create_job(create_job_request)

        # this is just for the user experience and the progress spinner
        time.sleep(0.3)
        progress.remove_task(create_job_task)

        success(
            f"Job with ID '[bold underline]{created_job.id}[/bold underline]' created successfully."
        )


@job_command.command("get", help="Get details about jobs")
@handle_exception(JobNotFoundException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(JobAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InvalidJobIdException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InvalidParametersException, exit=True, level=ExceptionLevel.WARNING)
def get_job(
    job_id: Annotated[Optional[str], typer.Argument(help="ID of job to get")] = None,
    all: Annotated[bool, typer.Option(help="Get all jobs for your account")] = False,
    last: Annotated[bool, typer.Option(help="Get last created job")] = False,
):
    if all:
        jobs = get_all()
        if len(jobs) == 0:
            raise JobNotFoundException("No jobs found for your account.")
        print_jobs_list(jobs)
        return

    if job_id:
        related_instance_type = None
        try:
            job_id_uuid = UUID(job_id)
        except Exception:
            raise InvalidJobIdException()
        job = get_job_by_id(job_id_uuid)
    elif last:
        jobs = get_all()
        if len(jobs) == 0:
            raise JobNotFoundException("No jobs found for your account.")
        job = jobs[0]
    else:
        raise InvalidParametersException(
            "Please provide a job ID or use '--all/--last' option."
        )

    if job.runtime_metadata.instance_type_id:
        related_instance_type = get_instance_type_by_id(
            job.runtime_metadata.instance_type_id
        )
    print_job_description(job, related_instance_type)


@job_command.command("cancel", help="Cancel a job")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(JobAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InvalidJobIdException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(JobAlreadyDoneException, exit=True, level=ExceptionLevel.WARNING)
def cancel_job_by_id(
    job_id: Annotated[Optional[str], typer.Argument(help="ID of job to cancel")] = None,
    last: Annotated[bool, typer.Option(help="Cancel last created job")] = False,
):
    if last:
        jobs = get_all()
        if len(jobs) == 0:
            raise JobNotFoundException("No jobs found for your account.")
        job_id = jobs[0].id
    elif not job_id:
        raise InvalidParametersException(
            "Please provide a job ID or use '--last' option."
        )
    else:
        try:
            job_id = UUID(job_id)
        except Exception:
            raise InvalidJobIdException()

    cancel_job(job_id)
    success(f"Job canceled successfully.")