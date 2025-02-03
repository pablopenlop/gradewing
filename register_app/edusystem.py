from django.db import models
from abc import ABC
from typing import Union

class ComplexChoices(ABC):
    class NAN(models.TextChoices):
        UNDEFINED = 'nan.undefined', 'Other'
        NONE = 'nan.none', 'None'

    @classmethod
    def choices(cls):
        def extract_choices(inner_class):
            choices_list = []
            for name, obj in vars(inner_class).items():
                if isinstance(obj, type) and issubclass(obj, models.TextChoices):
                    choices_list.extend(obj.choices)
                elif isinstance(obj, type):
                    choices_list.extend(extract_choices(obj))
            return choices_list
        return extract_choices(cls)
    
    @classmethod
    def choices_from_values(cls, codes: Union[str, list[str]]) -> list:
        result = []
        choices_classes = [
            subclass for name, subclass in cls.__dict__.items() 
            if isinstance(subclass, type) and issubclass(subclass, models.TextChoices)
        ]
        if isinstance(codes, str):
            codes = [codes]
        for code in codes:
            found = False
            for choices_class in choices_classes:
                for choice in choices_class:
                    if choice.value == code:
                        result.append(choice)
                        found = True
                        break
                if found:
                    break
        return result
    


class Board(models.TextChoices):
    UNDEFINED = "undefined", "Undefined"
    EDEXCEL = 'edexcel', 'Pearson Edexcel'
    BTEC = 'btec', 'Pearson BTEC'
    CIE = 'cie', 'Cambridge International'
    OXFORD_AQA = 'oxfordaqa', 'OxfordAQA'
    AQA = 'aqa', 'AQA'
    IB = 'ib', 'IB'
    OCR = 'ocr', 'OCR'
    WJEC = 'wjec', 'WJEC'
    EDUQAS = 'eduqas', 'WJEC Eduqas'

class MarkType(models.TextChoices):
    RAW = "raw", "raw"
    UMS = 'ums', 'UMS'
    NONE = 'none', ''
    PUM = 'pum', 'PUM'
    SCALED = 'scaled', 'scaled'
    POINTS = 'points', 'points'


class GradingScale(ComplexChoices):
    class AL(models.TextChoices):
        SINGLE_ASE = 'ol-A*-E',  'A* A B C D E (U)'
        SINGLE_AE = 'ol-A-E',  'A B C D E (U)'
    class GCSE_9(models.TextChoices):
        SINGLE_91 = 'gcse-9-1', '9 8 7 6 5 4 3 2 1 (U)'
        SINGLE_93 = 'gcse-9-3', '9 8 7 6 5 4 3 (U)'
        SINGLE_94 = 'gcse-9-4', '9 8 7 6 5 4 (U)'
        SINGLE_51 = 'gcse-5-1', '5 4 3 2 1 (U)'
        SINGLE_41 = 'gcse-4-1', '5 4 3 2 1 (U)'
        DOUBLE_91 = 'gcse-99-11','9-9 9-8 ... 1-1 (U)'
        DOUBLE_51 = 'gcse-55-11','5-5 5-4 ...  1-1 (U)'
        DOUBLE_93 = 'gcse-99-33','5-5 5-4 ... 1-1 (U)'
        DOUBLE_943 = 'gcse-99-43','9-9 9-8 ... 4-3 (U)'
        DOUBLE_PAIRED_91 = 'gcse-9p-1p', '9-9 8-8 ... 1-1 (U)'
        DOUBLE_PAIRED_51 = 'gcse-5p-1p', '5-5 4-4 ... 1-1 (U)'
        DOUBLE_PAIRED_41 = 'gcse-4p-1p', '4-4 3-3 ... 1-1 (U)'
        DOUBLE_PAIRED_93 = 'gcse-9p-3p', '9-9 8-8 ... 3-3 (U)'
        DOUBLE_PAIRED_94 = 'gcse-9p-4p', '9-9 8-8 ... 4-4 (U)'
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
        SINGLE_DSP = 'agq.D*-P', 'D* D M P (U)'
        DOUBLE_DSP = 'agq.D*D*-PP', 'D*D* D*D ... PP (U)'
        TRIPLE_DSP = 'agq.D*D*D*-PPP', 'D*D*D* D*D*D ... PPP (U)'
    @classmethod
    def grouped_choices(cls):
        choices =  [
            ("A levels & O levels", list(cls.AL.choices)),
            ("GCSE (9-1)", list(cls.GCSE_9.choices)),
            ("GCSE (A*-G)", list(cls.GCSE_A.choices)),
            ("IB", list(cls.IB.choices)),
            ("N/A", list(cls.NAN.choices)),
        ]
        return choices

    
class Tier(models.TextChoices):
    NONE = 'none', '-' 
    CORE = 'core', 'Core'
    FOUNDATION = 'foundation', 'Foundation Tier'
    EXTENDED = 'extended', 'Extended'
    EXTENSION = 'extension', 'Extension'
    HIGHER = 'higher', 'Higher Tier'

    @classmethod
    def core(cls):
        return [cls.CORE, cls.FOUNDATION]
    @classmethod
    def extended(cls):
        return [cls.CORE, cls.FOUNDATION]

class Series(ComplexChoices):
    class Exam(models.TextChoices):
        JANUARY = 'january', 'January'
        MARCH = 'march', 'March'
        MAY = 'may', 'May'
        MAY_JUNE = 'may_june', 'May/June'
        JUNE = 'june', 'June'
        NOVEMBER = 'november', 'November'

    def is_june_series(self, cls)->bool:
        june_series= Series.Exam.MAY_JUNE | Series.Exam.MAY | Series.Exam.JUNE
        return self in june_series
    


class SubjectGroup(ComplexChoices):
    class IB:
        class DP(models.TextChoices):
            LAL = "ib.g1.lal", "Group 1. Studies in Language and Literature"
            LA = "ib.g2.la", "Group 2. Language Acquisition"
            INDIV_SOC = "ib.g3.indiv", "Group 3. Individuals & Societies"
            SCIENCES = "ib.g4.science", "Group 4. Sciences"
            MATHS = "ib.g5.maths", "Group 5. Mathematics"
            ARTS = "ib.g6.arts", "Group 6.  The Arts"
            INTER = "ib.g7.inter", "Interdisciplinary"
            CORE = "ib.g0.dpcore", "DP Core"
        class CP(models.TextChoices):
            CORE = "ib_cpcore", "CP Core"
        class MYP(models.TextChoices):
            LA = "ib_myp_la", "Language Acquisition"
            LAL = "ib_myp_lal", "Language & Literature"
            INDIVIDUALS = "ib_myp_ind", "Individuals & Societies"
            MATHS = "ib_myp_maths", "Mathematics"
            SCIENCES = "ib_myp_science", "Sciences"
            ARTS = "ib_myp_arts", "Arts"
            PHE = "ib_myp_phe", "Physical & Health Education"
            DESIGN = "ib_myp_design", "Design"
            INTER = "ib_myp_inter", "Interdisciplinary"
            PROJECT = "ib_myp_project", "Personal Project"

    class UK(models.TextChoices):
        PROFESSIONAL = "uk_prof", "Creative and professional"
        ENGLISH = "uk_english", "English language and literature"
        HUMANITIES = "uk_humanities", "Humanities and social sciences"
        LANGUAGES = "uk_languages", "Languages"
        MATHS = "uk_sicences", "Mathematics"
        SCIENCES = "uk_maths", "Sciences"
        HEALTH = "uk_sh", "Sport & Health"
        ICT = "business", "ICT & Computing"
        PROJECT = "uk_project", "Project"

        
    @classmethod
    def grouped_choices(cls):
        choices =  [
            ("UK", list(cls.UK.choices)),
            ("IB DP & IB CP", list(cls.IB.DP.choices)),
            ("IB MYP", list(cls.IB.MYP.choices)),
        ]
        return choices
    

class QualificationKind(ComplexChoices):
    class UKN:
        class AL(models.TextChoices):
            A2 = 'ukn.al.a2', 'A level'
            AS = 'ukn.al.as', 'AS level'
        class GCSE(models.TextChoices):
            GCSE = 'ukn.gcse', 'GCSE'
            GCSE_DOUBLE = 'ukn.gcse.double', 'GCSE Double Award'
        class AAQ(models.TextChoices):
            CERT = 'ukn.aaq.cert', 'Certificate'
            CERT_EXT = 'ukn.aaq.ext_cert', 'Extended Certificate'
            @classmethod
            def premodifier(cls):
                return "Small AAQ"
        class PQ(models.TextChoices):
            L1 = 'ukn.pq.l1', 'Level 1 Foundation Project Qualification'
            L2 = 'ukn.pq.l2', 'Level 2 Higher Project Qualification'
            L3 = 'ukn.pq.l3', 'Level 3 Extended Project Qualification'
        class AGQ3(models.TextChoices):
            CERT = 'ukn.agq.l3.cert', 'Certificate'
            CERT_EXT = 'ukn.agq.l3.cert_ext', 'Extended Certificate'
            DIP_FDN = 'ukn.agq.l3.dip_f', 'Foundation Diploma'
            DIP = 'ukn.agq.l3.dip', 'Diploma'
            DIP_EXT = 'ukn.agq.l3.dip_ext', 'Extended Diploma'
            @classmethod
            def premodifier(cls):
                return "Level 3 Applied"
        class AGQ2(models.TextChoices):
            AWARD = 'ukn.agq2.award', 'Award'
            CERT = 'ukn.agq2.cert', 'Certificate'
            EXT_CERT = 'ukn.agq2.cert_ext', 'Extended Certificate'
            DIPLOMA = 'ukn.agq2.dip', 'Diploma'
            @classmethod
            def premodifier(cls):
                return "Level 2 Applied"    
    class UKI:
        class IAL(models.TextChoices):
            A2 = 'uki.ial.a2', 'International A level'
            AS = 'uki.ial.as', 'International AS level'
        class IGCSE(models.TextChoices):
            IGCSE = 'uki.igcse', 'International GCSE'
            IGCSE_DOUBLE = 'uki.igcse.double', 'International GCSE (Double Award)'
        class OLevel(models.TextChoices):
            OLEVEL = 'uki.ol', 'O level'
        class IPQ(models.TextChoices):
            EPQ = 'uki.ipq.epq', 'International EPQ'
        class BTEC3(models.TextChoices):
            CERT = 'uki.bteci3.cert', 'Certificate'
            DIP_SUB = 'uki.bteci.l3.sub_dip', 'Subsidiary Diploma'
            DIP_FDN = 'uki.bteci.l3.fdn_dip', 'Foundation Diploma'
            DIP = 'uki.bteci.l3.dip', 'Diploma'
            DIP_EXT = 'uki.bteci.l3.ext_cert', 'Extended Diploma'
            @classmethod
            def premodifier(cls):
                return "BTEC International Level 3"
        class BTEC2(models.TextChoices):
            AWARD = 'uki.bteci.l2.award', 'Award'
            CERT = 'uki.bteci.l2.cert', 'Certificate'
            EXT_CERT = 'uki.bteci.l2.cert_ext', 'Extended Certificate'
            DIPLOMA = 'uki.bteci.l2.dip', 'Diploma'
            @classmethod
            def premodifier(cls):
                return "BTEC International Level 2"
    class IB:
        class MYP(models.TextChoices):
            MYP = 'ib.myp',  'MYP'
        class DP(models.TextChoices):
            HL = 'ib.dp.hl', 'DP HL'
            SL = 'ib.dp.sl', 'DP SL'
            CORE = 'ib.dp.core', 'DP Core'
        class CP(models.TextChoices):
            CORE = 'ib.cp.core', 'CP Core'
   
class QualificationName(ComplexChoices):
    class UKN:
        class Edexcel(models.TextChoices):
            A2 = 'ukn.edexcel.a2', 'Pearson Edexcel Level 3 Advanced GCE'
            AS = 'ukn.edexcel.as', 'Pearson Edexcel Level 3 Advanced Subsidiary GCE'
            GCSE = 'ukn.edexcel.gcse', 'Pearson Edexcel Level 1/2 GCSE (9-1)'
            FPQ = 'ukn.edexcel.fpq', 'Pearson Edexcel Level 1 Foundation Project Qualification'
            HPQ = 'ukn.edexcel.hpq', 'Pearson Edexcel Level 2 Higher Project Qualification'
            EPQ = 'ukn.edexcel.epq', 'Pearson Edexcel Level 3 Extended Project Qualification'
        class OCR(models.TextChoices):
            A2 = 'ukn.ocr.a2', 'OCR Level 3 Advanced GCE'
            AS = 'ukn.ocr.as', 'OCR Level 3 Advanced Subsidiary GCE'
            GCSE = 'ukn.ocr.gcse', 'Pearson Edexcel Level 1/2 GCSE (9-1)'
            AAQ = 'ukn.ocr.aaq', 'OCR Level 3 AAQ Cambridge Advanced National'
            TECH = 'ukn.ocr.tech.l3', 'OCR Level 3 Cambridge Technical'
            NAT = 'ukn.ocr.nat', 'OCR Level 1/2 Cambridge National'
            EPQ = 'ukn.ocr.epq', 'OCR Level 3 Extended Project Qualification'
        class AQA(models.TextChoices):
            A2 = 'ukn.aqa.a2', 'AQA Level 3 Advanced GCE'
            AS = 'ukn.aqa.as', 'AQA Level 3 Advanced Subsidiary GCE'
            GCSE = 'ukn.aqa.gcse', 'AQA Level 1/2 GCSE (9-1)'
            APPL = 'ukn.aqa.appl', 'AQA Level 3 Applied'
            FPQ = 'ukn.aqa.fpq', 'AQA Level 1 Foundation Project Qualification'
            HPQ = 'ukn.aqa.hpq', 'AQA Level 2 Higher Project Qualification'
            EPQ = 'ukn.aqa.epq', 'AQA Level 3 Extended Project Qualification'
        class Eduqas(models.TextChoices):
            A2 = 'ukn.eduqas.a2', 'WJEC Eduqas Level 3 Advanced GCE'
            AS = 'ukn.eduqas.as', 'WJEC Eduqas Level 3 Advanced Subsidiary GCE'
            GCSE = 'ukn.eduqas.gcse', 'WJEC Eduqas Level 1/2 GCSE (9-1)'
            EPQ = 'ukn.eduqas.epq', 'WJEC Eduqas Level 3 Extended Project Qualification'
        class WJEC(models.TextChoices):
            A2 = 'ukn.al.wjec.a2', 'WJEC Level 3 Advanced GCE'
            AS = 'ukn.al.wjec.as', 'WJEC Level 3 Advanced Subsidiary GCE'
            GCSE = 'ukn.wjec.gcse', 'WJEC Level 1/2 GCSE (9-1)'
            VOC = 'ukn.wjec.voc', 'WJEC Vocational Level 1/2'
            APPL = 'ukn.wjec.appl', 'WJEC Level 3 Applied'
            EPQ = 'ukn.wjec.epq', 'WJEC Level 3 Extended Project Qualification'
            AAQ = 'ukn.wjec.aaq', 'WJEC Level 3 AAQ'

        class BTEC(models.TextChoices):
            AAQ = 'ukn.btec.aaq', 'Pearson Level 3 AAQ BTEC National'
            NAT = 'ukn.btec.nat', 'Pearson BTEC Level 3 National'
            FIRST = 'ukn.btec.first', 'Pearson BTEC Level 1/2 First'

        class IBO(models.TextChoices):
            AAQ_SL = 'ukn.ibo.aaq.sl', 'IBO Level 3 AAQ SL'
            AAQ_HL = 'ukn.ibo.aaq.hl', 'IBO Level 3 AAQ HL'

    class UKI:
        class Edexcel(models.TextChoices):
            A2 = 'uki.edexcel.ia2', 'Pearson Edexcel International A level'
            AS = 'uki.edexcel.ias', 'Pearson Edexcel International AS level'
            IGCSE = 'uki.edexcel.igcse', 'Pearson Edexcel International GCSE (9-1)'
        class CIE(models.TextChoices):
            A2 = 'uki.cie.ia2', 'Cambridge International A level'
            AS = 'uki.cie.ias', 'Cambridge International AS level'
            IGCSE_G9 = 'uki.cie.igcse.g9', 'Cambridge IGCSE (9-1)'
            IGCSE_GA = 'uki.cie.igcse.ga', 'Cambridge IGCSE'
            OL = 'uki.cie.ol', 'Cambridge O level'
            IPQ = 'uki.cie.ipq', 'Cambridge International Project Qualification'

        class OxfordAQA(models.TextChoices):
            A2 = 'uki.oxfordaqa.ia2', 'OxfordAQA International A level'
            AS = 'uki.oxfordaqa.ias', 'OxfordAQA International AS level'
            IGCSE = 'uki.oxfordaqa.igcse.g9', 'OxfordAQA IGCSE (9-1)'
            EPQ = 'uki.oxfordaqa.epq', 'OxfordAQA International Extended Project Qualification'
            IGCSE_PLUS = 'uki.oxfordaqa.igcse+', 'OxfordAQA International GCSE Plus'

        class BTEC(models.TextChoices):
            L2 = 'uki.bteci.l2', 'Pearson BTEC International Level 2'
            L3 = 'uki.bteci.l3', 'Pearson BTEC International Level 3'
    class IB:
        class MYP(models.TextChoices):
            MYP = 'ib.myp',  'IB MYP'
        class DP(models.TextChoices):
            HL = 'ib.dp.hl', 'IB DP HL'
            SL = 'ib.dp.sl', 'IB DP SL'
            CORE = 'ib.dp.core', 'IB DP'
        class CP(models.TextChoices):
            CORE = 'ib.cp.core', 'IB CP'
    

class QualificationSuite(ComplexChoices):
    class IB(models.TextChoices):
        DP = 'ib.dp',    'IB Diploma Programme'
        CP = 'ib.cp',    'IB Career-related Programme'
        MYP = 'ib.myp',  'IB Middle Years Programme'
        
    class UKN(models.TextChoices):
        AL = 'ukn.al', 'AS & A levels'
        AAQ = 'ukn.aaq', 'Applied Academic Qualifications (AAQs)'
        AGQ3 = 'ukn.agc.l3', 'Level 3 Applied General Qualifications'
        EPQ = 'ukn.epq', 'Level 3 Extended Project Qualifications'
        GCSE = 'ukn.gcse', 'GCSEs'
        AGQ2 = 'ukn.agc.l2', 'Level 2 Applied General Qualifications'
        PQ12 = 'ukn.pq.l12', 'Level 1/2 Project Qualifications'
          
    class UKI(models.TextChoices):
        IAL = 'uki.ial', 'International AS & A levels'
        BTECI3 = 'uki.bteci.l3', 'BTEC Interational Level 3'
        IPQ = 'uki.ipq', 'International Project Qualifications'
        IGCSE = 'uki.igcse', 'IGCSEs'
        OLEVEL = 'uki.olevel', 'O Levels'
        BTECI2 = 'uki.bteci.l2', 'BTEC Interational Level 2'
        
        

    @classmethod
    def grouped_choices(cls):
        return [
            ("UK National", list(cls.UKN.choices)),
            ("UK International", list(cls.UKI.choices)),
            ("IB", list(cls.IB.choices)),
        ]
    
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
        IB.DP: {QualificationName.IB.DP.CORE},
        IB.CP: {QualificationName.IB.CP.CORE}
    }
    @classmethod
    def get_core_qualification_names(cls, suite):
        return cls.MANDATORY_QN_MAP.get(suite, {QualificationName.NAN.NONE})
    
    @classmethod
    def get_qualification_names(cls, suite):
        return cls.QN_MAP.get(suite, {QualificationName.NAN.NONE})
   
    QN_MAP = {
        # UK National - A Levels
        UKN.AL: {
            QualificationName.UKN.Edexcel.A2,
            QualificationName.UKN.Edexcel.AS,
            QualificationName.UKN.OCR.A2,
            QualificationName.UKN.OCR.AS,
            QualificationName.UKN.AQA.A2,
            QualificationName.UKN.AQA.AS,
            QualificationName.UKN.Eduqas.A2,
            QualificationName.UKN.Eduqas.AS,
            QualificationName.UKN.WJEC.A2,
            QualificationName.UKN.WJEC.AS,
        },
        # UK National - GCSE
        UKN.GCSE: {
            QualificationName.UKN.Edexcel.GCSE,
            QualificationName.UKN.OCR.GCSE,
            QualificationName.UKN.AQA.GCSE,
            QualificationName.UKN.Eduqas.GCSE,
            QualificationName.UKN.WJEC.GCSE,
        },

        # UK National - Project Qualifications (Level 1/2)
        UKN.PQ12: {
            QualificationName.UKN.Edexcel.FPQ,
            QualificationName.UKN.Edexcel.HPQ,
            QualificationName.UKN.AQA.FPQ,
            QualificationName.UKN.AQA.HPQ,
        },
        # UK National - Applied General (Level 2)
        UKN.AGQ2: {
            QualificationName.UKN.BTEC.FIRST,
            QualificationName.UKN.OCR.NAT,
            QualificationName.UKN.WJEC.VOC,
        },
        # UK National - Applied General (Level 3)
        UKN.AGQ3: {
            QualificationName.UKN.BTEC.NAT,
            QualificationName.UKN.BTEC.AAQ,
            QualificationName.UKN.OCR.TECH,
            
        },
        # UK National - Alternative Academic Qualification (Level 3)
        UKN.AAQ: {
            QualificationName.UKN.BTEC.AAQ,
            QualificationName.UKN.OCR.AAQ,
            QualificationName.UKN.WJEC.AAQ,
            
        },
        # UK National - Extended Project Qualifications (Level 3)
        UKN.EPQ: {
            QualificationName.UKN.Edexcel.EPQ,
            QualificationName.UKN.OCR.EPQ,
            QualificationName.UKN.AQA.EPQ,
            QualificationName.UKN.Eduqas.EPQ,
            QualificationName.UKN.WJEC.EPQ,
        },

        # UK International - A Levels
        UKI.IAL: {
            QualificationName.UKI.Edexcel.A2,
            QualificationName.UKI.Edexcel.AS,
            QualificationName.UKI.CIE.A2,
            QualificationName.UKI.CIE.AS,
            QualificationName.UKI.OxfordAQA.A2,
            QualificationName.UKI.OxfordAQA.AS,
        },

        # UK International - IGCSEs
        UKI.IGCSE: {
            QualificationName.UKI.Edexcel.IGCSE,
            QualificationName.UKI.CIE.IGCSE_G9,
            QualificationName.UKI.CIE.IGCSE_GA,
            QualificationName.UKI.OxfordAQA.IGCSE,
            QualificationName.UKI.OxfordAQA.IGCSE_PLUS,
        },

        # UK International - O Levels
        UKI.OLEVEL: {
            QualificationName.UKI.CIE.OL,
        },

        # UK International - BTEC International (Level 2)
        UKI.BTECI2: {
            QualificationName.UKI.BTEC.L2,
        },
        # UK International - BTEC International (Level 3)
        UKI.BTECI3: {
            QualificationName.UKI.BTEC.L3,
        },
        # UK International - Project Qualifications
        UKI.IPQ: {
            QualificationName.UKI.CIE.IPQ,
            QualificationName.UKI.OxfordAQA.EPQ,
        },
        # IB Programmes
        IB.MYP: {
            QualificationName.IB.MYP.MYP,
        },
        IB.DP: {
            QualificationName.IB.DP.HL,
            QualificationName.IB.DP.SL,
            QualificationName.IB.DP.CORE,
        },
        IB.CP: {
            QualificationName.IB.CP.CORE,
            QualificationName.IB.DP.HL,
            QualificationName.IB.DP.SL,
        }
    }

class Programme(ComplexChoices):
    class IB(models.TextChoices):
        MYP = 'ib_myp',  'IB Middle Years Programme'
        DP = 'ib_dp',    'IB Diploma Programme'
        CP = 'ib_cp',    'IB Career-related Programme'
    class UKN(models.TextChoices):
        ALEVEL = 'alevel', 'AS/A levels'
        L3 = 'alevescscl', 'AS/A levels & Level 3 AAQ'
        GCSE = 'gcsed', 'GCSEs'
        L222 = 'gcseddv', 'GCSEs & Level 2 Vocational Qualifications'
        L2 = 'gcsewefew', 'Level 2 Vocational Qualifications'
    class UKI(models.TextChoices):
        IAL = 'ial', 'International AS & A levels'
        IGCSE = 'igcsesdv', 'IGCSEs'
        OLEVEL = 'olevel', 'O Level'
    class UKM(models.TextChoices):
        IAL = 'asdvl', 'AS/A level (International & GCE)'
        IALss = 'alsdv', 'AS/A level & BTEC International'
        BTEC = 'sdvsal', 'AS/A level & BTEC International Level 3'
        OLEVEL = 'olevel', 'O Levels'
        L2d = 'igcsedv', 'IGCSEs & O Levels'
        IGCSE = 'igcse', '(I)GCSEs & O Levels'
        
    

    @classmethod
    def choices(cls, multi=False, undefined=False):
        choices = [
            ("British", list(cls.British.choices)),
            ("IB", list(cls.IB.choices if multi else cls.IB.choices[:-1])),
        ]
        if undefined:
            choices.append(cls.UNDEFINED)
        return choices





































    
class QualificationNameOld(ComplexChoices):
    
    class UKN:
        class AL(models.TextChoices):
            A2 = 'ukn.al.a2', "Level 3 Advanced GCE",
            AS = 'ukn.al.as', "Level 3 Advanced Subsidiary GCE",
        class GCSE(models.TextChoices):
            GCSE = 'ukn.al.gcse', 'Level 1/2 GCSE (9-1)'
        class AAQ(models.TextChoices):
            BTEC = 'ukn.aaq.btec', 'Pearson Level 3 AAQ BTEC National'
            OCR = 'ukn.aaq.ocr', 'OCR Level 3 AAQ Cambridge Advanced National'
            WJEC = 'ukn.aaq.wjec', 'WJEC Level 3 AAQ'
            IBO_SL = 'ukn.aaq.ibo.sl', 'IBO Level 3 AAQ SL'
            IBO_HL = 'ukn.aaq.ibo.hl', 'IBO Level 3 AAQ HL'
            
        class EPQ(models.TextChoices):
            L1 = 'ukn.pq.l1', 'Level 1 Foundation Project Qualification'
            L2 = 'ukn.pq.l2', 'Level 2 Higher Project Qualification'
            L3 = 'ukn.pq.l3', 'Level 3 Extended Project Qualification'
        class AGQ3(models.TextChoices):
            OCR_TECH = 'ukn.acq.l3.ocr', 'OCR Level 3 Cambridge Technical'
            BTEC_NAT = 'ukn.acq.l3.btec', 'Pearson BTEC Level 3 National'
            WJEC_APPL = 'ukn.acq.l3.wjec', 'WJEC Level 3 Applied'
            AQA_APPL = 'ukn.acq.l3.aqa', 'AQA Level 3 Applied'
        class AGQ2(models.TextChoices):
            OCR_NAT = 'ukn.acq.l2.ocr', 'OCR Level 1/2 Cambridge National'
            BTEC_FIRST = 'ukn.acq.l2.btec', 'Pearson BTEC Level 1/2 First'
            WJEC_VOC = 'ukn.acq.l2.wjec', 'WJEC Vocational Level 1/2'
    class UKI:
        class IAL(models.TextChoices):
            A2 = 'uki.ial.ia2', 'International A level'
            AS = 'uki.ial.ias', 'International AS level'
        class IGCSE(models.TextChoices):
            G9 = 'uki.igcse', 'International GCSE (9-1)'
            GA = 'uki.igcse.double', 'International GCSE'
        class OLevel(models.TextChoices):
            OL = 'uki.ol', 'O level'
        class PQ(models.TextChoices):
            L1 = 'uki.pq.l1', 'Level 1 Foundation Project Qualification'
            L2 = 'uki.pq.l2', 'Level 2 Higher Project Qualification'
            L3 = 'uki.pq.l3', 'Level 3 Extended Project Qualification'
        class BTEC(models.TextChoices):
            L2 = 'uki.bteci.l2', 'Pearson BTEC International Level 2'
            L3 = 'uki.bteci.l3', 'Pearson BTEC International Level 3'
    class IB:
        class MYP(models.TextChoices):
            MYP = 'ib.myp',  'MYP'
        class DP(models.TextChoices):
            HL = 'ib.dp.hl', 'SL'
            SL = 'ib.dp.sl', 'IB DP HL Subject'
            CORE = 'ib.dp.core', 'IB DP Core'
        class CP(models.TextChoices):
            CORE = 'ib.cp.core', 'IB CP Core'
    




class AQSuite:
    class UKN(models.TextChoices):
        OCR_TECH = "OCR Level 3 Cambridge Technical"
        OCR_NATIONAL = "OCR Level 1/Level 2 Cambridge National"
        BTEC_NATIONAL = "Pearson BTEC Level 3 National"
        BTEC_FIRST = "Pearson BTEC Level 1/Level 2 First "
        WJEC_APPLIED = "WJEC Level 3 Applied"
        AQA_APPLIED = "AQA Level 3 Applied"
        AAQ_BTEC = "Pearson Level 3 AAQ BTEC National"
        AAQ_OCR = "OCR Level 3 AAQ Cambridge Advanced National"
        AAQ_IBO_SL = "IBO Level 3 AAQ SL"
        AAQ_IBO_HL = "IBO Level 3 AAQ HL"
    class UKI(models.TextChoices):
        BTECI_L2 = "Pearson BTEC International Level 2"
        BTECI_L3 = "Pearson BTEC International Level 3"
    
    

# Mapping dictionary
QUAL_BOARD_MAP = {
    AQSuite.UKN.OCR_TECH: Board.OCR,
    AQSuite.UKN.OCR_NATIONAL: Board.OCR,
    AQSuite.UKN.BTEC_NATIONAL: Board.BTEC,
    AQSuite.UKN.BTEC_FIRST: Board.BTEC,
    AQSuite.UKN.WJEC_APPLIED: Board.WJEC,
    AQSuite.UKN.AQA_APPLIED: Board.AQA,
    AQSuite.UKN.AAQ_BTEC: Board.BTEC,
    AQSuite.UKN.AAQ_OCR: Board.OCR,
    AQSuite.UKN.AAQ_IBO_SL: Board.IB,
    AQSuite.UKN.AAQ_IBO_HL: Board.IB,
    AQSuite.UKI.BTECI_L2: Board.BTEC,
    AQSuite.UKI.BTECI_L3: Board.BTEC,
}


class Gender(models.TextChoices):
    FEMALE = 'female', 'Female'
    MALE = 'male', 'Male'
    UNDEFINED = 'undefined', 'Undefined'
    

class Yeargroup(ComplexChoices):
    class UK(models.TextChoices):
        Y9 = 'y9', 'Year 9'
        Y10 = 'y10', 'Year 10'
        Y11 = 'y11', 'Year 11'
        Y12 = 'y12', 'Year 12'
        Y13 = 'y13', 'Year 13'

    class US(models.TextChoices):
        G8 = 'grade8', 'Grade 8'
        G9 = 'grade9', 'Grade 9'
        G10 = 'grade10', 'Grade 10'
        G11 = 'grade11', 'Grade 11'
        G12 = 'grade12', 'Grade 12'

    class Spain(models.TextChoices):
        ESO2 = 'eso2', '2º ESO'
        ESO3 = 'eso3', '3º ESO'
        ESO4 = 'eso4', '4º ESO'
        BACH1 = 'bach1', '1º Bachillerato'
        BACH2 = 'bach2', '2º Bachillerato'

    @classmethod
    def grouped_choices(cls):
        return [
            ("UK system", list(cls.UK.choices)),
            ("US system", list(cls.US.choices)),
            ("Spanish system", list(cls.Spain.choices)),
        ]


# make a distinction betwen  QT and Qualification Name
# QT Level 3 Applied Certificate
# QN Pearson BTEC Level 3 National Certificate

# QT A level
# QN Pearson Edexcel Level 3 GCE Advanced
        
class Qualification:
    UNDEFINED = "undefined", "Other"
    class British(models.TextChoices):
        A2 = 'a2', 'A level'
        AS = 'as', 'AS level'
        GCSE = 'gcse', 'GCSE'
        IA2 = 'ia2', 'International A level'
        IAS = 'ias', 'International AS level'
        IGCSE = 'igcse', 'IGCSE'
        OLEVEL = 'ol', 'O level'
    class IB(models.TextChoices):
        MYP = 'ib_myp',  'IB MYP'
        DP = 'ib_dp',    'IB DP'
        CP = 'ib_cp',    'IB CP'
        DP_CP = 'ib_dp_cp',    'IB DP & IB CP'

    @classmethod
    def choices(cls, multi=False, undefined=False):
        choices = [
            ("British", list(cls.British.choices)),
            ("IB", list(cls.IB.choices if multi else cls.IB.choices[:-1])),
        ]
        if undefined:
            choices.append(cls.UNDEFINED)
        return choices        
        


    
















class QualificationType:
    UNDEFINED = "undefined", "Undefined"
    class British(models.TextChoices):
        A2 = 'a2', 'A level'
        AS = 'as', 'AS level'
        GCSE = 'gcse', 'GCSE'
        IA2 = 'ia2', 'International A level'
        IAS = 'ias', 'International AS level'
        IGCSE = 'igcse', 'IGCSE'
        IGCSE_DOUBLE = 'igcse_double', 'IGCSE Double Award'
        OLEVEL = 'ol', 'O level'

    class IB(models.TextChoices):
        MYP = 'ib_myp',  'IB MYP'
        HL = 'ib_hl',    'IB DP SL'
        SL = 'ib_sl',    'IB DP HL'
        DPC = 'ib_dpc',   'IB DP Core'
        CPC = 'ib_cpc',   'IB CP Core'

    _title_mapping = {
        British.A2: "Level 3 Advanced GCE",
        British.AS: "Level 3 Advanced Subsidiary GCE",
        British.GCSE: "GCSE (9-1)",
        British.IA2: "International A Level",
        British.IAS: "GCSE (9-1)",
        British.IGCSE: "International GCSE",
        British.IGCSE_DOUBLE: "International GCSE",
        British.OLEVEL: "O Level",
        IB.MYP: "MYP",
        IB.HL: "DP",
        IB.SL: "DP",
        IB.CPC: "CP Core",
        IB.DPC: "DP Core",
    }

    # Mapping of qualifications to their official names
    _level_mapping = {
        British.A2: 2,
        British.AS: 1,
        British.GCSE: 0,
        British.IA2: 2,
        British.IAS: 1,
        British.IGCSE: 0,
        British.IGCSE_DOUBLE: 0,
        British.OLEVEL: 0,
        IB.MYP: 1,
        IB.HL: 3,
        IB.SL: 2,
        IB.CPC: 2,
        IB.DPC: 2,
    }

    @classmethod
    def title(cls, qual):
        return cls._title_mapping.get(qual)


    @classmethod
    def choices(cls, multi=False, undefined=False):
        choices =  [
            ("British", list(cls.British.choices)),
            ("IB", list(cls.IB.choices)),
        ]
        if undefined:
            choices.append(cls.UNDEFINED)
        return choices