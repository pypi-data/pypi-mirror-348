import datetime
from typing import Any, Dict, Generator, Optional

import numpy as np
import pandas as pd
from cehrbert.data_generators.hf_data_generator.hf_dataset_mapping import (
    ED_VISIT_TYPE_CODES,
    INPATIENT_VISIT_TYPE_CODES,
    INPATIENT_VISIT_TYPES,
    DatasetMapping,
    VisitObject,
    get_value,
    has_events_and_get_events,
    replace_escape_chars,
)
from cehrbert.med_extension.schema_extension import Event
from cehrbert.runners.hf_runner_argument_dataclass import DataTrainingArguments
from cehrbert_data.const.common import NA
from cehrbert_data.decorators.patient_event_decorator_base import get_att_function
from dateutil.relativedelta import relativedelta

from cehrgpt.models.tokenization_hf_cehrgpt import (
    NONE_BIN,
    UNKNOWN_BIN,
    CehrGptTokenizer,
)


def convert_date_to_posix_time(index_date: datetime.date) -> float:
    return datetime.datetime.combine(
        index_date, datetime.datetime.min.time()
    ).timestamp()


class MedToCehrGPTDatasetMapping(DatasetMapping):
    def __init__(
        self,
        data_args: DataTrainingArguments,
        include_inpatient_hour_token: bool = True,
    ):
        self._time_token_function = get_att_function(data_args.att_function_type)
        self._include_auxiliary_token = data_args.include_auxiliary_token
        self._inpatient_time_token_function = get_att_function(
            data_args.inpatient_att_function_type
        )
        self._include_demographic_prompt = data_args.include_demographic_prompt
        self._include_inpatient_hour_token = include_inpatient_hour_token

    """
    This mapping function converts the MED (https://github.com/Medical-Event-Data-Standard/meds/tree/main) extension
    to the CehrGPT format. We make several assumptions
    - The first event contains the demographic information
    - From the second event onward
        - the time of the event is visit_start_datetime.
        - the first measurement contains the code indicating a standard OMOP Visit concept_id (e.g. 9201, 9202)
        - in case of inpatient visits, the last measurement is assumed to
            contain the standard OMOP concept id for discharge facilities (e.g 8536)
        - in case of inpatient visits, datetime_value of the last measurement stores visit_end_datetime
    """

    def remove_columns(self):
        return ["patient_id", "visits", "birth_datetime"]

    @staticmethod
    def _update_cehrgpt_record(
        cehrgpt_record: Dict[str, Any],
        code: str,
        concept_value_mask: int = 0,
        number_as_value: float = 0.0,
        concept_as_value: str = "0",
        is_numeric_type: int = 0,
        unit: str = NA,
    ) -> None:
        cehrgpt_record["concept_ids"].append(replace_escape_chars(code))
        cehrgpt_record["concept_value_masks"].append(concept_value_mask)
        cehrgpt_record["number_as_values"].append(number_as_value)
        cehrgpt_record["concept_as_values"].append(concept_as_value)
        cehrgpt_record["units"].append(unit)
        cehrgpt_record["is_numeric_types"].append(is_numeric_type)

    def transform(self, record: Dict[str, Any]) -> Dict[str, Any]:
        cehrgpt_record = {
            "person_id": record["patient_id"],
            "concept_ids": [],
            "concept_value_masks": [],
            "number_as_values": [],
            "concept_as_values": [],
            "units": [],
            "is_numeric_types": [],
        }
        # Extract the demographic information
        birth_datetime = record["birth_datetime"]
        if isinstance(birth_datetime, pd.Timestamp):
            birth_datetime = birth_datetime.to_pydatetime()
        gender = record["gender"]
        race = record["race"]
        visits = record["visits"]
        # This indicates this is columnar format
        if isinstance(visits, dict):
            visits = sorted(self.convert_visit_columnar_to_python(visits))
        else:
            visits = sorted(visits, key=lambda _: get_value(_, "visit_start_datetime"))

        # Add the demographic tokens
        first_visit = visits[0]
        first_visit_start_datetime: datetime.datetime = get_value(
            first_visit, "visit_start_datetime"
        )
        year_str = f"year:{str(first_visit_start_datetime.year)}"
        age_str = f"age:{str(relativedelta(first_visit_start_datetime, birth_datetime).years)}"
        self._update_cehrgpt_record(cehrgpt_record, year_str)
        self._update_cehrgpt_record(cehrgpt_record, age_str)
        self._update_cehrgpt_record(cehrgpt_record, gender)
        self._update_cehrgpt_record(cehrgpt_record, race)

        # Use a data cursor to keep track of time
        datetime_cursor: Optional[datetime.datetime] = None
        visit: VisitObject
        # Loop through all the visits
        for i, visit in enumerate(visits):
            events: Generator[Event, None, None] = get_value(visit, "events")
            has_events, events = has_events_and_get_events(events)
            if not has_events:
                continue

            visit_start_datetime: datetime.datetime = get_value(
                visit, "visit_start_datetime"
            )
            # If visit_end_datetime is populated for the inpatient visit, we update the datetime_cursor
            visit_end_datetime: Optional[datetime.datetime] = get_value(
                visit, "visit_end_datetime"
            )

            # We assume the first measurement to be the visit type of the current visit
            visit_type = get_value(visit, "visit_type")
            is_er_or_inpatient = (
                visit_type in INPATIENT_VISIT_TYPES
                or visit_type in INPATIENT_VISIT_TYPE_CODES
                or visit_type in ED_VISIT_TYPE_CODES
            )

            # Add artificial time tokens to the patient timeline if timedelta exists
            if datetime_cursor is not None:
                time_delta = max((visit_start_datetime - datetime_cursor).days, 0)
                # This generates an artificial time token depending on the choice of the time token functions
                self._update_cehrgpt_record(
                    cehrgpt_record,
                    code=self._time_token_function(time_delta),
                )

            datetime_cursor = visit_start_datetime
            # Add a [VS] token
            self._update_cehrgpt_record(
                cehrgpt_record,
                code="[VS]",
            )
            # Add a visit type token
            self._update_cehrgpt_record(
                cehrgpt_record,
                code=visit_type,
            )
            # We need to insert an inpatient hour token right after the visit type, we calculate the hour interval
            # with respect to the midnight of the day
            if is_er_or_inpatient and self._include_inpatient_hour_token:
                if datetime_cursor.hour > 0:
                    # This generates an artificial time token depending on the choice of the time token functions
                    self._update_cehrgpt_record(
                        cehrgpt_record,
                        code=f"i-H{datetime_cursor.hour}",
                    )

            # Keep track of the existing outpatient events, we don't want to add them again
            existing_duplicate_events = list()
            for e in events:
                # If the event doesn't have a time stamp, we skip it
                event_time: datetime.datetime = e["time"]
                if not event_time:
                    continue

                # If numeric_value exists, this is a concept/value tuple, we indicate this using a concept_value_mask
                numeric_value = e.get("numeric_value", None)
                text_value = e.get("text_value", None)
                # The unit might be populated with a None value
                unit = e.get("unit", NA) if e.get("unit", NA) else NA
                concept_value_mask = int(
                    numeric_value is not None or text_value is not None
                )
                is_numeric_type = int(numeric_value is not None)
                code = replace_escape_chars(e["code"])

                # Create the event identity
                event_identity = (
                    (event_time, code, text_value, unit)
                    if is_er_or_inpatient
                    else (event_time.date(), code, text_value, unit)
                )

                # Add a medical token to the patient timeline
                # If this is an inpatient visit, we use the event time stamps to calculate age and date
                # because the patient can stay in the hospital for a period of time.
                if is_er_or_inpatient:
                    # Calculate the time diff in days w.r.t the previous measurement
                    time_diff_days = (event_time - datetime_cursor).days
                    # Update the datetime_cursor if the time diff between two neighboring measurements is greater than and
                    # equal to 1 day
                    if self._inpatient_time_token_function and time_diff_days > 0:
                        # This generates an artificial time token depending on the choice of the time token functions
                        self._update_cehrgpt_record(
                            cehrgpt_record,
                            code=f"i-{self._inpatient_time_token_function(time_diff_days)}",
                        )

                    if self._include_inpatient_hour_token:
                        # if the time difference in days is greater than 0, we calculate the hour interval
                        # with respect to the midnight of the day
                        time_diff_hours = (
                            event_time.hour
                            if time_diff_days > 0
                            else int(
                                (event_time - datetime_cursor).total_seconds() // 3600
                            )
                        )

                        if time_diff_hours > 0:
                            # This generates an artificial time token depending on the choice of the time token functions
                            self._update_cehrgpt_record(
                                cehrgpt_record,
                                code=f"i-H{time_diff_hours}",
                            )

                if event_identity in existing_duplicate_events:
                    continue

                self._update_cehrgpt_record(
                    cehrgpt_record,
                    code=code,
                    concept_value_mask=concept_value_mask,
                    unit=unit,
                    number_as_value=numeric_value if numeric_value else 0.0,
                    concept_as_value=(
                        replace_escape_chars(text_value) if text_value else "0"
                    ),
                    is_numeric_type=is_numeric_type,
                )
                existing_duplicate_events.append(event_identity)
                # we only want to update the time stamp when data_cursor is less than the event time
                if datetime_cursor < event_time or datetime_cursor is None:
                    datetime_cursor = event_time
                    # We need to bound the datetime_cursor if the current visit is an admission type of visit
                    # as the associated events could be generated after the visits are complete
                    if is_er_or_inpatient and visit_end_datetime is not None:
                        datetime_cursor = min(datetime_cursor, visit_end_datetime)

            # For inpatient or ER visits, we want to discharge_facility to the end of the visit
            if is_er_or_inpatient:
                # If visit_end_datetime is populated for the inpatient visit, we update the datetime_cursor
                if visit_end_datetime is not None:
                    datetime_cursor = visit_end_datetime

                if self._include_auxiliary_token:
                    # Reuse the age and date calculated for the last event in the patient timeline for the discharge
                    # facility event
                    discharge_facility = get_value(visit, "discharge_facility")
                    if not discharge_facility:
                        discharge_facility = "0"

                    self._update_cehrgpt_record(
                        cehrgpt_record,
                        code=discharge_facility,
                    )

            # Reuse the age and date calculated for the last event in the patient timeline
            self._update_cehrgpt_record(
                cehrgpt_record,
                code="[VE]",
            )

        # Generate the orders of the concepts that the cehrbert dataset mapping function expects
        cehrgpt_record["orders"] = list(
            range(1, len(cehrgpt_record["concept_ids"]) + 1)
        )

        # Add some count information for this sequence
        cehrgpt_record["num_of_concepts"] = len(cehrgpt_record["concept_ids"])
        cehrgpt_record["num_of_visits"] = len(visits)

        if record.get("index_date", None):
            cehrgpt_record["index_date"] = record["index_date"]
        if record.get("label", None):
            cehrgpt_record["label"] = record["label"]
        if record.get("age_at_index", None):
            cehrgpt_record["age_at_index"] = record["age_at_index"]

        return cehrgpt_record


class HFCehrGptTokenizationMapping(DatasetMapping):
    def __init__(
        self,
        concept_tokenizer: CehrGptTokenizer,
    ):
        self._concept_tokenizer = concept_tokenizer
        self._lab_token_ids = self._concept_tokenizer.lab_token_ids

    def remove_columns(self):
        return [
            "concept_value_masks",
            "is_numeric_types",
        ]

    def transform(self, record: Dict[str, Any]) -> Dict[str, Any]:
        # If any concept has a value associated with it, we normalize the value
        record["input_ids"] = self._concept_tokenizer.encode(record["concept_ids"])
        record["value_indicators"] = record["concept_value_masks"]
        if "number_as_values" not in record or "concept_as_values" not in record:
            record["number_as_values"] = [
                float(value) if isinstance(value, float) else None
                for value in record["concept_values"]
            ]
            record["is_numeric_types"] = [
                int(isinstance(value, float)) for value in record["concept_values"]
            ]
            record["concept_as_values"] = [
                value if isinstance(value, str) else None
                for value in record["concept_values"]
            ]
        if np.any(np.asarray(record["concept_value_masks"]) > 0):
            values = []
            for i, (
                concept_id,
                unit,
                concept_value_mask,
                number_as_value,
                concept_as_value,
                is_numeric_type,
            ) in enumerate(
                zip(
                    record["concept_ids"],
                    record["units"],
                    record["concept_value_masks"],
                    record["number_as_values"],
                    record["concept_as_values"],
                    record["is_numeric_types"],
                )
            ):
                if concept_value_mask == 1:
                    value = UNKNOWN_BIN
                    if is_numeric_type == 1:
                        if concept_id in self._concept_tokenizer.numeric_concept_ids:
                            value = self._concept_tokenizer.normalize(
                                concept_id, unit, number_as_value
                            )
                    elif isinstance(concept_as_value, str):
                        value = concept_as_value
                    values.append(value)
                else:
                    values.append(NONE_BIN)
            assert len(values) == len(record["input_ids"])
            record["values"] = self._concept_tokenizer.encode_value(values)
        else:
            record["values"] = self._concept_tokenizer.encode_value(
                [NONE_BIN for _ in range(len(record["concept_value_masks"]))]
            )
        # Delete these features because they contain null values and pyarrow cannot concatenate multiple records
        del record["number_as_values"]
        del record["concept_as_values"]
        return record


class HFFineTuningMapping(HFCehrGptTokenizationMapping):
    """Consider removing this transformation in the future."""

    def transform(self, record: Dict[str, Any]) -> Dict[str, Any]:
        record = super().transform(record)
        record.update(
            {
                "age_at_index": (
                    record["age"] if "age" in record else record["age_at_index"]
                ),
                "classifier_label": int(record["label"] > 0),
                "index_date": (
                    convert_date_to_posix_time(record["index_date"])
                    if "index_date" in record
                    else None
                ),
            }
        )
        return record

    def remove_columns(self):
        columns = super().remove_columns()
        columns.append("label")
        return columns
