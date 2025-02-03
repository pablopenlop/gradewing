from enum import Enum

class ExamResultState(Enum):
    FINAL = 'FINAL'
    PROVISIONAL = 'PROVISIONAL'
    OVERRIDEN = 'OVERRIDEN'
    
class QualificationState(Enum):
    AWARDED = 'AWARDED'
    PROVISIONAL = 'PROVISIONAL'
    PENDING = 'PENDING'
