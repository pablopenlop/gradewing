from .qualification_tree import QualificationTree as QT
from .choices import ComplexChoices
from django.db import models

class QualificationKind(ComplexChoices):
    class UKN:
        class AL(models.TextChoices):
            A2 = 'ukn.al.a2', 'A level'
            AS = 'ukn.al.as', 'AS level'
        class GCSE(models.TextChoices):
            GCSE = 'ukn.gcse', 'GCSE'
            GCSE_DOUBLE = 'ukn.gcse.double', 'GCSE Double Award'
        class AAQ(models.TextChoices):
            CERT = 'ukn.aaq.cert', 'AAQ Certificate'
            EXT_CERT = 'ukn.aaq.ext_cert', 'AAQ Extended Certificate'
        class PQ(models.TextChoices):
            L1 = 'ukn.pq.l1', 'Level 1 Foundation Project Qualification'
            L2 = 'ukn.pq.l2', 'Level 2 Higher Project Qualification'
        class EPQ(models.TextChoices):
            EPQ = 'ukn.epq.epq', 'Level 3 Extended Project Qualification'
        class VTQ3(models.TextChoices):
            CERT = 'ukn.vtq.l3.cert', 'Level 3 VTQ Certificate'
            EXT_CERT = 'ukn.vtq.l3.ext_cert', 'Level 3  VTQ Extended Certificate'
            FDN_DIP = 'ukn.vtq.l3.fdn_dip', 'Level 3 VTQ Foundation Diploma'
            DIP = 'ukn.vtq.l3.dip', 'Level 3 VTQ Diploma'
            EXT_DIP = 'ukn.vtq.l3.dip_ext', 'Level 3 Level 3 Extended Diploma'
        class VTQ2(models.TextChoices):
            AWARD = 'ukn.vtq.award', 'Level 2 VTQ Award'
            CERT = 'ukn.vtq.cert', 'Level 2 VTQ Certificate'
            EXT_CERT = 'ukn.vtq.cert_ext', 'Level 2 VTQ Extended Certificate'
            DIPLOMA = 'ukn.vtq.dip', 'Level 2 VTQ Diploma' 
    class UKI:
        class IAL(models.TextChoices):
            A2 = 'uki.ial.a2', 'International A level'
            AS = 'uki.ial.as', 'International AS level'
        class IGCSE(models.TextChoices):
            IGCSE = 'uki.igcse', 'International GCSE'
            IGCSE_DOUBLE = 'uki.igcse.double', 'International GCSE (Double Award)'
            IGCSE_PLUS= 'uki.igcse+', 'International GCSE & Endorsement'
            IGCSE_DOUBLE_PLUS = 'uki.igcse.double+', 'International GCSE (Double Award) & Endorsement'
        class OLevel(models.TextChoices):
            OLEVEL = 'uki.ol', 'O level'
        class IPQ(models.TextChoices):
            EPQ = 'uki.ipq.epq', 'International EPQ'
        class BTEC3(models.TextChoices):
            CERT = 'uki.btec.il3.cert', 'BTEC International Level 3 Certificate'
            EXT_CERT = 'uki.btec.il3.ext_cert', 'BTEC International Level 3 Extended Certificate'
            SUB_DIP = 'uki.btec.il3.sub_dip', 'BTEC International Level 3 Subsidiary Diploma'
            FDN_DIP = 'uki.btec.il3.fdn_dip', 'BTEC International Level 3 Foundation Diploma'
            DIP = 'uki.btec.il3.dip', 'BTEC International Level 3 Diploma'
            EXT_DIP = 'uki.btec.il3.ext_dip', 'BTEC International Level 3 Extended Diploma'
        class BTEC2(models.TextChoices):
            AWARD = 'uki.btec.il2.award', 'BTEC International Level 2 Award'
            CERT = 'uki.btec.il2.cert', 'BTEC International Level 2 Certificate'
            EXT_CERT = 'uki.btec.il2.cert_ext', 'BTEC International Level 2 Extended Certificate'
            DIP = 'uki.btec.il2.dip', 'BTEC International Level 2 Diploma'

    class IB:
        class MYP(models.TextChoices):
            MYP = 'ib.myp',  'MYP'
        class DP(models.TextChoices):
            HL = 'ib.dp.hl', 'DP HL'
            SL = 'ib.dp.sl', 'DP SL'
            CORE = 'ib.dp.core', 'DP Core'
            AGG = 'ib.dp.agg', 'DP Aggregate'
        class CP(models.TextChoices):
            CORE = 'ib.cp.core', 'CP Core'

    @classmethod
    def get_kind_from_name(cls, name):
        return cls.NAME_2_KIND.get(name, {cls.NONE.NONE})

    NAME_2_KIND = {
        # UKN - Edexcel
        QT.UKN.Edexcel.AL.A2: UKN.AL.A2,
        QT.UKN.Edexcel.AL.AS: UKN.AL.AS,
        QT.UKN.Edexcel.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.Edexcel.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,
        QT.UKN.Edexcel.PQ12.FPQ: UKN.PQ.L1,
        QT.UKN.Edexcel.PQ12.HPQ: UKN.PQ.L2,
        QT.UKN.Edexcel.EPQ.EPQ: UKN.EPQ.EPQ,

        # UKN - OCR
        QT.UKN.OCR.AL.A2: UKN.AL.A2,
        QT.UKN.OCR.AL.AS: UKN.AL.AS,
        QT.UKN.OCR.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.OCR.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,
        QT.UKN.OCR.AAQ.CERT: UKN.AAQ.CERT,
        QT.UKN.OCR.AAQ.EXT_CERT: UKN.AAQ.EXT_CERT,
        QT.UKN.OCR.TECH.CERT: UKN.VTQ3.CERT,
        QT.UKN.OCR.TECH.EXT_CERT: UKN.VTQ3.EXT_CERT,
        QT.UKN.OCR.TECH.FDN_DIP: UKN.VTQ3.FDN_DIP,
        QT.UKN.OCR.TECH.DIP: UKN.VTQ3.DIP,
        QT.UKN.OCR.TECH.EXT_DIP: UKN.VTQ3.EXT_DIP,
        QT.UKN.OCR.NAT.AWARD: UKN.VTQ2.AWARD,
        QT.UKN.OCR.EPQ.EPQ: UKN.EPQ.EPQ,

        # UKN - AQA
        QT.UKN.AQA.AL.A2: UKN.AL.A2,
        QT.UKN.AQA.AL.AS: UKN.AL.AS,
        QT.UKN.AQA.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.AQA.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,
        QT.UKN.AQA.AG.CERT: UKN.VTQ3.CERT,
        QT.UKN.AQA.AG.EXT_CERT: UKN.VTQ3.EXT_CERT,
        QT.UKN.AQA.PQ12.FPQ: UKN.PQ.L1,
        QT.UKN.AQA.PQ12.HPQ: UKN.PQ.L2,
        QT.UKN.AQA.EPQ.EPQ: UKN.EPQ.EPQ,

        # UKN - Eduqas
        QT.UKN.Eduqas.AL.A2: UKN.AL.A2,
        QT.UKN.Eduqas.AL.AS: UKN.AL.AS,
        QT.UKN.Eduqas.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.Eduqas.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,
        QT.UKN.Eduqas.EPQ.EPQ: UKN.EPQ.EPQ,

        # UKN - WJEC
        QT.UKN.WJEC.AL.A2: UKN.AL.A2,
        QT.UKN.WJEC.AL.AS: UKN.AL.AS,
        QT.UKN.WJEC.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.WJEC.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,
        QT.UKN.WJEC.VA.VA: UKN.VTQ2.AWARD,
        QT.UKN.WJEC.AQ.CERT: UKN.AAQ.CERT,
        QT.UKN.WJEC.AQ.EXT_CERT: UKN.VTQ3.EXT_CERT,
        QT.UKN.WJEC.AQ.DIP: UKN.VTQ3.DIP,
        QT.UKN.WJEC.EPQ.EPQ: UKN.EPQ.EPQ,
        QT.UKN.WJEC.AAQ.AAQ: UKN.AAQ.CERT,

        # UKN - CCEA
        QT.UKN.CCEA.AL.A2: UKN.AL.A2,
        QT.UKN.CCEA.AL.AS: UKN.AL.AS,
        QT.UKN.CCEA.GCSE.SINGLE: UKN.GCSE.GCSE,
        QT.UKN.CCEA.GCSE.DOUBLE: UKN.GCSE.GCSE_DOUBLE,

        # UKN - BTEC
        QT.UKN.BTEC.AAQ.CERT: UKN.AAQ.CERT,
        QT.UKN.BTEC.AAQ.EXT_CERT: UKN.AAQ.EXT_CERT,
        QT.UKN.BTEC.NAT.CERT: UKN.VTQ3.CERT,
        QT.UKN.BTEC.NAT.EXT_CERT: UKN.VTQ3.EXT_CERT,
        QT.UKN.BTEC.NAT.FDN_DIP: UKN.VTQ3.FDN_DIP,
        QT.UKN.BTEC.NAT.DIP: UKN.VTQ3.DIP,
        QT.UKN.BTEC.NAT.EXT_DIP: UKN.VTQ3.EXT_DIP,
        QT.UKN.BTEC.FIRST.AWARD: UKN.VTQ2.AWARD,
        QT.UKN.BTEC.FIRST.CERT: UKN.VTQ2.CERT,
        QT.UKN.BTEC.FIRST.EXT_CERT: UKN.VTQ2.EXT_CERT,
        QT.UKN.BTEC.FIRST.DIP: UKN.VTQ2.DIPLOMA,

        # UKI - Edexcel
        QT.UKI.Edexcel.IAL.A2: UKI.IAL.A2,
        QT.UKI.Edexcel.IAL.AS: UKI.IAL.AS,
        QT.UKI.Edexcel.IGCSE.SINGLE: UKI.IGCSE.IGCSE,
        QT.UKI.Edexcel.IGCSE.IGCSE: UKI.IGCSE.IGCSE_DOUBLE,

        # UKI - CIE
        QT.UKI.CIE.IAL.A2: UKI.IAL.A2,
        QT.UKI.CIE.IAL.AS: UKI.IAL.AS,
        QT.UKI.CIE.IGCSE.SINGLE_G9: UKI.IGCSE.IGCSE,
        QT.UKI.CIE.IGCSE.SINGLE_GA: UKI.IGCSE.IGCSE,
        QT.UKI.CIE.IGCSE.DOUBLE_G9: UKI.IGCSE.IGCSE_DOUBLE,
        QT.UKI.CIE.IGCSE.DOUBKE_GA: UKI.IGCSE.IGCSE_DOUBLE,
        QT.UKI.CIE.OL.OL: UKI.OLevel.OLEVEL,
        QT.UKI.CIE.IPQ.IPQ: UKI.IPQ.EPQ,

        # UKI - OxfordAQA
        QT.UKI.OxfordAQA.IAL.A2: UKI.IAL.A2,
        QT.UKI.OxfordAQA.IAL.AS: UKI.IAL.AS,
        QT.UKI.OxfordAQA.IGCSE.SINGLE: UKI.IGCSE.IGCSE,
        QT.UKI.OxfordAQA.IGCSE.SINGLE_PLUS: UKI.IGCSE.IGCSE_PLUS,
        QT.UKI.OxfordAQA.IGCSE.DOUBLE: UKI.IGCSE.IGCSE_DOUBLE,
        QT.UKI.OxfordAQA.IGCSE.DOUBLE_PLUS: UKI.IGCSE.IGCSE_DOUBLE_PLUS,
        QT.UKI.OxfordAQA.EPQ.EPQ: UKI.IPQ.EPQ,

         # UKI - BTEC
        QT.UKI.BTEC.IL3.CERT: UKI.BTEC3.CERT,
        QT.UKI.BTEC.IL3.EXT_CERT: UKI.BTEC3.EXT_CERT,
        QT.UKI.BTEC.IL3.SUB_DIP: UKI.BTEC3.SUB_DIP,
        QT.UKI.BTEC.IL3.FDN_DIP: UKI.BTEC3.FDN_DIP,
        QT.UKI.BTEC.IL3.DIP: UKI.BTEC3.DIP,
        QT.UKI.BTEC.IL3.EXT_DIP: UKI.BTEC3.EXT_DIP,
        QT.UKI.BTEC.IL2.AWARD: UKI.BTEC2.AWARD,
        QT.UKI.BTEC.IL2.CERT: UKI.BTEC2.CERT,
        QT.UKI.BTEC.IL2.EXT_CERT: UKI.BTEC2.EXT_CERT,
        QT.UKI.BTEC.IL2.DIP: UKI.BTEC2.DIP,

        # IB - MYP, DP, CP
        QT.IB.IBO.MYP.MYP: IB.MYP.MYP,
        QT.IB.IBO.DP.HL: IB.DP.HL,
        QT.IB.IBO.DP.SL: IB.DP.SL,
        QT.IB.IBO.DP.AGG: IB.DP.AGG,
        QT.IB.IBO.DP.CORE: IB.DP.CORE,
        QT.IB.IBO.CP.CORE: IB.CP.CORE,
        
    }
