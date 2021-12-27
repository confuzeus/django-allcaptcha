from unittest.mock import patch

from django.test import TestCase

from .utils import ACaptchaedForm


class TestAllcaptchaMixins(TestCase):
    def test_hcaptcha_form_mixin(self):

        with patch("allcaptcha.mixins.valid_response") as mock:

            mock.return_value = False

            form = ACaptchaedForm({"h-captcha-response": ""})

            self.assertFalse(form.is_valid())

            mock.return_value = True

            form = ACaptchaedForm({"h-captcha-response": ""})

            self.assertTrue(form.is_valid())
