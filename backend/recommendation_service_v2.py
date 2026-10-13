import re

from course_data_v2 import COURSES


SPECIALTY_PATTERNS = {
    "Critical Care Medicine": [
        "critical care",
        "critical",
        "icu",
        "intensive care",
        "ventilator",
        "ventilation",
        "sepsis"
    ],

    "Emergency Medicine": [
        "emergency medicine",
        "emergency",
        "trauma",
        "emergency room",
        " er "
    ],

    "Internal Medicine": [
        "internal medicine",
        "general medicine",
        "clinical medicine"
    ],

    "Diabetes Management": [
        "diabetes",
        "diabetology",
        "insulin",
        "cgm"
    ],

    "Family Medicine": [
        "family medicine",
        "primary care",
        "general practice",
        "opd"
    ],

    "Gynecology and Obstetrics": [
        "gynecology",
        "gynaecology",
        "obstetrics",
        "obgyn",
        "antenatal"
    ]
}


def detect_qualification(text: str):
    text = text.lower()

    qualifications = [
        ("MBBS", ["mbbs"]),
        ("DNB", ["dnb"]),
        ("MD", [" md ", "md doctor"]),
        ("MS", [" ms ", "ms doctor"]),
        ("FMG", ["fmg", "fmge", "foreign medical graduate"])
    ]

    padded = f" {text} "

    for qualification, terms in qualifications:
        for term in terms:
            if term in padded:
                return qualification

    return None


def detect_specialty(text: str):
    padded = f" {text.lower()} "

    best_specialty = None
    best_score = 0

    for specialty, keywords in SPECIALTY_PATTERNS.items():
        score = 0

        for keyword in keywords:
            if keyword in padded:
                score += 1

        if score > best_score:
            best_score = score
            best_specialty = specialty

    return best_specialty


def detect_city(text: str):
    cities = [
        "Hyderabad",
        "Bengaluru",
        "Bangalore",
        "Chennai",
        "Mumbai",
        "Pune",
        "Delhi",
        "Faridabad"
    ]

    lower = text.lower()

    for city in cities:
        if city.lower() in lower:
            if city == "Bangalore":
                return "Bengaluru"
            return city

    return None


def detect_work_status(text: str):
    lower = text.lower()

    if any(term in lower for term in [
        "not working",
        "unemployed",
        "not currently working"
    ]):
        return "Not currently working"

    if any(term in lower for term in [
        "working",
        "hospital job",
        "clinic",
        "dmo",
        "medical officer",
        "currently employed"
    ]):
        return "Working"

    return None


def detect_full_time_availability(text: str):
    lower = text.lower()

    negative_terms = [
        "cannot leave",
        "can't leave",
        "cant leave",
        "cannot do full time",
        "can't do full time",
        "part time only",
        "while working",
        "continue my job",
        "continue job"
    ]

    positive_terms = [
        "can do full time",
        "available full time",
        "full-time available",
        "ready for full time",
        "can leave my job"
    ]

    if any(term in lower for term in negative_terms):
        return False

    if any(term in lower for term in positive_terms):
        return True

    return None


def detect_intents(text: str):
    lower = text.lower()

    intents = []

    mappings = {
        "eligibility": [
            "eligible",
            "eligibility",
            "qualification required",
            "can i apply"
        ],

        "fees": [
            "fee",
            "fees",
            "cost",
            "price",
            "scholarship"
        ],

        "duration": [
            "duration",
            "how long",
            "months",
            "how many months"
        ],

        "clinical_training": [
            "clinical training",
            "hospital training",
            "hands on",
            "hands-on",
            "clinical exposure",
            "icu exposure"
        ],

        "curriculum": [
            "curriculum",
            "syllabus",
            "topics",
            "what will i learn",
            "what do i learn"
        ],

        "comparison": [
            "compare",
            "difference",
            "vs",
            "versus",
            "which is better"
        ],

        "admissions": [
            "admission",
            "join",
            "enroll",
            "enrol",
            "apply",
            "next batch"
        ],

        "stipend": [
            "stipend",
            "salary",
            "paid training"
        ],

        "location": [
            "location",
            "city",
            "where is training",
            "hospital location"
        ]
    }

    for intent, keywords in mappings.items():
        if any(keyword in lower for keyword in keywords):
            intents.append(intent)

    if not intents:
        intents.append("general")

    return intents


def extract_profile(message: str):
    return {
        "qualification": detect_qualification(message),
        "specialty_interest": detect_specialty(message),
        "city": detect_city(message),
        "employment_status": detect_work_status(message),
        "full_time_available": detect_full_time_availability(message)
    }


def merge_profile(old_profile: dict, new_profile: dict):
    result = dict(old_profile or {})

    for key, value in new_profile.items():
        if value is not None:
            result[key] = value

    return result


def recommend_courses(profile: dict, message: str = ""):
    specialty = profile.get("specialty_interest")
    full_time = profile.get("full_time_available")

    if not specialty:
        return []

    candidates = []

    for code, course in COURSES.items():
        if course["specialty"] != specialty:
            continue

        score = 50
        reasons = []

        if specialty == course["specialty"]:
            score += 25
            reasons.append(
                f"Matches your interest in {specialty}."
            )

        if full_time is False:
            if course["full_time_required"]:
                score -= 30
                reasons.append(
                    "This pathway requires full-time training, which may not fit your current availability."
                )
            else:
                score += 15
                reasons.append(
                    "The training format is more compatible with continuing your current work."
                )

        elif full_time is True:
            if course["full_time_required"]:
                score += 15
                reasons.append(
                    "You indicated that you are available for full-time training."
                )
            else:
                score += 5

        qualification = profile.get("qualification")

        if qualification:
            if qualification in course["eligibility"]:
                score += 10
                reasons.append(
                    f"Your stated qualification ({qualification}) appears within the listed eligibility."
                )

        score = max(0, min(score, 100))

        candidates.append({
            "program_code": code,
            "program_name": course["name"],
            "score": score,
            "reasons": reasons,
            "course": course
        })

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates


def build_verified_context(
    profile: dict,
    recommendations: list,
    intents: list,
    page_context: str = None
):
    lines = []

    lines.append("DOCTOR PROFILE:")
    lines.append(str(profile))

    lines.append("")
    lines.append("DETECTED INTENTS:")
    lines.append(", ".join(intents))

    if page_context:
        code = page_context.upper()

        if code in COURSES:
            lines.append("")
            lines.append("CURRENT PAGE PROGRAM:")
            lines.append(str(COURSES[code]))

    if recommendations:
        lines.append("")
        lines.append("RELEVANT PROGRAMS:")

        for item in recommendations[:3]:
            lines.append(
                str(item["course"])
            )

    else:
        lines.append("")
        lines.append(
            "No program recommendation has been established yet."
        )

    return "\n".join(lines)
