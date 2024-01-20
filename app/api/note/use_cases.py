import datetime
import math

from sqlalchemy import func, select
from werkzeug.exceptions import HTTPException

from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.note import Note, NoteSchema
from .schemas import CreateNoteRequest, UpdateNoteRequest

class CreateNote:
    def __init__(self) -> None:
        self.session = get_session()
    
    def execute(self, user_id, request: CreateNoteRequest) -> NoteSchema:
        with self.session as session:
            # Check if the title is already used by another note
            existing_note = session.execute(
                select(Note).where(
                    (Note.created_by == user_id) & (Note.title == request.title)
                )
            ).scalars().first()

            if existing_note:
                exception = HTTPException(description=f"Title '{request.title}' is already used by another note.")
                exception.code = 400
                raise exception

            # Create a new note
            note = Note()
            note.title=request.title
            note.content=request.content
            note.created_at=datetime.datetime.utcnow()
            note.updated_at=datetime.datetime.utcnow()
            note.created_by=user_id
            note.updated_by=user_id

            session.add(note)
            session.flush()

            return NoteSchema.from_orm(note)

class ReadOneNote:
    def __init__(self) -> None:
        self.session = get_session()
    def execute(self, user_id: int, note_id: int) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.created_by == user_id) & (Note.note_id == note_id) & (Note.deleted_at == None)
                )
            ).scalars().first()
            if not note:
                exception = HTTPException(description="notes not found")
                exception.code = 404
                raise exception
            return NoteSchema.from_orm(note)

class ReadAllNote:
    def __init__(self) -> None:
        self.session = get_session()
    def execute(
        self, 
        user_id: int, 
        page_params: PaginationParams,
        include_deleted: bool,
        filter_user: bool
    ) -> (list[dict], PaginationMetaResponse):
        with self.session as session:
            total_item = (
                select(func.count())
                .select_from(Note)
            )

            query = (
                select(Note)
                .offset((page_params.page-1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )

            if filter_user:
                total_item = total_item.filter(Note.created_by == user_id)
                query = query.filter(Note.created_by == user_id)

            if not include_deleted:
                total_item = total_item.filter(Note.deleted_at == None)
                query = query.filter(Note.deleted_at == None)

            total_item = session.execute(total_item).scalar()
            paginated_query = session.execute(query).scalars().all()

            notes = [NoteSchema.from_orm(p).__dict__ for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page)
            )

            return notes, meta

class UpdateNote:
    def __init__(self) -> None:
        self.session = get_session()
    def execute(self, user_id: int, note_id: int, request: UpdateNoteRequest) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                (Note.created_by == user_id) & (Note.note_id == note_id) & (Note.deleted_at == None)
                )
            ).scalars().first()
            if not note:
                exception = HTTPException(description="notes not found")
                exception.code = 404
                raise exception

            title_modified = note.title != request.title
            if title_modified:
                n = session.execute(
                    select(Note).where(
                        (Note.created_by == user_id) & (Note.title == request.title)
                    )
                ).scalars().first()
                if n:
                    exception = HTTPException(description=f"Title '{request.title}' is already used by another note.")
                    exception.code = 404
                    raise exception
                
            note.title = request.title
            note.content = request.content
            note.updated_at = datetime.datetime.utcnow()
            note.updated_by = user_id
            
            session.flush()
            return NoteSchema.from_orm(note)

class DeleteNote:
    def __init__(self) -> None:
        self.session = get_session()
    def execute(self, user_id: int, note_id: int) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(
                    (Note.created_by == user_id) & (Note.note_id == note_id) & (Note.deleted_at == None)
                )
            ).scalars().first()
            if not note:
                exception = HTTPException(description="notes not found")
                exception.code = 404
                raise exception

            note.deleted_at = datetime.datetime.utcnow()
            note.deleted_by = user_id

            session.flush()
            return NoteSchema.from_orm(note)
        