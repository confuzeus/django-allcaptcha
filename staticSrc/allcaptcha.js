var allcaptcha = (function(o) {
    o.main = {
        onHcaptchaSubmit: function onHcaptchaSubmit(token) {
            const form = document.querySelector("form");
            const responseInput = document.createElement("input");
            responseInput.setAttribute("type", "hidden");
            responseInput.setAttribute("name", "h-captcha-response");
            responseInput.setAttribute("value", token)
            form.appendChild(responseInput);
            form.submit();
        },
        init: function initAllCaptcha() {
            window.onHcaptchaSubmit = this.onHcaptchaSubmit;
        }
    }

    window.addEventListener("DOMContentLoaded", function () {
        o.main.init();
    });
    return o;
})(allcaptcha || {});
