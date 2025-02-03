from .models import Qualification, Component
from dataclasses import dataclass, field
from typing import Optional, List, Union
from choices import QT, QK, SG, Ser, Tier, MT, GS, Board
from fractions import Fraction
import pprint

def frac_to_percent_str(a, b)->str:
    frac = Fraction(a, b)
    percentage = frac * 100
    int_part, frac_part = divmod(percentage, 1)
    if frac_part == Fraction(1, 3):
        return f"{int(int_part)}⅓ %"
    elif frac_part == Fraction(2, 3):
        return f"{int(int_part)}⅔ %"
    elif frac_part == Fraction(1, 2):
        return f"{float(percentage):.1f} %"
    else:
        return f"{float(percentage):.0f} %"

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
    series: Optional[List[Ser.choices]] = None
    glh: Optional[int] = None
    qualification: Optional['QualificationLoad'] = None

    def __post_init__(self):
        self.set_glh_based_weighting()
        self.set_series()
    
    
    def fill_code(self, parent_code: str)->None:
        self.code = self.code.replace('*', parent_code)

    def set_glh_based_weighting(self):
        if self.weighting == "glh":
            self.weighting = frac_to_percent_str(self.glh, self.qualification.glh)

    def set_series(self):
        if not self.series:
            self.series = self.qualification.series

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
                'series': self.series,
                'qualification': self.qualification.to_model(),
            }
        )
        return component
    

@dataclass
class QualificationLoad:
    subject: str
    code: str
    name: QT.choices
    kind: QK.choices
    suite: QT.suite_choices
    grading: GS.choices
    board: Board.choices
    group: SG.choices
    mark: int
    mark_type: MT.choices
    first_assessment: int
    modular: bool
    series: List[Ser.choices]
    glh: int
    components: List[ComponentLoad] = field(default_factory=list)
    current: bool = True
    last_assessment: Optional[int] = None
    tier: Tier = Tier.NONE
    sbs: bool = False
    suffix: Optional[str] = None
    sub_qualification: Optional[str] = None
    core: bool = False
    mark_secondary: Optional[int] = None
    mark_secondary_type: MT = MT.NONE
    
    def add_component(self, component: ComponentLoad)->None:
        component.fill_code(self.code)
        self.components.append(component)

    def __post_init__(self):
        self.refine_subject()

    def refine_subject(self)->None:
        pass
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
        #--------------------------
        suite = QT.get_suite_from_choice(element["name"])
        board = QT.get_board_from_choice(element["name"])
        kind = QK.get_kind_from_name(element["name"])

        qualification = cls(**element, suite=suite, board=board, kind=kind)
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
                'mark_secondary': self.mark_secondary,
                'mark_secondary_type': self.mark_secondary_type,
            }
        )
        return qualification

from .qualification_data.uki.edexcel.edexcel_ial import SUBJECTS as edexcel_ial
from .qualification_data.ib.ib_dp import QUALIFICATIONS as ib_dp
from .qualification_data.ib.ib_myp import QUALIFICATIONS as ib_myp
from .qualification_data.uki.oxfordaqa.oxfordaqa_igcse import QUALIFICATIONS as oxfordaqa_igcse
from .qualification_data.uki.oxfordaqa.oxfordaqa_epq import QUALIFICATIONS as oxfordaqa_epq
from .qualification_data.uki.cie.cie_olevels import QUALIFICATIONS as cie_olevels
from .qualification_data.uki.cie.cie_ial import QUALIFICATIONS as cie_ial

from .qualification_data.uki.cie.cie_ipq import QUALIFICATIONS as cie_ipq
from .qualification_data.uki.btec.btec_il3 import QUALIFICATIONS as btec_il3
from .qualification_data.uki.btec.btec_il2 import QUALIFICATIONS as btec_il2

from .qualification_data.ukn.ocr.ocr_gcse import QUALIFICATIONS as ocr_gcse
from .qualification_data.ukn.aqa.aqa_a2 import QUALIFICATIONS as aqa_a2
from .qualification_data.ukn.edexcel.edexcel_as import QUALIFICATIONS as edexcel_as
from .qualification_data.ukn.btec.btec_aaq import QUALIFICATIONS as btec_aaq
from .qualification_data.ukn.ocr.ocr_epq import QUALIFICATIONS as ocr_epq
from .qualification_data.ukn.aqa.aqa_ag import QUALIFICATIONS as aqa_ag
from .qualification_data.ukn.btec.btec_firsts import QUALIFICATIONS as btec_firsts
def load_subjects():
    dl = DataLoader()
    dl.load(cie_ial)
    dl.load(edexcel_ial)
    dl.load(oxfordaqa_igcse)
    dl.load(cie_olevels)
    dl.load(oxfordaqa_igcse)
    dl.load(btec_il3)
    dl.load(btec_il2)
    dl.load(cie_ipq)
    dl.load(oxfordaqa_epq)
    dl.load(ib_dp)
    dl.load(ib_myp)
    dl.load(ocr_gcse)
    dl.load(aqa_a2)
    dl.load(edexcel_as)
    dl.load(btec_aaq)
    dl.load(ocr_epq)
    dl.load(aqa_ag)
    dl.load(btec_firsts)

#load_subjects()
#dl = DataLoader()
#dl.load(btec_firsts)

