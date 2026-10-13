COURSES = {
    "FCCM": {
        "code": "FCCM",
        "name": "Fellowship in Critical Care Medicine",
        "specialty": "Critical Care Medicine",
        "eligibility": ["MBBS", "MD", "MS", "DNB"],
        "duration": "12 months",
        "learning_mode": "Hybrid",
        "online_training": "9 months",
        "clinical_training": "3 months supervised ICU training",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Airway management",
            "Mechanical ventilation",
            "Hemodynamic monitoring",
            "Sepsis and shock",
            "POCUS",
            "Central venous access",
            "Chest tube",
            "Tracheostomy",
            "Infection control"
        ],
        "keywords": [
            "critical care",
            "critical",
            "icu",
            "intensive care",
            "ventilation",
            "ventilator",
            "sepsis",
            "shock"
        ],
        "best_for": [
            "Doctors interested in Critical Care Medicine",
            "Working doctors who prefer a hybrid pathway",
            "Doctors seeking structured ICU learning and clinical exposure"
        ],
        "alternatives": ["AFCCM"]
    },

    "AFCCM": {
        "code": "AFCCM",
        "name": "Advanced Fellowship in Critical Care Medicine",
        "specialty": "Critical Care Medicine",
        "eligibility": ["MBBS", "MD", "MS", "DNB"],
        "duration": "12 months",
        "learning_mode": "Full-time hospital based",
        "clinical_training": "Full-time ICU training",
        "clinical_training_available": True,
        "full_time_required": True,
        "topics": [
            "Critical care",
            "ICU workflow",
            "Emergency stabilization",
            "Mechanical ventilation",
            "Hemodynamic management"
        ],
        "keywords": [
            "advanced critical care",
            "full time icu",
            "icu training",
            "critical care"
        ],
        "best_for": [
            "Doctors who can commit to full-time ICU training",
            "Doctors seeking intensive hospital-based exposure"
        ],
        "alternatives": ["FCCM"]
    },

    "FIM": {
        "code": "FIM",
        "name": "Fellowship in Internal Medicine",
        "specialty": "Internal Medicine",
        "eligibility": ["MBBS", "MD", "DNB"],
        "duration": "12 months",
        "learning_mode": "Hybrid",
        "online_training": "9 months",
        "clinical_training": "3 months hospital training",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Clinical reasoning",
            "Symptom-based assessment",
            "Ward workflow",
            "Internal medicine",
            "Case-based clinical learning"
        ],
        "keywords": [
            "internal medicine",
            "general medicine",
            "medicine",
            "ward",
            "clinical medicine"
        ],
        "best_for": [
            "Doctors seeking stronger Internal Medicine knowledge",
            "Doctors wanting structured clinical reasoning training"
        ],
        "alternatives": []
    },

    "FDM": {
        "code": "FDM",
        "name": "Fellowship in Diabetes Management",
        "specialty": "Diabetes Management",
        "eligibility": ["MBBS", "MD", "DNB"],
        "duration": "12 months",
        "learning_mode": "Hybrid",
        "clinical_training": "Clinical training included",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Diabetes management",
            "Insulin therapy",
            "CGM",
            "AGP",
            "Time in Range",
            "GLP-1 therapies",
            "SGLT2 inhibitors"
        ],
        "keywords": [
            "diabetes",
            "diabetology",
            "insulin",
            "cgm",
            "glucose",
            "diabetic"
        ],
        "best_for": [
            "Doctors interested in contemporary diabetes care",
            "Doctors managing diabetes in clinical practice"
        ],
        "alternatives": []
    },

    "FEM": {
        "code": "FEM",
        "name": "Fellowship in Emergency Medicine",
        "specialty": "Emergency Medicine",
        "eligibility": ["MBBS", "MD", "DNB"],
        "duration": "12 months",
        "learning_mode": "Structured Emergency Medicine pathway",
        "clinical_training": "Hospital-based clinical training",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Emergency assessment",
            "Trauma",
            "Resuscitation",
            "Acute care",
            "Emergency department workflow"
        ],
        "keywords": [
            "emergency",
            "emergency medicine",
            "er",
            "emergency room",
            "trauma",
            "acute care"
        ],
        "best_for": [
            "Doctors interested in Emergency Medicine",
            "Doctors seeking emergency department experience"
        ],
        "alternatives": ["AFEM"]
    },

    "AFEM": {
        "code": "AFEM",
        "name": "Advanced Fellowship in Emergency Medicine",
        "specialty": "Emergency Medicine",
        "eligibility": ["MBBS", "MD", "DNB"],
        "duration": "12 months",
        "learning_mode": "Full-time hospital based",
        "clinical_training": "Full-time Emergency Department training",
        "clinical_training_available": True,
        "full_time_required": True,
        "topics": [
            "Emergency medicine",
            "Trauma",
            "Resuscitation",
            "Emergency procedures",
            "Acute patient management"
        ],
        "keywords": [
            "advanced emergency",
            "full time emergency",
            "emergency training",
            "emergency medicine"
        ],
        "best_for": [
            "Doctors able to commit to full-time Emergency Medicine training"
        ],
        "alternatives": ["FEM"]
    },

    "FFM": {
        "code": "FFM",
        "name": "Fellowship in Family Medicine",
        "specialty": "Family Medicine",
        "eligibility": ["MBBS", "MD", "DNB"],
        "duration": "12 months",
        "learning_mode": "Hybrid",
        "clinical_training": "Clinical exposure included",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Primary care",
            "OPD practice",
            "Common clinical presentations",
            "Longitudinal patient care"
        ],
        "keywords": [
            "family medicine",
            "primary care",
            "opd",
            "general practice",
            "family physician"
        ],
        "best_for": [
            "Doctors interested in primary care and OPD practice"
        ],
        "alternatives": []
    },

    "FGO": {
        "code": "FGO",
        "name": "Fellowship in Gynecology and Obstetrics",
        "specialty": "Gynecology and Obstetrics",
        "eligibility": ["MBBS", "MD", "MS", "DNB"],
        "duration": "12 months",
        "learning_mode": "Hybrid",
        "clinical_training": "Supervised hospital training",
        "clinical_training_available": True,
        "full_time_required": False,
        "topics": [
            "Antenatal care",
            "Abnormal uterine bleeding",
            "Postpartum hemorrhage",
            "Eclampsia",
            "Obstetric emergencies"
        ],
        "keywords": [
            "gynecology",
            "gynaecology",
            "obstetrics",
            "obgyn",
            "pregnancy",
            "antenatal"
        ],
        "best_for": [
            "Doctors interested in Gynecology and Obstetrics"
        ],
        "alternatives": []
    }
}


def get_course(code: str):
    if not code:
        return None

    return COURSES.get(code.upper())


def get_all_courses():
    return list(COURSES.values())
