from django.db import models
from django.utils.safestring import mark_safe

class CheckpointScope(models.TextChoices):
    CLASS_LANDMARK = 'class_landmark', 'Subject Class Landmark'
    SUBJECT_BENCHMARK = 'subject_benchmark', 'Subject Benchmark'
    GENERAL_BENCHMARK = 'general_benchmark', 'General Benchmark'
    
    
class CheckpointFieldKind(models.TextChoices):
    CATEGORICAL = 'categorical', 'Categorical'
    COMMENT = 'comment', 'Comment'
    GRADE = 'grade', 'Grade'
    MARK = 'mark', 'Mark'
    MOCK = 'mock', 'Mock exam'
    PERCENTAGE = 'percentage', 'Percentage mark'
    
class CheckpointState(models.TextChoices):
    HIDDEN = 'hidden', 'HIDDEN',
    OPEN = 'open', 'OPEN', 
    PROTECTED = 'protected', 'PROTECTED', 
    
    @classmethod
    def detailed_choices(cls):
        """Return a list of choices with descriptions."""
        helptexts = {
            cls.HIDDEN: 'Users cannot view this checkpoint.',
            cls.OPEN: 'Users can view and enter data into this checkpoint.',
            cls.PROTECTED: 'Users can view this checkpoint but cannot make changes.',
        }
        icons = {
        cls.HIDDEN: mark_safe('<i class="fa-solid fa-eye-slash me-2"></i>'),  
        cls.OPEN: mark_safe('<i class="fa-solid fa-check me-2"></i>'),     
        cls.PROTECTED: mark_safe('<i class="fa-solid fa-lock me-2"></i>'),      
    }
        return [(c.value, c.label, helptexts[c], icons[c]) for c in cls]


class CheckpointEntryStatus(models.TextChoices):
    IP = 'ip', 'IN PROGRESS',
    DONE = 'done', 'DONE', 
    NR = 'nr', 'NOT REQUIRED', 