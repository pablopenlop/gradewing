from .models import Qualification, Component
from django.db import transaction

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Union


from register_app.edusystem import Programme, Board 
from register_app.edusystem import QualificationName as QN
from register_app.edusystem import QualificationKind as QK 
from register_app.edusystem import QualificationSuite as QS 
from register_app.edusystem import SubjectGroup as SG
from register_app.edusystem import GradingScale as GS
from register_app.edusystem import Series 
from register_app.edusystem import Tier
from register_app.edusystem import MarkType as MT


import pprint

@dataclass
class DataLoader:
    count = 0

    @staticmethod
    def flatten_aggregate(aggregate: dict)->List[dict]:
        if "subset" not in aggregate:
            return [aggregate]
        entries=[]
        
        for item in aggregate["subset"]:
                entry = {**{k: v for k, v in aggregate.items() if k != 'subset'}, **item}
                is_packet= any(isinstance(v, tuple) for v in item.values())
                if not is_packet:
                    entry = {k: (v[0] if isinstance(v, tuple) else v) for k, v in entry.items()}
                entries.append(entry)
        return entries

    @staticmethod
    def flatten_packet(packet: dict)->List[dict]:
        compound = {key: value for key, value in packet.items() if key in QualificationLoad.__annotations__}
        csize = next((len(value) for value in compound.values() if isinstance(value, tuple)), None)
        if csize is None:
            components = []
            for comp in packet['components']:
                compflat = {k: (v[0] if isinstance(v, tuple) else v) for k, v in comp.items()}
                if compflat['weighting']is not None:
                    components.append(compflat)
            compound['components'] = components
            return [compound]
        simples = []
        for i in range(csize):
            simple = {k: (v[i] if isinstance(v, tuple) else v) for k, v in compound.items()}
            components = []
            for comp in packet['components']:
                compflat = {k: (v[i] if isinstance(v, tuple) else v) for k, v in comp.items()}
                if compflat['weighting'] is not None:
                    components.append(compflat)
            simple['components'] = components
            simples.append(simple)
        return simples
    

    def load(self, data: List[dict], commit: bool=False):
        for item in data:
            packets = self.flatten_aggregate(item)
            for packet in packets:
                elements = self.flatten_packet(packet)
                for element in elements:
                    pprint.pprint(element)
                    subject = QualificationLoad.from_dict(element)
                    self.count = self.count+1
                    print(subject.to_model())
                    for component in subject.components:
                        print(component.to_model())
                        pass
                  

@dataclass
class ComponentLoad:
    name: str
    code: str
    weighting: str
    
    grading: SG.choices
    internal: bool
    duration: str=""
    mark: Optional[int] = None
    mark_type: MT = MT.RAW
    mark_adjusted: Optional[int] = None
    mark_adjusted_type: MT = MT.NONE
    optional: bool=False
    glh: Optional[int] = None
    qualification: Optional['QualificationLoad'] = None
    
    
    def fill_code(self, parent_code: str)->None:
        self.code = self.code.replace('*', parent_code)

    def set_glh_based_weighting(self):
        if self.weighting == "glh":
            self.weighting = f"{self.glh/self.qualification.glh*100:.1f}%"


    def to_model(self):
        component, created = Component.objects.update_or_create(
            code=self.code, 
            qualification__code =self.qualification.code,
            qualification__name = self.qualification.name,
            qualification__tier = self.qualification.tier,
            qualification__first_assessment = self.qualification.first_assessment,
            defaults={ 
                'name': self.name,
                'weighting': self.weighting,
                'duration': self.duration,
                'internal': self.internal,
                'mark': self.mark,
                'mark_type': self.mark_type,
                'mark_adjusted': self.mark_adjusted,
                'mark_adjusted_type': self.mark_adjusted_type,
                'grading': self.grading,
                'glh': self.glh,
                'optional': self.optional,
                'qualification': self.qualification.to_model(),
            }
        )
        return component
    

@dataclass
class QualificationLoad:
    subject: str
    code: str
    name: QN.choices
    kind: QK.choices
    suite: QS.choices
    grading: GS.choices
    board: Board
    group: SG.choices
    mark: int
    mark_type: MT
    first_assessment: int
    modular: bool
    series: List[Series.choices]
    glh: int
    components: List[ComponentLoad] = field(default_factory=list)
    current: bool = True
    last_assessment: Optional[int] = None
    tier: Tier = Tier.NONE
    sbs: bool = False
    suffix: Optional[str] = None
    sub_qualification: Optional[str] = None
    core: bool = False
    
    def add_component(self, component: ComponentLoad)->None:
        component.fill_code(self.code)
        self.components.append(component)

    def __post_init__(self):
        self.refine_subject()

    def refine_subject(self)->None:
        if self.suffix:
            self.subject = f"{self.subject} {self.suffix}"
        if self.tier !=Tier.NONE:
            self.subject = f"{self.subject}  ({self.tier.label})"
    # We require a full_name for technicals
    # Also subject with years?
    @property
    def get_name(self)->str:
        # if QK.kind_in_name(self.kind):
        if self.kind == QK.UKI.BTEC3.DIP:
            return f"{self.name.label} {self.kind.label}"
        return self.name.label
    @property
    def title(self):
        year = f" ({self.first_assessment}-{self.last_assessment})" if not self.current else ""
        subject =f" in {self.subject}" if bool(self.subject) else ""
        return f"{self.get_name}{subject}{year}"
    
    def str_series(self):
        return ','.join([s.value for s in self.series])

    @classmethod
    def from_dict(cls, element: dict) -> 'QualificationLoad':
        components = element.pop("components", [])
        qualification = cls(**element)
        for component in components:
            component = {k: v for k, v in component.items() if k in ComponentLoad.__annotations__}
            qualification.add_component(ComponentLoad(**component, qualification=qualification))
        return qualification
    
    def to_model(self):
        subqual = None
        if self.sub_qualification:
            subqual = Qualification.objects.filter(
                code=self.sub_qualification.get('code'),
                name=self.sub_qualification.get('name'),
                first_assessment=self.sub_qualification.get('first_assessment')
            ).first()


        qualification, created = Qualification.objects.update_or_create(
            code=self.code, 
            name=self.name,
            tier = self.tier,
            first_assessment = self.first_assessment,
            defaults={ 
                'subject': self.subject,
                'kind': self.kind,
                'title': self.title,
                'suite': self.suite,
                'board': self.board,
                'group': self.group,
                'last_assessment': self.last_assessment,
                'modular': self.modular,
                'grading': self.grading,
                'glh': self.glh,
                'mark': self.mark,
                'mark_type': self.mark_type,
                'tier': self.tier,
                'series': self.series,
                'sbs': self.sbs,
                'current': self.current,
                'sub_qualification': subqual,
                'core': self.core,
            }
        )
        return qualification

# from .qualification_data.uki.edexcel.edexcel_ial import SUBJECTS as EDEX
# from .qualification_data.ib.ib_dp import QUALIFICATIONS as IBDP
# from .qualification_data.ib.ib_myp import QUALIFICATIONS as IBMYP
# from .qualification_data.uki.oxfordaqa.oxfordaqa_epq import QUALIFICATIONS as OAQA_EPQ
# from .qualification_data.uki.cie.cie_ipq import QUALIFICATIONS as ciepq
# from .qualification_data.uki.btec.btec_il3 import QUALIFICATIONS as bteci3
def load_subjects():
    dl = DataLoader()
    # dl.load(bteci3)
    # dl.load(EDEX)
    # dl.load(IBMYP)
    # dl.load(OAQA_EPQ)
    # dl.load(IBDP)

""" 
from .data.edexcel_igcse import SUBJECTS as EDEXCEL_IGCSE
from .data.aqa_a2level import SUBJECTS as AQA_A2
from .data.aqa_aslevel import SUBJECTS as AQA_AS
from .data.cie_olevels import SUBJECTS as CIE_OL
from .data.ib_myp import SUBJECTS as IB_MYP
from .data.ib import SUBJECTS as IB
from .data.cie_igcse import SUBJECTS as CIE_IGCSE

from .data.ocr_a2level import SUBJECTS as OCR_A2
from .data.ocr_aslevel import SUBJECTS as OCR_AS

#s3= flatten_entry(TEST_AQA[0])
dl = DataLoader()

#pprint.pprint(dl.flatten_aggregate(IB[0])[0])
#element = dl.flatten_aggregate(IB[0])[6]
#pprint.pprint(dl.flatten_packet(element))
#pprint.pprint(dl.flatten_packet(IB[7]))
print(dl.count)
#dl.load(IB)

#dl.load(CIE_IGCSE)

 dl.load(EDEXCEL_IGCSE)

dl.load(AQA_A2)

dl.load(AQA_AS)

dl.load(CIE_OL)
 
dl.load(IB_MYP)

dl.load(OCR_A2)

dl.load(OCR_AS)

dl.load(IB_MYP)
 """




















