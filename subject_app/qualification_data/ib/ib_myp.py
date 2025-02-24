from choices import QT, GS, Ser, SG, MT

QUALIFICATIONS = [
    {
        "group": SG.IB.MYP.LA,
        "subject": (
            "Arabic",
            "Chinese (Mandarin) Simplified",
            "Chinese (Mandarin) Traditional",
            "Dutch",
            "English",
            "French",
            "German",
            "Hindi",
            "Spanish",
            "Urdu"
        ),
        "suffix": "Language Acquisition",
        "code": (
            "IBMYP-100",
            "IBMYP-101",
            "IBMYP-102",
            "IBMYP-103",
            "IBMYP-104",
            "IBMYP-105",
            "IBMYP-106",
            "IBMYP-107",
            "IBMYP-108",
            "IBMYP-109",
        ),
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2023,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 96,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "On-screen: Spoken & written comprehension, Writing",
                "internal": False,
                "duration": "2 hours",
                "weighting": 75,
                "mark": 72,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
             {
                "name": "Individual speaking assessment",
                "internal": True,
                "duration": "2 hours",
                "weighting": 25,
                "mark": 24,
                "code": "*/2",
                "grading": GS.IB.SINGLE_71,
            }
        ]
    },
    {
        "group": SG.IB.MYP.LAL,
        "subject": (
            "Arabic",
            "Chinese (Mandarin) Simplified",
            "Chinese (Mandarin) Traditional",
            "Dutch",
            "English",
            "French",
            "German",
            "Kiswahili",
            "Korean",
            "Spanish"
        ),
        "code": (
            "IBMYP-200",
            "IBMYP-201",
            "IBMYP-202",
            "IBMYP-203",
            "IBMYP-204",
            "IBMYP-205",
            "IBMYP-206",
            "IBMYP-207",
            "IBMYP-208",
            "IBMYP-209",
        ),
        "suffix": "Language & Literature",
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2014,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 80,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "On-screen: Analysis & creative writing",
                "internal": False,
                "duration": "2 hours",
                "weighting": 100,
                "mark": 80,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.INDIVIDUALS,
        "subject": (
            "Geography",
            "History",
            "Integrated Humanities"
        ),
        "code": (
            "IBMYP-300",
            "IBMYP-301",
            "IBMYP-302",
        ),
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2014,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 80,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "On-screen: Investigating, communicating & thinking critically",
                "internal": False,
                "duration": "2 hours",
                "weighting": 100,
                "mark": 80,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.SCIENCES,
        "subject": (
            "Biology",
            "Chemistry",
            "Integrated sciences",
            "Physics"
        ),
        "code": (
            "IBMYP-400",
            "IBMYP-401",
            "IBMYP-402",
            "IBMYP-404",
        ),
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2014,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 100,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "On-screen: Knowing, investigating & applying",
                "internal": False,
                "duration": "2 hours",
                "weighting": 100,
                "mark": 100,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.MATHS,
        "subject": (
            "Extended Mathematics",
            "Mathematics",
        ),
        "code": (
            "IBMYP-500",
            "IBMYP-501",
        ),
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2022,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 100,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "On-screen: Knowing, investigating & applying",
                "internal": False,
                "duration": "2 hours",
                "weighting": 100,
                "mark": 100,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.ARTS,
        "subject": (
            "Dance",
            "Drama",
            "Media",
            "Music",
            "Visual Arts",
        ),
        "code": (
            "IBMYP-600",
            "IBMYP-601",
            "IBMYP-602",
            "IBMYP-604",
            "IBMYP-605",
        ),
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2023,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 32,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "ePortfolio (Arts)",
                "internal": False,
                "duration": "",
                "weighting": 100,
                "mark": 32,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.DESIGN,
        "subject": "DESIGN",
        "code": "IBMYP-700",
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2014,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 32,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "ePortfolio (Design)",
                "internal": False,
                "duration": "",
                "weighting": 100,
                "mark": 32,
                "grading": GS.NONE.NONE,
                "code": "*/1",
            },
        ]
    },
    {
        "group": SG.IB.MYP.PHE,
        "subject": "Physical Health Education",
        "code": "IBMYP-800",
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2014,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 32,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "ePortfolio (Design)",
                "internal": False,
                "duration": "",
                "weighting": 100,
                "mark": 32,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.INTER,
        "subject": "Interdisciplinary",
        "code": "IBMYP-900",
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2023,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 80,
        "modular": False,
        "mark_type": MT.RAW,
        "components": [
            {
                "name": "On-screen: Evaluating, synthesizing & reflecting",
                "internal": False,
                "duration": "2 hours",
                "weighting": 100,
                "mark": 80,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    },
    {
        "group": SG.IB.MYP.PROJECT,
        "subject": "Personal Project",
        "code": "IBMYP-901",
        "name": QT.IB.IBO.MYP.MYP,
        "grading": GS.IB.SINGLE_71,
        "series": [Ser.Exam.MAY, Ser.Exam.NOV],
        "first_assessment": 2023,
        "last_assessment": None,
        "glh": 250,
        "current": True,
        "mark": 24,
        "mark_type": MT.RAW,
        "modular": False,
        "components": [
            {
                "name": "ePortfolio: Personal Project",
                "internal": False,
                "duration": "",
                "weighting": 100,
                "mark": 24,
                "code": "*/1",
                "grading": GS.IB.SINGLE_71,
            },
        ]
    }

]



############################

"""

class MYP:
    EP = "ePortfolio"
    ONSCREEN = "On-screen"
    EA = "eAssessment"
    INTERNAL = "Internally assessed"


SUBJECT_GROUPS_OLD = {
    "Language Acquisition": {
        "subjects": [
            "ARABIC",
            "CHINESE (MANDARIN) SIMPLIFIED",
            "CHINESE (MANDARIN) TRADITIONAL",
            "DUTCH",
            "ENGLISH",
            "FRENCH",
            "GERMAN",
            "HINDI",
            "SPANISH",
            "URDU"
        ],
        "suffix": "LA",
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2023,
        "components":  {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [
                        ("Spoken comprehension", 24), 
                        ("Written comprehension", 24),
                        ("Writing", 24)
                    ],
                    "type": MYP.ONSCREEN,
                    "mark": 72
                },
                {
                    "tasks": [
                        ("Individual speaking assessment", 24)
                    ],
                    "type": MYP.INTERNAL,
                    "mark": 24
                }
            ]
        }
    },
    "Language & Literature": {
        "subjects": [
            "ARABIC",
            "CHINESE (MANDARIN) SIMPLIFIED",
            "CHINESE (MANDARIN) TRADITIONAL",
            "DUTCH",
            "ENGLISH",
            "FRENCH",
            "GERMAN",
            "KISWAHILI",
            "KOREAN",
            "SPANISH"
        ],
        "suffix": "LAL",
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2014,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [
                        ("Analysis", 30), 
                        ("Creative writing", 50)
                    ],
                    "type": MYP.ONSCREEN,
                    "mark": 80
                }
            ]
        }
    },
    "Individuals & Societies": {
        "subjects": [
            "GEOGRAPHY",
            "HISTORY",
            "INTEGRATED HUMANITIES"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2014,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [
                        ("Investigating", 26), 
                        ("Communicating", 18),
                        ("Thinking critically", 36)
                    ],
                    "type": MYP.ONSCREEN,
                    "mark": 80
                }
            ]
        }
    },
    "Sciences": {
        "subjects": [
            "BIOLOGY",
            "CHEMISTRY",
            "INTEGRATED SCIENCES",
            "PHYSICS"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2014,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [
                        ("Knowing and understanding", 25), 
                        ("Investigating skills", 50),
                        ("Applying science", 25)
                    ],
                    "type": MYP.ONSCREEN,
                    "mark": 100,
                    "notes": "Task marks and total mark may vary"
                }
            ]
        }
    },
    "Mathematics": {
        "subjects": [
            "EXTENDED MATHEMATICS",
            "MATHEMATICS"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2022,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                "tasks": [
                    ("Knowing and understanding", 33), 
                    ("Investigating patterns", 33),
                    ("Applying mathematics in real-life contexts", 33)
                ],
                "type": MYP.ONSCREEN,
                "mark": 100,
                "notes": "Task marks may vary (31-35)"
                }
            ]
        }
    },
    "Arts": {
        "subjects": [
            "DANCE",
            "DRAMA",
            "MEDIA",
            "MUSIC",
            "VISUAL ARTS"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2023,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [],
                    "type": MYP.EP,
                    "mark": None,
                    
                }
            ]
        }
    },
    "Physical & Health Education": {
        "subjects": [
            "PHYSICAL HEAL EDUCATION"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2014,
        "components": {
            "tag": MYP.EA,
            "kind": "EP",
            "content": []
        }
    },
    "Design": {
        "subjects": [
            "DESIGN"
        ],
        "qualification": QT.IB.MYP,
        "programme": Programme.IB.MYP,
        "board": Board.IB,
        "suite": QT.IB.MYP._SUITE,
        "grading": GS.IB.SINGLE_71,
        "series": [ES.MAY, ES.NOV],
        "first_assessment": 2014,
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [],
                    "type": MYP.EP,
                    "mark": None,
                    
                }
            ]
        }
    },
    "Interdisciplinary": {
        "subjects": [
            "INTERDISCIPLINARY"
        ],
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [
                        ("(A1) Evaluating & Reflecting", 24), 
                        ("(A2) Synthesizing", 12), 
                        ("(B1) Evaluating", 12), 
                        ("(B2) Synthesizing & Reflecting", 24)
                    ],
                    "type":  MYP.ONSCREEN,
                    "mark": 36,
                    "notes": "Assessment comprises either Tasks (A1, A2) or Tasks (B1, B2)"
                }
            ]
        }
    },
    "Personal project": {
        "subjects": [
            "PERSONAL PROJECT"
        ],
        "components": {
            "tag": MYP.EA,
            "content": [
                {
                    "tasks": [],
                    "type": MYP.EP,
                    "mark": None,
                    
                }
            ]
        }
    }
}

 """