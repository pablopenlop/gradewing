from choices import QT, GS, Ser, SG, MT

QUALIFICATIONS = [
        {
        'subject': '',
        'code': '9980',
        'group': SG.UK.PROJECT,
        'name': QT.UKI.CIE.IPQ.IPQ,
        'glh': 120,
        'first_assessment': 2023,
        'last_assessment': None,
        'current': True,
        'mark': 80,
        'mark_type': MT.RAW,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.MAR, Ser.Exam.JUN, Ser.Exam.NOV],
        'modular': False, 
        'sub_qualification': None,
        'components': [
            {
                'name': 'Paper 1: Research project',
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