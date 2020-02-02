from rest_framework import serializers
from rest_framework import status


class CustomAPIException(serializers.ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"

    def __init__(self, msg, code, status_code=None, fields=None):
        # TODO pending change status_code to code for v2 API
        self.detail = {"error": {"status_code": code, "message": msg}}

        if fields is not None:
            self.detail["error"]["fields"] = fields

        if status_code is not None:
            self.status_code = status_code


def handling_errors(list_errors):
    errors = dict()

    for error in list_errors:
        if error[1][0].code == "required":
            if "required" not in errors:
                errors["required"] = list()

            errors["required"].append(
                {"field": error[0], "message": error[1][0]}
            )

        elif error[1][0].code == "blank":
            if "blank" not in errors:
                errors["blank"] = list()

            errors["blank"].append(
                {"field": error[0], "message": error[1][0]}
            )

        elif error[1][0].code == "invalid":
            if "invalid" not in errors:
                errors["invalid"] = list()

            errors["invalid"].append(
                {"field": error[0], "message": error[1][0]}
            )

        elif error[1][0].code == "min_length":
            if "min_length" not in errors:
                errors["min_length"] = list()

            errors["min_length"].append(
                {"field": error[0], "message": error[1][0]}
            )

        elif error[1][0].code == "max_length":
            if "max_length" not in errors:
                errors["max_length"] = list()

            errors["max_length"].append(
                {"field": error[0], "message": error[1][0]}
            )

        if error[1][0].code == "null":
            if "null" not in errors:
                errors["null"] = list()

            errors["null"].append(
                {"field": error[0], "message": error[1][0]}
            )

    if "blank" in errors:
        return CustomAPIException(
            "{} can't be empty.".format(errors["blank"]),
            1005,
            fields=errors["blank"]
        )

    if "required" in errors:
        return CustomAPIException(
            "{} are required.".format(errors["required"]),
            1006,
            fields=errors["required"]
        )

    if "min_length" in errors:
        return CustomAPIException(
            "{} are too short.".format(errors["min_length"]),
            1007,
            fields=errors["min_length"]
        )

    if "max_length" in errors:
        return CustomAPIException(
            "{} are too long.".format(errors["max_length"]),
            1008,
            fields=errors["max_length"]
        )

    if "invalid" in errors:
        return CustomAPIException(
            "The email is invalid.".format(errors["invalid"]),
            1009,
            fields=errors["invalid"]
        )

    if "null" in errors:
        return CustomAPIException(
            "{} isn't valid.".format(errors["null"]),
            1010,
            fields=errors["null"]
        )