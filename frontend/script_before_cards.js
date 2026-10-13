let doctynSessionId = localStorage.getItem("doctyn_session_id") || null;
let currentPageContext = null;

function openGrok(event) {
    if (event) {
        event.preventDefault();
    }

    document.getElementById("homePage").classList.add("hidden");
    document.getElementById("grokPage").classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function closeGrok() {
    document.getElementById("grokPage").classList.add("hidden");
    document.getElementById("homePage").classList.remove("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function openGrokWithTopic(topic) {
    openGrok();

    document.getElementById("chatInput").value =
        `Tell me about ${topic}`;
}

function askSuggestion(message) {
    document.getElementById("chatInput").value = message;
    sendChat();
}

async function sendChat() {
    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if (!message) {
        return;
    }

    const messages = document.getElementById("chatMessages");

    const userBlock = document.createElement("div");
    userBlock.className = "user-message";

    userBlock.innerHTML = `
        <p>${escapeHtml(message)}</p>
    `;

    messages.appendChild(userBlock);

    input.value = "";

    const botBlock = document.createElement("div");
    botBlock.className = "bot-message";

    botBlock.innerHTML = `
        <div class="message-avatar">✦</div>

        <div class="message-content">
            <strong>Doctyn AI</strong>
            <p>Thinking...</p>
        </div>
    `;

    messages.appendChild(botBlock);

    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    session_id: doctynSessionId,
                    page_context: currentPageContext
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Backend returned ${response.status}`);
        }

        const data = await response.json();

        if (data.response.session_id) {
            doctynSessionId = data.response.session_id;

            localStorage.setItem(
                "doctyn_session_id",
                doctynSessionId
            );
        }

        botBlock
            .querySelector("p")
            .innerText = data.response.answer;

    } catch (error) {
        botBlock
            .querySelector("p")
            .innerText =
                "I could not connect to the Doctyn AI service. Please make sure the backend is running.";

        console.error(error);
    }

    messages.scrollTop = messages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}
