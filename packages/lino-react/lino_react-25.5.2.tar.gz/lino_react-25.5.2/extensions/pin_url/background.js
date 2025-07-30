const openTab = () => {
    var newTab = browser.tabs.create({
        url: "https://google.com",
        active: true
    });
}

browser.browserAction.onClicked.addListener(openTab);
