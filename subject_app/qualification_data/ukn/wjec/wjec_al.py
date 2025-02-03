from subject_app.models import Programme, Board
from register_app.edusystem import QualificationType as QT 
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import ExamSeries as ES
from register_app.edusystem import SubjectGroup as SG

SUBJECTS = [
    {
        'name': 'BIOLOGY',
        'code': '',
        'group': SG.British.SCIENCES,
        'QT': (QT.British.AS, QT.British.A2),
        'programme': Programme.British.ALEVEL,
        'board': Board.WJEC,
        'first_assessment': 2019,
        'mark': 200,
        'grading': (GS.ALevel.SINGLE_AE, GS.ALevel.SINGLE_ASE), 
        'series': [ES.JUNE],
        'modular': False,
        'components': [
            {
                'name': 'AS Unit 1',
                'code': '',
                'mark': 80,
                'weighting': 20,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (True, True)
            },
            {
                'name': 'AS Unit 2',
                'code': '',
                'mark': 80,
                'weighting': 20,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (True, True)
            },
            {
                'name': 'AS Unit 2',
                'code': '',
                'mark': 80,
                'weighting': 20,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (False, True)
            },
            {
                'name': 'A2 Unit 3',
                'code': '',
                'mark': 90,
                'weighting': 25,
                'duration': '2 hours',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (False, True)
            },
            {
                'name': 'A2 Unit 4',
                'code': '',
                'mark': 90,
                'weighting': 25,
                'duration': '2 hours',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (False, True)
            },
            {
                'name': 'A2 Unit 5',
                'code': '',
                'mark': 50,
                'weighting': 10,
                'duration': '1 hour 30 minutes',
                'grading': GS.ALevel.SINGLE_AE,
                'internal': False,
                'eligible': (False, True)
            },

        ]
    }
]
