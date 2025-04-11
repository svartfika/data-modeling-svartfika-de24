from datetime import date


BRANCHES = [
    {"name": "STI Liljeholmen", "city": "Stockholm"},
    {"name": "STI Nordstan", "city": "Göteborg"},
]

PROGRAMS_COURSES = [
    {
        "name": "Data Engineer",
        "code": "DE",
        "courses": [
            {
                "name": "SQL",
                "code": "SQ",
            },
            {
                "name": "Data modelling",
                "code": "DM",
            },
            {
                "name": "Programmering inom data platform development",
                "code": "DP",
            },
        ],
    },
    {
        "name": "UX-designer",
        "code": "UX",
        "courses": [
            {
                "name": "Interaktionsdesign",
                "code": "ID",
            },
            {
                "name": "Frontend",
                "code": "FE",
            },
            {
                "name": "UX research, tjänstedesign och användbarhetstestning",
                "code": "RE",
            },
        ],
    },
    {
        "name": "Systemutvecklare Inbyggda system",
        "code": "SU",
        "courses": [
            {
                "name": "Digitalteknik och elektronik",
                "code": "DT",
            },
            {
                "name": "Objektorienterad programmering och design",
                "code": "OP",
            },
            {
                "name": "Algoritmer, datastrukturer och design patterns",
                "code": "AL",
            },
        ],
    },
    {
        "name": "Javautvecklare",
        "code": "JA",
        "courses": [
            {
                "name": "Java Enterprise och Eclipse",
                "code": "EE",
            },
            {
                "name": "Testdriven utveckling",
                "code": "TU",
            },
            {
                "name": "Molntjänster",
                "code": "MT",
            },
        ],
    },
    {
        "name": "iOS/Android Developer",
        "code": "AD",
        "courses": [
            {
                "name": "Hybridutveckling med Javascript 1",
                "code": "HJ",
            },
            {
                "name": "OOP, datastrukturer, algoritmer och design",
                "code": "DS",
            },
            {
                "name": "Webbkommunikation, APIer och backend",
                "code": "WA",
            },
        ],
    },
]

SEMESTERS = {
    "HT24": {
        "date_start": date(2024, 8, 18),
        "date_end": date(2025, 12, 22),
    },
    "VT25": {
        "date_start": date(2025, 1, 6),
        "date_end": date(2025, 6, 8),
    },
    "HT25": {
        "date_start": date(2025, 8, 18),
        "date_end": date(2025, 12, 28),
    },
    "VT26": {
        "date_start": date(2025, 12, 29),
        "date_end": date(2026, 5, 31),
    },
}
