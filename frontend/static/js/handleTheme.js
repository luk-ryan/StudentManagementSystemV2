/**
 * Loads the theme into the website.
 *
 * If the `theme` item in local storage is `light` (or is not defined) then we
 * load the light theme. If the `theme` item in local storage is `dark` then we
 * load the dark theme.
 */
function loadTheme() {
    const theme = localStorage.getItem("theme");

    if (theme == null || theme == "light") {
        // Current theme is light, so make sure light theme is loaded
        setThemeToLight();
    } else {
        // Current theme is dark, so make sure dark theme is loaded
        setThemeToDark();
    }
}

/**
 * Toggles between the light and dark theme of the website.
 * Also changes the `theme` item in local storage.
 */
function toggleTheme() {
    const currentTheme = localStorage.getItem("theme");

    if (currentTheme == null || currentTheme == "light") {
        // Current theme is light, so change it to dark
        setThemeToDark();
    } else {
        // Current theme is dark, so change it to light
        setThemeToLight();
    }
}

/**
 * Sets the theme of the website to light theme. Also sets the `theme` item in
 * local storage to `light`.
 */
function setThemeToLight() {
    const root = document.documentElement;
    root.classList.add("light-theme");
    root.classList.remove("dark-theme");

    const toggleImgSrc = "/static/svg/moon-solid.svg";
    document.getElementById("toggleThemeImg").src = toggleImgSrc;

    localStorage.setItem("theme", "light");
}

/**
 * Sets the theme of the website to dark theme. Also sets the `theme` item in
 * local storage to `dark`.
 */
function setThemeToDark() {
    const root = document.documentElement;
    root.classList.add("dark-theme");
    root.classList.remove("light-theme");

    const toggleImgSrc = "/static/svg/sun-solid.svg";
    document.getElementById("toggleThemeImg").src = toggleImgSrc;

    localStorage.setItem("theme", "dark");
}
