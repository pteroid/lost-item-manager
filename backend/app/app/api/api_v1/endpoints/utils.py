import uuid

import boto3
from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app.api.utils.security import get_current_active_admin
from app.core import config
from app.core.celery_app import celery_app
from app.models.admin import Admin as DBUser
from app.schemas.msg import Msg
from app.utils import send_test_email

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id=config.STORAGE_ACCESS_KEY,
    aws_secret_access_key=config.STORAGE_SECRET_KEY,
)

router = APIRouter()


@router.post("/test-celery/", response_model=Msg, status_code=201)
def test_celery(msg: Msg, current_user: DBUser = Depends(get_current_active_admin)):
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr, current_user: DBUser = Depends(get_current_active_admin)
):
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.post("/geturl/", response_model=Msg, status_code=201)
def get_presigned_url(
    file_type: str, current_user: DBUser = Depends(get_current_active_admin),
):
    if file_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=403,
            detail=f"{file_type} is not allowed. Allowed content type is image/jpeg and image/png.",
        )

    ext = file_type.split("/").pop()
    key = str(uuid.uuid4()) + "." + ext

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": config.STORAGE_BUCKET_NAME,
            "Key": key,
            "ContentType": file_type,
        },
        ExpiresIn=3600,
        HttpMethod="PUT",
    )

    return {"msg": url}
