from pydantic import BaseModel, Field
from api.base.base_schemas import BaseResponse,PaginationParams

from models.note import NoteSchema

class CreateNoteRequest(BaseModel):
    title: str = Field(...,min_length=1, max_length=255)
    content: str = Field(...,min_length=6, max_length=500)

class CreateNoteResponse(BaseResponse):
    data: dict | None

class ReadOneNoteResponse(BaseResponse):
    data: dict | None

class ReadAllNoteRequest(PaginationParams):
    include_deleted: bool = False
    filter_user: bool = True

class ReadAllNoteResponse(BaseResponse):
    data: dict | None

class UpdateNoteRequest(BaseModel):
    title: str = Field(...,min_length=1, max_length=255)
    content: str = Field(...,min_length=6, max_length=500)

class UpdateNoteResponse(BaseResponse):
    data: dict | None

class DeleteNoteResponse(BaseResponse):
    data: dict | None