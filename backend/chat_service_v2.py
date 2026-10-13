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


def get_session(session_id=None):
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = create_session()

    return session_id, SESSIONS[session_id]


def local_fallback(profile, recommendations, intents, message=""):

    # No specialty/course established yet
    if not recommendations:
        specialty = profile.get("specialty_interest")

        if not specialty:
            return (
                "I can help you identify a relevant Doctyn fellowship. "
                "Which area are you interested in: Critical Care, "
                "Emergency Medicine, Internal Medicine, Diabetes, "
                "Family Medicine, or Gynecology and Obstetrics?"
            )

    top = recommendations[0]
    course = top["course"]
    program_name = top["program_name"]

    # -------------------------
    # DURATION
    # -------------------------
    if "duration" in intents:
        duration = course.get("duration")

        online = course.get("online_training")
        clinical = course.get("clinical_training")

        answer = f"{program_name} has a duration of {duration}."

        if online:
            answer += f"\n\nStructured learning: {online}."

        if clinical:
            answer += f"\nClinical training: {clinical}."

        return answer

    # -------------------------
    # CLINICAL TRAINING
    # -------------------------
    if "clinical_training" in intents:
        clinical = course.get(
            "clinical_training",
            "Clinical training details are not currently verified."
        )

        mode = course.get("learning_mode")

        answer = (
            f"For {program_name}, the clinical component is: "
            f"{clinical}."
        )

        if mode:
            answer += f"\n\nLearning format: {mode}."

        if course.get("full_time_required"):
            answer += (
                "\n\nThis pathway requires full-time hospital-based training."
            )
        else:
            answer += (
                "\n\nThis pathway does not require full-time training "
                "throughout the entire program."
            )

        return answer

    # -------------------------
    # ELIGIBILITY
    # -------------------------
    if "eligibility" in intents:
        eligibility = course.get("eligibility", [])

        eligibility_text = ", ".join(eligibility)

        answer = (
            f"The currently listed eligibility for {program_name} "
            f"includes: {eligibility_text}."
        )

        qualification = profile.get("qualification")

        if qualification:
            if qualification in eligibility:
                answer += (
                    f"\n\nBased on the qualification you shared "
                    f"({qualification}), you appear to meet the listed "
                    f"qualification requirement."
                )
            else:
                answer += (
                    f"\n\nYour qualification is recorded as {qualification}. "
                    "Eligibility should be confirmed with the Doctyn "
                    "admissions team."
                )

        return answer

    # -------------------------
    # CURRICULUM
    # -------------------------
    if "curriculum" in intents:
        topics = course.get("topics", [])

        if not topics:
            return (
                f"I don't currently have a verified detailed curriculum "
                f"for {program_name}."
            )

        answer = f"Key learning areas in {program_name} include:\n\n"

        for topic in topics:
            answer += f"• {topic}\n"

        return answer.strip()

    # -------------------------
    # FEES
    # -------------------------
    if "fees" in intents:
        return (
            f"I don't have a verified current fee for {program_name} "
            "in this knowledge base. Fees, scholarships and current offers "
            "can change by intake, so these should be confirmed with a "
            "Doctyn program advisor."
        )

    # -------------------------
    # STIPEND
    # -------------------------
    if "stipend" in intents:
        return (
            f"I don't have a verified current stipend value for "
            f"{program_name} in this version of the knowledge base. "
            "A Doctyn advisor can confirm whether the current intake "
            "has a stipend or paid training arrangement."
        )

    # -------------------------
    # LOCATION
    # -------------------------
    if "location" in intents:
        city = profile.get("city")

        if city:
            return (
                f"You previously mentioned {city}. I have recorded that "
                f"as your preferred city. The current hospital/training "
                f"location for {program_name} should be confirmed against "
                "the active Doctyn intake."
            )

        return (
            f"Which city would you prefer for the clinical component "
            f"of {program_name}?"
        )

    # -------------------------
    # COMPARISON
    # -------------------------
    if "comparison" in intents:
        if len(recommendations) > 1:
            first = recommendations[0]
            second = recommendations[1]

            c1 = first["course"]
            c2 = second["course"]

            return (
                f"{first['program_name']} vs "
                f"{second['program_name']}:\n\n"

                f"{first['program_name']}\n"
                f"• Duration: {c1.get('duration', 'Not verified')}\n"
                f"• Format: {c1.get('learning_mode', 'Not verified')}\n"
                f"• Clinical training: "
                f"{c1.get('clinical_training', 'Not verified')}\n"
                f"• Full-time required: "
                f"{'Yes' if c1.get('full_time_required') else 'No'}\n\n"

                f"{second['program_name']}\n"
                f"• Duration: {c2.get('duration', 'Not verified')}\n"
                f"• Format: {c2.get('learning_mode', 'Not verified')}\n"
                f"• Clinical training: "
                f"{c2.get('clinical_training', 'Not verified')}\n"
                f"• Full-time required: "
                f"{'Yes' if c2.get('full_time_required') else 'No'}\n\n"

                f"Based on what you have told me so far, "
                f"{first['program_name']} appears to fit your current "
                f"situation better."
            )

    # -------------------------
    # ADMISSIONS
    # -------------------------
    if "admissions" in intents:
        return (
            f"You are currently exploring {program_name}. "
            "For admission, the next step is to confirm your eligibility, "
            "preferred clinical-training location, current batch availability "
            "and approved fee with the Doctyn admissions team."
        )

    # -------------------------
    # GENERAL RECOMMENDATION
    # -------------------------
    answer = (
        f"Based on the information you shared, {program_name} "
        f"may be the most relevant pathway."
    )

    if top["reasons"]:
        answer += "\n\nWhy it may fit:\n"

        for reason in top["reasons"][:3]:
            answer += f"• {reason}\n"

    answer += (
        "\nYou can ask me about eligibility, duration, curriculum, "
        "clinical training, fees or program comparisons."
    )

    return answer.strip()


def chat_with_doctyn_v2(
    message,
    session_id=None,
    page_context=None
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
            intents,
            message
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
