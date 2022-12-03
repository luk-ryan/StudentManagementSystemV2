/**
 * Loads the theme into the website.
 *
 * If the `theme` item in local storage is `light` (or is not defined) then we
 * load the light theme.
 * If the `theme` item in local storage is `dark` then we load the dark theme.
 *
 * By loading the theme, we set the background color, text color, and the image
 * of the toggle theme button.
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
 *
 * Using the `theme` item in local storage, we switch between light and dark.
 *
 * By loading the theme, we set the background color, text color, and the image
 * of the toggle theme button.
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
 * Sets the theme of the website to light theme.
 *
 * This sets the background to a light color, text to a dark color, and the
 * image of the toggle theme button to a moon. Also sets the `theme` item in
 * local storage to `light`.
 */
function setThemeToLight() {
    const backgroundColor = getComputedStyle(document.documentElement).getPropertyValue("--light-theme-background-color");
    const textColor = getComputedStyle(document.documentElement).getPropertyValue("--light-theme-text-color");
    const toggleImgSrc = "/static/svg/moon-solid.svg";

    document.documentElement.style.setProperty("--background-color", backgroundColor);
    document.documentElement.style.setProperty("--text-color", textColor);
    document.getElementById("toggleThemeImg").src = toggleImgSrc;

    localStorage.setItem("theme", "light");
}

/**
 * Sets the theme of the website to dark theme.
 *
 * This sets the background to a dark color, text to a light color, and the
 * image of the toggle theme button to a sun. Also sets the `theme` item in
 * local storage to `dark`.
 */
function setThemeToDark() {
    const backgroundColor = getComputedStyle(document.documentElement).getPropertyValue("--dark-theme-background-color");
    const textColor = getComputedStyle(document.documentElement).getPropertyValue("--dark-theme-text-color");
    const toggleImgSrc = "/static/svg/sun-solid.svg";

    document.documentElement.style.setProperty("--background-color", backgroundColor);
    document.documentElement.style.setProperty("--text-color", textColor);
    document.getElementById("toggleThemeImg").src = toggleImgSrc;

    localStorage.setItem("theme", "dark");
}
