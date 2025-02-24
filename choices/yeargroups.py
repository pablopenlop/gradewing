from django.db import models


class YearGroupLevel(models.TextChoices):
    YG6 = 'ygl.7', '7th to last year'
    YG5 = 'ygl.6', '6th to last year'
    YG4 = 'ygl.5', '5th to last year'
    YG3 = 'ygl.4', '4th to last year'
    YG2 = 'ygl.3', '3rd to last year'
    YG1 = 'ygl.2', '2nd to last year'
    YG0 = 'ygl.1', 'Final year'
    

class YearGroupSystem(models.TextChoices):
    UK = 'ygs.uk', 'UK'
    US = 'ygs.us', 'US'
    IB = 'ygs.ib', 'IB'
    CUSTOM = 'ygs.custom', 'Custom'
    DEFAULT = 'ygs.def', 'Default'


class YearGroupManager:
    NAME_MAPPINGS = {
        YearGroupLevel.YG6: {
            YearGroupSystem.UK: 'Year 7',
            YearGroupSystem.US: 'Grade 6',
            YearGroupSystem.IB: 'MYP Year 1',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG6.label,
        },
        YearGroupLevel.YG5: {
            YearGroupSystem.UK: 'Year 8',
            YearGroupSystem.US: 'Grade 7',
            YearGroupSystem.IB: 'MYP Year 2',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG5.label,
        },
        YearGroupLevel.YG4: {
            YearGroupSystem.UK: 'Year 9',
            YearGroupSystem.US: 'Grade 8',
            YearGroupSystem.IB: 'MYP Year 3',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG4.label,
        },
        YearGroupLevel.YG3: {
            YearGroupSystem.UK: 'Year 10',
            YearGroupSystem.US: 'Grade 9',
            YearGroupSystem.IB: 'MYP Year 4',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG3.label,
        },
        YearGroupLevel.YG2: {
            YearGroupSystem.UK: 'Year 11',
            YearGroupSystem.US: 'Grade 10',
            YearGroupSystem.IB: 'MYP Year 5',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG2.label,
        },
        YearGroupLevel.YG1: {
            YearGroupSystem.UK: 'Year 12',
            YearGroupSystem.US: 'Grade 11',
            YearGroupSystem.IB: 'IB Year 1',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG1.label,
        },
        YearGroupLevel.YG0: {
            YearGroupSystem.UK: 'Year 13',
            YearGroupSystem.US: 'Grade 12',
            YearGroupSystem.IB: 'IB Year 2',
            YearGroupSystem.DEFAULT: YearGroupLevel.YG0.label,
        },
    }

    @classmethod
    def custom_names(cls, school, level=None):
        return school.yeargroups.values_list('custom_name', flat=True)
    

    @classmethod
    def names(cls, system, level=None):
        if level:
            return cls.NAME_MAPPINGS[level][system]
        return [names[system] for names in cls.NAME_MAPPINGS.values()]
    
    @staticmethod
    def levels(level=None):
        if level:
            return ''.join(filter(str.isdigit, level))
        return  [str(i) for i in range(7, 0, -1)]

