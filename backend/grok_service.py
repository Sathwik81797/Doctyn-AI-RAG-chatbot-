from course_data import COURSES


def analyze_lead(lead_data: dict):
    interest = (lead_data.get("interest") or "").lower()
    message = (lead_data.get("message") or "").lower()
    qualification = (lead_data.get("qualification") or "").lower()
    training = (lead_data.get("clinical_training_available") or "").lower()

    combined_text = f"{interest} {message}"

    scores = {}

    for code, course in COURSES.items():
        score = 0

        for keyword in course["keywords"]:
            if keyword in combined_text:
                score += 25

        scores[code] = score

    recommended_code = max(scores, key=scores.get)
    recommended_course = COURSES[recommended_code]

    if "critical" in combined_text or "icu" in combined_text:
        if "full time" in training and "cannot" not in training:
            recommended_code = "AFCCM"
        else:
            recommended_code = "FCCM"

        recommended_course = COURSES[recommended_code]

    base_score = 50

    # Direct course-interest match
    if recommended_code == "FCCM" and ("critical" in combined_text or "icu" in combined_text):
        base_score += 25

    elif recommended_code == "AFCCM" and ("critical" in combined_text or "icu" in combined_text):
        base_score += 25

    elif recommended_code == "FIM" and ("internal medicine" in combined_text or "medicine" in combined_text):
        base_score += 25

    elif recommended_code == "FDM" and ("diabetes" in combined_text or "diabetology" in combined_text):
        base_score += 25

    elif recommended_code == "FEM" and ("emergency" in combined_text or "trauma" in combined_text):
        base_score += 25

    elif recommended_code == "FFM" and ("family medicine" in combined_text or "primary care" in combined_text):
        base_score += 25

    if qualification:
        base_score += 5

    if interest:
        base_score += 5

    if message:
        base_score += 5

    if lead_data.get("clinical_training_available"):
        base_score += 5

    match_score = min(base_score, 95)

    if interest and qualification and message:
        lead_status = "Warm"
        priority = "High"
    elif interest:
        lead_status = "Warm"
        priority = "Medium"
    else:
        lead_status = "Needs More Information"
        priority = "Medium"

    if "call me" in message or "join" in message or "admission" in message:
        lead_status = "Hot"
        priority = "High"

    missing_information = []

    if not lead_data.get("qualification"):
        missing_information.append("Qualification")

    if not lead_data.get("city"):
        missing_information.append("City")

    if not lead_data.get("clinical_training_available"):
        missing_information.append("Clinical training availability")

    if not lead_data.get("employment_status"):
        missing_information.append("Current employment status")

    reason = (
        f"{recommended_course['name']} is the strongest match based on the "
        f"doctor's stated interest and learning requirement."
    )

    next_action = (
        f"Counsellor should contact the lead and confirm eligibility, "
        f"clinical training availability, preferred intake and expectations "
        f"for {recommended_course['name']}."
    )

    doctor_name = lead_data.get("name") or "Doctor"

    whatsapp_message = (
        f"Hello {doctor_name}, thank you for your interest in Doctyn Academy. "
        f"Based on the details shared, {recommended_course['name']} may be relevant "
        f"to your learning goals. Our counsellor can explain the course structure, "
        f"eligibility and clinical training options."
    )

    return {
        "recommended_program": recommended_course["name"],
        "program_code": recommended_code,
        "match_score": match_score,
        "lead_status": lead_status,
        "priority": priority,
        "reason": reason,
        "missing_information": missing_information,
        "next_action": next_action,
        "whatsapp_message": whatsapp_message
    }


if __name__ == "__main__":
    test_lead = {
        "name": "Dr Rahul",
        "qualification": "MBBS",
        "city": "Hyderabad",
        "experience": "2 years",
        "interest": "Critical Care",
        "employment_status": "Working in hospital",
        "clinical_training_available": "Cannot leave job full time",
        "message": "I want to specialize in critical care while continuing my job"
    }

    print(analyze_lead(test_lead))
