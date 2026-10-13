
const LANDING_PAGES = {
    FCCM: "http://127.0.0.1:5500/../landing-pages/fccm/",
    AFCCM: "http://127.0.0.1:5500/../landing-pages/afccm/",
    FIM: "http://127.0.0.1:5500/../landing-pages/fim/",
    FDM: "http://127.0.0.1:5500/../landing-pages/fdm/",
    FEM: "http://127.0.0.1:5500/../landing-pages/fem/",
    AFEM: "http://127.0.0.1:5500/../landing-pages/afem/",
    FFM: "http://127.0.0.1:5500/../landing-pages/ffm/",
    FGO: "http://127.0.0.1:5500/../landing-pages/fgo/"
};

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

    currentPageContext = detectPageContext(topic);

    document.getElementById("chatInput").value =
        `Tell me about ${topic}`;
}

function detectPageContext(topic) {
    const text = String(topic || "").toLowerCase();

    if (text.includes("critical")) return "FCCM";
    if (text.includes("internal")) return "FIM";
    if (text.includes("diabetes")) return "FDM";
    if (text.includes("emergency")) return "FEM";
    if (text.includes("family")) return "FFM";
    if (text.includes("gyne") || text.includes("obstetric")) return "FGO";

    return null;
}

function askSuggestion(message) {
    document.getElementById("chatInput").value = message;
    sendChat();
}

async function sendChat() {
    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if (!message) return;

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

            <div class="bot-answer">
                <p>Thinking...</p>
            </div>
        </div>
    `;

    messages.appendChild(botBlock);

    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch(
            "https://doctyn-ai-rag-chatbot-9g3grvxm0-sathwikind-7124s-projects.vercel.app/chat",
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
        const result = data.response;

        if (result.session_id) {
            doctynSessionId = result.session_id;

            localStorage.setItem(
                "doctyn_session_id",
                doctynSessionId
            );
        }

        renderBotResponse(botBlock, result);

    } catch (error) {
        botBlock.querySelector(".bot-answer").innerHTML = `
            <p>
                I could not connect to the Doctyn AI service.
                Please make sure the backend is running.
            </p>
        `;

        console.error(error);
    }

    messages.scrollTop = messages.scrollHeight;
}

function renderBotResponse(botBlock, result) {
    const answerArea = botBlock.querySelector(".bot-answer");

    answerArea.innerHTML = `
        <div class="ai-answer-text">
            ${formatAnswer(result.answer)}
        </div>
    `;

    if (result.recommended_program) {
        const card = document.createElement("div");
        card.className = "ai-program-card";

        const reasons =
            result.recommended_program.reasons || [];

        card.innerHTML = `
            <div class="ai-program-label">
                Recommended pathway
            </div>

            <h4>
                ${escapeHtml(
                    result.recommended_program.program_name
                )}
            </h4>

            <div class="ai-match-score">
                ${result.recommended_program.match_score}% match
            </div>

            ${
                reasons.length > 0
                    ? `
                    <ul class="ai-reasons">
                        ${reasons
                            .map(
                                reason =>
                                    `<li>${escapeHtml(reason)}</li>`
                            )
                            .join("")}
                    </ul>
                    `
                    : ""
            }
        `;

        answerArea.appendChild(card);
    }

    if (
        result.alternatives &&
        result.alternatives.length > 0
    ) {
        const alternatives = document.createElement("div");
        alternatives.className = "ai-alternatives";

        alternatives.innerHTML = `
            <div class="ai-section-title">
                You may also consider
            </div>
        `;

        result.alternatives.forEach(item => {
            const button = document.createElement("button");

            button.className = "ai-alternative-button";

            button.innerText =
                `${item.program_name} (${item.match_score}%)`;

            button.addEventListener("click", () => {
                askSuggestion(
                    `Tell me about ${item.program_name}`
                );
            });

            alternatives.appendChild(button);
        });

        answerArea.appendChild(alternatives);
    }

    if (
        result.quick_actions &&
        result.quick_actions.length > 0
    ) {
        const actions = document.createElement("div");
        actions.className = "ai-quick-actions";

        result.quick_actions.forEach(action => {
            const button = document.createElement("button");

            button.innerText = action;

            button.addEventListener("click", () => {
                askSuggestion(action);
            });

            actions.appendChild(button);
        });

        answerArea.appendChild(actions);
    }
}

function formatAnswer(text) {
    if (!text) return "";

    return escapeHtml(text)
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}
