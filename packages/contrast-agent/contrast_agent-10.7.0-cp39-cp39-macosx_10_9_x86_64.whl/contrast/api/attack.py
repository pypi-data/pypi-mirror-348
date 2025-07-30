# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto
from typing import Optional

import contrast
from contrast.agent.request import Request
from contrast.api.sample import Sample
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ProtectResponse(Enum):
    NO_ACTION = auto()
    BLOCKED = auto()
    MONITORED = auto()
    PROBED = auto()
    BLOCKED_AT_PERIMETER = auto()


# Certain rules in Protect can only be confirmed as suspicious, meaning they didn't get evaluated against user input
# or they didn't have input tracing applied. We report these rules differently.
SUSPICIOUS_RULES = [
    "malformed-header",
    "reflected-xss",
    "unsafe-file-upload",
    "zip-file-overwrite",
]


class Attack:
    """
    Class storing all data necessary to report a protect attack.
    """

    def __init__(self, rule_id: str):
        self.rule_id: str = rule_id
        self.samples: list[Sample] = []
        self.response: Optional[ProtectResponse] = None
        self.start_time_ms = contrast.CS__CONTEXT_TRACKER.current().request.timestamp_ms

    @property
    def blocked(self) -> bool:
        return self.response == ProtectResponse.BLOCKED

    @property
    def perimeter_blocked(self) -> bool:
        return self.response == ProtectResponse.BLOCKED_AT_PERIMETER

    def add_sample(self, sample: Sample) -> None:
        self.samples.append(sample)

    def _convert_samples(self, request: Request) -> list[dict]:
        if request is not None:
            reportable_request = request.reportable_format
        else:
            reportable_request = {}

        return [
            {
                "blocked": self.blocked,
                "input": self._convert_user_input(sample),
                "details": sample.details,
                "request": reportable_request,
                "stack": [
                    {
                        "declaringClass": stack.declaring_class,
                        "methodName": stack.method_name,
                        "fileName": stack.file_name,
                        "lineNumber": stack.line_number,
                    }
                    for stack in sample.stack
                ],
                "timestamp": {
                    "start": sample.timestamp_ms,  # in ms
                    "elapsed": (
                        now_ms() - sample.timestamp_ms
                    ),  # in ms which is the format TS accepts
                },
            }
            for sample in self.samples
        ]

    def _convert_user_input(self, sample: Sample) -> dict:
        json_sample = {
            "documentType": sample.user_input.document_type.name,
            "filters": sample.user_input.matcher_ids,
            "time": sample.timestamp_ms,
            "type": sample.user_input.type.name,
            "value": sample.user_input.value,
        }
        if sample.user_input.path:
            json_sample["documentPath"] = sample.user_input.path
        if sample.user_input.name:
            json_sample["name"] = sample.user_input.name
        return json_sample

    def report_result(self) -> str:
        response_map = {
            ProtectResponse.BLOCKED: "blocked",
            ProtectResponse.BLOCKED_AT_PERIMETER: "blocked",
            ProtectResponse.PROBED: "ineffective",
            ProtectResponse.MONITORED: (
                "suspicious" if self.rule_id in SUSPICIOUS_RULES else "exploited"
            ),
        }
        return response_map[self.response]

    def to_json(self, request: Request) -> dict:
        common_fields = {
            "startTime": 0,
            "total": 0,
        }
        json = {
            "startTime": self.start_time_ms,
            "blocked": common_fields,
            "exploited": common_fields,
            "ineffective": common_fields,
            "suspicious": common_fields,
        }

        relevant_mode = self.report_result()

        samples = self._convert_samples(request)

        json[relevant_mode] = {
            "total": 1,  # always 1 until batching happens
            "startTime": self.start_time_ms,
            "samples": samples,
        }

        return json
