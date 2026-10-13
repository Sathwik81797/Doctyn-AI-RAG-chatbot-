import re
import uuid

from retrieval_service_v3 import search_doctyn_knowledge


SESSIONS = {}


PROGRAM_NAMES = {
    "FCCM": "Fellowship in Critical Care Medicine",
    "AFCCM": "Advanced Fellowship in Critical Care Medicine",
    "FEM": "Fellowship in Emergency Medicine",
    "AFEM": "Advanced Fellowship in Emergency Medicine",
    "FIM": "Fellowship in Internal Medicine",
    "FDM": "Fellowship in Diabetes Management",
    "FFM": "Fellowship in Family Medicine",
    "FGO": "Fellowship in Gynecology and Obstetrics"
}


def get_session(session_id=None):
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "history": [],
            "program_code": None
        }

    return session_id, SESSIONS[session_id]


def detect_program(message):
    text = message.lower()

    if "afccm" in text or "advanced fellowship in critical" in text:
        return "AFCCM"

    if (
        "fccm" in text
        or "critical care" in text
        or "critical care medicine" in text
    ):
        return "FCCM"

    if "afem" in text or "advanced fellowship in emergency" in text:
        return "AFEM"

    if (
        "fem" in text
        or "emergency medicine" in text
    ):
        return "FEM"

    if (
        "fim" in text
        or "internal medicine" in text
    ):
        return "FIM"

    if (
        "fdm" in text
        or "diabetes" in text
        or "diabetology" in text
    ):
        return "FDM"

    if (
        "ffm" in text
        or "family medicine" in text
    ):
        return "FFM"

    if (
        "fgo" in text
        or "gynecology" in text
        or "gynaecology" in text
        or "obstetrics" in text
    ):
        return "FGO"

    return None


def clean_chunk(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_answer(
    question,
    results,
    program_code=None
):
    if not results:
        return (
            "I could not find verified information for that "
            "question in the current Doctyn knowledge base."
        )

    question_lower = question.lower()

    program_name = PROGRAM_NAMES.get(
        program_code,
        "this program"
    )

    combined = " ".join(
        clean_chunk(result["content"])
        for result in results[:3]
    )

    # Duration
    if (
        "duration" in question_lower
        or "how long" in question_lower
    ):
        match = re.search(
            r"\b(\d{1,2})[\s-]*(?:month|months)\b",
            combined,
            re.IGNORECASE
        )

        if match:
            months = match.group(1)

            answer = (
                f"{program_name} has a duration of "
                f"{months} months according to the current "
                f"program material."
            )

            if "100% online" in combined.lower():
                answer += (
                    " The brochure describes the program "
                    "as 100% online with structured learning."
                )

            return answer

    # Eligibility
    if (
        "eligible" in question_lower
        or "eligibility" in question_lower
        or "qualification" in question_lower
    ):
        return (
            f"According to the current {program_name} material:\n\n"
            f"{clean_chunk(results[0]['content'])}"
        )

    # Curriculum / topics
    if (
        "curriculum" in question_lower
        or "topics" in question_lower
        or "learn" in question_lower
        or "syllabus" in question_lower
        or "covers" in question_lower
    ):
        return (
            f"The current {program_name} material includes "
            f"the following relevant information:\n\n"
            f"{clean_chunk(results[0]['content'])}"
        )

    # Clinical training
    if (
        "clinical training" in question_lower
        or "hospital training" in question_lower
        or "clinical exposure" in question_lower
        or "icu training" in question_lower
    ):
        return (
            f"According to the current {program_name} material:\n\n"
            f"{clean_chunk(results[0]['content'])}"
        )

    # General answer
    top_text = clean_chunk(results[0]["content"])

    if len(top_text) > 700:
        top_text = top_text[:700].rsplit(" ", 1)[0] + "..."

    return (
        f"Based on the current {program_name} material:\n\n"
        f"{top_text}"
    )


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

    detected_program = detect_program(message)

    if page_context:
        detected_program = page_context.upper()

    if detected_program:
        session["program_code"] = detected_program

    program_code = session.get("program_code")

    results = search_doctyn_knowledge(
        message,
        top_k=5,
        program_code=program_code
    )

    answer = build_answer(
        message,
        results,
        program_code=program_code
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

    seen = set()

    for result in results:
        key = (
            result["source_name"],
            result["page"]
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "name": result["source_name"],
            "page": result["page"],
            "score": result["score"]
        })

        if len(sources) >= 3:
            break

    return {
        "answer": answer,
        "session_id": session_id,
        "program_code": program_code,
        "sources": sources,
        "source": "doctyn-rag"
    }
