from typing import Literal

from pydantic import BaseModel, EmailStr


class SendEmailPayload(BaseModel):
    """Data required to send an email.

    Attributes
    ----------
    to : EmailStr
        The recipient's email address.
    subject : str
        The subject line of the email.
    body : str
        The plain text or HTML content of the email.

    """

    to: EmailStr
    subject: str
    body: str


class SendEmailTask(BaseModel):
    """Task model for sending an email.

    Attributes
    ----------
    type : Literal["send_email"]
        The type of task, fixed as "send_email".
    payload : SendEmailPayload
        The payload containing email-specific data.

    """

    type: Literal["send_email"]
    payload: SendEmailPayload


EnqueueTaskRequest = SendEmailTask
