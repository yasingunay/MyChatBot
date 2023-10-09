



document.addEventListener("DOMContentLoaded", function() {
    const messagesList = document.querySelector(".messages-list");
    const messageForm = document.querySelector(".message-form");
    const messageInput = document.querySelector(".message-input");


    messageForm.addEventListener('submit', (event) => {
        // prevent the default form behavior
        event.preventDefault();

        // delete whitespace from the message
        const message = messageInput.value.trim();
        if (message.length === 0){
            return;
        }

        const messageItem = document.createElement("li");
        messageItem.classList.add('message', 'sent');
        messageItem.innerHTML = `
        <div class="message-text">
            <div class="message-sender">
              <b>You</b>
            </div>
            <div class="message-content">
              ${message}
            </div>
          </div>`;
        messagesList.appendChild(messageItem);

        messageInput.value ="";

        // send the message to the server
        fetch("",{
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: new URLSearchParams({
                "csrfmiddlewaretoken": document.querySelector('[name="csrfmiddlewaretoken"]').value,
                "message": message
            })
        })
        .then(response => response.json())
        .then(data =>{
            const response = data.response;
            console.log(data);
            const messageItem = document.createElement("li");
            messageItem.classList.add('message', 'received');
            messageItem.innerHTML = `
            <div class="message-text">
            <div class="message-sender">
                <b>AI Chatbot</b>
                </div>
                <div class="message-content">
                ${response}
             </div>
            </div>`;
        messagesList.appendChild(messageItem);
        })
    })
});



