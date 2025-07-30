// alert("This extension is up and running")

const PINNED_RSs = 'PINNED_RSs'

const getObject = (key) => {
    return JSON.parse(localStorage.getItem(key))
}

const setObject = (key, value) => {
    localStorage.setItem(key, JSON.stringify(value))
}


browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.sender === 'ext-popup') {
        const pins = getObject(PINNED_RSs) || {values: []};
        pins.current = document.URL.split('?')[1].split('rs=')[1].split('&')[0];
        if (request.command === 'init') {
            sendResponse(pins);
        } else if (request.command === 'add') {
            const rs = pins.current;
            if (!pins.values.includes(rs)) {
                pins.values.unshift(rs);
                pins[rs] = request.name;
            }
            setObject(PINNED_RSs, pins);
            sendResponse(pins);
        } else if (request.command === 'load') {
            console.log('load event');
            const up = getObject(parseInt(request.rs));
            let url = `#${up.path}?rs=${request.rs}`;
            if (!["", null, undefined].includes(up.mk))
                url += `&mk=${up.mk}`;
            if (!["", null, undefined].includes(up.mt))
                url += `&mt=${up.mt}`
            window.open(url);
        }
    }
})
