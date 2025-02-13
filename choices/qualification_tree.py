from django.db import models
from .choices import ComplexChoices

class Edusystem(models.TextChoices):
    UKN = 'ukn', 'UK National'
    UKI = 'uki', 'UK International'
    IB = 'ib', 'International Baccalaureate'

class Board(models.TextChoices):
    UNDEFINED = "undefined", "Undefined"
    EDEXCEL = 'edexcel', 'Pearson Edexcel'
    BTEC = 'btec', 'Pearson BTEC'
    CIE = 'cie', 'Cambridge International'
    OXFORD_AQA = 'oxfordaqa', 'OxfordAQA'
    AQA = 'aqa', 'AQA'
    IB = 'ib', 'IBO'
    OCR = 'ocr', 'OCR'
    WJEC = 'wjec', 'WJEC'
    EDUQAS = 'eduqas', 'WJEC Eduqas'
    CCEA = 'ccea', 'CCEA'
     
class QualificationTree(ComplexChoices):
    class UKN:
        EDU = Edusystem.UKN
        class Edexcel:
            BOARD = Board.EDEXCEL
            class AL(models.TextChoices):
                _SUITE = 'ukn.edexcel.al.', 'Pearson Edexcel A levels'
                A2 = 'ukn.edexcel.al.a2', 'Pearson Edexcel Level 3 Advanced GCE'
                AS = 'ukn.edexcel.al.as', 'Pearson Edexcel Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.edexcel.gcse.', 'Pearson Edexcel GCSEs'
                SINGLE = 'ukn.edexcel.gcse.single', 'Pearson Edexcel Level 1/2 GCSE (9-1)'
                DOUBLE = 'ukn.edexcel.gcse.double', 'Pearson Edexcel Level 1/2 GCSE (9-1) (Double Award)'
            class PQ12(models.TextChoices):
                _SUITE = 'ukn.edexcel.pq12.', 'Pearson Edexcel Level 1/2 Project Qualifications'
                FPQ = 'ukn.edexcel.fpq', 'Pearson Edexcel Level 1 Foundation Project Qualification'
                HPQ = 'ukn.edexcel.hpq', 'Pearson Edexcel Level 2 Higher Project Qualification'
            class EPQ(models.TextChoices):
                _SUITE = 'ukn.edexcel.epq.', 'Pearson Edexcel Level 3 Extended Project Qualification'
                EPQ = 'ukn.edexcel.epq.epq', 'Pearson Edexcel Level 3 Extended Project Qualification'
                
        class OCR:
            BOARD = Board.OCR
            class AL(models.TextChoices):
                _SUITE = 'ukn.icr.al.', 'OCR A levels'
                A2 = 'ukn.ocr.al.a2', 'OCR Level 3 Advanced GCE'
                AS = 'ukn.ocr.al.as', 'OCR Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.ocr.gcse.', 'OCR GCSEs'
                SINGLE = 'ukn.ocr.gcse.single', 'OCR GCSE (9-1)'
                DOUBLE = 'ukn.ocr.gcse.double', 'OCR GCSE (9-1) (Double Award)'
            class AAQ(models.TextChoices):     
                _SUITE = 'ukn.ocr.aaq.', 'OCR Level 3 AAQ Cambridge Advanced Nationals'
                CERT = 'ukn.ocr.aaq.cert', 'OCR Level 3 AAQ Cambridge Advanced National (Certificate)'
                EXT_CERT = 'ukn.ocr.aaq.ext_cert', 'OCR Level 3 AAQ Cambridge Advanced National (Extended Certificate)'
            class TECH(models.TextChoices): 
                _SUITE = 'ukn.ocr.tech', 'OCR Level 3 Cambridge Technicals'
                CERT = 'ukn.ocr.tech.cert', 'OCR Level 3 Cambridge Technical (Certificate)'
                EXT_CERT = 'ukn.ocr.tech.ext_cert', 'OCR Level 3 Cambridge Technical (Extended Certificate)'
                FDN_DIP = 'ukn.ocr.tech.fdn_dip', 'OCR Level 3 Cambridge Technical (Foundation Diploma)'
                DIP = 'ukn.ocr.tech.dip', 'OCR Level 3 Cambridge Technical (Diploma)'
                EXT_DIP = 'ukn.ocr.tech.ext_dip', 'OCR Level 3 Cambridge Technical (Extended Diploma)'
            class NAT(models.TextChoices): 
                _SUITE = 'ukn.ocr.nat.', 'OCR Level 1/2 Cambridge National'
                AWARD = 'ukn.ocr.nat.award', 'OCR Level 1/2 Cambridge National Award'
            class EPQ(models.TextChoices): 
                _SUITE = 'ukn.ocr.epq.', 'OCR Level 3 Extended Project Qualification'
                EPQ = 'ukn.ocr.epq.epq', 'OCR Level 3 Extended Project Qualification'
        class AQA:
            BOARD = Board.AQA
            class AL(models.TextChoices):
                _SUITE = 'ukn.aqa.al.', 'AQA AS & A levels'
                A2 = 'ukn.aqa.al.a2', 'AQA Level 3 Advanced GCE'
                AS = 'ukn.aqa.al.as', 'AQA Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.aqa.gcse.', 'AQA GCSEs'
                SINGLE = 'ukn.aqa.gcse.single', 'AQA Level 1/2 GCSE (9-1)'
                DOUBLE = 'ukn.aqa.gcse.double', 'AQA Level 1/2 GCSE (9-1) (Double Award)'
            class AG(models.TextChoices):
                _SUITE = 'ukn.aqa.ag.', 'AQA Level 3 Applied Generals'
                CERT = 'ukn.aqa.ag.cert', 'AQA Level 3 Certificate'
                EXT_CERT = 'ukn.ag.appl.ext_cert', 'AQA Level 3 Extended Certificate'
            class PQ12(models.TextChoices):    
                _SUITE = 'ukn.aqa.appl.', 'AQA Level 1/2 Project Qualifications'
                FPQ = 'ukn.aqa.pq12.fpq', 'AQA Level 1 Foundation Project Qualification'
                HPQ = 'ukn.aqa.pq.12.hpq', 'AQA Level 2 Higher Project Qualification'
            class EPQ(models.TextChoices):    
                _SUITE = 'ukn.aqa.epq.', 'AQA Level 3 Extended Project Qualification'
                EPQ = 'ukn.aqa.epq.epq', 'AQA Level 3 Extended Project Qualification'
        class Eduqas:
            BOARD = Board.EDUQAS
            class AL(models.TextChoices):
                _SUITE = 'ukn.eduqas.', 'WJEC Eduqas A levels'
                A2 = 'ukn.eduqas.al.a2', 'WJEC Eduqas Level 3 Advanced GCE'
                AS = 'ukn.eduqas.al.as', 'WJEC Eduqas Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.eduqas.gcse.', 'WJEC Eduqas GCSEs'
                SINGLE = 'ukn.eduqas.gcse.single', 'WJEC Eduqas GCSE (9-1)'
                DOUBLE = 'ukn.eduqas.gcse.double', 'WJEC Eduqas GCSE (9-1) (Double Award)'
            class EPQ(models.TextChoices):
                _SUITE = 'ukn.eduqas.epq.', 'WJEC Eduqas Level 3 Extended Project Qualification'
                EPQ = 'ukn.eduqas.epq.epq', 'WJEC Eduqas Level 3 Extended Project Qualification'
        class WJEC:
            BOARD = Board.WJEC
            class AL(models.TextChoices):
                _SUITE = 'ukn.al.wjec.al.', 'WJEC Level 3 Advanced GCE'
                A2 = 'ukn.al.wjec.al.a2', 'WJEC Level 3 Advanced GCE'
                AS = 'ukn.al.wjec.al.as', 'WJEC Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.wjec.gcse.', 'WJEC GCSEs'
                SINGLE = 'ukn.wjec.gcse.single', 'WJEC GCSE (9-1)'
                DOUBLE = 'ukn.wjec.gcse.double', 'WJEC Level GCSE (9-1) (Double Award)'
                
            class VA(models.TextChoices):
                _SUITE = 'ukn.wjec.vq.', 'WJEC Level 1/2 Vocational Awards'
                VA = 'ukn.wjec.va.va', 'WJEC Vocational Level 1/2 Vocational Award'
            class AQ(models.TextChoices):
                _SUITE = 'ukn.wjec.aq.', 'WJEC Level 3 Applied Qualifications'
                CERT = 'ukn.wjec.aq.cert', 'WJEC Level 3 Applied Certificate'
                EXT_CERT = 'ukn.wjec.aq.ext_cert', 'WJEC Level 3 Applied Extended Certificate'
                DIP = 'ukn.wjec.aq.dip', 'WJEC Level 3 Applied Diploma'
            class EPQ(models.TextChoices):
                _SUITE = 'ukn.wjec.epq.', 'WJEC Level 3 Extended Project Qualification'
                EPQ = 'ukn.wjec.epq.epq', 'WJEC Level 3 Extended Project Qualification'
            class AAQ(models.TextChoices):
                _SUITE = 'ukn.wjec', 'WJEC Level 3 AAQ'
                AAQ = 'ukn.wjec.aaq', 'WJEC Level 3 Alternative Academic Qualification (Certificate)'
        class CCEA:
            BOARD = Board.CCEA    
            class AL(models.TextChoices):
                _SUITE = 'ukn.eduqas.', 'CCEA A levels'
                A2 = 'ukn.ccea.al.a2', 'CCEA Level 3 Advanced GCE'
                AS = 'ukn.ccea.al.as', 'CCEA Level 3 Advanced Subsidiary GCE'
            class GCSE(models.TextChoices):
                _SUITE = 'ukn.ccea.gcse', 'CCEA GCSEs'
                SINGLE = 'ukn.ccea.gcse.single', 'CCEA Level 1/2 GCSE'
                DOUBLE = 'ukn.ccea.gcse.double', 'CCEA Level 1/2 GCSE Double Award'

        class BTEC:
            BOARD = Board.BTEC
            class AAQ(models.TextChoices):
                _SUITE = 'ukn.btec.aaq.', 'Pearson Level 3 Alternative Academic Qualification BTEC Nationals'
                CERT = 'ukn.btec.aaq.cert', 'Pearson Level 3 AAQ BTEC National (Certificate)'
                EXT_CERT = 'ukn.btec.aaq.ext_cert', 'Pearson Level 3 AAQ BTEC National (Certificate)'
            class NAT(models.TextChoices):
                _SUITE = 'ukn.btec.nat.', 'Pearson BTEC Level 3 Nationals'
                CERT = 'ukn.btec.nat.cert', 'Pearson BTEC Level 3 National'
                EXT_CERT = 'ukn.btec.nat.ext_cert', 'Pearson BTEC Level 3 National'
                FDN_DIP = 'ukn.btec.nat.fdn_dip', 'Pearson BTEC Level 3 National'
                DIP = 'ukn.btec.nat.dip', 'Pearson BTEC Level 3 National'
                EXT_DIP = 'ukn.btec.nat.ext_dip', 'Pearson BTEC Level 3 National'
            class FIRST(models.TextChoices):
                _SUITE = 'ukn.btec.first.', 'Pearson BTEC Level 1/2 Firsts'
                AWARD = 'ukn.btec.first.award', 'Pearson BTEC Level 1/2 First Award'
                CERT = 'ukn.btec.first.cert', 'Pearson BTEC Level 1/2 First Certificate'
                EXT_CERT = 'ukn.btec.first.ext_cert', 'Pearson BTEC Level 1/2 First Extended Certificate'
                DIP = 'ukn.btec.first.dip', 'Pearson BTEC Level 1/2 First Diploma'

    class UKI:
        EDU = Edusystem.UKI
        class Edexcel:
            BOARD = Board.EDEXCEL
            class IAL(models.TextChoices):
                _SUITE = 'uki.edexcel.ial.', 'Pearson Edexcel International A levels'
                A2 = 'uki.edexcel.ial.a2', 'Pearson Edexcel International A level'
                AS = 'uki.edexcel.ial.as', 'Pearson Edexcel International AS level'
            class IGCSE(models.TextChoices):    
                _SUITE = 'uki.edexcel.igcse.', 'Pearson Edexcel International GCSEs'
                SINGLE = 'uki.edexcel.igcse.single', 'Pearson Edexcel International GCSE (9-1)'
                IGCSE = 'uki.edexcel.igcse.igcse', 'Pearson Edexcel International GCSE (9-1)'
        class CIE:
            BOARD = Board.CIE
            class IAL(models.TextChoices):
                _SUITE = 'uki.cie.ial.', 'Cambridge International A levels'
                A2 = 'uki.cie.ial.a2', 'Cambridge International A level'
                AS = 'uki.cie.ial.as', 'Cambridge International AS level'
            class IGCSE(models.TextChoices):    
                _SUITE = 'uki.cie.igcse.', 'Cambridge IGCSEs'
                SINGLE_G9 = 'uki.cie.igcse.single_g9', 'Cambridge IGCSE (9-1)'
                SINGLE_GA = 'uki.cie.igcse.single_ga', 'Cambridge IGCSE'
                DOUBLE_G9 = 'uki.cie.igcse.double_g9', 'Cambridge IGCSE (9-1) Double Award'
                DOUBKE_GA = 'uki.cie.igcse.double_ga', 'Cambridge IGCSE Double Award'
            class OL(models.TextChoices):  
                _SUITE = 'uki.cie.ol.', 'Cambridge O levels'
                OL = 'uki.cie.ol.ol', 'Cambridge O level'
            class IPQ(models.TextChoices):      
                _SUITE = 'uki.cie.ipq.', 'Cambridge International Project Qualification'
                IPQ = 'uki.cie.ipq.ipq', 'Cambridge International Project Qualification'

        class OxfordAQA:
            BOARD = Board.OXFORD_AQA
            class IAL(models.TextChoices):
                _SUITE = 'uki.oxfordaqa.ial.', 'OxfordAQA International A levels'
                A2 = 'uki.oxfordaqa.ial.a2', 'OxfordAQA International A level'
                AS = 'uki.oxfordaqa.ial.as', 'OxfordAQA International AS level'
            class IGCSE(models.TextChoices):
                _SUITE = 'uki.oxfordaqa.igcse.', 'OxfordAQA IGCSEs'
                SINGLE = 'uki.oxfordaqa.igcse.single', 'OxfordAQA IGCSE (9-1)'
                SINGLE_PLUS = 'uki.oxfordaqa.igcse.igcse+', 'OxfordAQA International GCSE (9-1) Plus'
                DOUBLE = 'uki.oxfordaqa.igcse.double', 'OxfordAQA IGCSE (9-1) Double Award'
                DOUBLE_PLUS = 'uki.oxfordaqa.igcse.double+', 'OxfordAQA International GCSE (9-1) Double Award Plus'
            class EPQ(models.TextChoices):
                _SUITE = 'uki.oxfordaqa.epq.', 'OxfordAQA International Extended Project Qualification'
                EPQ = 'uki.oxfordaqa.epq.epq', 'OxfordAQA International Extended Project Qualification'  
            
        class BTEC:
            BOARD = Board.BTEC
            class IL3(models.TextChoices):
                _SUITE = 'uki.btec.il3.', 'Pearson BTEC International Level 3'
                CERT = 'uki.btec.il3.cert', 'Pearson BTEC International Level 3 Certificate'
                EXT_CERT = 'uki.btec.il3.ext_cert', 'Pearson BTEC International Level 3 Extended Certificate'
                SUB_DIP = 'uki.btec.il3.sub_dip', 'Pearson BTEC International Level 3 Subsidiary Diploma'
                FDN_DIP = 'uki.btec.il3.fdn_dip', 'Pearson BTEC International Level 3 Foundation Diploma'
                DIP = 'uki.btec.il3.dip', 'Pearson BTEC International Level 3 Diploma'
                EXT_DIP = 'uki.btec.il3.ext_dip', 'Pearson BTEC International Level 3 Extended Diploma'
            class IL2(models.TextChoices):
                _SUITE = 'uki.btec.il2.', 'Pearson BTEC International Level 2'
                AWARD = 'uki.btec.il2.award', 'Pearson BTEC International Level 2 Award'
                CERT = 'uki.btec.il2.cert', 'Pearson BTEC International Level 2 Certificate'
                EXT_CERT = 'uki.btec.il2.ext_cert', 'Pearson BTEC International Level 2 Extended Certificate'
                DIP = 'uki.btec.il2.dip', 'Pearson BTEC International Level 2 Diploma'

    class IB:
        EDU = Edusystem.IB
        class IBO:
            BOARD = Board.IB
            class MYP(models.TextChoices):
                _SUITE = 'ib.myp.',  'IB Middle Years Programme'
                MYP = 'ib.myp.myp',  'IB MYP'
            class DP(models.TextChoices):
                _SUITE = 'ib.dp.',  'IB Diploma Programme'
                HL = 'ib.dp.hl', 'IB DP HL'
                SL = 'ib.dp.sl', 'IB DP SL'
                CORE = 'ib.dp.core', 'IB DP'
                AGG = 'ib.dp.agg', 'IB DP'
            class CP(models.TextChoices):
                _SUITE = 'ib.cp.',  'IB Career-related Programme'
                CORE = 'ib.cp.core', 'IB CP'
    
    
    @classmethod
    def choices(cls):
        cs = super().choices()
        return [c for c in cs if not c[0].endswith('.')] 
    
    @classmethod
    def suite_choices(cls):
        cs = super().choices() 
        return [c for c in cs if c[0].endswith('.')] 

    
    @classmethod
    def choices_from_suite_class(cls, suite_class, values_only=False):
        choices =  [c for c in suite_class.choices if not c[0].endswith('.')] 
        if values_only:
            return [c[0] for c in choices]
        return choices
    

    @classmethod
    def get_board_from_choice(cls, choice):
        for l1 in cls.__dict__.values():
            if isinstance(l1, type):
                for l2 in l1.__dict__.values():
                    if isinstance(l2, type):
                        for l3 in l2.__dict__.values():
                            if isinstance(l3, type) and issubclass(l3, models.TextChoices):
                                for _, member in l3.__members__.items():
                                    if member == choice:
                                        return getattr(l2, 'BOARD', None)
        return None 
    
    @classmethod
    def get_suite_from_choice(cls, choice):
        for l1 in cls.__dict__.values():
            if isinstance(l1, type):
                for l2 in l1.__dict__.values():
                    if isinstance(l2, type):
                        for l3 in l2.__dict__.values():
                            if isinstance(l3, type) and issubclass(l3, models.TextChoices):
                                for _, member in l3.__members__.items():
                                    if member == choice:
                                        return getattr(l3, '_SUITE', None)
        return None 
    
# board1 = QualificationTree.get_board_from_choice(QualificationTree.UKN.OCR.AL.A2)
# board2 = QualificationTree.get_board_from_choice(QualificationTree.UKN.Edexcel.AL.A2)
# board3 = QualificationTree.get_board_from_choice(QualificationTree.IB.IBO.DP.HL)
# board4 = QualificationTree.get_board_from_choice(QualificationTree.UKI.BTEC.IL2.CERT)

# board1 = QualificationTree.get_suite_from_choice(QualificationTree.UKN.OCR.AL.A2)
# board2 = QualificationTree.get_suite_from_choice(QualificationTree.UKN.Edexcel.AL.A2)
# board3 = QualificationTree.get_suite_from_choice(QualificationTree.IB.IBO.DP.HL)
# board4 = QualificationTree.get_suite_from_choice(QualificationTree.UKI.BTEC.IL2.CERT)
# print(board1, board2, board3, board4)  # Output: Board.EDEXCEL

#print(QualificationTree.choices_from_suite_class(QualificationTree.UKI.OxfordAQA.IAL))


