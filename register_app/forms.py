from django import forms
from django.db.models import Subquery, Count
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import School, Period, YearGroup
from .models import Student, Enrollment, StudentTag
from .models import StudentProgramme, StudentQualification, EnrollmentQualification
from .models import Teacher, TeacherTag, TeachingClass
from subject_app.models import Qualification
from .models import Checkpoint, CheckpointField, CheckpointYearGroup
from ast import literal_eval
from choices import CheckpointScope, CheckpointFieldKind
from shared.utils.form_utils import widget_limits_from_validators, helptext_from_validators
from choices import QF


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '',
                'autocomplete': 'off'
            }),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }

        
        
class YearGroupForm(forms.ModelForm):
    id = forms.IntegerField(
         widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
        }), 
        required=True,
    ) 
    class Meta:
        model = YearGroup
        fields = ['custom_name', 'id']

        widgets = {
            'custom_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                'autocomplete': 'off',
            }),
          
        }


class PeriodForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }), 
        required=False
    )

    class Meta:
        model = Period
        fields = [
            'id',
            'name',
            'start_date',
            'end_date',
            'school'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                'autocomplete': 'off',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'school': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        name = cleaned_data.get("name")
        school = cleaned_data.get("school")
        period_id = self.instance.id if self.instance else None

        if not name and not school and not start_date and not end_date:
            return cleaned_data

        if end_date < start_date:
                self.add_error("end_date", "End date cannot be earlier than the start date.")
        if Period.objects.filter(name=name, school=school).exclude(id=period_id).exists():
            self.add_error('name', "A period with this name already exists.")
        
        return cleaned_data



class StudentForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }), 
        required=False
    )

    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'id',
            'school',
            'tags',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }), 
            'school': forms.NumberInput(attrs={
                'class': 'form-control',
            }), 
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['tags'].queryset = school.student_tags


class EnrollmentForm(forms.ModelForm):
    id = forms.IntegerField(
         widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
        }), 
        required= False,
    )

    class Meta:
        model = Enrollment
        fields = ['period', 'yeargroup', 'id', 'student', 'tags']
        widgets = {
            'yeargroup': forms.Select(attrs={
                'class': 'form-select',
            }),
            'period': forms.Select(attrs={
                'class': 'form-select',
            }),
            'student': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'id_enrollment_tags',
            }),
        }
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        student = self.cleaned_data.get('student')
        if student and tags:
            return tags.exclude(students=student)
        else:
            return tags
            

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        instance = kwargs.get('instance')
        
        super().__init__(*args, **kwargs)
  
        if student:
            available_periods = Period.objects.filter(school=student.school)
            existing_periods = student.enrollments.values_list('period_id', flat=True)
            if instance and instance.id:
                existing_periods = existing_periods.exclude(id=instance.id)
            self.fields['period'].queryset = available_periods.exclude(id__in=existing_periods)
            self.fields['period'].empty_label = None

            self.fields['yeargroup'].queryset= student.school.yeargroups.all()
            self.fields['yeargroup'].empty_label = None
            available_tags = student.school.student_tags.exclude(students=student)
            self.fields['tags'].queryset = available_tags

class StudentProgrammeForm(forms.ModelForm):
    class Meta:
        model = StudentProgramme
        fields = ['name', 'student']
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'student': forms.NumberInput(attrs={
                'class': 'form-control',
            }),   
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            existing_sqs = list(student.programmes.values_list('name', flat=True))
            #self.fields['name'].choices = QualificationFamily.available_grouped_choices(existing_sqs)
            self.fields['name'].choices = QF.available_grouped_choices(existing_sqs)
            for fieldname in ['name']:
                self.fields[fieldname].choices = [("", "")] + list(self.fields[fieldname].choices)



class StudentQualificationForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }), 
        required=False
    )
    class Meta:
        model = StudentQualification
        fields = ['id', 'qualification', 'programme', 'enrollments']
        widgets = {
            'qualification': forms.Select(attrs={
                'class': 'form-control',
            }),
            'programme':  forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'enrollments': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),     
        }
    def __init__(self, *args, **kwargs):
        programme = kwargs.pop('programme', None)
        super().__init__(*args, **kwargs)
        if programme:
            # Enrollments queryset
            self.fields['enrollments'].queryset = programme.student.enrollments
            # Qualification queryset
            if self.instance and self.instance.pk:
                self.fields['qualification'].queryset = Qualification.objects.filter(id=self.instance.qualification_id)
                self.fields['qualification'].empty_label = None 
            elif programme:
                
                qfam = QF.choices_from_values(programme.name)[0]
                qnames = QF.get_qualification_name_choices(qfam, values_only=True)
                available_qualifications = Qualification.objects.filter(name__in=qnames)
                #existing_qualifications = programme.qualifications.values_list('qualification_id', flat=True)
                existing_qualifications = programme.student.qualifications().values_list('qualification_id', flat=True)
                available_qualifications = available_qualifications.exclude(id__in=existing_qualifications)
                self.fields['qualification'].queryset = available_qualifications
        
        
            
            
            """ GROUPED CHOICES ..TOO SLOW
            # Group qualifications by board
            grouped_choices = []
            boards = available_qualifications.values_list('board', flat=True).distinct()
            for board in boards:
                # Get the "nice" name for each board using get_board_display()
                board_nice_name = available_qualifications.filter(board=board).first().get_board_display()
                board_qualifications = available_qualifications.filter(board=board)
                grouped_choices.append((board_nice_name, [(qual.id, qual.title) for qual in board_qualifications]))
            # Assign the grouped choices to the qualification field
            self.fields['qualification'].choices = grouped_choices 
            """

 
""" class StudentQualificationPeriodForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        required=True
    )
    class Meta:
        model = StudentQualification
        fields = ['enrollments', 'id']
        widgets = {
            'enrollments': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            
        }
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            available_enrollments = student.enrollments
            self.fields['enrollments'].queryset = available_enrollments """



class TeacherForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }), 
        required=False
    )

    class Meta:
        model = Teacher
        fields = [
            'id',
            'school',
            'first_name',
            'last_name',
            'email',
            'gender',
            'periods',
            'tags'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
                
            }),
            'school': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'periods': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['tags'].queryset = school.teacher_tags
            self.fields['periods'].queryset = school.periods


class BaseTagForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=False
    )

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.upper()

    class Meta:
        fields = ['id', 'name', 'school']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'style': 'text-transform: uppercase;',
            }),
            'school': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }

class StudentTagForm(BaseTagForm):
    class Meta(BaseTagForm.Meta):
        model = StudentTag

class TeacherTagForm(BaseTagForm):
    class Meta(BaseTagForm.Meta):
        model = TeacherTag



class AddStudentTagsForm(forms.Form):
    CHOICES = [
    ("Learning Disabilities", [
        ("ADHD", "ADHD"),
        ("AUTISM", "AUTISM"),
        ("DYSLEXIA", "DYSLEXIA"),
        ("DYSCALCULIA", "DYSCALCULIA"),
        ("DYSGRAPHIA", "DYSGRAPHIA"),
        ("HEARING IMPAIRMENT", "HEARING IMPAIRMENT"),
        ("INTELLECTUAL DISABILITY", "INTELLECTUAL DISABILITY"),
        ("SEND", "SEND"),
        ("SPEECH IMPAIRMENT", "SPEECH IMPAIRMENT"),
        ("VISUAL IMPAIRMENT", "VISUAL IMPAIRMENT"),
    ]),
    ("Emotional Disturbance", [
        ("ANXIETY", "ANXIETY"),
        ("BLINDNESS", "BLINDNESS"),
        ("DEAFNESS", "DEAFNESS"),
        ("EMOTIONAL DISTURBANCE", "EMOTIONAL DISTURBANCE"),
        ("SEMH", "SEMH"),
    ]),
    ("Physical & Health", [
        ("CHRONIC FATIGUE", "CHRONIC FATIGUE"),
        ("DIABETES", "DIABETES"),
        ("EPILEPSY", "EPILEPSY"),
    ]),
    ("Ability", [
        ("GIFTED", "GIFTED"),
        ("HIGH ABILITY", "HIGH ABILITY"),
        ("LOW ABILITY", "LOW ABILITY"),
    ]),
    ]
    tags = forms.CharField(
        widget=forms.SelectMultiple(
            choices=CHOICES,
            attrs={
            'class': 'form-select',
        }),
        label="Student tags",
        required=False,
    )

    def clean_tags(self):
        tags_str = self.cleaned_data['tags']
        return literal_eval(tags_str)




class AddTeacherTagsForm(forms.Form):
    CHOICES = [
        ("Department or Subject", [
            ("ART", "ART"),
            ("BIOLOGY", "BIOLOGY"),
            ("BUSINESS", "BUSINESS"),
            ("CHEMISTRY", "CHEMISTRY"),
            ("COMPUTER SCIENCE", "COMPUTER SCIENCE"),
            ("ECONOMICS", "ECONOMICS"),
            ("ENGLISH", "ENGLISH"),
            ("FURTHER MATHEMATICS", "FURTHER MATHEMATICS"),
            ("FRENCH", "FRENCH"),
            ("GEOGRAPHY", "GEOGRAPHY"),
            ("HISTORY", "HISTORY"),
            ("MATHEMATICS", "MATHEMATICS"),
            ("MEDIA", "MEDIA"),
            ("MUSIC", "MUSIC"),
            ("PE", "PE"),  
            ("PHYSICS", "PHYSICS"),
            ("PSYCHOLOGY", "PSYCHOLOGY"),
            ("SPANISH", "SPANISH"),
        ]),
        ("Programme", [
            ("A LEVEL", "A LEVEL"),
            ("BTEC", "BTEC"),
            ("EPQ", "EPQ"),
            ("GCSE", "GCSE"),
            ("IAL", "IAL"),
            ("IB DP", "IB DP"),
            ("IGCSE", "IGCSE"),
        ]),
        ("Role", [
            ("EXAMINER", "EXAMINER"),
            ("FORM TUTOR", "FORM TUTOR"),
            ("HEAD OF DEPARTMENT", "HEAD OF DEPARTMENT"),
            ("HEAD OF SUBJECT", "HEAD OF SUBJECT"),
            ("MENTOR", "MENTOR"),
            ("SLT", "SLT"), 
        ]),
        ("Specializations", [
            ("CAREERS ADVISOR", "CAREERS ADVISOR"),
            ("EAL SPECIALIST", "EAL SPECIALIST"),  
            ("SEND COORDINATOR", "SEND COORDINATOR"),  
            ("SEND SPECIALIST", "SEND SPECIALIST"),  
        ]),
    ]
    
    tags = forms.CharField(
        widget=forms.SelectMultiple(
            choices=CHOICES,
            attrs={
            'class': 'form-select',
        }),
        label="Teacher tags",
        required=False,
    )

    def clean_tags(self):
        tags_str = self.cleaned_data['tags']
        return literal_eval(tags_str)





class TeachingClassPreForm1(forms.ModelForm):
    
    class Meta:
        model = TeachingClass
        fields = [
            'period',
        ]
        widgets = {
            'period': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        help_texts = {
            'period':   """Only academic periods with at least one taught qualification 
                        and one allocated teacher are available as options.""",
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['period'].queryset = school.teachable_periods()

        
class TeachingClassPreForm2(forms.ModelForm):
    class Meta:
        model = TeachingClass
        fields = [
            'period',
            'qualification',
        ]
        widgets = {
            'period': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'qualification': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        period = kwargs.pop('period', None)
        super().__init__(*args, **kwargs)
        if period:
            self.fields['qualification'].queryset = period.qualifications()


class TeachingClassForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=False
    )
    class Meta:
        model = TeachingClass
        fields = [
            'id',
            'period',
            'qualification',
            'name', 
            'yeargroup',
            'teachers',
            'enrollment_qualifications'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'off',
            }),
            'period': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'qualification': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'yeargroup': forms.Select(attrs={
                'class': 'form-select',
            }),
            'teachers': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'enrollment_qualifications': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'enrollment_qualifications': 'Students',
        }
        
    def __init__(self, *args, **kwargs):
        period = kwargs.pop('period', None)
        qualification = kwargs.pop('qualification', None)
        super().__init__(*args, **kwargs)
        if period:
            self.fields['teachers'].queryset = period.teachers.all()
 
            eqs = EnrollmentQualification.objects.filter(
                enrollment__period=period,
                student_qualification__qualification__id=qualification.id
            )

            self.fields['enrollment_qualifications'].queryset = eqs 
            self.fields['enrollment_qualifications'].label_from_instance = (
                lambda obj: f"{obj.enrollment.student.catalog_name} [{obj.enrollment.yeargroup}]"
            )

            self.fields['yeargroup'].queryset = YearGroup.objects.filter(
                enrollments__enrollment_qualifications__in=eqs
            ).distinct()
            
            self.fields['yeargroup'].empty_label = None

      
class CheckpointPreForm1(forms.ModelForm):
    class Meta:
        model = Checkpoint
        fields = [
            'period',
            'scope', 
        ]
        widgets = {
            'period': forms.Select(attrs={
                'class': 'form-select',
            }),
            'scope': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        help_texts = {
            'scope': """
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <b>Subject Class Landmark</b>
                        <ul  style="list-style-type: disc; padding-left: 15px; ">
                            <li>Comprises subject grades and other subject performance indicators of pupils in a <b>teaching class</b>, set by teachers.</li>
                            <li><i>Suitable for working grades, effort grades, internal and mock exam results.</i></li>
                        </ul>
                    </li>
                    <li class="list-group-item">
                        <b>Subject Benchmark</b>
                        <ul  style="list-style-type: disc; padding-left: 15px; ">
                            <li>Comprises subject grades and other subject performance indicators, set exclusively by senior leadership.</li>
                            <li><i>Suitable for target grades and predicted grades.</i></li>
                        </ul>
                    </li>
                    <li class="list-group-item">
                        <b>Generic Benchmark</b>
                        <ul  style="list-style-type: disc; padding-left: 15px; ">
                            <li>Comprises generalized performance indicators, set exclusively by senior leadership.</li>
                            <li><i>Suitable for results of cognitive and other standardized tests.</i></li>
                        </ul>
                    </li>
                </ul>
            """
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['period'].queryset = school.periods.all()
            self.fields['period'].empty_label = None
        

class CheckpointPreForm2(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=False
    )
    class Meta:
        model = Checkpoint
        fields = [
            'id',
            'period',
            'scope', 
            'name',
            'date',
            'yeargroups',
        ]
        widgets = {
            'period': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'scope': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
        }
    
            
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        period = self.initial.get('period', self.data.get('period'))
        self.yeargroup_data = {}
        if school:
            self.fields['date'].help_text = f"{period.period}"

                
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        period = cleaned_data.get("period")
        if date > period.end_date or date < period.start_date:
                self.add_error("date", "The checkpoint date must fall within the selected academic period.")        
        return cleaned_data
    
    
class CheckpointFieldForm(forms.ModelForm):

    CHOICES = [
        ("General descriptors", [
            ("Excellent", "Excellent"),
            ("Outstanding", "Outstanding"),
            ("Very good", "Very good"),
            ("Good", "Good"),
            ("Satisfactory", "Satisfactory"),
            ("Needs Improvement", "Needs Improvement"),
            ("Poor", "Poor"),
        ]),
        ("Behaviour descriptors", [
            ("Exemplary", "Exemplary"),
            ("Cooperative", "Cooperative"),
            ("Disruptive", "Disruptive"),
            ("Unacceptable", "Unacceptable"),
        ]),
        ("Expectations", [
            ("Exceeds Expectations", "Exceeds Expectations"),
            ("Meets Expectations", "Meets Expectations"),
            ("Partially Meets Expectations", "Partially Meets Expectations"),
            ("Below Expectations", "Below Expectations"),
        ]),
        ("Gradeset", [
            ("A*", "A*"),
            ("A", "A"),
            ("B+", "B+"),
            ("B", "B"),
            ("C+", "C+"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("F", "F"),
            ("U", "U"),
        ]),
        ("Binary", [
            ("Pass", "Pass"),
            ("Fail", "Fail"),
            ("Yes", "Yes"),
            ("No", "No"),
        ]),
    ]

    categories = forms.CharField(
        widget=forms.SelectMultiple(
            choices=CHOICES,
            attrs={
            'class': 'form-control',
        }),
        label="Categories",
        required=True,
    )
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=False
    )
    class Meta:
        model = CheckpointField
        fields = [
            'id',
            'checkpoint',
            'kind',
            'name',
            'minmark',
            'maxmark',
            'minlength',
            'maxlength',
            'stepsize',
            'categories'
        ]
        widgets = {
            'checkpoint': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Field name',
            }),
             'kind': forms.TextInput(attrs={
                'class': "form-control" ,
                'readonly': 'readonly',
            }),
            'maxmark': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'onkeypress': "return (event.charCode >= 48 && event.charCode <= 57) || event.keyCode === 13"
            }),
            'minmark': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'onkeypress': "return (event.charCode >= 48 && event.charCode <= 57) || event.keyCode === 13"
            }),
            'stepsize': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': '',
            }),
            'maxlength': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'onkeypress': "return (event.charCode >= 48 && event.charCode <= 57) || event.keyCode === 13"
            }),
            'minlength': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'onkeypress': "return (event.charCode >= 48 && event.charCode <= 57) || event.keyCode === 13"
            }),
        }
    
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kind = self.initial.get('kind', self.data.get('kind'))
        self.fields['categories'].required = False
        
        for field_name in ['minmark', 'maxmark', 'minlength', 'maxlength']:
            widget_limits_from_validators(self, field_name)
            helptext_from_validators(self, field_name)
                
        if kind == CheckpointFieldKind.MARK:
            self.fields['stepsize'].required = True 
            self.fields['maxmark'].required = True
            self.fields['minmark'].required = True
            self.fields['stepsize'].choices = CheckpointField.STEP_CHOICES
            if not self.instance.pk:
                self.fields['minmark'].initial = 0
                self.fields['maxmark'].initial = 10
                self.fields['stepsize'].initial = 0.01
            self.fields['stepsize'].choices = CheckpointField.STEP_CHOICES
                
        elif kind == CheckpointFieldKind.PERCENTAGE:
            self.fields['stepsize'].required = True 
            self.fields['maxmark'].required = True
            self.fields['minmark'].required = True
            
            self.fields['stepsize'].choices = CheckpointField.STEP_CHOICES
            self.fields['maxmark'].widget.attrs.update({'readonly': 'readonly'})
            self.fields['minmark'].widget.attrs.update({'readonly': 'readonly'})
            self.fields['maxmark'].help_text = ""
            self.fields['minmark'].help_text = ""
            if not self.instance.pk:
                self.fields['minmark'].initial = 0
                self.fields['maxmark'].initial = 100
            
        elif kind == CheckpointFieldKind.GRADE:
            self.fields['kind'].help_text = """
            This field includes a grade entry for each subject qualification.
            """
        elif kind == CheckpointFieldKind.MOCK:
            self.fields['kind'].help_text = """
            This field includes a grade & mark entry from one selected exam component for each subject qualification.
            """
        elif kind == CheckpointFieldKind.COMMENT:
            if not self.instance.pk:
                self.fields['maxlength'].initial = 1000
                self.fields['minlength'].initial = 0
                self.fields['maxlength'].required = True
                self.fields['minlength'].required = True
                
        elif kind == CheckpointFieldKind.CATEGORICAL:
            self.fields['categories'].required = True   
       
                
    def clean(self):
        cleaned_data = super().clean()
        kind = cleaned_data.get("kind")
        if kind == CheckpointFieldKind.MARK: 
            stepsize = cleaned_data.get("stepsize")
            minmark = cleaned_data.get("minmark")
            maxmark = cleaned_data.get("maxmark")
            if minmark >= maxmark:
                self.add_error("maxmark", "The maximum mark must exceed the minimum mark by at least 1 mark.")
            if float(stepsize) > maxmark-minmark:
                self.add_error("stepsize", "The selected mark step size is too large.")
            
        elif kind == CheckpointFieldKind.COMMENT:    
            minlength = cleaned_data.get("minlength")
            maxlength = cleaned_data.get("maxlength")   
            if maxlength - minlength<10:
                self.add_error("maxlength", "The maximum character count must exceed the minimum by at least 10 characters.") 
        elif kind == CheckpointFieldKind.CATEGORICAL:
            categories = cleaned_data.get("categories")
            if len(categories)<2:
                self.add_error("categories", "At least two categories should be provided.") 
            elif len(categories)>10:
                self.add_error("categories", "No more than ten categories should be provided.")

        checkpoint = cleaned_data.get("checkpoint")
        name = cleaned_data.get("name")
        checkpointfield_id = self.instance.id if self.instance else None
        if CheckpointField.objects.filter(name=name, checkpoint=checkpoint).exclude(id=checkpointfield_id).exists():
            self.add_error('name', "This checkpoint already contains a field with this name.")
        return cleaned_data
        
    def clean_categories(self):
        categories_str = self.cleaned_data['categories']
        if categories_str:
            return literal_eval(categories_str)
            

class CheckpointYeargroupForm(forms.ModelForm):
    class Meta:
        yeargroup = forms.ModelChoiceField(
            queryset=YearGroup.objects.none(), 
            widget=forms.Select(attrs={'class': 'form-select'}),
            empty_label=None  
        )
        
        model = CheckpointYearGroup
        fields = ['checkpoint', 'yeargroup']
        widgets = {
            'checkpoint': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'yeargroup': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        
    
    def __init__(self, *args, **kwargs):
        checkpoint = kwargs.pop('checkpoint', None)
        super().__init__(*args, **kwargs)
    
        if checkpoint:  
            eligible_ygs = checkpoint.period.school.yeargroups.exclude(
                id__in=checkpoint.yeargroups.values_list('id', flat=True)
            )
            self.fields['yeargroup'].queryset = eligible_ygs
            self.fields['yeargroup'].empty_label = None


   