from subject_app.models import Programme, Board
from register_app.edusystem import QualificationType as QT 
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import ExamSeries as ES
from register_app.edusystem import SubjectGroup as SG
from register_app.edusystem import Tier
from register_app.edusystem import MarkType as MT

SUBJECTS = [
        {
        'name': 'CHINESE (Spoken Mandarin)',
        'code': ('8673F', '8673H'),
        'group': SG.British.LANGUAGES,
        'tier': (Tier.FOUNDATION, Tier.HIGHER),
        'qualification': QT.British.GCSE,
        'programme': Programme.British.GCSE,
        'board': Board.AQA,
        'first_assessment': 2018,
        'mark': (240, 240),
        'mark_type': MT.SCALED,
        'grading': (GS.GCSE_9.SINGLE_51, GS.GCSE_9.SINGLE_93), 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'CHINESE LISTENING TEST TIER F',
                'code': '8673/LF',
                'mark': 40,
                'mark_adjusted': 60,
                'mark_adjusted_type': MT.SCALED,
                'weighting': (25, None),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_51,
                'internal': False,
            },
            {
                'name': 'CHINESE LISTENING TEST TIER H',
                'code': '8673/LH',
                'mark': 50,
                'mark_type': MT.RAW,
                'mark_adjusted': 60,
                'mark_adjusted_type': MT.SCALED,
                'weighting': (None, 25),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_51,
                'internal': False,
            },
            {
                'name': 'CHINESE READING TEST TIER F',
                'code': '8673/RF',
                'mark': 60,
                'weighting': (25, None),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
                'eligible': (False, True),
                'internal': False,
            },
            {
                'name': 'CHINESE READING TEST TIER H',
                'code': '8673/RH',
                'mark': 60,
                'weighting': (None, 25),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
                'eligible': (False, True),
                'internal': False,
            },
            {
                'name': 'CHINESE SPEAKING TEST TIER F',
                'code': '8673/SF',
                'mark': 60,
                'mark_type': MT.RAW,
                'weighting': (25, None),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
            },
            {
                'name': 'CHINESE SPEAKING TEST TIER H',
                'code': '8673/SH',
                'mark': 90,
                'weighting': (None, 25),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
            },
            {
                'name': 'CHINESE WRITING TEST TIER F',
                'code': '8673/WF',
                'mark': 60,
                'weighting': (25, None),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
                'internal': False,
            },
            {
                'name': 'CHINESE WRITING TEST TIER H',
                'code': '8673/WH',
                'mark': 90,
                'weighting': (None, 25),
                'duration': '1 hour 45 minutes',
                'grading': GS.GCSE_9.SINGLE_93,
                'internal': False,
            },
            
        ]
    },
    {
        'name': 'HISTORY (all options)',
        'code': '8154 (AA-UM)',
        'group': SG.British.HUMANITIES,
        'qualification': QT.British.GCSE,
        'programme': Programme.British.GCSE,
        'board': Board.AQA,
        'first_assessment': 2018,
        'mark': 168,
        'mark_type': MT.RAW,
        'grading': GS.GCSE_9.SINGLE_91, 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: Understanding the modern world',
                'code': '8154/LF',
                'mark': 84,
                'weighting': 50,
                'duration': '2 hours',
                'grading': GS.GCSE_9.SINGLE_91,
                'internal': False,
            },
            {
                'name': 'Paper 2: Shaping the nation',
                'code': '8154/LH',
                'mark': 84,
                'weighting': 50,
                'duration': '2 hours',
                'grading': GS.GCSE_9.SINGLE_91,
                'internal': False,
            },

            
        ]
    },
]