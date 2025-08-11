document.addEventListener("DOMContentLoaded", function () {
    const themeOptions = document.querySelectorAll(".dropdown-item[data-theme]");
    const themeIcon = document.getElementById("themeIcon");
    const registerContainer = document.getElementById("register");

    let savedTheme = localStorage.getItem("theme") || "auto";
    applyTheme(savedTheme);

    themeOptions.forEach(option => {
        option.addEventListener("click", function (event) {
            event.preventDefault();  // 👈 Solo cancelamos si es botón de tema
            const selectedTheme = this.getAttribute("data-theme");
            localStorage.setItem("theme", selectedTheme);
            applyTheme(selectedTheme);
        });
    });

    function applyTheme(theme) {
        if (theme === "auto") {
            theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }

        document.documentElement.setAttribute("data-bs-theme", theme);
        document.documentElement.classList.toggle("dark-mode", theme === "dark");

        if (registerContainer) {
            registerContainer.classList.toggle("bg-dark", theme === "dark");
            registerContainer.classList.toggle("bg-light", theme !== "dark");
        }

        if (themeIcon) {
            themeIcon.innerHTML = theme === "dark"
                ? '<i class="bi bi-brightness-high"></i>'
                : '<i class="bi bi-moon"></i>';
        }
    }
});