from subject_app.models import Programme, Board
from register_app.edusystem import QualificationType as QT 
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import ExamSeries as ES
from register_app.edusystem import SubjectGroup as SG
from register_app.edusystem import MarkType as MT

SUBJECTS = [
    {
        'name': 'COMPUTER SCIENCE',
        'code': '7516(A-E)',
        'group': SG.British.PROFESSIONAL,
        'qualification': QT.British.AS,
        'programme': Programme.British.ALEVEL,
        'board': Board.AQA,
        'first_assessment': 2016,
        'mark': 150,
        'mark_type': MT.SCALED,
        'grading': GS.ALevel.SINGLE_AE, 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'Paper 1: On-screen',
                'code': '7516/1(A-E)',
                'mark': 75,
                'weighting': 50,
                'duration': '1 hour 45 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': True,
            },
            {
                'name': 'Paper 2: Written exam',
                'code': '7516/2',
                'mark': 75,
                'weighting': 50,
                'duration': '1 hour 45 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': True,
            },
            
        ]
    },
]
    