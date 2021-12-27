from unittest.mock import patch
from allcaptcha import settings
from django.test import TestCase

from allcaptcha.templatetags import allcaptcha_tags


class TestAllcaptchaTemplateTags(TestCase):
    def test_templatetags(self):

        with patch("allcaptcha.templatetags.allcaptcha_tags.settings") as mock_settings:
            # Test with Hcaptcha
            mock_settings.HCAPTCHA_PROVIDER_NAME = "abcd"
            mock_settings.PROVIDER = "abcd"
            mock_settings.CAPTCHA_SECRET_KEY = "cyx"
            mock_settings.CAPTCHA_SITE_KEY = "kjsjd"
            mock_settings.PROVIDER_CLASS_NAME = "h-captcha"
            mock_settings.PROVIDER_JS_CALLBACK = "onHcaptchaSubmit"

            sitekey = allcaptcha_tags.get_sitekey()

            self.assertEqual(sitekey, "kjsjd")

            klass = allcaptcha_tags.get_challenge_class()

            self.assertEqual(klass, "h-captcha")

            cb_name = allcaptcha_tags.get_callback_name()

            self.assertEqual(cb_name, "onHcaptchaSubmit")

            challenge_ctx = allcaptcha_tags.render_challenge()

            self.assertEqual(challenge_ctx["challenge_type"], "visible")
            self.assertEqual(challenge_ctx["callback"], "onHcaptchaSubmit")
            self.assertEqual(challenge_ctx["text"], "submit")
            self.assertEqual(challenge_ctx["class_name"], "h-captcha")
            self.assertEqual(challenge_ctx["sitekey"], "kjsjd")

            mock_settings.RECAPTCHA_PROVIDER_NAME = "xyz"
            mock_settings.PROVIDER = "xyz"

            challenge_ctx = allcaptcha_tags.render_challenge()

            self.assertEqual(challenge_ctx["challenge_type"], "visible")
            self.assertEqual(challenge_ctx["callback"], "onHcaptchaSubmit")
            self.assertEqual(challenge_ctx["text"], "submit")
            self.assertEqual(challenge_ctx["class_name"], "h-captcha")
            self.assertEqual(challenge_ctx["sitekey"], "kjsjd")

            mock_settings.RECAPTCHA_VERSION = 3

            with self.assertRaises(ValueError):
                allcaptcha_tags.render_challenge()
