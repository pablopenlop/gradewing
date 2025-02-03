from choices import QT, GS, Ser, SG, MT

QUALIFICATIONS = [
    {
        'subject': (
            'Art & Design: Art, Craft & Design',
            'Art & Design: Fine Art',
            'Art & Design: Graphic Communication',
            'Art & Design: Textile design',
            'Art & Design: 3D design',
            'Art & Design: Photography',
            ),
        'code': (
            '7201',
            '7202',
            '7203',
            '7204',
            '7205',
            '7206',
        ),
        'group': SG.UK.PROFESSIONAL,
        'name': QT.UKN.AQA.AL.A2,
        'glh': 360,
        'first_assessment': 2017,
        'mark': 480,
        'mark_type': MT.SCALED,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JUN],
        'modular': False,
        'components': [
            {
                'name': 'Component 1 (NEA): Personal investigation',
                'code': '*/C',
                'mark': 96,
                'mark_type': MT.RAW,
                'weighting': '60%',
                'duration': '',
                'grading': GS.AL.SINGLE_ASE,
                'internal': True,
            },
            {
                'name': 'Component 2: Externally set assignment',
                'code': '*/X',
                'mark': 72,
                'mark_type': MT.RAW,
                'weighting': '40%',
                'duration': 'Prep. period + 15 hours',
                'grading': GS.AL.SINGLE_ASE,
                'internal': True,
            },
            
        ]
    },

        {
        'subject': 'History',
        'code': '7042',
        'group': SG.UK.HUMANITIES,
        'name': QT.UKN.AQA.AL.A2,
        'glh': 360,
        'first_assessment': 2019,
        'mark': 200,
        'mark_type': MT.SCALED,
        'grading': GS.AL.SINGLE_ASE, 
        'series': [Ser.Exam.JUN],
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Breadth study',
                'code': '*/1A(L)',
                'mark': 80,
                'mark_type': MT.RAW,
                'weighting': '40%',
                'duration': '2 hours 30 minutes',
                'grading': GS.AL.SINGLE_ASE,
                'internal': False,
            },
            {
               'name': 'Paper 2: Depth study',
                'code': '*/2A(T)',
                'mark': 80,
                'mark_type': MT.RAW,
                'weighting': '40%',
                'duration': '2 hours 30 minutes',
                'grading': GS.AL.SINGLE_ASE,
                'internal': False,
            },
            {
                'name': 'Component 3 (NEA): Historical investigation',
                'code': '*/C',
                'mark': 40,
                'mark_type': MT.RAW,
                'weighting': '20%',
                'duration': '',
                'grading': GS.AL.SINGLE_ASE,
                'internal': True,
            },
            
        ]
    },
]
    