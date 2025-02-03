from choices import YearGroupSystem, YearGroupManager
from dataclasses import dataclass

@dataclass 
class YearGroupVis:
    name: str
    level: str
    default_name: str

@dataclass
class YearGroupSystemVis:
    system:  tuple

    def yeargroups(self) -> list['YearGroupVis']:
        levels = YearGroupManager.levels()
        names = YearGroupManager.names(self.system)
        default_names = YearGroupManager.names(YearGroupSystem.DEFAULT)

        yeargroups = [
            YearGroupVis(level=level, name=name, default_name=default_name)
            for level, name, default_name in zip(levels, names, default_names)
        ]
        yeargroups.reverse()
        return yeargroups

           
@dataclass
class YearGroupPresetsVis:
    @staticmethod
    def systems():
        return [
                YearGroupSystemVis(YearGroupSystem.UK), 
                YearGroupSystemVis(YearGroupSystem.IB), 
                YearGroupSystemVis(YearGroupSystem.US)
            ]
    @staticmethod
    def custom_system():
        return  YearGroupSystemVis(YearGroupSystem.CUSTOM)
   