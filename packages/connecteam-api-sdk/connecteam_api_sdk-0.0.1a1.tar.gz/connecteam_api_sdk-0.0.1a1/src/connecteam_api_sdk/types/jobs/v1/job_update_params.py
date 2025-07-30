# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ...._utils import PropertyInfo
from .assign_data_in_param import AssignDataInParam
from ...time_clock.v1.gps_data_param import GpsDataParam

__all__ = ["JobUpdateParams", "SubJobUpdateRequest", "JobUpdateRequest"]


class SubJobUpdateRequest(TypedDict, total=False):
    parent_id: Required[Annotated[str, PropertyInfo(alias="parentId")]]
    """The ID of the parent job, if any"""

    title: Required[str]
    """The title of the job"""

    use_parent_data: Required[Annotated[bool, PropertyInfo(alias="useParentData")]]
    """Indicates whether to use the parent job's data or not"""

    assign: AssignDataInParam
    """Data related to job assignment"""

    code: str
    """The code of the job"""

    description: str
    """The description of the job"""

    gps: GpsDataParam
    """The GPS data of the job"""


class JobUpdateRequest(TypedDict, total=False):
    title: Required[str]
    """The title of the job"""

    assign: AssignDataInParam
    """Settings related to job assignment"""

    code: str
    """The code of the job"""

    color: str
    """The color associated with the job.

    Should be one of the following colors: ['#4B7AC5', '#801A1A', '#AE2121',
    '#DC7A7A', '#B0712E', '#D4985A', '#E4B37F', '#AE8E2D', '#CBA73A', '#D9B443',
    '#487037', '#6F9B5C', '#91B282', '#365C64', '#5687B3', '#7C9BA2', '#3968BB',
    '#85A6DA', '#225A8C', '#548CBE', '#81A8CC', '#4E3F75', '#604E8E', '#8679AA',
    '#983D73', '#A43778', '#D178AD', '#6B2E4C', '#925071', '#B57D9A', '#3a3a3a',
    '#616161', '#969696']
    """

    description: str
    """The description of the job"""

    gps: GpsDataParam
    """The GPS data of the job"""

    instance_ids: Annotated[Iterable[int], PropertyInfo(alias="instanceIds")]
    """List of instance ids (scheduler id or time clock id) to assign the job to"""


JobUpdateParams: TypeAlias = Union[SubJobUpdateRequest, JobUpdateRequest]
