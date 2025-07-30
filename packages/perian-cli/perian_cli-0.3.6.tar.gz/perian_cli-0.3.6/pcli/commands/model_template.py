from typing import Annotated, Optional

import typer

from pcli import PerianTyper
from pcli.api.model_template import search_model_templates
from pcli.responses import DefaultApiException, handle_exception, ExceptionLevel, NoOrganizationException, \
    ModelTemplateNotFoundException
from pcli.util.formatter import print_model_templates_list

model_template_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Find Model Templates",
)

@model_template_command.command("get", help="Get available instance types")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
def get_model_templates(
    name: Annotated[
        Optional[str],
        typer.Option(
            help="Name of the Model Template to search for."
        ),
    ] = None,
    limit: Annotated[
        int, typer.Option(help="Number of instance types to display")
    ] = 25,
):
    model_templates = search_model_templates(name, limit)
    if len(model_templates) == 0:
        raise ModelTemplateNotFoundException(
            "No instance types for given filters found."
        )

    print_model_templates_list(model_templates)