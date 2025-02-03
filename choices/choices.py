from abc import ABC
from typing import Union
from django.db import models
from inspect import isclass

class ComplexChoices(ABC):
    class NONE(models.TextChoices):
        UNDEFINED = 'nan.undefined', 'Other'
        NONE = 'nan.none', ''
        NA = 'none.na', 'Not available'
        NAP = 'none.nap', 'Not applicable'


    @classmethod
    def choices(cls):
        """ Returns a list of Enums (models.TextChoices)"""
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
    def choices_from_values_old(cls, codes: Union[str, list[str]]) -> list:
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
    
    @classmethod
    def _get_all_textchoices_subclasses(cls):
        subclasses = []
        
        # Inspect all attributes of the class
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name, None)
            if isclass(attr) and issubclass(attr, models.TextChoices):
                subclasses.append(attr)

        return subclasses

    @classmethod
    def choices_from_values(cls, codes: Union[str, list[str]]) -> list:
        """ Returns a list of Enums (models.TextChoices)"""
        result = []

        # Get all subclasses of TextChoices, including statically defined ones
        choices_classes = cls._get_all_textchoices_subclasses()

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
    