from django import forms
from gradebook_app.models import QualificationExamResult, ComponentExamResult
from choices import GS
from django.core.validators import MinValueValidator, MaxValueValidator
class QualificationExamResultForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }), 
        required=False
    )
    grade = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    class Meta:
        model = QualificationExamResult
        fields = ['id', 'year', 'series', 'grade', 'mark', 'mark_secondary', 'is_final', 'student_qualification']
        widgets = {
            'series': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Exam series',
            }),    
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'mark_secondary': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'is_final': forms.CheckboxInput(attrs={
                'class': 'form-check-input check-input-lg',
               
            }),
            'student_qualification': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
        }
        help_texts = {
            'is_final':   """
                Qualification will not be retaken and no component is awaiting a remark.
            """,
        }

    def __init__(self, *args, qualification=None, **kwargs):
        super().__init__(*args, **kwargs)
        year_dbfield = self._meta.model._meta.get_field('year')
        for v in year_dbfield.validators:
            if isinstance(v, MinValueValidator):
                self.fields['year'].widget.attrs.update({'min': v.limit_value})
            elif isinstance(v, MaxValueValidator):
                self.fields['year'].widget.attrs.update({'max': v.limit_value})

        if qualification:
            self.fields['series'].choices = qualification.get_form_series()
            grading = GS.choices_from_values(qualification.grading)[0]
            self.fields['grade'].choices = GS.grade_tuples(grading)
            self.fields['mark'].widget.attrs.update({'max': qualification.mark})
            self.fields['mark'].widget.attrs.update({'min': 0})
            #self.fields['mark_adjusted'].widget.attrs.update({'max': qualification.mark_adjusted})


class ComponentExamResultForm(forms.ModelForm):
    id = forms.IntegerField(
         widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': 'readonly',
        }), 
        required=False
    )
    grade = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={
        'class': 'form-select',
        })
    )

    undertaken = forms.BooleanField(
        required=False,
           widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input mx-1',
            }),
    )
    class Meta:
        model = ComponentExamResult
        fields = [
            'id', 'year', 'series', 'grade', 'mark', 
            'is_final', 'student_qualification',
            'mark_adjusted', 'component', 'available',
        ]
        widgets = {
            'series': forms.Select(attrs={
                'class': 'form-select',

            }),    
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'mark_adjusted': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': '',
            }),
            'is_final': forms.CheckboxInput(attrs={
                'class': 'form-check-input  check-input-lg',
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input mx-1',
                'pointer-events': 'none',
            }),
            
            'student_qualification': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'component': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
        }
        help_texts = {
            'is_final': """
                Examination will not be retaken or remarked.
            """
        }

    def __init__(self, *args, component=None, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['undertaken'].initial = True

        if component:
            
            self.fields['series'].choices = component.get_form_series()
            print("aaa, ", component.grading)
            grading = GS.choices_from_values(component.grading)
            print(grading)
            grading = GS.choices_from_values(component.grading)[0]
            
            self.fields['grade'].choices = GS.grade_tuples(grading)
            self.fields['mark'].widget.attrs.update({'max': component.mark})
            self.fields['mark'].widget.attrs.update({'min': 0})
            self.fields['mark_adjusted'].widget.attrs.update({'max': component.mark_adjusted})