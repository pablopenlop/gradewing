from choices import QK, QT, GS, Ser, SG, MT, Board

QUALIFICATIONS = [
        {
        'subject': '',
        'code': '9695',
        'group': SG.UK.PROJECT,
        'name': QT.UKI.OxfordAQA.EPQ.EPQ,
        'glh': 120,
        'first_assessment': 2024,
        'last_assessment': None,
        'current': True,
        'mark': 80,
        'mark_type': MT.RAW,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.MAYJUN],
        'modular': False, 
        'sub_qualification': None,
        'components': [
            {
                'name': 'Research project',
                'code': '*/01',
                'mark': 80,
                'weighting': '100%',
                'duration': '',
                'grading': GS.AL.SINGLE_AE,
                'internal': False,
            },
        ]
    },
]