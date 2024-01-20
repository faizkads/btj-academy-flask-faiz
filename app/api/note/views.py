import logging
from flask import Blueprint, jsonify, request
from api.base.base_schemas import BaseResponse
from middlewares.authentication import (
    refresh_access_token,
    get_user_id_from_access_token,
)
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from .schemas import (
    CreateNoteRequest, 
    CreateNoteResponse,
    ReadOneNoteResponse,
    ReadAllNoteRequest,
    ReadAllNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
    DeleteNoteResponse
)
from .use_cases import CreateNote, ReadOneNote, UpdateNote, DeleteNote, ReadAllNote

router = Blueprint("notes", __name__, url_prefix='/api/v1/notes')
logger = logging.getLogger(__name__)

@router.route("/", methods=['POST'])
@validate()
def create(body: CreateNoteRequest,) -> CreateNoteResponse:
    try:
        token_user_id = get_user_id_from_access_token(request)
        resp_data = CreateNote().execute(user_id=token_user_id, request=body)

        return jsonify(CreateNoteResponse(
            status="success",
            message="success created note",
            data = resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(CreateNoteResponse(
            status="error",
            message=ex.description,
            data = None
        ).__dict__), ex.code

    except Exception as e:
        message = "failed to create a new note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return jsonify(CreateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["GET"])
@validate()
def read_one(note_id: int):
    try:
        token_user_id = get_user_id_from_access_token(request)
        resp_data = ReadOneNote().execute(user_id=token_user_id, note_id=note_id)

        return jsonify(ReadOneNoteResponse(
            status = "success",
            message = "success read one note",
            data = resp_data.__dict__,
        ).__dict__), 200
        
    except HTTPException as ex:
        return jsonify(ReadOneNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message = "failed to read one note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadOneNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/", methods=["GET"])
@validate()
def read_all(query: ReadAllNoteRequest) -> ReadAllNoteResponse:
    try:
        logger.info("Start processing read all notes request")

        token_user_id = get_user_id_from_access_token(request)
        resp_data = ReadAllNote().execute(
            user_id=token_user_id, 
            page_params=query, 
            include_deleted=query.include_deleted,
            filter_user=query.filter_user
        )

        logger.info("Successfully processed read all notes request")

        return jsonify(ReadAllNoteResponse(
            status="success",
            message="Success read notes",
            data={"records": resp_data[0], "meta": resp_data[1].__dict__},
        ).__dict__), 200

    except HTTPException as ex:
        logger.error(f"HTTPException: {ex}")
        return jsonify(ReadAllNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        logger.exception("Unhandled exception during read all notes request")
        message = "Failed to read notes"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadAllNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["PUT"])
@validate()
def update(note_id: int, body: UpdateNoteRequest) -> UpdateNoteResponse:
    try:
        token_user_id = get_user_id_from_access_token(request)
        resp_data = UpdateNote().execute(user_id=token_user_id, note_id=note_id, request=body)
        return jsonify(UpdateNoteResponse(
            status="success",
            message=f"success update note with id {note_id}",
            data = resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(UpdateNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code
    except Exception as e:
        message="failed to update note"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(UpdateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["DELETE"])
@validate()
def delete(note_id: int):
    try:
        token_user_id = get_user_id_from_access_token(request)
        resp_data = DeleteNote().execute(user_id=token_user_id, note_id=note_id)

        return jsonify(DeleteNoteResponse(
            status = "success",
            message = f"success delete note with id {note_id}",
            data = resp_data.__dict__,
        ).__dict__), 200
        
    except HTTPException as ex:
        return jsonify(DeleteNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message = "failed to delete note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(DeleteNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500