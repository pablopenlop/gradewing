
from django.db import models
from .choices import ComplexChoices

class MarkType(models.TextChoices):
    RAW = "raw", "Raw mark"
    UMS = 'ums', 'UMS mark'
    NONE = 'none', ''
    PUM = 'pum', 'PUM'
    SCALED = 'scaled', 'Scaled mark'
    POINTS = 'points', 'Points'


class Gradeset(ComplexChoices):
    class AL(models.TextChoices):
        SINGLE_ASE = 'ol-A*-E',  'A* A B C D E U'
        SINGLE_AE = 'ol-A-E',  'A B C D E (U)'
    class GCSE_9(models.TextChoices):
        SINGLE_91 = 'gcse-9-1', '9 8 7 6 5 4 3 2 1 U'
        SINGLE_93 = 'gcse-9-3', '9 8 7 6 5 4 3 (U)'
        SINGLE_94 = 'gcse-9-4', '9 8 7 6 5 4 (U)'
        SINGLE_51 = 'gcse-5-1', '5 4 3 2 1 (U)'
        SINGLE_41 = 'gcse-4-1', '4 3 2 1 (U)'
        DOUBLE_91 = 'gcse-99-11','9-9 9-8 8-8 8-7 7-7 7-6 6-6 6-5 5-5 5-4 4-4 4-3 3-3 3-2 2-2 2-1 1-1 U'
        DOUBLE_51 = 'gcse-55-11','5-5 5-4 ...  1-1 U'
        DOUBLE_93 = 'gcse-99-33','5-5 5-4 ... 1-1 U'
        DOUBLE_943 = 'gcse-99-43','9-9 9-8 ... 4-3 U'
        DOUBLE_PAIRED_91 = 'gcse-9p-1p', '9-9 8-8 ... 1-1 U'
        DOUBLE_PAIRED_51 = 'gcse-5p-1p', '5-5 4-4 ... 1-1 U'
        DOUBLE_PAIRED_41 = 'gcse-4p-1p', '4-4 3-3 ... 1-1 U'
        DOUBLE_PAIRED_93 = 'gcse-9p-3p', '9-9 8-8 ... 3-3 U'
        DOUBLE_PAIRED_94 = 'gcse-9p-4p', '9-9 8-8 ... 4-4 U'
    class GCSE_A(models.TextChoices):
        SINGLE_ASG = 'gcse-A*-G', 'A* A B C D E F G (U)'
        SINGLE_AG = 'gcse-A-G', 'A B C D E F G (U)'
        SINGLE_ASE = 'gcse-A*-E', 'A* A B C D E (U)'
        SINGLE_AE = 'gcse-A-E', 'A B C D E (U)'
        SINGLE_CG = 'gcse-C-G', 'C D E F G (U)'
        DOUBLE_PAIRED_ASG = 'gcse-A*A*-GG', 'A*-A* A-A ... G-G (U)'
        DOUBLE_PAIRED_AG = 'gcse-AA-GG', 'A-A ... G-G (U)'
        DOUBLE_PAIRED_CG = 'gcse-CC-GG', 'C-C D-D ... G-G (U)'
        DOUBLE_PAIRED_EXT = 'gcse-A*A*-EE', 'A*-A* A-A ... E-E (U)'
    class IB(models.TextChoices):
        SINGLE_71 = 'ib-7-1', '7 6 5 4 3 2 1 (N)'
        SINGLE_AE = 'ib-A-E', 'A B C D E (N)'
    class AGQ(models.TextChoices):
        SINGLE_DP = 'agq.D-P', 'D M P (U)'
        SINGLE_DN = 'agq.D-N', 'D M P N (U)'
        SINGLE_DSP = 'agq.D*-P', 'D* D M P (U)'
        DOUBLE_DSP = 'agq.D*D*-PP', 'D*D* D*D ... PP (U)'
        TRIPLE_DSP = 'agq.D*D*D*-PPP', 'D*D*D* DDD ... PPP (U)'
    class VTQ2(models.TextChoices):
        SINGLE_2D1 = 'vtq2.L2D-L1', 'L2-D L2-M L2-P L1 (U)'
        SINGLE_2DS1 = 'vtq2.L2D*-L1', 'L2-D* L2-D L2-M L2-P L1 (U)'

    @classmethod
    def grade_tuples(cls, grade_choice) -> list[tuple[str, str]]:
        if not isinstance(grade_choice, models.TextChoices):
            grade_choice= cls.choices_from_values(grade_choice)[0]
            
        label = grade_choice.label
        if grade_choice == Gradeset.NONE.NAP:
            return [(label, label)]
        
        
        grade_list = label.split()
        grade_tuples = [(grade, grade) for grade in grade_list]
        
        return grade_tuples


    @classmethod
    def grouped_choices(cls):
        choices =  [
            ("A levels & O levels", list(cls.AL.choices)),
            ("GCSE (9-1)", list(cls.GCSE_9.choices)),
            ("GCSE (A*-G)", list(cls.GCSE_A.choices)),
            ("IB", list(cls.IB.choices)),
            ("N/A", list(cls.NONE.choices)),
        ]
        return choices
