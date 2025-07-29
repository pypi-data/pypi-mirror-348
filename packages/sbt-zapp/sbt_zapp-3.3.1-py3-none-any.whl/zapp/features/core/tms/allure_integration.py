from enum import Enum
from allure import step, attach
from allure_commons.types import AttachmentType
import json
from jsonschema import ValidationError

class AllureTag(Enum):
    TMS = "allure.link.tms"
    ISSUE = "allure.issue"
    API_TEST = "api_test"
    SCHEMA_VALIDATION = "schema_validation"
    PARALLEL_TEST = "parallel_test"
    JWT_AUTH = "jwt_auth"

    @staticmethod
    def get_value(tag):
        return tag.split(":")[-1]

def get_tms_key(tags) -> str:
    for tag in tags:
        if AllureTag.TMS.value in tag:
            return AllureTag.get_value(tag)

def get_issue_links(tags) -> list[str]:
    return [AllureTag.get_value(tag) for tag in tags if AllureTag.ISSUE.value in tag]


def handle_schema_validation_error(context, exception):
    error_info = {
        "message": str(exception.message),
        "schema_path": " > ".join(map(str, exception.absolute_path)),
        "value": exception.instance
    }
    attach(
        name="Validation Error",
        body=json.dumps(error_info, indent=2),
        attachment_type=AttachmentType.JSON
    )
    context.failed_validation = True