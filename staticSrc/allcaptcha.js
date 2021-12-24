(function () {

    const form = document.querySelector("form");

    function appendToForm(name, token) {
        const responseInput = document.createElement("input");
        responseInput.setAttribute("type", "hidden");
        responseInput.setAttribute("name", name);
        responseInput.setAttribute("value", token);
        form.appendChild(responseInput);
    }

    function onHcaptchaSubmit(token) {
        appendToForm("h-captcha-response", token);
        form.submit();
    }

    function onRecaptchaSubmit(token) {
        appendToForm("g-recaptcha-response", token);
        form.submit();
    }

    window.addEventListener("DOMContentLoaded", function () {
        window.onHcaptchaSubmit = onHcaptchaSubmit;
        window.onRecaptchaSubmit = onRecaptchaSubmit;
    });
})();
