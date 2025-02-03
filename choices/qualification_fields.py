from django.db import models
from .choices import ComplexChoices
class Tier(models.TextChoices):
    NONE = 'none', '-' 
    CORE = 'core', 'Core / Foundation Tier'
    EXTENDED = 'extended', 'Extended / Higher Tier'

  
class Month(models.TextChoices):
    JAN = 'm.01', 'January'
    FEB = 'm.02', 'February'
    MAR = 'm.03', 'March'
    APR = 'm.04', 'April'
    MAY = 'm.05', 'May'
    JUN = 'm.06', 'June'
    SEP = 'm.09', 'September'
    OCT = 'm.10', 'October'
    NOV = 'm.11', 'November'
    DEC = 'm.12', 'December'

class Series(ComplexChoices):
    class Exam(models.TextChoices):
        JAN = Month.JAN.value, Month.JAN.label
        FEB = Month.FEB.value, Month.FEB.label
        MAR = Month.MAR.value, Month.MAR.label
        MAY = Month.MAY.value, Month.MAY.label
        MAYJUN = 'm.05/06', 'May/June'
        JUN = Month.JUN.value, Month.JUN.label
        OCT = Month.OCT.value, Month.OCT.label
        NOV = Month.NOV.value, Month.NOV.label
    class Flex(models.TextChoices):
        ALL = "m.all", "Flexible Timing"

    @classmethod
    def entry_choices(cls):
        choices = cls.Exam.choices + Month.choices
        return sorted(set(choices), key=lambda x: x[0])

    
    @classmethod
    def is_june_series(cls, choice)->bool:
        june_series= Series.Exam.MAYJUN | Series.Exam.MAY | Series.Exam.JUN
        return choice in june_series





