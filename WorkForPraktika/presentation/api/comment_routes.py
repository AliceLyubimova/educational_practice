from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.use_cases.comment_case import (
    AddCommentUseCase,
    GetCommentsUseCase,
    SelfCommentError,
)
from application.use_cases.user_case import UserNotFoundError
from presentation.api.dependencies import (
    get_add_comment_use_case,
    get_comments_use_case,
)


class AddCommentRequest(BaseModel):
    user_id: int           # кто оставляет
    target_user_id: int    # о ком
    text: str


router = APIRouter(prefix="/api/comments", tags=["Комментарии"])


@router.post("")
def add_comment(
    req: AddCommentRequest,
    use_case: AddCommentUseCase = Depends(get_add_comment_use_case),
):
    try:
        return use_case.execute(req.user_id, req.target_user_id, req.text)
    except SelfCommentError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{target_user_id}")
def get_comments(
    target_user_id: int,
    use_case: GetCommentsUseCase = Depends(get_comments_use_case),
):
    return {"comments": use_case.execute(target_user_id)}
