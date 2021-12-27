import secrets
from unittest.mock import patch, MagicMock

from django.test import TestCase

from allcaptcha import settings
from allcaptcha import utils

from .utils import ACaptchaedForm


class TestAllCaptchaUtils(TestCase):
    def test_get_captcha_response(self):
        with patch("allcaptcha.utils.settings") as mock_settings:

            mock_settings.CAPTCHA_SECRET_KEY = "abcd"
            mock_settings.CAPTCHA_SITE_KEY = "xyz"

            mock_settings.HCAPTCHA_PROVIDER_NAME = "hcaptcha"
            mock_settings.PROVIDER = "hcaptcha"

            form = ACaptchaedForm({"h-captcha-response": "abcd"})
            captcha_response = utils.get_captcha_response(form)
            self.assertEqual(captcha_response, "abcd")

            form = ACaptchaedForm({})
            captcha_response = utils.get_captcha_response(form)
            self.assertEqual(len(captcha_response), 0)

            mock_settings.RECAPTCHA_PROVIDER_NAME = "recaptcha"
            mock_settings.PROVIDER = "recaptcha"

            form = ACaptchaedForm({"g-recaptcha-response": "abcd"})
            captcha_response = utils.get_captcha_response(form)
            self.assertEqual(captcha_response, "abcd")

    def test_build_submission_data(self):

        with patch("allcaptcha.utils.settings") as mock_settings:

            mock_settings.CAPTCHA_SECRET_KEY = "abcd"
            mock_settings.CAPTCHA_SITE_KEY = "xyz"

            # Test with HCaptcha
            mock_settings.HCAPTCHA_PROVIDER_NAME = "hcaptcha"
            mock_settings.PROVIDER = "hcaptcha"

            data = utils._build_submission_data("abcd")

            self.assertEqual(data["secret"], "abcd")
            self.assertEqual(data["sitekey"], "xyz")
            self.assertEqual(data["response"], "abcd")

            # Test with Recaptcha
            mock_settings.RECAPTCHA_PROVIDER_NAME = "recaptcha"
            mock_settings.PROVIDER = "recaptcha"

            data = utils._build_submission_data("abcd")

            self.assertEqual(data["secret"], "abcd")
            self.assertEqual(data["response"], "abcd")

            # Test with non-existent provider

            mock_settings.PROVIDER = secrets.token_hex(4)
            data = utils._build_submission_data("abcd")

            self.assertEqual(len(data.keys()), 0)

    def test_determine_success(self):

        response = None

        success = utils._determine_success(response)

        self.assertFalse(success)

        response = MagicMock()
        response.status_code = 400

        success = utils._determine_success(response)

        self.assertFalse(success)

        with patch("allcaptcha.utils.settings") as mock_settings:

            # Test with Hcaptcha
            mock_settings.PROVIDER = "abcd"
            mock_settings.HCAPTCHA_PROVIDER_NAME = "abcd"

            response.status_code = 200

            response.json.return_value = {"success": True}

            success = utils._determine_success(response)

            self.assertTrue(success)

            response.json.return_value = {"success": False}

            success = utils._determine_success(response)

            self.assertFalse(success)

            response.json.return_value = {"success": True}

            response.json.side_effect = Exception

            self.assertFalse(success)

            response.json.side_effect = None

            # Test with Recaptcha

            mock_settings.PROVIDER = "xyz"
            mock_settings.RECAPTCHA_PROVIDER_NAME = "xyz"

            response.json.return_value = {"success": True}

            mock_settings.RECAPTCHA_VERSION = 2

            success = utils._determine_success(response)

            self.assertTrue(success)

            response.json.return_value = {"success": False}

            success = utils._determine_success(response)

            self.assertFalse(success)

            mock_settings.RECAPTCHA_VERSION = 3
            mock_settings.RECAPTCHA_MIN_SCORE = 0.6

            response.json.return_value = {"success": True, "score": 0.7}

            success = utils._determine_success(response)

            self.assertTrue(success)

            response.json.return_value = {"success": False, "score": 0.7}

            success = utils._determine_success(response)

            self.assertFalse(success)

            response.json.return_value = {"success": True, "score": 0.5}

            success = utils._determine_success(response)

            self.assertFalse(success)

            # Test with non-existant provider

            response.json.return_value = {"success": True, "score": 0.8}

            mock_settings.PROVIDER = secrets.token_hex(4)

            success = utils._determine_success(response)

            self.assertFalse(success)

    def test_get_provider_response(self):

        with patch("allcaptcha.utils.settings") as mock_settings:
            with patch("allcaptcha.utils.requests") as mock_requests:

                mock_settings.PROVIDER = "abcd"
                mock_settings.HCAPTCHA_PROVIDER_NAME = "abcd"

                mock_requests.post.return_value = MagicMock()

                self.assertIsInstance(utils._get_provider_response({}), MagicMock)

                mock_settings.PROVIDER = "xyz"
                mock_settings.RECAPTCHA_PROVIDER_NAME = "xyz"

                self.assertIsInstance(utils._get_provider_response({}), MagicMock)

                mock_requests.post.side_effect = Exception

                self.assertIsNone(utils._get_provider_response({}))

    def test_valid_response(self):

        with patch("allcaptcha.utils.settings") as mock_settings:
            with patch("allcaptcha.utils.requests") as mock_requests:

                mock_settings.CAPTCHA_SECRET_KEY = "asdf"
                mock_settings.CAPTCHA_SITE_KEY = "dvorak"

                mock_settings.PROVIDER = "abcd"
                mock_settings.HCAPTCHA_PROVIDER_NAME = "abcd"

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
