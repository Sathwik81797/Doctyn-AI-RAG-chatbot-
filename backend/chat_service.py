from course_data import COURSES


def chat_with_doctyn(message: str):
    text = message.lower().strip()

    if not text:
        return {
            "answer": "Please enter a question.",
            "source": "doctyn-local"
        }

    # Critical Care
    if "critical" in text or "icu" in text:
        return {
            "answer": (
                "For Critical Care, the most suitable pathway depends mainly on "
                "your current work status and ability to attend hospital training. "
                "A working doctor who cannot leave employment full-time may be "
                "better aligned with the Fellowship in Critical Care Medicine, "
                "which combines structured learning with supervised ICU training. "
                "Doctors who can commit to full-time ICU-based training can also "
                "explore the Advanced Fellowship pathway."
            ),
            "recommended_program": "Fellowship in Critical Care Medicine",
            "program_code": "FCCM",
            "source": "doctyn-local"
        }

    # Internal Medicine
    if "internal medicine" in text or "general medicine" in text:
        return {
            "answer": (
                "The Fellowship in Internal Medicine is designed for doctors "
                "looking to strengthen clinical reasoning, symptom-based assessment, "
                "ward decision-making and structured hospital exposure. "
                "The program combines structured online learning with clinical training."
            ),
            "recommended_program": "Fellowship in Internal Medicine",
            "program_code": "FIM",
            "source": "doctyn-local"
        }

    # Diabetes
    if "diabetes" in text or "diabetology" in text or "insulin" in text:
        return {
            "answer": (
                "The Fellowship in Diabetes Management is relevant for doctors who "
                "want structured learning in contemporary diabetes care, including "
                "insulin management, CGM interpretation and modern therapeutic approaches. "
                "Suitability also depends on your qualification and current clinical role."
            ),
            "recommended_program": "Fellowship in Diabetes Management",
            "program_code": "FDM",
            "source": "doctyn-local"
        }

    # Emergency Medicine
    if "emergency" in text or "trauma" in text or " er " in f" {text} ":
        return {
            "answer": (
                "For Emergency Medicine, we would first understand your current ER "
                "experience, employment status and ability to attend hospital-based "
                "training. Doctyn offers structured Emergency Medicine learning pathways "
                "for doctors looking to build practical emergency-care experience."
            ),
            "recommended_program": "Fellowship in Emergency Medicine",
            "program_code": "FEM",
            "source": "doctyn-local"
        }

    # Family Medicine
    if "family medicine" in text or "primary care" in text or "opd" in text:
        return {
            "answer": (
                "The Fellowship in Family Medicine is suited to doctors interested "
                "in primary care, OPD practice and longitudinal patient management. "
                "It combines structured learning with supervised clinical exposure."
            ),
            "recommended_program": "Fellowship in Family Medicine",
            "program_code": "FFM",
            "source": "doctyn-local"
        }

    # Working doctor
    if "working" in text or "job" in text or "hospital role" in text:
        return {
            "answer": (
                "If you are currently working, a hybrid fellowship may be more practical. "
                "Tell me your qualification, area of interest, city and whether you can "
                "attend a clinical training period, and I can narrow the recommendation."
            ),
            "source": "doctyn-local"
        }

    # Eligibility
    if "eligible" in text or "eligibility" in text or "mbbs" in text:
        return {
            "answer": (
                "Several Doctyn clinical fellowship programs are designed for MBBS "
                "graduates and above. Eligibility can vary by program, so tell me which "
                "specialty you are interested in and I can guide you more specifically."
            ),
            "source": "doctyn-local"
        }

    # Fees
    if "fee" in text or "price" in text or "cost" in text:
        return {
            "answer": (
                "Course fees can vary by program and intake. I should not invent a fee. "
                "Please select the program you are interested in or speak with a Doctyn "
                "counsellor for the current approved fee."
            ),
            "source": "doctyn-local"
        }

    return {
        "answer": (
            "I can help you identify a suitable Doctyn fellowship. "
            "Please tell me your qualification, area of interest, current work status "
            "and whether you can attend clinical training."
        ),
        "source": "doctyn-local"
    }
