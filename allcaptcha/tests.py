import secrets
from unittest.mock import patch, MagicMock
from django import forms
from django.test import TestCase

from allcaptcha.mixins import CaptchaFormMixin
from . import settings
from . import utils


class AForm(forms.Form):
    pass


class ACaptchaedForm(CaptchaFormMixin, AForm):
    pass


class AllCaptchaTests(TestCase):
    def test_get_captcha_response(self):

        form = ACaptchaedForm({"h-captcha-response": "abcd"})
        captcha_response = utils.get_captcha_response(form)
        self.assertEqual(captcha_response, "abcd")

        form = ACaptchaedForm({})
        captcha_response = utils.get_captcha_response(form)
        self.assertEqual(len(captcha_response), 0)

    def test_build_submission_data(self):

        with patch("allcaptcha.utils.settings") as mock_settings:

            # Test with HCaptcha
            mock_settings.HCAPTCHA_PROVIDER_NAME = settings.HCAPTCHA_PROVIDER_NAME
            mock_settings.PROVIDER = settings.HCAPTCHA_PROVIDER_NAME
            mock_settings.CAPTCHA_SECRET_KEY = settings.HCAPTCHA_SECRET_KEY
            mock_settings.CAPTCHA_SITE_KEY = settings.HCAPTCHA_SITE_KEY
            data = utils._build_submission_data("abcd")

            self.assertEqual(data["secret"], settings.HCAPTCHA_SECRET_KEY)
            self.assertEqual(data["sitekey"], settings.HCAPTCHA_SITE_KEY)
            self.assertEqual(data["response"], "abcd")

            # Test with non-existent provider

            mock_settings.HCAPTCHA_PROVIDER_NAME = secrets.token_hex(4)
            data = utils._build_submission_data("abcd")

            self.assertEqual(len(data.keys()), 0)

    def test_determine_success(self):

        response = None

        success = utils._determine_success(response)

        self.assertFalse(success)

        response = MagicMock()

        response.json.return_value = {"success": True}

        response.status_code = 200

        success = utils._determine_success(response)

        self.assertTrue(success)

        response.json.return_value = {"success": False}

        success = utils._determine_success(response)

        self.assertFalse(success)

        response.json.return_value = {"success": True}

        response.status_code = 400

        self.assertFalse(success)

        response.status_code = 200

        response.json.side_effect = Exception

        self.assertFalse(success)

    def test_get_provider_response(self):

        with patch("allcaptcha.utils.requests") as mock_requests:

            mock_requests.post.return_value = MagicMock()

            self.assertIsInstance(utils._get_provider_response({}), MagicMock)

            mock_requests.post.side_effect = Exception

            self.assertIsNone(utils._get_provider_response({}))

    def test_valid_response(self):

        with patch("allcaptcha.utils.requests") as mock_requests:
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = {"success": True}
            mock_requests.post.return_value = response

            self.assertTrue(utils.valid_response("abcd"))

            self.assertFalse(utils.valid_response(""))

            response = MagicMock()
            response.status_code = 400
            response.json.return_value = {"success": True}
            mock_requests.post.return_value = response

            self.assertFalse(utils.valid_response("abcd"))

            response = MagicMock()
            response.status_code = 200
            response.json.return_value = {"success": False}
            mock_requests.post.return_value = response

            self.assertFalse(utils.valid_response("abcd"))

            response = MagicMock()
            response.status_code = 400
            response.json.return_value = {"success": False}
            mock_requests.post.return_value = response

            self.assertFalse(utils.valid_response("abcd"))

    def test_hcaptcha_form_mixin(self):

        with patch("allcaptcha.mixins.valid_response") as mock:

            mock.return_value = False

            form = ACaptchaedForm({"h-captcha-response": ""})

            self.assertFalse(form.is_valid())

            mock.return_value = True

            form = ACaptchaedForm({"h-captcha-response": ""})

            self.assertTrue(form.is_valid())
