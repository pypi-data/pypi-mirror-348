from typing import Optional

from pydantic import BaseModel

from fa_common.models import StorageLocation

from .enums import EmailBodyType


class ExtraContent(BaseModel):
    type: EmailBodyType = EmailBodyType.PLAIN
    body: str = ""


class CallbackMetaData(BaseModel):
    """
    storage_location: should contain the base path to
                      where the workflows are stored
    ui_res_link:      USE THIS IF YOU WISH TO EMBED a
                      LINK to THE RESULTS IN UI.
    """

    storage_location: StorageLocation | None = None
    project_id: Optional[str] = None
    project_name: Optional[str] = ""
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    ui_res_link: Optional[str] = None
    extra_content: Optional[ExtraContent] = None
    show_detailed_info: Optional[bool] = True
