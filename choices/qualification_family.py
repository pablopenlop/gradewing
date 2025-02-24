from .qualification_tree import QualificationTree as QT
from .choices import ComplexChoices
from django.db import models
from .qualification_tree import Edusystem as Edu
from .yeargroups import YearGroupLevel as YL

class QualificationFamily(ComplexChoices):
    class IB(models.TextChoices):
        DP = 'ib.dp',    'IB Diploma Programme'
        CP = 'ib.cp',    'IB Career-related Programme'
        MYP = 'ib.myp',  'IB Middle Years Programme'
    class UKN(models.TextChoices):
        AL = 'ukn.al', 'GCE A levels'
        AAQ = 'ukn.aaq', 'Applied Academic Qualifications (AAQs)'
        AGQ3 = 'ukn.agq.l3', 'Level 3 Applied General (Vocational Technical) Qualifications'
        EPQ = 'ukn.epq', 'Level 3 Extended Project Qualifications'
        GCSE = 'ukn.gcse', 'GCSEs'
        VTQ2 = 'ukn.vtq.l12', 'Level 1/2 Vocational Technical Qualifications'
        PQ12 = 'ukn.pq.l12', 'Level 1/2 Project Qualifications'
          
    class UKI(models.TextChoices):
        IAL = 'uki.ial', 'International A levels'
        BTECI3 = 'uki.btec.il3', 'BTEC International Level 3'
        IPQ = 'uki.ipq', 'International Project Qualifications'
        IGCSE = 'uki.igcse', 'IGCSEs'
        OLEVEL = 'uki.olevel', 'O Levels'
        BTECI2 = 'uki.btec.il2', 'BTEC International Level 2'
        
    
    @classmethod
    def count(cls):
        return len(cls.choices())
        
    @classmethod
    def grouped_choices(cls):
        return [
            ("UK National", list(cls.UKN.choices)),
            ("UK International", list(cls.UKI.choices)),
            ("IB", list(cls.IB.choices)),
        ]
    
    @classmethod
    def get_edusystem_from_choice(cls, family):
        PREFIX_2_SYSTEM = {
        'ukn': Edu.UKN,
        'uki': Edu.UKI,
        'ib':  Edu.IB,
        }
        prefix = family.value.split('.')[0]
        return PREFIX_2_SYSTEM.get(prefix, "")
    
    @classmethod
    def available_grouped_choices(cls, existing_choices: list[str]):
        all_choices = cls.grouped_choices() 
        available_choices = []
        for group, choices in all_choices:
            filtered_choices = [
                (value, label) for value, label in choices 
                if value not in existing_choices
            ]
            if filtered_choices:
                available_choices.append((group, filtered_choices))

        return available_choices
    
    
    MANDATORY_QN_MAP = {
        IB.DP: {QT.IB.IBO.DP.CORE, QT.IB.IBO.DP.AGG},
        IB.CP: {QT.IB.IBO.CP.CORE}
    }
    @classmethod
    def get_core_qualification_names(cls, family):
        return cls.MANDATORY_QN_MAP.get(family, {QT.NONE.NONE})
    

    @classmethod
    def get_suite_classes(cls, family):
        return cls.FAM_2_SUITECLASS.get(family, None)
    
    @classmethod
    def compatible_yeargroup_levels(cls, family):
        return cls.FAM_2_YGLEVEL.get(family, None)
    
    @classmethod
    def get_qualification_name_choices(cls, family, values_only=False):
        suites = cls.get_suite_classes(family)
        choices = []
        for suite in suites:
            choices = choices + QT.choices_from_suite_class(suite, values_only)
        return choices

    FAM_2_SUITECLASS = {
        UKN.AL: {
            QT.UKN.Edexcel.AL,
            QT.UKN.OCR.AL,
            QT.UKN.AQA.AL,
            QT.UKN.Eduqas.AL,
            QT.UKN.WJEC.AL,
        },
        UKN.GCSE: {
            QT.UKN.Edexcel.GCSE,
            QT.UKN.OCR.GCSE,
            QT.UKN.AQA.GCSE,
            QT.UKN.Eduqas.GCSE,
            QT.UKN.WJEC.GCSE,
        },
        UKN.PQ12: {
            QT.UKN.Edexcel.PQ12,
            QT.UKN.AQA.PQ12,
        },
        UKN.AAQ: {
            QT.UKN.BTEC.AAQ,
            QT.UKN.OCR.AAQ,
            QT.UKN.WJEC.AAQ,
            
        },
        UKN.VTQ2: {
            QT.UKN.BTEC.FIRST,
            QT.UKN.OCR.NAT,
            QT.UKN.WJEC.VA,
        },
        UKN.AGQ3: {
            QT.UKN.BTEC.NAT,
            QT.UKN.OCR.TECH,
            QT.UKN.AQA.AG,
        },
        UKN.EPQ: {
            QT.UKN.Edexcel.EPQ,
            QT.UKN.AQA.EPQ,
            QT.UKN.Eduqas.EPQ,
            QT.UKN.OCR.EPQ,
            QT.UKN.WJEC.EPQ,
        },
        UKI.IAL: {
            QT.UKI.Edexcel.IAL,
            QT.UKI.CIE.IAL,
            QT.UKI.OxfordAQA.IAL,
        },
        UKI.IGCSE: {
            QT.UKI.Edexcel.IGCSE,
            QT.UKI.CIE.IGCSE,
            QT.UKI.CIE.IGCSE,
            QT.UKI.OxfordAQA.IGCSE,
        },
        UKI.OLEVEL: {
            QT.UKI.CIE.OL,
        },
        UKI.BTECI2: {
            QT.UKI.BTEC.IL2,
        },
        UKI.BTECI3: {
            QT.UKI.BTEC.IL3,
        },
        UKI.IPQ: {
            QT.UKI.CIE.IPQ,
            QT.UKI.OxfordAQA.EPQ,
        },
        IB.MYP: {
            QT.IB.IBO.MYP,
        },
        IB.DP: {
            QT.IB.IBO.DP,
        },
        IB.CP: {
            QT.IB.IBO.CP,
            QT.IB.IBO.DP,

        }
    }
    
    FAM_2_YGLEVEL = {
         UKN.AL: {
            YL.YG0, YL.YG1, 
        },
        UKN.GCSE: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKN.PQ12: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKN.AAQ: {
            YL.YG0, YL.YG1, 
        },
        UKN.VTQ2: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKN.AGQ3: {
            YL.YG0, YL.YG1, 
        },
        UKN.EPQ: {
            YL.YG0, YL.YG1, 
        },
        UKI.IAL: {
            YL.YG0, YL.YG1, 
        },
        UKI.IGCSE: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKI.OLEVEL: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKI.BTECI2: {
            YL.YG2, YL.YG3, YL.YG4,
        },
        UKI.BTECI3: {
            YL.YG0, YL.YG1, 
        },
        UKI.IPQ: {
            YL.YG0, YL.YG1, 
        },
        IB.MYP: {
            YL.YG2, YL.YG3, YL.YG4, YL.YG5, YL.YG6, 
        },
        IB.DP: {
            YL.YG0, YL.YG1, 
        },
         IB.CP: {
            YL.YG0, YL.YG1, 
        },
    }

