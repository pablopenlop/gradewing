from choices import QT, GS, Ser, SG, MT, Tier


SUBJECTS = [
    {
        'subject': 'Art & Design',
        'code': ('0400', '0989'),
        'name': (
            QT.UKI.CIE.IGCSE.SINGLE_GA,
            QT.UKI.CIE.IGCSE.SINGLE_G9,
        ),
        'first_assessment': 2023,
        'last_assessment': 2026,
        'current': True,
        'mark': 200,
        'mark_type': MT.SCALED,
        'grading': (
            GS.GCSE_A.SINGLE_ASG, 
            GS.GCSE_9.SINGLE_91,
        ), 
        'series': [Ser.Exam.JUN], 
        'modular': False,
        'group': SG.UK.PROFESSIONAL,
        'current': True,
        'components': [
            {
                'name': 'Component 1: Coursework',
                'code': '*/1',
                'mark': 100,
                'weighting': '50%',
                'duration': '',
                'internal': False,
                'grading': (GS.GCSE_A.SINGLE_AG, GS.GCSE_9.SINGLE_91), 
            },
            {
                'name': 'Component 2: Externally Set Assignment',
                'code': '*/2',
                'mark': 100,
                'weighting': '50%',
                'duration': '8 hours',
                'internal': False,
                'grading': (GS.GCSE_A.SINGLE_AG, GS.GCSE_9.SINGLE_91), 
            },
        ]
    },
    {
        'name': 'MATHEMATICS',
        'code': (
            '0580', '0580', 
            '0980', '0980'
        ),
        'qualification': QT.British.IGCSE,
        'programme': Programme.British.IGCSE,
        'board': Board.CIE,
        'level': (
            Tier.CORE, Tier.EXTENDED, 
            Tier.CORE, Tier.EXTENDED
        ),
        'first_assessment': 2023,
        'last_assessment': 2024,
        'current': False,
        'mark': (
            160, 200,
            160, 200,
        ),
        'mark_type': MT.SCALED,
        'grading': (
            GS.GCSE_A.SINGLE_CG, GS.GCSE_A.SINGLE_ASE, 
            GS.GCSE_9.SINGLE_51, GS.GCSE_9.SINGLE_93
        ), 
        'series': [Ser.Exam.JUNE, Ser.Exam.NOVEMBER], 
        'modular': False,
        'group': SG.British.MATHS,
        'components': [
            {
                'name': 'Paper 1 (Core)',
                'code': '*/1',
                'mark': 56,
                'weighting': (
                    35, None,
                    35, None,
                ),
                'duration': '1 hour',
                'internal': False,
                'grading': (
                    GS.GCSE_A.SINGLE_CG, None,
                    GS.GCSE_9.SINGLE_41, None,
                ),
            },
            {
                'name': 'Paper 2 (Extended)',
                'code': '*/2',
                'mark': 70,
                'weighting': (
                    None, 35, 
                    None, 35, 
                ),
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': GS.GCSE_A.SINGLE_AE,
                'grading': (
                    None, GS.GCSE_A.SINGLE_AE,
                    None, GS.GCSE_9.SINGLE_94,
                ),
            },
            {
                'name': 'Paper 3 (Core)',
                'code': '*/3',
                'mark': 104,
                'weighting': (
                    65, None,
                    65, None,
                ),
                'duration': '2 hours',
                'internal': False,
                'grading': (
                    GS.GCSE_A.SINGLE_CG, None,
                    GS.GCSE_9.SINGLE_41, None,
                ),
            },
            {
                'name': 'Paper 4 (Extended)',
                'code': '*/4',
                'mark': 130,
                'weighting': (
                    None, 65, 
                    None, 65, 
                ),
                'duration': '2 hours 30 minutes',
                'internal': False,
                'grading': (
                    None, GS.GCSE_A.SINGLE_AE,
                    None, GS.GCSE_9.SINGLE_94,
                ),
            },
        ]
    },
    {
        'name': 'MATHEMATICS',
        'code': (
            '0580', '0580', 
            '0980', '0980',
        ),
        'qualification': QT.British.IGCSE,
        'programme': Programme.British.IGCSE,
        'board': Board.CIE,
        'level': (
            Tier.CORE, Tier.EXTENDED, 
            Tier.CORE, Tier.EXTENDED,
        ),
        'first_assessment': 2025,
        'last_assessment': 2027,
        'current': True,
        'mark': (
            160, 200,
            160, 200,
        ),
        'mark_type': MT.SCALED,
        'grading': (
            GS.GCSE_A.SINGLE_CG, GS.GCSE_A.SINGLE_ASE, 
            GS.GCSE_9.SINGLE_51, GS.GCSE_9.SINGLE_93,
        ), 
        'series': [ES.JUNE, ES.NOVEMBER], 
        'modular': False,
        'group': SG.British.MATHS,
        'current': True,
        'components': [
            {
                'name': 'Paper 1: Non-calculator (Core)',
                'code': '*/1',
                'mark': 80,
                'weighting': (
                    50, None,
                    50, None,
                ),
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': (
                    GS.GCSE_A.SINGLE_CG, None,
                    GS.GCSE_9.SINGLE_41, None,
                ),
            },
            {
                'name': 'Paper 2: Non-calculator (Extended)',
                'code': '*/2',
                'mark': 100,
                'weighting': (
                    None, 50,
                    None, 50,
                ),
                'duration': '2 hours',
                'internal': False,
                'grading': GS.GCSE_A.SINGLE_AE,
                'grading': (
                    None, GS.GCSE_A.SINGLE_AE,
                    None, GS.GCSE_9.SINGLE_94,
                ),
            },
            {
                'name': 'Paper 3: Calculator (Core)',
                'code': '*/3',
                'mark': 80,
                'weighting': (
                    50, None,
                    50, None,
                ),
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': (
                    GS.GCSE_A.SINGLE_CG, None,
                    GS.GCSE_9.SINGLE_41, None,
                ),
            },
            {
                'name': 'Paper 4: Calculator (Extended)',
                'code': '*/4',
                'mark': 100,
                'weighting': (
                    None, 50,
                    None, 50,
                ),
                'duration': '2 hours',
                'internal': False,
                'grading': (
                    None, GS.GCSE_A.SINGLE_AE,
                    None, GS.GCSE_9.SINGLE_94,
                ),
            },
        ]
    },
    
    {
        'name': 'Co-ordinated Sciences',
        'code': (
            '0654', '0654',
            '0973', '0973',
        ),
        'qualification': QT.British.IGCSE_DOUBLE,
        'programme': Programme.British.IGCSE,
        'board': Board.CIE,
        'level': (
            Tier.CORE, Tier.EXTENDED,
            Tier.CORE, Tier.EXTENDED,
        ),
        'first_assessment': 2023,
        'last_assessment': 2027,
        'current': True,
        'mark': 240,
        'mark_type': MT.SCALED,
        'grading': (
            GS.GCSE_A.DOUBLE_PAIRED_CG, GS.GCSE_A.DOUBLE_PAIRED_ASG,
            GS.GCSE_9.DOUBLE_PAIRED_51, GS.GCSE_9.DOUBLE_PAIRED_91,
        ),
        'series': [ES.MARCH, ES.JUNE, ES.NOVEMBER], 
        'modular': False,
        'group': SG.British.SCIENCES,
   
        'components': [
            {
                'name': 'Paper 1: Multiple Choice (Core)',
                'code': '*/1',
                'mark': 40,
                'weighting': (
                    30, None,
                    30, None,
                ),
                'duration': '45 minutes',
                'internal': False,
                'grading': (
                    GS.GCSE_A.DOUBLE_PAIRED_CG, None,
                    GS.GCSE_9.DOUBLE_PAIRED_41, None,
                ),
            },
            {
                'name': 'Paper 2: Multiple Choice (Extended)',
                'code': '*/2',
                'mark': 40,
                'weighting': (
                    None, 30,
                    None, 30,
                ),
                'duration': '45 minutes',
                'internal': False,
                'grading': (
                    None, GS.GCSE_A.DOUBLE_PAIRED_AG,
                    None, GS.GCSE_9.DOUBLE_PAIRED_91,
                )
            },
            {
                'name': 'Paper 3: Theory (Core)',
                'code': '*/3',
                'mark': 120,
                'weighting': (
                    50, None,
                    50, None
                ),
                'duration': '2 hours',
                'internal': False,
                'grading': (
                    GS.GCSE_A.DOUBLE_PAIRED_CG, None,
                    GS.GCSE_9.DOUBLE_PAIRED_41, None,
                ),
            },
            {
                'name': 'Paper 4: Theory (Extended)',
                'code': '*/4',
                'mark': 120,
                'weighting': (
                    None, 50,
                    None, 50,
                ),
                'duration': '2 hours',
                'internal': False,
                'grading': (
                    None, GS.GCSE_A.DOUBLE_PAIRED_AG,
                    None, GS.GCSE_9.DOUBLE_PAIRED_91,
                )
            },
            {
                'name': 'Paper 5: Practical Test',
                'code': '*/5',
                'mark': 60,
                'weighting': 20,
                'duration': '2 hours',
                'internal': False,
                'grading': (
                    GS.GCSE_A.DOUBLE_PAIRED_AG, GS.GCSE_A.DOUBLE_PAIRED_AG,
                    GS.GCSE_9.DOUBLE_PAIRED_91, GS.GCSE_9.DOUBLE_PAIRED_91,
                )
            },
            {
                'name': 'Paper 6: Alternative to Practical',
                'code': '*/6',
                'mark': 60,
                'weighting': 20,
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': (
                    GS.GCSE_A.DOUBLE_PAIRED_AG, GS.GCSE_A.DOUBLE_PAIRED_AG,
                    GS.GCSE_9.DOUBLE_PAIRED_91, GS.GCSE_9.DOUBLE_PAIRED_91,
                )
            }

        ]
    },
    
]
