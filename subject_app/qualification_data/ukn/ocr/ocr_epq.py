from choices import QT, GS, Ser, SG, MT

QUALIFICATIONS = [
        {
        'subject': '',
        'code': 'H857',
        'group': SG.UK.PROJECT,
        'name': QT.UKN.OCR.EPQ.EPQ,
        'glh': 120,
        'first_assessment': 2019,
        'last_assessment': None,
        'current': True,
        'mark': 60,
        'mark_type': MT.RAW,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JAN, Ser.Exam.JUN],
        'modular': False, 
        'sub_qualification': None,
        'components': [
            {
                'name': 'Research project',
                'code': '*/01',
                'mark': 60,
                'weighting': '100%',
                'duration': '',
                'grading': GS.AL.SINGLE_ASE,
                'internal': False,
            },
        ]
    },
    
]