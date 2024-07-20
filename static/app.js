class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),  // Przycisk otwierający chatbox
            chatBox: document.querySelector('.chatbox__support'),  // Kontener chatbox
            sendButton: document.querySelector('.send__button')  // Przycisk wysyłania wiadomości
        }

        this.state = false;  // Stan chatbox (otwarty/zamknięty)
        this.message = [];  // Lista wiadomości
        this.inactivityTime = 5 * 60 * 1000;  // Czas bezczynności (5 min)
        this.inactivityTimer = null;  // Timer bezczynności

    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', (key) => {
            if (key.key === 'Enter') {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        clearTimeout(this.inactivityTimer);
        this.inactivityTimer = setTimeout(() => this.onLogButton(), this.inactivityTime);

        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === '') {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.message.push(msg1)

        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(response => {
                let msg2 = { name: "Sam", message: response.answer }
                this.message.push(msg2)
                this.updateChatText(chatbox)
                textField.value = ''
            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
    }

    onLogButton() {
        fetch($SCRIPT_ROOT + '/log', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(response => {
                console.log(response.status)
            }).catch((error) => {
                console.error('Error:', error);
            });
    }

    updateChatText(chatbox) {
        var html = '';
        this.message.slice().reverse().forEach(function (item, index) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display()
