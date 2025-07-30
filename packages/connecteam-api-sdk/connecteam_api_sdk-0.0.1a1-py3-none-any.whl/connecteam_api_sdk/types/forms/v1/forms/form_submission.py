# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from ....._utils import PropertyInfo
from .form_image import FormImage
from ....._models import BaseModel
from .manager_field_file import ManagerFieldFile
from ....time_clock.v1.gps_data import GpsData
from .manager_field_status_option import ManagerFieldStatusOption
from ..form_multiple_choice_option import FormMultipleChoiceOption

__all__ = [
    "FormSubmission",
    "Answer",
    "AnswerDescriptionAnswer",
    "AnswerMultipleChoiceAnswer",
    "AnswerNumberAnswer",
    "AnswerOpenEndedAnswer",
    "AnswerYesNoAnswer",
    "AnswerScannerAnswer",
    "AnswerImageSelectionAnswer",
    "AnswerImageSelectionAnswerSelectedAnswer",
    "AnswerLocationAnswer",
    "AnswerAudioAnswer",
    "AnswerTaskAnswer",
    "AnswerDateTimeAnswer",
    "AnswerRatingAnswer",
    "AnswerImageAnswer",
    "AnswerSignatureAnswer",
    "AnswerFilesAnswer",
    "AnswerFilesAnswerFile",
    "AnswerSliderAnswer",
    "AnswerFormulaAnswer",
    "ManagerField",
    "ManagerFieldManagerFieldDate",
    "ManagerFieldManagerFieldFile",
    "ManagerFieldManagerFieldSignature",
    "ManagerFieldManagerFieldOwner",
    "ManagerFieldV2FeaturesWorkflowExternalAPIV1FormSubmissionsModelsResponseFormSubmissionResponseModelManagerFieldStatus",
    "ManagerFieldManagerFieldNote",
]


class AnswerDescriptionAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["description"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerMultipleChoiceAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    selected_answers: List[FormMultipleChoiceOption] = FieldInfo(alias="selectedAnswers")
    """The selected answers."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["multipleChoice"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerNumberAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    input_value: Optional[float] = FieldInfo(alias="inputValue", default=None)
    """The input value."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["number"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerOpenEndedAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["openEnded"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    value: Optional[str] = None
    """The input text."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerYesNoAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["yesNo"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    selected_index: Optional[int] = FieldInfo(alias="selectedIndex", default=None)
    """The selected index."""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerScannerAnswer(BaseModel):
    images: List[FormImage]
    """The images."""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["scanDocument"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerImageSelectionAnswerSelectedAnswer(BaseModel):
    image: str
    """The URL of the image."""

    image_selection_id: str = FieldInfo(alias="imageSelectionId")
    """The ID of the image selection."""

    text: str
    """The text of the image selection."""


class AnswerImageSelectionAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    selected_answers: List[AnswerImageSelectionAnswerSelectedAnswer] = FieldInfo(alias="selectedAnswers")
    """The selected answers."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["imageSelection"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerLocationAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    location_input: Optional[GpsData] = FieldInfo(alias="locationInput", default=None)
    """The location input."""

    question_type: Optional[Literal["location"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerAudioAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    audio_length: Optional[int] = FieldInfo(alias="audioLength", default=None)
    """The audio length in seconds."""

    audio_url: Optional[str] = FieldInfo(alias="audioUrl", default=None)
    """The audio url."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["audioRecording"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerTaskAnswer(BaseModel):
    is_checked: bool = FieldInfo(alias="isChecked")
    """Whether the task is checked"""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["task"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerDateTimeAnswer(BaseModel):
    is_date_submitted: bool = FieldInfo(alias="isDateSubmitted")
    """Whether the date was submitted."""

    is_time_submitted: bool = FieldInfo(alias="isTimeSubmitted")
    """Whether the time was submitted."""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["datetime"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    timestamp: Optional[int] = None
    """The timestamp of the answer."""

    timezone: Optional[str] = None
    """The timezone of the answer."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerRatingAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["rating"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    rating_value: Optional[int] = FieldInfo(alias="ratingValue", default=None)
    """The rating value."""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerImageAnswer(BaseModel):
    images: List[FormImage]
    """The images."""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["image"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerSignatureAnswer(BaseModel):
    images: List[FormImage]
    """The images."""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["signature"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerFilesAnswerFile(BaseModel):
    file_name: str = FieldInfo(alias="fileName")
    """The name of the file."""

    size: int
    """The size of the file in bytes."""

    url: str
    """The URL of the file."""


class AnswerFilesAnswer(BaseModel):
    files: List[AnswerFilesAnswerFile]
    """The files."""

    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["files"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerSliderAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["slider"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    value: Optional[int] = None
    """The value of the slider."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


class AnswerFormulaAnswer(BaseModel):
    question_id: str = FieldInfo(alias="questionId")
    """The questions id."""

    was_submitted_empty: bool = FieldInfo(alias="wasSubmittedEmpty")
    """Whether the submission was empty."""

    location: Optional[GpsData] = None
    """The location of the submission."""

    question_type: Optional[Literal["formula"]] = FieldInfo(alias="questionType", default=None)
    """The questions type"""

    result: Optional[float] = None
    """The result of the formula."""

    status: Optional[str] = None
    """The status of the formula."""

    submission_timestamp: Optional[int] = FieldInfo(alias="submissionTimestamp", default=None)
    """The timestamp of the submission."""

    update_timestamp: Optional[int] = FieldInfo(alias="updateTimestamp", default=None)
    """The timestamp of the last update."""

    update_user_id: Optional[int] = FieldInfo(alias="updateUserId", default=None)
    """The user id of the last update."""

    was_hidden: Optional[bool] = FieldInfo(alias="wasHidden", default=None)
    """Whether the submission was hidden (by a condition)."""


Answer: TypeAlias = Annotated[
    Union[
        AnswerDescriptionAnswer,
        AnswerMultipleChoiceAnswer,
        AnswerNumberAnswer,
        AnswerOpenEndedAnswer,
        AnswerYesNoAnswer,
        AnswerScannerAnswer,
        AnswerImageSelectionAnswer,
        AnswerLocationAnswer,
        AnswerAudioAnswer,
        AnswerTaskAnswer,
        AnswerDateTimeAnswer,
        AnswerRatingAnswer,
        AnswerImageAnswer,
        AnswerSignatureAnswer,
        AnswerFilesAnswer,
        AnswerSliderAnswer,
        AnswerFormulaAnswer,
    ],
    PropertyInfo(discriminator="question_type"),
]


class ManagerFieldManagerFieldDate(BaseModel):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    date: Optional[str] = None
    """The date filled in the field."""

    manager_field_type: Optional[Literal["date"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""


class ManagerFieldManagerFieldFile(BaseModel):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    files: Optional[List[ManagerFieldFile]] = None
    """The files."""

    manager_field_type: Optional[Literal["file"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""


class ManagerFieldManagerFieldSignature(BaseModel):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    image: Optional[str] = None
    """The image of the signature."""

    manager_field_type: Optional[Literal["signature"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""

    signing_timestamp: Optional[int] = FieldInfo(alias="signingTimestamp", default=None)
    """The timestamp of the signing."""

    signing_user_id: Optional[int] = FieldInfo(alias="signingUserId", default=None)
    """The user id of the signing user."""


class ManagerFieldManagerFieldOwner(BaseModel):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    manager_field_type: Optional[Literal["owner"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""

    user_id: Optional[int] = FieldInfo(alias="userId", default=None)
    """The user id of the assigned owner."""


class ManagerFieldV2FeaturesWorkflowExternalAPIV1FormSubmissionsModelsResponseFormSubmissionResponseModelManagerFieldStatus(
    BaseModel
):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    last_updated_timestamp: Optional[int] = FieldInfo(alias="lastUpdatedTimestamp", default=None)
    """The timestamp of the status update."""

    manager_field_type: Optional[Literal["status"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""

    status: Optional[ManagerFieldStatusOption] = None
    """The status of the field."""


class ManagerFieldManagerFieldNote(BaseModel):
    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The manager field id."""

    manager_field_type: Optional[Literal["note"]] = FieldInfo(alias="managerFieldType", default=None)
    """The field type"""

    note: Optional[str] = None
    """The note filled in the field."""


ManagerField: TypeAlias = Annotated[
    Union[
        ManagerFieldManagerFieldDate,
        ManagerFieldManagerFieldFile,
        ManagerFieldManagerFieldSignature,
        ManagerFieldManagerFieldOwner,
        ManagerFieldV2FeaturesWorkflowExternalAPIV1FormSubmissionsModelsResponseFormSubmissionResponseModelManagerFieldStatus,
        ManagerFieldManagerFieldNote,
    ],
    PropertyInfo(discriminator="manager_field_type"),
]


class FormSubmission(BaseModel):
    answers: List[Answer]
    """The answers."""

    entry_num: int = FieldInfo(alias="entryNum")
    """The entry number."""

    form_id: int = FieldInfo(alias="formId")
    """The forms id."""

    form_submission_id: str = FieldInfo(alias="formSubmissionId")
    """The form submission id."""

    is_anonymous: bool = FieldInfo(alias="isAnonymous")
    """Whether the submission is anonymous."""

    manager_fields: List[ManagerField] = FieldInfo(alias="managerFields")
    """The manager fields."""

    submission_timestamp: int = FieldInfo(alias="submissionTimestamp")
    """The timestamp of the submission."""

    submission_timezone: str = FieldInfo(alias="submissionTimezone")
    """The timezone of the submission."""

    submitting_user_id: int = FieldInfo(alias="submittingUserId")
    """The user id of the submitting user."""
