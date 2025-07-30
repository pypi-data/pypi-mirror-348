function loadRS(rs) {
    browser.tabs.query({active: true, currentWindow: true}).then(tabs => {
        browser.tabs.sendMessage(tabs[0].id, {command: 'load', rs: rs, sender: 'ext-popup'}), (response) => {
            console.log(response);
        }
    });
}

function addRS(name) {
    browser.tabs.query({active: true, currentWindow: true}).then(tabs => {
        browser.tabs.sendMessage(tabs[0].id, {command: 'add', name: name, sender: 'ext-popup'}), (response) => {
            init(response);
        }
    });
}

function init(response) {
    const cntnt = document.getElementById('popup-content');
    if (!response.values.includes(response.current)) {
        const input = document.createElement('input');
        input.onkeydown = (e) => {
            if (e.code === 'Enter' && !['', null, undefined].includes(input.value)) {
                const name = input.value;
                while (cntnt.firstChild) {
                    cntnt.removeChild(cntnt.lastChild);
                }
                addRS(name);
            }
        }
        cntnt.appendChild(input);
    }
    response.values.forEach((rs, i) => {
        const button = document.createElement('button');
        button.innerText = response[rs];
        button.onclick = () => loadRS(rs);
        cntnt.appendChild(button);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    browser.tabs.query({active: true, currentWindow: true}).then(tabs => {
        browser.tabs.sendMessage(tabs[0].id, {command: "init", sender: 'ext-popup'}, (response) => {
            init(response);
        });
    });
})
