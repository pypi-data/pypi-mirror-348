# Me

Types:

```python
from connecteam_api_sdk.types import MeRetrieveResponse
```

Methods:

- <code title="get /me">client.me.<a href="./src/connecteam_api_sdk/resources/me.py">retrieve</a>() -> <a href="./src/connecteam_api_sdk/types/me_retrieve_response.py">MeRetrieveResponse</a></code>

# Settings

## V1

### Webhooks

Types:

```python
from connecteam_api_sdk.types.settings.v1 import (
    PagingResponse,
    PublicBaseWebhookResponse,
    WebhookListResponse,
    WebhookDeleteResponse,
)
```

Methods:

- <code title="post /settings/v1/webhooks">client.settings.v1.webhooks.<a href="./src/connecteam_api_sdk/resources/settings/v1/webhooks.py">create</a>(\*\*<a href="src/connecteam_api_sdk/types/settings/v1/webhook_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/settings/v1/public_base_webhook_response.py">PublicBaseWebhookResponse</a></code>
- <code title="get /settings/v1/webhooks/{webhookId}">client.settings.v1.webhooks.<a href="./src/connecteam_api_sdk/resources/settings/v1/webhooks.py">retrieve</a>(webhook_id) -> <a href="./src/connecteam_api_sdk/types/settings/v1/public_base_webhook_response.py">PublicBaseWebhookResponse</a></code>
- <code title="put /settings/v1/webhooks/{webhookId}">client.settings.v1.webhooks.<a href="./src/connecteam_api_sdk/resources/settings/v1/webhooks.py">update</a>(webhook_id, \*\*<a href="src/connecteam_api_sdk/types/settings/v1/webhook_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/settings/v1/public_base_webhook_response.py">PublicBaseWebhookResponse</a></code>
- <code title="get /settings/v1/webhooks">client.settings.v1.webhooks.<a href="./src/connecteam_api_sdk/resources/settings/v1/webhooks.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/settings/v1/webhook_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/settings/v1/webhook_list_response.py">WebhookListResponse</a></code>
- <code title="delete /settings/v1/webhooks/{webhookId}">client.settings.v1.webhooks.<a href="./src/connecteam_api_sdk/resources/settings/v1/webhooks.py">delete</a>(webhook_id) -> <a href="./src/connecteam_api_sdk/types/settings/v1/webhook_delete_response.py">WebhookDeleteResponse</a></code>

# Attachments

## V1

### Files

Types:

```python
from connecteam_api_sdk.types.attachments.v1 import (
    FileRetrieveResponse,
    FileCompleteUploadResponse,
    FileGenerateUploadURLResponse,
)
```

Methods:

- <code title="get /attachments/v1/files/{fileId}">client.attachments.v1.files.<a href="./src/connecteam_api_sdk/resources/attachments/v1/files.py">retrieve</a>(file_id) -> <a href="./src/connecteam_api_sdk/types/attachments/v1/file_retrieve_response.py">FileRetrieveResponse</a></code>
- <code title="put /attachments/v1/files/complete-upload/{fileId}">client.attachments.v1.files.<a href="./src/connecteam_api_sdk/resources/attachments/v1/files.py">complete_upload</a>(file_id) -> <a href="./src/connecteam_api_sdk/types/attachments/v1/file_complete_upload_response.py">FileCompleteUploadResponse</a></code>
- <code title="post /attachments/v1/files/generate-upload-url">client.attachments.v1.files.<a href="./src/connecteam_api_sdk/resources/attachments/v1/files.py">generate_upload_url</a>(\*\*<a href="src/connecteam_api_sdk/types/attachments/v1/file_generate_upload_url_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/attachments/v1/file_generate_upload_url_response.py">FileGenerateUploadURLResponse</a></code>

# Forms

## V1

### Forms

Types:

```python
from connecteam_api_sdk.types.forms.v1 import (
    FormMultipleChoiceOption,
    FormResponse,
    LimitAdminsWhoCanEdit,
    FormRetrieveResponse,
    FormListResponse,
)
```

Methods:

- <code title="get /forms/v1/forms/{formId}">client.forms.v1.forms.<a href="./src/connecteam_api_sdk/resources/forms/v1/forms/forms.py">retrieve</a>(form_id) -> <a href="./src/connecteam_api_sdk/types/forms/v1/form_retrieve_response.py">FormRetrieveResponse</a></code>
- <code title="get /forms/v1/forms">client.forms.v1.forms.<a href="./src/connecteam_api_sdk/resources/forms/v1/forms/forms.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/forms/v1/form_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/forms/v1/form_list_response.py">FormListResponse</a></code>

#### FormSubmissions

Types:

```python
from connecteam_api_sdk.types.forms.v1.forms import (
    FormImage,
    FormSubmission,
    ManagerFieldFile,
    ManagerFieldStatusOption,
    FormSubmissionRetrieveResponse,
    FormSubmissionUpdateResponse,
    FormSubmissionListResponse,
)
```

Methods:

- <code title="get /forms/v1/forms/{formId}/form-submissions/{formSubmissionId}">client.forms.v1.forms.form_submissions.<a href="./src/connecteam_api_sdk/resources/forms/v1/forms/form_submissions.py">retrieve</a>(form_submission_id, \*, form_id) -> <a href="./src/connecteam_api_sdk/types/forms/v1/forms/form_submission_retrieve_response.py">FormSubmissionRetrieveResponse</a></code>
- <code title="put /forms/v1/forms/{formId}/form-submissions/{formSubmissionId}">client.forms.v1.forms.form_submissions.<a href="./src/connecteam_api_sdk/resources/forms/v1/forms/form_submissions.py">update</a>(form_submission_id, \*, form_id, \*\*<a href="src/connecteam_api_sdk/types/forms/v1/forms/form_submission_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/forms/v1/forms/form_submission_update_response.py">FormSubmissionUpdateResponse</a></code>
- <code title="get /forms/v1/forms/{formId}/form-submissions">client.forms.v1.forms.form_submissions.<a href="./src/connecteam_api_sdk/resources/forms/v1/forms/form_submissions.py">list</a>(form_id, \*\*<a href="src/connecteam_api_sdk/types/forms/v1/forms/form_submission_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/forms/v1/forms/form_submission_list_response.py">FormSubmissionListResponse</a></code>

# Scheduler

## V1

### Schedulers

Types:

```python
from connecteam_api_sdk.types.scheduler.v1 import (
    TimestampWithTimezoneScheduler,
    SchedulerListResponse,
    SchedulerGetUserUnavailabilitiesResponse,
)
```

Methods:

- <code title="get /scheduler/v1/schedulers">client.scheduler.v1.schedulers.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/schedulers.py">list</a>() -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/scheduler_list_response.py">SchedulerListResponse</a></code>
- <code title="get /scheduler/v1/schedulers/user-unavailability">client.scheduler.v1.schedulers.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/schedulers.py">get_user_unavailabilities</a>(\*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/scheduler_get_user_unavailabilities_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/scheduler_get_user_unavailabilities_response.py">SchedulerGetUserUnavailabilitiesResponse</a></code>

#### Shifts

Types:

```python
from connecteam_api_sdk.types.scheduler.v1.schedulers import (
    APIResponseShiftBulk,
    HTMLNoteData,
    LocationData,
    ShiftBreakType,
    ShiftBulkResponse,
    ShiftResponseScheduler,
    SortOrder,
    ShiftRetrieveResponse,
    ShiftListResponse,
    ShiftDeleteResponse,
    ShiftDeleteShiftResponse,
)
```

Methods:

- <code title="post /scheduler/v1/schedulers/{schedulerId}/shifts">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">create</a>(scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/api_response_shift_bulk.py">APIResponseShiftBulk</a></code>
- <code title="get /scheduler/v1/schedulers/{schedulerId}/shifts/{shiftId}">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">retrieve</a>(shift_id, \*, scheduler_id) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_retrieve_response.py">ShiftRetrieveResponse</a></code>
- <code title="put /scheduler/v1/schedulers/{schedulerId}/shifts">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">update</a>(scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/api_response_shift_bulk.py">APIResponseShiftBulk</a></code>
- <code title="get /scheduler/v1/schedulers/{schedulerId}/shifts">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">list</a>(scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_list_response.py">ShiftListResponse</a></code>
- <code title="delete /scheduler/v1/schedulers/{schedulerId}/shifts">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">delete</a>(scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_delete_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_delete_response.py">ShiftDeleteResponse</a></code>
- <code title="delete /scheduler/v1/schedulers/{schedulerId}/shifts/{shiftId}">client.scheduler.v1.schedulers.shifts.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/shifts.py">delete_shift</a>(shift_id, \*, scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_delete_shift_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_delete_shift_response.py">ShiftDeleteShiftResponse</a></code>

##### AutoAssign

Types:

```python
from connecteam_api_sdk.types.scheduler.v1.schedulers.shifts import (
    AutoAssignCreateRequestResponse,
    AutoAssignGetStatusResponse,
)
```

Methods:

- <code title="post /scheduler/v1/schedulers/{schedulerId}/shifts/auto-assign">client.scheduler.v1.schedulers.shifts.auto_assign.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/auto_assign.py">create_request</a>(scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shifts/auto_assign_create_request_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shifts/auto_assign_create_request_response.py">AutoAssignCreateRequestResponse</a></code>
- <code title="get /scheduler/v1/schedulers/{schedulerId}/shifts/auto-assign/{autoAssignRequestId}">client.scheduler.v1.schedulers.shifts.auto_assign.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shifts/auto_assign.py">get_status</a>(auto_assign_request_id, \*, scheduler_id) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shifts/auto_assign_get_status_response.py">AutoAssignGetStatusResponse</a></code>

#### ShiftLayers

Types:

```python
from connecteam_api_sdk.types.scheduler.v1.schedulers import (
    ShiftLayerListResponse,
    ShiftLayerGetValuesResponse,
)
```

Methods:

- <code title="get /scheduler/v1/schedulers/{schedulerId}/shift-layers">client.scheduler.v1.schedulers.shift_layers.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shift_layers.py">list</a>(scheduler_id) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_layer_list_response.py">ShiftLayerListResponse</a></code>
- <code title="get /scheduler/v1/schedulers/{schedulerId}/shift-layers/{layerId}/values">client.scheduler.v1.schedulers.shift_layers.<a href="./src/connecteam_api_sdk/resources/scheduler/v1/schedulers/shift_layers.py">get_values</a>(layer_id, \*, scheduler_id, \*\*<a href="src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_layer_get_values_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/scheduler/v1/schedulers/shift_layer_get_values_response.py">ShiftLayerGetValuesResponse</a></code>

# Jobs

## V1

### Jobs

Types:

```python
from connecteam_api_sdk.types.jobs.v1 import (
    APIResponse,
    AssignDataIn,
    AssignDataTypes,
    BaseJobResponse,
    JobsResponse,
    JobCreateResponse,
    JobListResponse,
    JobDeleteResponse,
)
```

Methods:

- <code title="post /jobs/v1/jobs">client.jobs.v1.jobs.<a href="./src/connecteam_api_sdk/resources/jobs/v1/jobs.py">create</a>(\*\*<a href="src/connecteam_api_sdk/types/jobs/v1/job_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/jobs/v1/job_create_response.py">JobCreateResponse</a></code>
- <code title="get /jobs/v1/jobs/{jobId}">client.jobs.v1.jobs.<a href="./src/connecteam_api_sdk/resources/jobs/v1/jobs.py">retrieve</a>(job_id) -> <a href="./src/connecteam_api_sdk/types/jobs/v1/api_response.py">APIResponse</a></code>
- <code title="put /jobs/v1/jobs/{jobId}">client.jobs.v1.jobs.<a href="./src/connecteam_api_sdk/resources/jobs/v1/jobs.py">update</a>(job_id, \*\*<a href="src/connecteam_api_sdk/types/jobs/v1/job_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/jobs/v1/api_response.py">APIResponse</a></code>
- <code title="get /jobs/v1/jobs">client.jobs.v1.jobs.<a href="./src/connecteam_api_sdk/resources/jobs/v1/jobs.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/jobs/v1/job_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/jobs/v1/job_list_response.py">JobListResponse</a></code>
- <code title="delete /jobs/v1/jobs/{jobId}">client.jobs.v1.jobs.<a href="./src/connecteam_api_sdk/resources/jobs/v1/jobs.py">delete</a>(job_id) -> <a href="./src/connecteam_api_sdk/types/jobs/v1/job_delete_response.py">JobDeleteResponse</a></code>

# Users

## V1

Types:

```python
from connecteam_api_sdk.types.users import (
    V1GetCustomFieldCategoriesResponse,
    V1GetPerformanceIndicatorsResponse,
    V1GetSmartGroupsResponse,
)
```

Methods:

- <code title="get /users/v1/custom-field-categories">client.users.v1.<a href="./src/connecteam_api_sdk/resources/users/v1/v1.py">get_custom_field_categories</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1_get_custom_field_categories_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1_get_custom_field_categories_response.py">V1GetCustomFieldCategoriesResponse</a></code>
- <code title="get /users/v1/performance-indicators">client.users.v1.<a href="./src/connecteam_api_sdk/resources/users/v1/v1.py">get_performance_indicators</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1_get_performance_indicators_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1_get_performance_indicators_response.py">V1GetPerformanceIndicatorsResponse</a></code>
- <code title="get /users/v1/smart-groups">client.users.v1.<a href="./src/connecteam_api_sdk/resources/users/v1/v1.py">get_smart_groups</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1_get_smart_groups_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1_get_smart_groups_response.py">V1GetSmartGroupsResponse</a></code>
- <code title="post /users/v1/admins">client.users.v1.<a href="./src/connecteam_api_sdk/resources/users/v1/v1.py">promote_admin</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1_promote_admin_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_base.py">APIResponseBase</a></code>

### Users

Types:

```python
from connecteam_api_sdk.types.users.v1 import (
    BaseCustomField,
    User,
    UserType,
    UserCreateResponse,
    UserUpdateResponse,
    UserListResponse,
    UserArchiveResponse,
    UserCreateNoteResponse,
    UserUpdatePerformanceResponse,
)
```

Methods:

- <code title="post /users/v1/users">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">create</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/user_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_create_response.py">UserCreateResponse</a></code>
- <code title="put /users/v1/users">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">update</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/user_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_update_response.py">UserUpdateResponse</a></code>
- <code title="get /users/v1/users">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/user_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_list_response.py">UserListResponse</a></code>
- <code title="delete /users/v1/users">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">archive</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/user_archive_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_archive_response.py">UserArchiveResponse</a></code>
- <code title="post /users/v1/users/{userId}/notes">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">create_note</a>(user_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/user_create_note_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_create_note_response.py">UserCreateNoteResponse</a></code>
- <code title="put /users/v1/users/{userId}/performance/{date}">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">update_performance</a>(date, \*, user_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/user_update_performance_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/user_update_performance_response.py">UserUpdatePerformanceResponse</a></code>
- <code title="post /users/v1/users/{userId}/payslips">client.users.v1.users.<a href="./src/connecteam_api_sdk/resources/users/v1/users.py">upload_payslip</a>(user_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/user_upload_payslip_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_base.py">APIResponseBase</a></code>

### CustomFields

Types:

```python
from connecteam_api_sdk.types.users.v1 import (
    APIResponseGetCustomFieldsSettings,
    GetCustomFieldsSettings,
    UserCustomFields,
    CustomFieldListResponse,
    CustomFieldDeleteResponse,
)
```

Methods:

- <code title="post /users/v1/custom-fields">client.users.v1.custom_fields.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/custom_fields.py">create</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_field_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/api_response_get_custom_fields_settings.py">APIResponseGetCustomFieldsSettings</a></code>
- <code title="put /users/v1/custom-fields">client.users.v1.custom_fields.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/custom_fields.py">update</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_field_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/api_response_get_custom_fields_settings.py">APIResponseGetCustomFieldsSettings</a></code>
- <code title="get /users/v1/custom-fields">client.users.v1.custom_fields.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/custom_fields.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_field_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_field_list_response.py">CustomFieldListResponse</a></code>
- <code title="delete /users/v1/custom-fields">client.users.v1.custom_fields.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/custom_fields.py">delete</a>(\*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_field_delete_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_field_delete_response.py">CustomFieldDeleteResponse</a></code>

#### Options

Types:

```python
from connecteam_api_sdk.types.users.v1.custom_fields import (
    APIResponseBase,
    APIResponseDropdownCustomFieldOption,
    CreateDropdownCustomFieldOption,
    DropdownCustomFieldOptionResponse,
    OptionListResponse,
)
```

Methods:

- <code title="post /users/v1/custom-fields/{customFieldId}/options">client.users.v1.custom_fields.options.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/options.py">create</a>(custom_field_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_fields/option_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_dropdown_custom_field_option.py">APIResponseDropdownCustomFieldOption</a></code>
- <code title="put /users/v1/custom-fields/{customFieldId}/options/{optionId}">client.users.v1.custom_fields.options.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/options.py">update</a>(option_id, \*, custom_field_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_fields/option_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_dropdown_custom_field_option.py">APIResponseDropdownCustomFieldOption</a></code>
- <code title="get /users/v1/custom-fields/{customFieldId}/options">client.users.v1.custom_fields.options.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/options.py">list</a>(custom_field_id, \*\*<a href="src/connecteam_api_sdk/types/users/v1/custom_fields/option_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/option_list_response.py">OptionListResponse</a></code>
- <code title="delete /users/v1/custom-fields/{customFieldId}/options/{optionId}">client.users.v1.custom_fields.options.<a href="./src/connecteam_api_sdk/resources/users/v1/custom_fields/options.py">delete</a>(option_id, \*, custom_field_id) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_base.py">APIResponseBase</a></code>

# TimeOff

## V1

Types:

```python
from connecteam_api_sdk.types.time_off import V1CreateRequestResponse
```

Methods:

- <code title="post /time-off/v1/requests">client.time_off.v1.<a href="./src/connecteam_api_sdk/resources/time_off/v1/v1.py">create_request</a>(\*\*<a href="src/connecteam_api_sdk/types/time_off/v1_create_request_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_off/v1_create_request_response.py">V1CreateRequestResponse</a></code>

### PolicyTypes

Types:

```python
from connecteam_api_sdk.types.time_off.v1 import PolicyTypeListResponse
```

Methods:

- <code title="get /time-off/v1/policy-types">client.time_off.v1.policy_types.<a href="./src/connecteam_api_sdk/resources/time_off/v1/policy_types/policy_types.py">list</a>() -> <a href="./src/connecteam_api_sdk/types/time_off/v1/policy_type_list_response.py">PolicyTypeListResponse</a></code>

#### Balances

Types:

```python
from connecteam_api_sdk.types.time_off.v1.policy_types import (
    TimeOffUserBalance,
    BalanceUpdateResponse,
    BalanceListResponse,
)
```

Methods:

- <code title="put /time-off/v1/policy-types/{policyTypeId}/balances/{userId}">client.time_off.v1.policy_types.balances.<a href="./src/connecteam_api_sdk/resources/time_off/v1/policy_types/balances.py">update</a>(user_id, \*, policy_type_id, \*\*<a href="src/connecteam_api_sdk/types/time_off/v1/policy_types/balance_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_off/v1/policy_types/balance_update_response.py">BalanceUpdateResponse</a></code>
- <code title="get /time-off/v1/policy-types/{policyTypeId}/balances">client.time_off.v1.policy_types.balances.<a href="./src/connecteam_api_sdk/resources/time_off/v1/policy_types/balances.py">list</a>(policy_type_id, \*\*<a href="src/connecteam_api_sdk/types/time_off/v1/policy_types/balance_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_off/v1/policy_types/balance_list_response.py">BalanceListResponse</a></code>

# TimeClock

## V1

### TimeClocks

Types:

```python
from connecteam_api_sdk.types.time_clock.v1 import (
    GpsData,
    ShiftAttachmentType,
    ShiftResponseTimeClock,
    TimeActivityTimePoint,
    TimeClockListResponse,
    TimeClockClockInResponse,
    TimeClockClockOutResponse,
    TimeClockGetManualBreaksResponse,
    TimeClockGetShiftAttachmentsResponse,
)
```

Methods:

- <code title="get /time-clock/v1/time-clocks">client.time_clock.v1.time_clocks.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_clocks.py">list</a>() -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clock_list_response.py">TimeClockListResponse</a></code>
- <code title="post /time-clock/v1/time-clocks/{timeClockId}/clock-in">client.time_clock.v1.time_clocks.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_clocks.py">clock_in</a>(time_clock_id, \*\*<a href="src/connecteam_api_sdk/types/time_clock/v1/time_clock_clock_in_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clock_clock_in_response.py">TimeClockClockInResponse</a></code>
- <code title="post /time-clock/v1/time-clocks/{timeClockId}/clock-out">client.time_clock.v1.time_clocks.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_clocks.py">clock_out</a>(time_clock_id, \*\*<a href="src/connecteam_api_sdk/types/time_clock/v1/time_clock_clock_out_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clock_clock_out_response.py">TimeClockClockOutResponse</a></code>
- <code title="get /time-clock/v1/time-clocks/{timeClockId}/manual-breaks">client.time_clock.v1.time_clocks.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_clocks.py">get_manual_breaks</a>(time_clock_id) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clock_get_manual_breaks_response.py">TimeClockGetManualBreaksResponse</a></code>
- <code title="get /time-clock/v1/time-clocks/{timeClockId}/shift-attachments">client.time_clock.v1.time_clocks.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_clocks.py">get_shift_attachments</a>(time_clock_id) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clock_get_shift_attachments_response.py">TimeClockGetShiftAttachmentsResponse</a></code>

#### TimeActivities

Types:

```python
from connecteam_api_sdk.types.time_clock.v1.time_clocks import (
    TimestampWithTimezoneActivity,
    UserTimeActivity,
    TimeActivityCreateResponse,
    TimeActivityUpdateResponse,
    TimeActivityListResponse,
)
```

Methods:

- <code title="post /time-clock/v1/time-clocks/{timeClockId}/time-activities">client.time_clock.v1.time_clocks.time_activities.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_activities.py">create</a>(time_clock_id, \*\*<a href="src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_create_response.py">TimeActivityCreateResponse</a></code>
- <code title="put /time-clock/v1/time-clocks/{timeClockId}/time-activities">client.time_clock.v1.time_clocks.time_activities.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_activities.py">update</a>(time_clock_id, \*\*<a href="src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_update_response.py">TimeActivityUpdateResponse</a></code>
- <code title="get /time-clock/v1/time-clocks/{timeClockId}/time-activities">client.time_clock.v1.time_clocks.time_activities.<a href="./src/connecteam_api_sdk/resources/time_clock/v1/time_clocks/time_activities.py">list</a>(time_clock_id, \*\*<a href="src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/time_clock/v1/time_clocks/time_activity_list_response.py">TimeActivityListResponse</a></code>

# Tasks

## V1

### Taskboards

Types:

```python
from connecteam_api_sdk.types.tasks.v1 import TaskboardListResponse, TaskboardGetLabelsResponse
```

Methods:

- <code title="get /tasks/v1/taskboards">client.tasks.v1.taskboards.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/taskboards.py">list</a>() -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboard_list_response.py">TaskboardListResponse</a></code>
- <code title="get /tasks/v1/taskboards/{taskBoardId}/labels">client.tasks.v1.taskboards.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/taskboards.py">get_labels</a>(task_board_id, \*\*<a href="src/connecteam_api_sdk/types/tasks/v1/taskboard_get_labels_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboard_get_labels_response.py">TaskboardGetLabelsResponse</a></code>

#### Tasks

Types:

```python
from connecteam_api_sdk.types.tasks.v1.taskboards import (
    TaskDescription,
    TaskStatus,
    TaskType,
    TaskCreateResponse,
    TaskUpdateResponse,
    TaskListResponse,
    TaskDeleteResponse,
)
```

Methods:

- <code title="post /tasks/v1/taskboards/{taskBoardId}/tasks">client.tasks.v1.taskboards.tasks.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/tasks.py">create</a>(task_board_id, \*\*<a href="src/connecteam_api_sdk/types/tasks/v1/taskboards/task_create_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboards/task_create_response.py">TaskCreateResponse</a></code>
- <code title="put /tasks/v1/taskboards/{taskBoardId}/tasks/{taskId}">client.tasks.v1.taskboards.tasks.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/tasks.py">update</a>(task_id, \*, task_board_id, \*\*<a href="src/connecteam_api_sdk/types/tasks/v1/taskboards/task_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboards/task_update_response.py">TaskUpdateResponse</a></code>
- <code title="get /tasks/v1/taskboards/{taskBoardId}/tasks">client.tasks.v1.taskboards.tasks.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/tasks.py">list</a>(task_board_id, \*\*<a href="src/connecteam_api_sdk/types/tasks/v1/taskboards/task_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboards/task_list_response.py">TaskListResponse</a></code>
- <code title="delete /tasks/v1/taskboards/{taskBoardId}/tasks/{taskId}">client.tasks.v1.taskboards.tasks.<a href="./src/connecteam_api_sdk/resources/tasks/v1/taskboards/tasks.py">delete</a>(task_id, \*, task_board_id) -> <a href="./src/connecteam_api_sdk/types/tasks/v1/taskboards/task_delete_response.py">TaskDeleteResponse</a></code>

# DailyInfo

## V1

Methods:

- <code title="post /daily-info/v1/daily-notes">client.daily_info.v1.<a href="./src/connecteam_api_sdk/resources/daily_info/v1/v1.py">create_daily_note</a>(\*\*<a href="src/connecteam_api_sdk/types/daily_info/v1_create_daily_note_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/daily_info/v1/daily_note_response.py">DailyNoteResponse</a></code>

### DailyNote

Types:

```python
from connecteam_api_sdk.types.daily_info.v1 import DailyNoteResponse, DailyNoteDeleteResponse
```

Methods:

- <code title="get /daily-info/v1/daily-note/{noteId}">client.daily_info.v1.daily_note.<a href="./src/connecteam_api_sdk/resources/daily_info/v1/daily_note.py">retrieve</a>(note_id) -> <a href="./src/connecteam_api_sdk/types/daily_info/v1/daily_note_response.py">DailyNoteResponse</a></code>
- <code title="put /daily-info/v1/daily-note/{noteId}">client.daily_info.v1.daily_note.<a href="./src/connecteam_api_sdk/resources/daily_info/v1/daily_note.py">update</a>(note_id, \*\*<a href="src/connecteam_api_sdk/types/daily_info/v1/daily_note_update_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/daily_info/v1/daily_note_response.py">DailyNoteResponse</a></code>
- <code title="delete /daily-info/v1/daily-note/{noteId}">client.daily_info.v1.daily_note.<a href="./src/connecteam_api_sdk/resources/daily_info/v1/daily_note.py">delete</a>(note_id) -> <a href="./src/connecteam_api_sdk/types/daily_info/v1/daily_note_delete_response.py">DailyNoteDeleteResponse</a></code>

# Chat

## V1

### Conversations

Types:

```python
from connecteam_api_sdk.types.chat.v1 import ConversationPostMessage, ConversationListResponse
```

Methods:

- <code title="get /chat/v1/conversations">client.chat.v1.conversations.<a href="./src/connecteam_api_sdk/resources/chat/v1/conversations.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/chat/v1/conversation_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/chat/v1/conversation_list_response.py">ConversationListResponse</a></code>
- <code title="post /chat/v1/conversations/{conversationId}/message">client.chat.v1.conversations.<a href="./src/connecteam_api_sdk/resources/chat/v1/conversations.py">send_message</a>(conversation_id, \*\*<a href="src/connecteam_api_sdk/types/chat/v1/conversation_send_message_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_base.py">APIResponseBase</a></code>
- <code title="post /chat/v1/conversations/privateMessage/{userId}">client.chat.v1.conversations.<a href="./src/connecteam_api_sdk/resources/chat/v1/conversations.py">send_private_message</a>(user_id, \*\*<a href="src/connecteam_api_sdk/types/chat/v1/conversation_send_private_message_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/users/v1/custom_fields/api_response_base.py">APIResponseBase</a></code>

# Publishers

## V1

Types:

```python
from connecteam_api_sdk.types.publishers import V1ListResponse
```

Methods:

- <code title="get /publishers/v1/publishers">client.publishers.v1.<a href="./src/connecteam_api_sdk/resources/publishers/v1.py">list</a>(\*\*<a href="src/connecteam_api_sdk/types/publishers/v1_list_params.py">params</a>) -> <a href="./src/connecteam_api_sdk/types/publishers/v1_list_response.py">V1ListResponse</a></code>
