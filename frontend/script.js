
let conversationId = null;

async function sendMessage() {

    const input = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");
    const button = document.getElementById("send-btn");

    const message = input.value.trim();

    if (!message || button.disabled) return;

    // Display user message
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.textContent = "You: " + message;

    chatBox.appendChild(userDiv);

    input.value = "";
    button.disabled = true;

    const loading = document.createElement("div");
    loading.className = "bot-message";
    loading.textContent = "Thinking...";

    chatBox.appendChild(loading);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    message: message
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        conversationId = data.conversation_id;

        loading.textContent = "Bot: " + data.response;

    } catch (error) {

        loading.textContent = "Error: " + error.message;

    } finally {

        button.disabled = false;
        chatBox.scrollTop = chatBox.scrollHeight;
        input.focus();
    }
}

document.getElementById("message").addEventListener(
    "keydown",
    function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
);
