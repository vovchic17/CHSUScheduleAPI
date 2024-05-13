// workaround to remove `auto` theme
if (window.matchMedia("(prefers-color-scheme: dark)").matches)
    document.body.dataset.theme = "dark";

function setTheme(mode) {
    document.body.dataset.theme = mode;
    localStorage.setItem("theme", mode);
}

function switchTheme() {
    let theme = localStorage.getItem("theme") || "auto";
    if (theme === "auto") {
        theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    if (theme === "dark") {
        setTheme("light");
    } else {
        setTheme("dark");
    }
}

document.querySelectorAll(".theme-toggle").forEach(
    async button => {
        setTimeout(() => button.outerHTML = button.outerHTML, 1);
    }
);

(async () => {
    await new Promise(resolve => setTimeout(resolve, 1));
    document.querySelectorAll(".theme-toggle").forEach(
        button => {
            button.addEventListener("click", switchTheme);
        }
    )
})()
