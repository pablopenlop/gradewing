from subject_app.models import Programme, Board
from register_app.edusystem import QualificationType as QT 
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import ExamSeries as ES
from register_app.edusystem import SubjectGroup as SG
from register_app.edusystem import MarkType as MT
## 34 SUBJECTS

SUBJECTS = [
    {
        'name': 'CLASSICAL CIVILISATION',
        'code': 'H008',
        'group': SG.British.HUMANITIES,
        'qualification': QT.British.AS,
        'programme': Programme.British.ALEVEL,
        'board': Board.OCR,
        'first_assessment': 2018,
        'mark': 250,
        'mark_type': MT.SCALED,
        'grading': GS.ALevel.SINGLE_AE, 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'The World of the Hero',
                'code': 'H008/11',
                'mark': 65,
                'weighting': 50,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': 'Greek Theatre',
                'code': 'H008/21',
                'mark': 65,
                'weighting': 50,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': 'Imperial Image',
                'code': 'H008/22',
                'mark': 65,
                'weighting': 50,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
        ]
    },
    {
        'name': 'FURTHER MATHEMATICS B (MEI)',
        'code': 'H635',
        'group': SG.British.MATHS,
        'qualification': QT.British.AS,
        'programme': Programme.British.ALEVEL,
        'board': Board.OCR,
        'first_assessment': 2018,
        'mark': 180,
        'mark_type': MT.SCALED,
        'grading': GS.ALevel.SINGLE_AE, 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'Core Pure',
                'code': 'Y410',
                'mark': 60,
                'weighting': 33.3,
                'duration': '1 hour 15 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': ' Mechanics a',
                'code': 'Y411',
                'mark': 60,
                'weighting': 33.3,
                'duration': '1 hour 15 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': 'Statistics a',
                'code': 'Y412',
                'mark': 60,
                'weighting': 33.3,
                'duration': '1 hour 15 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': 'Modelling with Algorithms',
                'code': 'Y413',
                'mark': 60,
                'weighting': 33.3,
                'duration': '1 hour 15 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
            {
                'name': 'Numerical Methods',
                'code': 'Y414',
                'mark': 60,
                'weighting': 33.3,
                'duration': '1 hour 15 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
            },
        ]
    },
]