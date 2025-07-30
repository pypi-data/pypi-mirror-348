import time
from typing import Annotated, Optional
from uuid import UUID
from rich import print as rich_print

import typer
from pcli.api.model_template import get_model_template_by_id
from rich.progress import SpinnerColumn, Progress, TextColumn
from rich.prompt import Confirm, Prompt

from pcli import PerianTyper
from pcli.api.instance_type import (
    get_by_id as get_instance_type_by_id,
    get_by_requirements as get_instance_type_by_requirements,
)
from pcli.api.inference import (
    get_by_id as get_inference_by_id,
    get_all,
    cancel_inference_service,
    create_inference_service as api_create_inference_service,
)
from pcli.colors import PERIAN_PURPLE_LIGHT
from pcli.responses import (
    InstanceTypeApiException,
    InvalidFilterCriteriaException,
    handle_exception,
    ExceptionLevel,
    InferenceServiceNotFoundException,
    DefaultApiException,
    InferenceServiceAPIException,
    InvalidInferenceServiceIdException,
    NoOrganizationException,
    success,
    InferenceServiceAlreadyDoneException,
    InvalidWorkloadManifestException,
    InvalidParametersException,
    InvalidInstanceTypeIdException,
    InsufficientQuotaException,
    InstanceTypeNotFoundException,
    warning, InvalidModelTemplateIdException, AbortedException,
)
from pcli.util import load_instance_type_filter_from_values, load_workload_manifest_from_json
from pcli.util.formatter import (
    print_inference_list,
    print_inference_description,
    format_instance_type_query,
)
from pcli.util.string_similarity import validate_billing_granularity
from perian import InstanceTyperQueryView, CreateInferenceServiceRequest
from pcli import db
from urllib.parse import urlparse
from perian.models import DockerRegistryCredentials

inference_command = PerianTyper(
    no_args_is_help=True, rich_markup_mode="rich", help="Create and manage inference services"
)


def _parse_container_image_name(image_name) -> tuple[str, Optional[str]]:
    if not ":" in image_name:
        return image_name, None
    split_image = image_name.rsplit(":", 1)
    return split_image[0], split_image[1]


def _validate_inference_description(inference_description: dict):
    if not "instance_type_id" in inference_description:
        raise InvalidInstanceTypeIdException()

    if (
            not "docker_run_parameters" in inference_description
            or not "image_name" in inference_description["docker_run_parameters"]
    ):
        raise InvalidParametersException("Please provide a valid container image name.")

    if "requirements" in inference_description:
        inference_description["requirements"] = format_instance_type_query(
            inference_description["requirements"]
        )

    return inference_description


def _inject_stored_registry(inference_description: dict):
    # getting already stored registry data
    registry_data = db.get("registry")

    image_url = urlparse(
        "https://" + inference_description["docker_run_parameters"]["image_name"]
    )

    if registry_data:
        for registry_name in registry_data:
            registry_url = urlparse(registry_data[registry_name]["url"])

            if registry_url.netloc == image_url.netloc:
                inference_description["docker_registry_credentials"] = (
                    DockerRegistryCredentials(
                        url=registry_data[registry_name]["url"],
                        username=registry_data[registry_name]["username"],
                        password=registry_data[registry_name]["password"],
                    )
                )
    return inference_description


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


INFERENCE_SERVICE_COMMAND_FLAG_HELP = (
        "Specify the shell command to be executed inside the Docker container. "
        + " Examples: "
        + "--command '/bin/sh -c cat /etc/hosts'"
)

def _prompt_expected_instance_price(model_template_id: UUID):
    model_template = get_model_template_by_id(model_template_id)
    instance_type_query = format_instance_type_query(model_template.requirement_metadata.requirements.to_dict())
    instance_types = get_instance_type_by_requirements(instance_type_query, 1)
    cheapest_instance_type = instance_types[0]
    price = cheapest_instance_type.price.unit_price
    rich_print(f"The estimated cost of this deployment is {price}. This may vary slightly based on resource availability.")
    confirm_override = Confirm.ask(
        "Do you want to continue?"
    )
    if not confirm_override:
        raise AbortedException()


@inference_command.command("create", help="Create an inference service")
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
@handle_exception(InferenceServiceAPIException, exit=True, level=ExceptionLevel.ERROR)
def create_inference_service(
        image: Annotated[Optional[str], typer.Option(help="Container image name")] = None,
        command: Annotated[Optional[str], typer.Option(help=INFERENCE_SERVICE_COMMAND_FLAG_HELP)] = None,
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
        manifest: Annotated[
            Optional[str],
            typer.Option(
                help="Inference service description manifest. A JSON string or the path to a JSON file is expected here"
            ),
        ] = None,
        container_port: Annotated[Optional[int], typer.Option(help="container port to be mapped to host")] = None,
        model_template_id: Annotated[
            Optional[str], typer.Option(help="ID of model template")
        ] = None,
):
    inference_description = {}

    with Progress(
            SpinnerColumn(style=PERIAN_PURPLE_LIGHT),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        # we can load the entire inference service description from file
        if manifest:
            inference_description = load_workload_manifest_from_json(manifest)
        elif not manifest:

            if model_template_id:
                try:
                    model_template_id = UUID(model_template_id)
                except Exception:
                    raise InvalidModelTemplateIdException()
                _prompt_expected_instance_price(model_template_id)
                inference_description["model_template_id"] = str(model_template_id)
            else:
                if not image:
                    raise InvalidParametersException(
                        "Please provide a valid container image name."
                    )

                # handling container image
                _image_name, _tag = _parse_container_image_name(image)
                inference_description["docker_run_parameters"] = {"image_name": _image_name}
                if _tag:
                    inference_description["docker_run_parameters"]["image_tag"] = _tag
                if command:
                    inference_description["docker_run_parameters"]["command"] = command
                # handling instance type for inference service
                # user has provided a specific instance type id
                if instance_type_id:
                    try:
                        instance_type_id = UUID(instance_type_id)
                    except Exception:
                        raise InvalidInstanceTypeIdException()
                    inference_description["instance_type_id"] = str(instance_type_id)

                # no specific instance type id, we need to find a suitable one first
                else:
                    if billing_granularity:
                        validated_granularity = validate_billing_granularity(billing_granularity)
                        if not validated_granularity:
                            warning(
                                f"Invalid billing granularity: '{billing_granularity}'. Valid options are: PER_SECOND, PER_MINUTE, PER_HOUR, PER_10_MINUTES")
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
                    inference_description["requirements"] = instance_type_filters

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

                    inference_description["instance_type_id"] = instance_types[0].id

                    # this is just for the user experience and the progress spinner
                    time.sleep(0.3)
                    progress.remove_task(selecting_instance_type_task)

                # validating input before calling API
                inference_description = _validate_inference_description(inference_description)

                # inject private registry previously saved via the CLI
                inference_description = _inject_stored_registry(inference_description)

        # add container port
        inference_description["container_port"] = container_port

        # creating inference service request and calling API
        create_inference_task = progress.add_task(
            description="Submitting inference service to Sky Platform", total=None
        )
        create_inference_request = CreateInferenceServiceRequest(**inference_description)
        created_inference_service = api_create_inference_service(create_inference_request)

        # this is just for the user experience and the progress spinner
        time.sleep(0.3)
        progress.remove_task(create_inference_task)

        success(
            f"Inference service with ID '[bold underline]{created_inference_service.id}[/bold underline]' created successfully."
        )


@inference_command.command("get", help="Get details about inference service")
@handle_exception(InferenceServiceNotFoundException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InferenceServiceAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InvalidInferenceServiceIdException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InvalidParametersException, exit=True, level=ExceptionLevel.WARNING)
def get_inference_service(
        inference_id: Annotated[Optional[str], typer.Argument(help="ID of inference service to get")] = None,
        all: Annotated[bool, typer.Option(help="Get all inference services for your account")] = False,
        last: Annotated[bool, typer.Option(help="Get last created inference service")] = False,
):
    if all:
        inference_services = get_all(show_all=False)
        if len(inference_services) == 0:
            raise InferenceServiceNotFoundException("No inference services found for your account.")
        print_inference_list(inference_services)
        return

    if inference_id:
        related_instance_type = None
        try:
            inference_id_uuid = UUID(inference_id)
        except Exception:
            raise InvalidInferenceServiceIdException()
        inference_service = get_inference_by_id(inference_id_uuid)
    elif last:
        inference_services = get_all(show_all=True)
        if len(inference_services) == 0:
            raise InferenceServiceNotFoundException("No inference services found for your account.")
        inference_service = inference_services[0]
    else:
        raise InvalidParametersException(
            "Please provide a inference service ID or use '--all/--last' option."
        )

    if inference_service.runtime_metadata.instance_type_id:
        related_instance_type = get_instance_type_by_id(
            inference_service.runtime_metadata.instance_type_id
        )
    print_inference_description(inference_service, related_instance_type)


@inference_command.command("cancel", help="Cancel an inference service")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InferenceServiceAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InvalidInferenceServiceIdException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InferenceServiceAlreadyDoneException, exit=True, level=ExceptionLevel.WARNING)
def cancel_inference_service_by_id(
        inference_id: Annotated[Optional[str], typer.Argument(help="ID of inference service to cancel")] = None,
        last: Annotated[bool, typer.Option(help="Cancel last created inference service")] = False,
):
    if last:
        inferece_service = get_all()
        if len(inferece_service) == 0:
            raise InferenceServiceNotFoundException("No inference services found for your account.")
        inference_id = inferece_service[0].id
    elif not inference_id:
        raise InvalidParametersException(
            "Please provide a inference service ID or use '--last' option."
        )
    else:
        try:
            inference_id = UUID(inference_id)
        except Exception:
            raise InvalidInferenceServiceIdException()

    cancel_inference_service(inference_id)
    success(f"Inference service canceled successfully.")