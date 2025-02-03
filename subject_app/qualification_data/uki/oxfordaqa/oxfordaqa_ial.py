from subject_app.models import Programme, Board
from register_app.edusystem import QualificationType as QT 
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import ExamSeries as ES
from register_app.edusystem import MarkType as MT

SUBJECTS = [
    {
        'name': 'BIOLOGY',
        'code': ('9611', '9612'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark': (300, 600),
        'mark_type': MT.UMS,
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'BIOLOGY UNIT 1',
                'code': 'BL01',
                'mark': 75,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'BIOLOGY UNIT 2',
                'code': 'BL02',
                'mark': 75,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'BIOLOGY UNIT 3',
                'code': 'BL03',
                'mark': 75,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'BIOLOGY UNIT 4',
                'code': 'BL04',
                'mark': 75,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'BIOLOGY UNIT 5',
                'code': 'BL04',
                'mark': 75,
                'mark_ums': 100,
                'eligible': (False, True)
            },

        ]
    },

    {
        'name': 'BUSINESS',
        'code': ('9626', '9627'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (160, 400),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'BUSINESS UNIT 1',
                'code': 'BU01',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'BUSINESS UNIT 2',
                'code': 'BU02',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'BUSINESS UNIT 3',
                'code': 'BU03',
                'mark': 80,
                'mark_ums': 120,
                'eligible': (False, True)
            },
            {
                'name': 'BUSINESS UNIT 4',
                'code': 'BU04',
                'mark': 80,
                'mark_ums': 120,
                'eligible': (False, True)
            }
        ]
    },

    {
        'name': 'CHEMISTRY',
        'code': ('9621', '9622'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (200, 500),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'CHEMISTRY UNIT 1',
                'code': 'CH01',
                'mark': 70,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'CHEMISTRY UNIT 2',
                'code': 'CH02',
                'mark': 70,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'CHEMISTRY UNIT 3',
                'code': 'CH03',
                'mark': 80,
                'mark_ums': 105,
                'eligible': (False, True)
            },
            {
                'name': 'CHEMISTRY UNIT 4',
                'code': 'CH04',
                'mark': 80,
                'mark_ums': 105,
                'eligible': (False, True)
            },
            {
                'name': 'CHEMISTRY UNIT 5',
                'code': 'CH05',
                'mark': 60,
                'mark_ums': 90,
                'eligible': (False, True)
            }
        ]
    },

    {
        'name': 'ECONOMICS',
        'code': ('9641', '9642'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (160, 400), 
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'ECONOMICS UNIT 1',
                'code': 'EC01',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'ECONOMICS UNIT 2',
                'code': 'EC02',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'ECONOMICS UNIT 3',
                'code': 'EC03',
                'mark': 90,
                'mark_ums': 120,
                'eligible': (False, True)
            },
            {
                'name': 'ECONOMICS UNIT 4',
                'code': 'EC04',
                'mark': 90,
                'mark_ums': 120,
                'eligible': (False, True)
            }
        ]
    },
    {
        'name': 'ENGLISH LANGUAGE',
        'code': ('9671', '9672'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (160, 400),  
        'components': [
            {
                'name': 'ENGLISH LANGUAGE UNIT 1',
                'code': 'EN01',
                'mark': 50,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'ENGLISH LANGUAGE UNIT 2',
                'code': 'EN02',
                'mark': 50,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'ENGLISH LANGUAGE UNIT 3',
                'code': 'EN03',
                'mark': 50,
                'mark_ums': 120,
                'eligible': (False, True)
            },
            {
                'name': 'ENGLISH LANGUAGE UNIT 4A',
                'code': 'EN04A',
                'mark': 50,
                'mark_ums': 120,
                'eligible': (False, True)
            },
            {
                'name': 'ENGLISH LANGUAGE UNIT 4B',
                'code': 'EN04B',
                'mark': 50,
                'mark_ums': 120,
                'eligible': (False, True)
            }
        ]
    },
    {
        'name': 'ENGLISH LITERATURE',
        'code': ('9676', '9677'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'mark_ums': (160, 400), 
        'first_assessment': (2018, 2019),
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'ENGLISH LITERATURE UNIT 1',
                'code': 'LT01',
                'mark': 50,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'ENGLISH LITERATURE UNIT 2',
                'code': 'LT02',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            }
        ]
    },
    {
        'name': 'Further Mathematics',
        'code': ('9666', '9667'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (320, 770),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'FURTHER MATHS UNIT 1 (FP1)',
                'code': 'FM01',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'FURTHER MATHS UNIT 2 (FPSM1)',
                'code': 'FM02',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'FURTHER MATHS UNIT 3 (FP2)',
                'code': 'FM03',
                'mark': 120,
                'mark_ums': 150,
                'eligible': (False, True)
            },
            {
                'name': 'FURTHER MATHS UNIT 4 (FS2)',
                'code': 'FM04',
                'mark': 80,
                'mark_ums': 90,
                'eligible': (False, True)
            },
            {
                'name': 'FURTHER MATHS UNIT 5 (FM2)',
                'code': 'FM05',
                'mark': 80,
                'mark_ums': 90,
                'eligible': (False, True)
            }
        ]
    },
    {
        'name': 'GEOGRAPHY',
        'code': ('9636', '9637'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (200, 500),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'GEOGRAPHY UNIT 1 OPTION A',
                'code': 'GG01A',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'GEOGRAPHY UNIT 2',
                'code': 'GG02',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'GEOGRAPHY UNIT 3',
                'code': 'GG03',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'GEOGRAPHY UNIT 4',
                'code': 'GG04',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'GEOGRAPHY UNIT 5',
                'code': 'GG05',
                'mark': 60,
                'mark_ums': 100,
                'eligible': (False, True)
            }
        ]
    },
    {
        'name': 'MATHEMATICS',
        'code': ('9661', '9662'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (160, 400),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'MATHS UNIT 1 (P1)',
                'code': 'MA01',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'MATHS UNIT 2 (PSM1)',
                'code': 'MA02',
                'mark': 80,
                'mark_ums': 80,
                'eligible': (True, True)
            },
            {
                'name': 'MATHS UNIT 3 (P2)',
                'code': 'MA03',
                'mark': 120,
                'mark_ums': 150,
                'eligible': (False, True)
            },
            {
                'name': 'MATHS UNIT 4 (S2)',
                'code': 'MA04',
                'mark': 80,
                'mark_ums': 90,
                'eligible': (False, True)
            },
            {
                'name': 'MATHS UNIT 5 (M2)',
                'code': 'MA05',
                'mark': 80,
                'mark_ums': 90,
                'eligible': (False, True)
            }
        ]
    },
    {
        'name': 'PHYSICS',
        'code': ('9631', '9632'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (200, 500),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'PHYSICS UNIT 1',
                'code': 'PH01',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'PHYSICS UNIT 2',
                'code': 'PH02',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'PHYSICS UNIT 3',
                'code': 'PH03',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'PHYSICS UNIT 4',
                'code': 'PH04',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'PHYSICS UNIT 5',
                'code': 'PH05',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            }
        ]
    },

    {
        'name': 'PSYCHOLOGY',
        'code': ('9686', '9687'),
        'qualification': (QT.British.IAS, QT.British.IA2),
        'programme': Programme.British.IAL,
        'board': Board.OXFORD_AQA,
        'first_assessment': (2018, 2019),
        'mark_ums': (160, 400),  
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.MAYJUNE, ES.NOVEMBER],
        'components': [
            {
                'name': 'PSYCHOLOGY UNIT 1',
                'code': 'PY01',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'PSYCHOLOGY UNIT 2',
                'code': 'PY02',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (True, True)
            },
            {
                'name': 'PSYCHOLOGY UNIT 3',
                'code': 'PY03',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            },
            {
                'name': 'PSYCHOLOGY UNIT 4',
                'code': 'PY04',
                'mark': 80,
                'mark_ums': 100,
                'eligible': (False, True)
            }
        ]
    }

]