from choices import QT, GS, Ser, SG, MT

QUALIFICATIONS = [
    {
        'subject': 'Accounting',
        'code': '7707',
        'name': QT.UKI.CIE.OL.OL,
        'group': SG.UK.PROFESSIONAL,
        'first_assessment': 2023,
        'glh': 130,
        'mark': 143,
        'mark_type': MT.SCALED,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JUN], 
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Multiple choice',
                'code': '7707/1',
                'mark': 35,
                'weighting': '30%',
                'duration': '1 hour 15 minutes',
                'internal': False,
                'grading': GS.AL.SINGLE_AE, 
            },
            {
                'name': 'Paper 2: Written examination',
                'code': '7707/2',
                'mark': 100,
                'weighting': '70%',
                'duration': '1 hour 45 minutes',
                'internal': False,
                'grading': GS.AL.SINGLE_AE, 
            },
        ]
    },
    {
        'subject': 'Agriculture',
        'code': '5038',
        'group': SG.UK.PROFESSIONAL,
        'name': QT.UKI.CIE.OL.OL,
        'first_assessment': 2024,
        'glh': 130,
        'mark': 200,
        'mark_type': MT.SCALED,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JUN], 
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Theory',
                'code': '5038/1',
                'mark': 100,
                'weighting': '70%',
                'duration': '1 hour 15 minutes',
                'internal': False,
                'grading': GS.AL.SINGLE_AE, 
            },
            {
                'name': 'Component 2: Practical Coursework',
                'code': '5038/2',
                'mark': 90,
                'weighting': '30%',
                'duration': '',
                'internal': True,
                'grading': GS.AL.SINGLE_AE, 
            },
        ]
    },
    {
        'subject': 'Mathematics D',
        'code': '4024',
        'name': QT.UKI.CIE.OL.OL,
        'group': SG.UK.MATHS,
        'first_assessment': 2025,
        'glh': 130,
        'mark': 200,
        'mark_type': MT.SCALED,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JUN], 
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Non-calculator',
                'code': '*/1',
                'mark': 100,
                'weighting': '50%',
                'duration': '2 hours',
                'internal': False,
                'grading': GS.AL.SINGLE_AE, 
            },
            {
                'name': 'Component 2: Calculator',
                'code': '*/2',
                'mark': 100,
                'weighting': '50%',
                'duration': '2 hours',
                'internal': False,
                'grading': GS.AL.SINGLE_AE, 
            },
        ]
    },
]