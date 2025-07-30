from typing import Optional
from uuid import UUID

from perian import Configuration, ApiClient, ModelTemplateApi, ApiException

from pcli import db
from pcli.responses import DefaultApiException
from pcli.util.organization import validate_organization, generate_organization_header


def search_model_templates(name: Optional[str], limit: Optional[int]):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = ModelTemplateApi(api_client)

        try:
            api_response = api_instance.get_all_model_templates(
                name=name,
                limit=limit,
                _headers=generate_organization_header(organization_data),
            )
            return api_response.model_templates

        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))

def get_model_template_by_id(id: UUID):
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = ModelTemplateApi(api_client)

        try:
            api_response = api_instance.get_model_template_by_id(model_template_id=str(id), _headers=generate_organization_header(organization_data))
            return api_response.model_template
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))