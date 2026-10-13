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

    if "fem" in text or "emergency medicine" in text:
        return "FEM"

    if "fim" in text or "internal medicine" in text:
        return "FIM"

    if (
        "fdm" in text
        or "diabetes" in text
        or "diabetology" in text
    ):
        return "FDM"

    if "ffm" in text or "family medicine" in text:
        return "FFM"

    if (
        "fgo" in text
        or "gynecology" in text
        or "gynaecology" in text
        or "obstetrics" in text
    ):
        return "FGO"

    return None


def build_search_query(message, program_code=None):
    """
    Expand short conversational questions into search terms
    that are more likely to occur inside the brochures.
    """

    text = message.lower()

    program_name = PROGRAM_NAMES.get(
        program_code,
        ""
    )

    expansion = ""

    if any(term in text for term in [
        "topics",
        "topic",
        "cover",
        "covers",
        "curriculum",
        "syllabus",
        "learn",
        "learning"
    ]):
        expansion = (
            "curriculum syllabus modules topics learning areas "
            "program highlights clinical concepts"
        )

    elif any(term in text for term in [
        "clinical training",
        "hospital training",
        "clinical exposure",
        "hands on",
        "hands-on",
        "icu training"
    ]):
        expansion = (
            "clinical training hospital training clinical exposure "
            "hands-on training ICU exposure"
        )

    elif any(term in text for term in [
        "duration",
        "how long",
        "months",
        "year"
    ]):
        expansion = (
            "duration months program duration course duration"
        )

    elif any(term in text for term in [
        "eligible",
        "eligibility",
        "qualification",
        "apply",
        "who can"
    ]):
        expansion = (
            "eligibility qualification eligible doctors admission criteria"
        )

    elif any(term in text for term in [
        "certificate",
        "certification",
        "cpd",
        "accreditation"
    ]):
        expansion = (
            "certificate certification CPD accreditation completion"
        )

    elif any(term in text for term in [
        "assessment",
        "exam",
        "examination",
        "quiz",
        "logbook"
    ]):
        expansion = (
            "assessment examination quizzes logbook viva OSCE"
        )

    elif any(term in text for term in [
        "fee",
        "fees",
        "cost",
        "price"
    ]):
        expansion = (
            "fees course fee program fee price"
        )

    return f"{program_name} {message} {expansion}".strip()


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
            "I could not find verified information for that question "
            "in the current Doctyn knowledge base."
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
                    " The current brochure describes the program "
                    "as 100% online with structured learning."
                )

            return answer

    if any(term in question_lower for term in [
        "topics",
        "topic",
        "cover",
        "covers",
        "curriculum",
        "syllabus",
        "learn"
    ]):
        topic_result = next(
            (r for r in results if r.get("page") not in (None, 1)),
            results[0]
        )

        text = clean_chunk(max(results, key=lambda r: sum(k in r["content"].lower() for k in ["airway", "ventilation", "haemodynamic", "shock", "sepsis", "organ dysfunction", "pharmacology", "infection prevention", "patient safety"]))["content"])

        return (
            f"According to the current {program_name} material, "
            f"the relevant curriculum information includes:\n\n"
            f"{text}"
        )

    if any(term in question_lower for term in [
        "clinical training",
        "hospital training",
        "clinical exposure",
        "icu training"
    ]):
        return (
            f"According to the current {program_name} material:\n\n"
            f"{clean_chunk(results[0]['content'])}"
        )

    if any(term in question_lower for term in [
        "eligible",
        "eligibility",
        "qualification",
        "who can apply"
    ]):
        return (
            f"According to the current {program_name} material:\n\n"
            f"{clean_chunk(results[0]['content'])}"
        )

    top_text = clean_chunk(results[0]["content"])

    if len(top_text) > 800:
        top_text = top_text[:800].rsplit(" ", 1)[0] + "..."

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

    search_query = build_search_query(
        message,
        program_code
    )

    results = search_doctyn_knowledge(
        search_query,
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
