# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .limit_admins_who_can_edit import LimitAdminsWhoCanEdit
from .form_multiple_choice_option import FormMultipleChoiceOption

__all__ = [
    "FormResponse",
    "Question",
    "QuestionDescriptionQuestion",
    "QuestionMultipleChoiceQuestion",
    "QuestionNumberQuestion",
    "QuestionOpenEndedQuestion",
    "QuestionYesNoQuestion",
    "QuestionYesNoQuestionAllAnswer",
    "QuestionImageSelectionQuestion",
    "QuestionImageSelectionQuestionOption",
    "QuestionImageQuestion",
    "QuestionScannerQuestion",
    "QuestionLocationQuestion",
    "QuestionAudioRecordingQuestion",
    "QuestionTaskQuestion",
    "QuestionDateQuestion",
    "QuestionRatingQuestion",
    "QuestionSignatureQuestion",
    "QuestionFileQuestion",
    "QuestionSliderQuestion",
    "QuestionFormulaQuestion",
    "Settings",
    "SettingsLimitEntriesPerUser",
    "SettingsLimitEntriesUntilTimestamp",
    "SettingsLimitTotalEntries",
    "SettingsManagerField",
    "SettingsManagerFieldFileManagerField",
    "SettingsManagerFieldSignatureManagerField",
    "SettingsManagerFieldDateManagerField",
    "SettingsManagerFieldOwnerManagerField",
    "SettingsManagerFieldNoteManagerField",
    "SettingsManagerFieldStatusManagerField",
    "SettingsManagerFieldStatusManagerFieldStatus",
]


class QuestionDescriptionQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["description"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionMultipleChoiceQuestion(BaseModel):
    all_answers: List[FormMultipleChoiceOption] = FieldInfo(alias="allAnswers")
    """List of all the options, including deleted options"""

    description: str
    """The question's description"""

    display_sorted_answers: bool = FieldInfo(alias="displaySortedAnswers")
    """Indicates if display sorted answers is enabled"""

    is_multiple_select: bool = FieldInfo(alias="isMultipleSelect")
    """Indication if multiple selection is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["multipleChoice"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionNumberQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["number"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionOpenEndedQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["openEnded"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionYesNoQuestionAllAnswer(BaseModel):
    text: str
    """The answer text"""

    yes_no_option_id: int = FieldInfo(alias="yesNoOptionId")
    """The answer option ID"""


class QuestionYesNoQuestion(BaseModel):
    all_answers: List[QuestionYesNoQuestionAllAnswer] = FieldInfo(alias="allAnswers")
    """Lise of the answer options"""

    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["yesNo"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionImageSelectionQuestionOption(BaseModel):
    image: str
    """The URL to the image"""

    image_selection_option_id: str = FieldInfo(alias="imageSelectionOptionId")
    """The answer selection option ID"""

    is_deleted: bool = FieldInfo(alias="isDeleted")
    """Indication if this option is deleted"""

    text: str
    """The option text"""


class QuestionImageSelectionQuestion(BaseModel):
    description: str
    """The question's description"""

    is_multiple_selection: bool = FieldInfo(alias="isMultipleSelection")
    """Indication if multiple selection is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    options: List[QuestionImageSelectionQuestionOption]
    """List of image selection options"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["imageSelection"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionImageQuestion(BaseModel):
    description: str
    """The question's description"""

    is_camera_enabled: bool = FieldInfo(alias="isCameraEnabled")
    """Indicates if taking a picture through camera is enabled"""

    is_gallery_enabled: bool = FieldInfo(alias="isGalleryEnabled")
    """Indicates if choosing a picture through gallery is enabled"""

    is_multiple_image_upload_allowed: bool = FieldInfo(alias="isMultipleImageUploadAllowed")
    """Indicates if multiple uploads is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["image"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionScannerQuestion(BaseModel):
    description: str
    """The question's description"""

    is_camera_enabled: bool = FieldInfo(alias="isCameraEnabled")
    """Indicates if taking a picture through camera is enabled"""

    is_gallery_enabled: bool = FieldInfo(alias="isGalleryEnabled")
    """Indicates if choosing a picture through gallery is enabled"""

    is_multiple_image_upload_allowed: bool = FieldInfo(alias="isMultipleImageUploadAllowed")
    """Indicates if multiple uploads is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["scanDocument"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionLocationQuestion(BaseModel):
    can_search_location: bool = FieldInfo(alias="canSearchLocation")
    """Indication if location search is enabled"""

    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["location"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionAudioRecordingQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["audioRecording"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionTaskQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["task"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionDateQuestion(BaseModel):
    description: str
    """The question's description"""

    is_date_active: bool = FieldInfo(alias="isDateActive")
    """Indication if selecting a date is enabled"""

    is_time_active: bool = FieldInfo(alias="isTimeActive")
    """Indication if selecting a time is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["datetime"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionRatingQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    max_value: int = FieldInfo(alias="maxValue")
    """Maximum rating value"""

    max_value_text: str = FieldInfo(alias="maxValueText")
    """Maximum rating value text"""

    min_value: int = FieldInfo(alias="minValue")
    """Minimum rating value"""

    min_value_text: str = FieldInfo(alias="minValueText")
    """Minimum rating value text"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["rating"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionSignatureQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["signature"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionFileQuestion(BaseModel):
    description: str
    """The question's description"""

    is_multiple_file_upload_allowed: bool = FieldInfo(alias="isMultipleFileUploadAllowed")
    """Indicates if multiple file uploads is enabled"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["files"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionSliderQuestion(BaseModel):
    description: str
    """The question's description"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    max_value: int = FieldInfo(alias="maxValue")
    """Maximum value in slider"""

    min_value: int = FieldInfo(alias="minValue")
    """Minimum value in slider"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["slider"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


class QuestionFormulaQuestion(BaseModel):
    description: str
    """The question's description"""

    formula_expression: str = FieldInfo(alias="formulaExpression")
    """The mathematical expression to calculate the result"""

    location_required: bool = FieldInfo(alias="locationRequired")
    """Indication if the gps location is required or not"""

    question_id: str = FieldInfo(alias="questionId")
    """The question's ID"""

    question_type: Literal["formula"] = FieldInfo(alias="questionType")
    """The type of the question"""

    submission_required: bool = FieldInfo(alias="submissionRequired")
    """Indication if this question needs to be filled to be able to submit the form"""

    title: str
    """The question's title"""


Question: TypeAlias = Annotated[
    Union[
        QuestionDescriptionQuestion,
        QuestionMultipleChoiceQuestion,
        QuestionNumberQuestion,
        QuestionOpenEndedQuestion,
        QuestionYesNoQuestion,
        QuestionImageSelectionQuestion,
        QuestionImageQuestion,
        QuestionScannerQuestion,
        QuestionLocationQuestion,
        QuestionAudioRecordingQuestion,
        QuestionTaskQuestion,
        QuestionDateQuestion,
        QuestionRatingQuestion,
        QuestionSignatureQuestion,
        QuestionFileQuestion,
        QuestionSliderQuestion,
        QuestionFormulaQuestion,
    ],
    PropertyInfo(discriminator="question_type"),
]


class SettingsLimitEntriesPerUser(BaseModel):
    enabled: bool
    """Is total number of entries per user limit enabled"""

    limit_entries_per_user: int = FieldInfo(alias="limitEntriesPerUser")
    """The amount of entries that can be submitted per user"""


class SettingsLimitEntriesUntilTimestamp(BaseModel):
    enabled: bool
    """Is time limit until when entries can be submitted enabled"""

    limit_entries_until_timestamp: int = FieldInfo(alias="limitEntriesUntilTimestamp")
    """The time limit indicating until when entries can be submitted"""


class SettingsLimitTotalEntries(BaseModel):
    enabled: bool
    """Is total number of entries limit enabled"""

    limit_total_entries: int = FieldInfo(alias="limitTotalEntries")
    """The amount of entries that can be submitted"""


class SettingsManagerFieldFileManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["file"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""


class SettingsManagerFieldSignatureManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["signature"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""


class SettingsManagerFieldDateManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["date"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""


class SettingsManagerFieldOwnerManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["owner"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""


class SettingsManagerFieldNoteManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["note"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""


class SettingsManagerFieldStatusManagerFieldStatus(BaseModel):
    color: str
    """The status's background color"""

    manager_field_status_id: str = FieldInfo(alias="managerFieldStatusId")
    """The Manager Field's status ID"""

    name: str
    """The Manager Field's status"""


class SettingsManagerFieldStatusManagerField(BaseModel):
    admins_who_can_edit: LimitAdminsWhoCanEdit = FieldInfo(alias="adminsWhoCanEdit")
    """Limit the admins who can edit this manager field.

    Owners can always edit the manager field.
    """

    manager_field_id: str = FieldInfo(alias="managerFieldId")
    """The Manager Field's ID"""

    manager_field_type: Literal["status"] = FieldInfo(alias="managerFieldType")
    """The Manager Field's type"""

    mobile_users_can_see: bool = FieldInfo(alias="mobileUsersCanSee")
    """Indication if mobile users can see the Manager Field"""

    mobile_users_notify_when_changes: bool = FieldInfo(alias="mobileUsersNotifyWhenChanges")
    """Indication if mobile users will be notified if the Manager Field changes"""

    name: str
    """The Manager Field's name"""

    statuses: List[SettingsManagerFieldStatusManagerFieldStatus]
    """List of Manager Field's possible statuses"""


SettingsManagerField: TypeAlias = Annotated[
    Union[
        SettingsManagerFieldFileManagerField,
        SettingsManagerFieldSignatureManagerField,
        SettingsManagerFieldDateManagerField,
        SettingsManagerFieldOwnerManagerField,
        SettingsManagerFieldNoteManagerField,
        SettingsManagerFieldStatusManagerField,
    ],
    PropertyInfo(discriminator="manager_field_type"),
]


class Settings(BaseModel):
    enable_users_to_download_pdf: bool = FieldInfo(alias="enableUsersToDownloadPdf")
    """Indication if users can download a PDF of the entry"""

    is_anonymous: bool = FieldInfo(alias="isAnonymous")
    """Indication if the form submissions are anonymous"""

    limit_entries_per_user: SettingsLimitEntriesPerUser = FieldInfo(alias="limitEntriesPerUser")
    """The settings for the total number of entries per user limit"""

    limit_entries_until_timestamp: SettingsLimitEntriesUntilTimestamp = FieldInfo(alias="limitEntriesUntilTimestamp")
    """The settings for time limit indicating until when entries can be submitted"""

    limit_total_entries: SettingsLimitTotalEntries = FieldInfo(alias="limitTotalEntries")
    """The settings for the total number of entries limit"""

    manager_fields: List[SettingsManagerField] = FieldInfo(alias="managerFields")
    """List of manager fields in the form"""


class FormResponse(BaseModel):
    created_at: int = FieldInfo(alias="createdAt")
    """Form's creation timestamp"""

    form_id: int = FieldInfo(alias="formId")
    """The Form's ID"""

    form_name: str = FieldInfo(alias="formName")
    """The Form's title"""

    last_updated_at: int = FieldInfo(alias="lastUpdatedAt")
    """The Form's last update timestamp"""

    questions: List[Question]
    """List of the Form's questions"""

    settings: Settings
    """The Form's settings"""
