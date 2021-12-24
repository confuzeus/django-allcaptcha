from typing import Optional

import requests
import logging

from django.forms import BaseForm
from requests import Response

from . import settings

log = logging.getLogger(__name__)


def get_captcha_response(form: BaseForm) -> str:
    captcha_response = ""
    if settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME:
        captcha_response = form.data.get("h-captcha-response", "")
    elif settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME:
        captcha_response = form.data.get("g-recaptcha-response", "")
    return captcha_response


def _build_submission_data(response: str) -> dict:
    data = {}
    if settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME:
        data.update(
            {
                "secret": settings.CAPTCHA_SECRET_KEY,
                "sitekey": settings.CAPTCHA_SITE_KEY,
                "response": response,
            }
        )
    elif settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME:
        data.update(
            {
                "secret": settings.CAPTCHA_SECRET_KEY,
                "response": response,
            }
        )

    return data


def _determine_success(provider_response: Optional[Response]) -> bool:
    success = False
    if provider_response and getattr(provider_response, "status_code", None) == 200:
        if settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME:
            try:
                success = provider_response.json()["success"]
            except Exception as e:
                log.exception(e)
        elif settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME:
            try:
                json = provider_response.json()
                recaptcha_success = json["success"]
                if recaptcha_success:
                    if settings.RECAPTCHA_VERSION == 3:

                        score = json["score"]

                        if score >= settings.RECAPTCHA_MIN_SCORE:
                            success = True
                    else:
                        success = True
            except Exception as e:
                log.exception(e)
    return success


def _get_provider_response(data: dict) -> Optional[Response]:
    provider_response = None
    if (
        settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME
        or settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME
    ):
        try:
            provider_response = requests.post(settings.PROVIDER_URL, data=data)
        except Exception as e:
            log.exception(e)
    return provider_response


def valid_response(response: str) -> bool:
    success = False

    if len(response) > 0:
        data = _build_submission_data(response)

        provider_response = _get_provider_response(data)

        success = _determine_success(provider_response)

    return success
