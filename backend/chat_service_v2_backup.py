import uuid

from recommendation_service_v2 import (
    extract_profile,
    merge_profile,
    detect_intents,
    recommend_courses,
    build_verified_context
)

from grok_service_v2 import ask_grok


SESSIONS = {}


def create_session():
    return {
        "profile": {},
        "history": []
    }


def get_session(session_id: str = None):
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = create_session()

    return session_id, SESSIONS[session_id]


def local_fallback(
    profile,
    recommendations,
    intents
):
    if not recommendations:
        specialty = profile.get("specialty_interest")

        if not specialty:
            return (
                "I can help you find a suitable Doctyn fellowship. "
                "Which area are you most interested in — Critical Care, "
                "Emergency Medicine, Internal Medicine, Diabetes, "
                "Family Medicine or Gynecology and Obstetrics?"
            )

    top = recommendations[0]

    answer = (
        f"Based on the information shared, "
        f"{top['program_name']} may be the most relevant pathway."
    )

    if top["reasons"]:
        answer += "\n\nWhy it may fit:\n"

        for reason in top["reasons"][:3]:
            answer += f"• {reason}\n"

    course = top["course"]

    if "duration" in intents:
        answer += (
            f"\nDuration: {course.get('duration', 'Not verified')}"
        )

    if "clinical_training" in intents:
        answer += (
            f"\nClinical training: "
            f"{course.get('clinical_training', 'Not verified')}"
        )

    if "eligibility" in intents:
        eligibility = ", ".join(
            course.get("eligibility", [])
        )

        answer += (
            f"\nListed eligibility: {eligibility}"
        )

    if "curriculum" in intents:
        topics = course.get("topics", [])

        if topics:
            answer += "\n\nKey learning areas:\n"

            for topic in topics[:7]:
                answer += f"• {topic}\n"

    if "fees" in intents:
        answer += (
            "\n\nI don't have a verified current fee in this "
            "knowledge base. A Doctyn advisor should confirm "
            "the latest approved fee and any current offer."
        )

    return answer.strip()


def chat_with_doctyn_v2(
    message: str,
    session_id: str = None,
    page_context: str = None
):
    message = (message or "").strip()

    if not message:
        return {
            "answer": "Please enter a question.",
            "session_id": session_id,
            "source": "doctyn-v2"
        }

    session_id, session = get_session(session_id)

    new_profile = extract_profile(message)

    session["profile"] = merge_profile(
        session["profile"],
        new_profile
    )

    intents = detect_intents(message)

    recommendations = recommend_courses(
        session["profile"],
        message
    )

    verified_context = build_verified_context(
        profile=session["profile"],
        recommendations=recommendations,
        intents=intents,
        page_context=page_context
    )

    answer = ask_grok(
        user_message=message,
        verified_context=verified_context,
        conversation_history=session["history"]
    )

    source = "grok"

    if not answer:
        answer = local_fallback(
            session["profile"],
            recommendations,
            intents
        )

        source = "doctyn-local-fallback"

    session["history"].append({
        "role": "user",
        "content": message
    })

    session["history"].append({
        "role": "assistant",
        "content": answer
    })

    top_recommendation = None

    if recommendations:
        item = recommendations[0]

        top_recommendation = {
            "program_code": item["program_code"],
            "program_name": item["program_name"],
            "match_score": item["score"],
            "reasons": item["reasons"]
        }

    quick_actions = [
        "Check eligibility",
        "View curriculum",
        "Clinical training",
        "Compare programs",
        "Fees and admissions",
        "Talk to advisor"
    ]

    return {
        "answer": answer,
        "session_id": session_id,
        "doctor_profile": session["profile"],
        "intents": intents,
        "recommended_program": top_recommendation,
        "alternatives": [
            {
                "program_code": item["program_code"],
                "program_name": item["program_name"],
                "match_score": item["score"]
            }
            for item in recommendations[1:3]
        ],
        "quick_actions": quick_actions,
        "source": source
    }
