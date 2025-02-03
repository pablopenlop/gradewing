
from choices import QT, GS, Ser, SG, MT, Tier


QUALIFICATIONS = [

    {
        'subject': 'Media Studies',
        'code': '9257',
        'group': SG.UK.PROFESSIONAL,
        'name': QT.UKI.OxfordAQA.IGCSE.SINGLE,
        'first_assessment': 2025,
        'glh': 120,
        'mark': 200,
        'mark_type': MT.SCALED,
        'grading': GS.GCSE_9.SINGLE_91, 
        'series': [Ser.Exam.MAYJUN, Ser.Exam.NOV], 
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Media Knowledge and Understanding',
                'code': '9257/1',
                'mark': 100,
                'weighting': '50%',
                'duration': '2 hours',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_91,
            },
            {
                'name': 'Non-exam assessment: Creating a media product',
                'code': '9257/2',
                'mark': 100,
                'weighting': '50%',
                'duration': '',
                'internal': True,
                'grading': GS.GCSE_9.SINGLE_91,
            },
        ]
    },


    {
        'subject': (
            'Combined Science (Core)',
            'Combined Science (Core)',
            'Combined Science (Extension)',
            'Combined Science (Extension)',
        ),
        'code': ('9204C', '9204CE', '9204E', '9204EE'),
        'group': SG.UK.SCIENCES,
        'name': (
            QT.UKI.OxfordAQA.IGCSE.DOUBLE,
            QT.UKI.OxfordAQA.IGCSE.DOUBLE_PLUS,
            QT.UKI.OxfordAQA.IGCSE.DOUBLE,
            QT.UKI.OxfordAQA.IGCSE.DOUBLE_PLUS,
        ),
        'tier': (Tier.CORE, Tier.CORE, Tier.EXTENDED, Tier.EXTENDED),
        'first_assessment': 2018,
        'glh': 240,
        'mark': 300,
        'mark_type': MT.SCALED,
        'grading': (
            GS.GCSE_9.DOUBLE_PAIRED_51, 
            GS.GCSE_9.DOUBLE_PAIRED_51,
            GS.GCSE_9.DOUBLE_PAIRED_93,
            GS.GCSE_9.DOUBLE_PAIRED_93,
        ), 
        'series': [Ser.Exam.JUN, Ser.Exam.NOV], 
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Biology (Core)',
                'code': '9204/BC',
                'mark': 100,
                'weighting': ('33⅓%', '33⅓%', None, None),
                'duration': '1 hour 45 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_51,

            },
            {
                'name': 'Paper 2: Chemistry (Core)',
                'code': '9204/CC',
                'mark': 100,
                'weighting': ('33⅓%', '33⅓%', None, None),
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_51,
            },
            {
                'name': 'Paper 3: Physics (Core)',
                'code': '9204/PC',
                'mark': 100,
                'weighting': ('33⅓%', '33⅓%', None, None),
                'duration': '1 hour 45 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_51,
            },
            {
                'name': 'Paper 1: Biology (Extension)',
                'code': '9204/BE',
                'mark': 100,
                'weighting': (None, None, '33⅓%', '33⅓%'),
                'duration': '1 hour 45 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_93,
            },
            {
                'name': 'Paper 2: Chemistry (Extension)',
                'code': '9204/CE',
                'mark': 100,
                'weighting': (None, None, '33⅓%', '33⅓%'),
                'duration': '1 hour 30 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_93,
            },
            {
                'name': 'Paper 3: Physics (Extension)',
                'code': '9204/PE',
                'mark': 100,
                'weighting': (None, None, '33⅓%', '33⅓%'),
                'duration': '1 hour 45 minutes',
                'internal': False,
                'grading': GS.GCSE_9.SINGLE_93,
            },
            {
                'name': 'IGCSE Plus: 2,000 word report',
                'code': '',
                'mark': 30,
                'weighting': (None, '-', None, '-'),
                'duration': '30 hours',
                'internal': False,
                'grading': GS.AGQ.SINGLE_DP,
            },
        ]
    },
    
    
]
