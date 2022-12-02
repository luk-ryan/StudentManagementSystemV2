function toggleTheme() {
    const backgroundColor = getComputedStyle(document.documentElement).getPropertyValue("--background-color");
    const textColor = getComputedStyle(document.documentElement).getPropertyValue("--text-color");

    document.documentElement.style.setProperty("--background-color", textColor);
    document.documentElement.style.setProperty("--text-color", backgroundColor);
}
