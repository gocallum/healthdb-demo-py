import logging
from datetime import datetime

# Generate OperationOutcome JSON response
# for the FHIR response, https://hl7.org/fhir/stu3/operationoutcome-example.json.html

API_URL = "https://ausbizconsultingservices.com.au/api/fhir/"
ROUTE_NAME = "GP Referral Services Response"
SERVICE_NAME = "AUSBIZ TECHBOOMP Healthcare Referral Services"
HTTP_METHOD = "POST"


def generate_operation_outcome(resource_id, message, system, code, display, diagnostics, action, route):
    operation_outcome = {
        "resourceType": "OperationOutcome",
        "id": resource_id,
        "text": {
            "status": "generated",
            "div": f"<div xmlns='http://www.w3.org/1999/xhtml'><p>{message}</p></div>"
        },
        "issue": [
            {
                "severity": "information",
                "code": "informational",
                "details": {
                    "coding": [
                        {
                            "system": system,
                            "code": code,
                            "display": message
                        },
                        {
                            "system": API_URL,
                            "code": code,
                            "display": display
                        }
                    ],
                    "text": message + " | Validation passed"
                },
                "diagnostics": f"{route}|{action}|Time={datetime.now().isoformat()}|{diagnostics}"
            }
        ]
    }
    return operation_outcome


# diagnostic message for the OperationOutcome which is the actual technical error message we want to send back to the client


def send_error_response(diagnostics):
    logging.error("Failed to process referral.")
    outcome_json = generate_operation_outcome(
        resource_id="exception",
        message="Failed to process referral",
        system=SERVICE_NAME,
        code="exception",
        display="See diagnostics for further details",
        diagnostics=diagnostics,
        action=HTTP_METHOD,
        route=ROUTE_NAME
    )
    return outcome_json

def send_success_response(diagnostics):
    logging.info("Referral processed successfully.")
    outcome_json = generate_operation_outcome(
        resource_id="success",
        message="Message processed successfully",
        system=SERVICE_NAME,
        code="202",  # standard http response code for record created in a POST method
        display="Inbound message has been received and stored. See diagnostics for further details",
        diagnostics=diagnostics,
        action=HTTP_METHOD,
        route=ROUTE_NAME
    )
    return outcome_json
