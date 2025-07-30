from pcli import db
from pcli.responses import (
    DefaultApiException,
    InsufficientQuotaException,
    InferenceServiceNotFoundException,
    InferenceServiceAPIException,
    InferenceServiceAlreadyDoneException,
)
from pcli.util.organization import validate_organization, generate_organization_header
from perian import (
    InferenceApi,
    ApiClient,
    Configuration,
    ApiException,
)


def get_by_id(inference_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InferenceApi(api_client)

        try:
            api_response = api_instance.get_inference_service_by_id(
                inference_service_id=str(inference_id),
                _headers=generate_organization_header(organization_data),
            )
            return api_response.inference_services[0]

        except ApiException as e:
            if "No inference service found found" in str(e):
                raise InferenceServiceNotFoundException(
                    f"No inference services with ID '[bold underline]{inference_id}[/bold underline]' found."
                )
            else:
                raise InferenceServiceAPIException(InferenceServiceAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def get_all(show_all: bool=True):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InferenceApi(api_client)

        try:
            api_response = api_instance.get_all_inference_services(
                show_all=show_all,
                _headers=generate_organization_header(organization_data)
            )
            return api_response.inference_services

        except ApiException as e:
            raise InferenceServiceAPIException(InferenceServiceAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def cancel_inference_service(inference_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InferenceApi(api_client)

        try:
            api_response = api_instance.cancel_inference_service(
                inference_service_id=str(inference_id),
                _headers=generate_organization_header(organization_data),
            )
        except ApiException as e:
            if "already complete" in str(e):
                raise InferenceServiceAlreadyDoneException()
            else:
                raise InferenceServiceAPIException(InferenceServiceAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def create_inference_service(inference_service_request):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InferenceApi(api_client)

        try:
            api_response = api_instance.create_inference_service(
                create_inference_service_request=inference_service_request,
                _headers=generate_organization_header(organization_data),
            )
            return api_response
        except ApiException as e:
            if "insufficient quota" in str(e):
                raise InsufficientQuotaException()
            raise InferenceServiceAPIException(InferenceServiceAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))
