import uuid

from retrieval_service_v3 import search_doctyn_knowledge


SESSIONS = {}


def get_session(session_id=None):
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "history": []
        }

    return session_id, SESSIONS[session_id]


def build_answer(question, results):
    if not results:
        return (
            "I could not find verified Doctyn information for that question "
            "in the current knowledge base."
        )

    top = results[0]

    answer = top["content"]

    if len(answer) > 900:
        answer = answer[:900].rsplit(" ", 1)[0] + "..."

    return answer


def chat_with_doctyn_v3(
    message,
    session_id=None,
    page_context=None
):
    message = (message or "").strip()

    if not message:
        return {
            "answer": "Please enter a question.",
            "session_id": session_id,
            "sources": [],
            "source": "doctyn-rag"
        }

    session_id, session = get_session(session_id)

    search_query = message

    if page_context:
        search_query = f"{page_context} {message}"

    results = search_doctyn_knowledge(
        search_query,
        top_k=5
    )

    answer = build_answer(
        message,
        results
    )

    session["history"].append({
        "role": "user",
        "content": message
    })

    session["history"].append({
        "role": "assistant",
        "content": answer
    })

    sources = []

    for result in results[:3]:
        sources.append({
            "name": result["source_name"],
            "page": result["page"],
            "score": result["score"]
        })

    return {
        "answer": answer,
        "session_id": session_id,
        "sources": sources,
        "source": "doctyn-rag"
    }
