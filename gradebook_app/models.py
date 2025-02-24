from django.db import models
from register_app.models import (
    StudentQualification, EnrollmentQualification, Enrollment, ClassEnrollment, 
    CheckpointField, CheckpointYearGroup
)
from subject_app.models import Qualification, Component
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from choices import Ser
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from choices.qualification_states import ExamResultState
from choices.checkpoints import CheckpointFieldKind
from shared.utils.format_utils import truncate_html, truncate_text
from django.utils.html import escape

class QualificationExamResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_qualification = models.ForeignKey(
        StudentQualification, 
        on_delete=models.CASCADE, 
        related_name='exam_entries'
    )
    year = models.SmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2099)]
    )
    series = models.CharField(
        max_length=10,
        choices=Ser.entry_choices(),
        default=Ser.NONE.UNDEFINED,
    )
    grade = models.CharField(
        max_length=20,
    )
    mark = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)]
    )
    mark_secondary = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)]
    )
    is_final = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_final','-year', '-series'] 
        constraints = [
            UniqueConstraint(
                fields =['year', 'series', 'student_qualification'], 
                name = 'unique_qualification_exam_result',
            )
        ]

    def save(self, *args, **kwargs):
        super(QualificationExamResult, self).save(*args, **kwargs)
        if self.is_final:
            QualificationExamResult.objects.filter(
                student_qualification=self.student_qualification
            ).exclude(id=self.id).update(is_final=False)


    def clean(self):
        # Check for existing instance with the same values
        if QualificationExamResult.objects.filter(
            year=self.year, 
            series=self.series, 
            student_qualification=self.student_qualification
        ).exclude(pk=self.pk).exists():
            raise ValidationError("An entry for this year and series already exists.")
        super().clean()


    def __str__(self):
        return self.student_qualification.qualification.__str__()
    
    
    def state(self)->str:
        if self.is_final:
            return ExamResultState.FINAL.value
        if QualificationExamResult.objects.filter(
            student_qualification=self.student_qualification,
            is_final=True
        ).exists():
            return ExamResultState.OVERRIDEN.value
        else:
            return ExamResultState.PROVISIONAL.value
    
    def series_year(self):
        return f"{self.get_series_display()} {self.year}"

class ComponentExamResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_qualification = models.ForeignKey(
        StudentQualification, 
        on_delete=models.CASCADE, 
        related_name='exam_component_entries'
    )
    component = models.ForeignKey(
        Component, 
        on_delete=models.CASCADE, 
        related_name='entries'
    )
    qualification_entry = models.ForeignKey(
        QualificationExamResult, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name='components'
    )
    year = models.SmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2099)]
    )
    series = models.CharField(
        max_length=10,
        choices=Ser.entry_choices(),
        default=Ser.NONE.UNDEFINED,
    )
    grade = models.CharField(
        max_length=20,
    )
    mark = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)]
    )
    mark_adjusted = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)]
    )
    is_final = models.BooleanField(default=True) 
    available = models.BooleanField(default=True) 
    
    class Meta:
        ordering = ['-is_final', '-year', '-series'] 
        constraints = [
            UniqueConstraint(
                fields =['year', 'series', 'student_qualification', 'component'], 
                name = 'unique_component_exam_result',
            )
        ]

    def save(self, *args, **kwargs):
        super(ComponentExamResult, self).save(*args, **kwargs)
        if self.qualification_entry:
            self.is_final=self.qualification_entry.is_final
            super().save(update_fields=['is_final'])
        if self.is_final:
            ComponentExamResult.objects.filter(
                student_qualification=self.student_qualification,
                component=self.component
            ).exclude(id=self.id).update(is_final=False)


    def clean(self):
        if ComponentExamResult.objects.filter(
            year=self.year, 
            series=self.series, 
            student_qualification=self.student_qualification,
            component=self.component
        ).exclude(pk=self.pk).exists():
            raise ValidationError("An entry for this year and series already exists.")
        super().clean()

    def __str__(self):
        return self.component.__str__()
    
    def state(self)->str:
        if self.is_final:
            return ExamResultState.FINAL.value
        if ComponentExamResult.objects.filter(
            student_qualification=self.student_qualification,
            component=self.component,
            is_final=True
        ).exists():
            return ExamResultState.OVERRIDEN.value
        else:
            return ExamResultState.PROVISIONAL.value
        
    def series_year(self):
        return f"{self.get_series_display()} {self.year}"
        
    
class CheckpointEntry(models.Model):
    id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(
        Enrollment, 
        on_delete=models.CASCADE, 
        related_name='checkpoint_entries'
    )
    enrollment_qualification = models.ForeignKey(
        EnrollmentQualification, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='checkpoint_entries'
    )
    class_enrollment = models.ForeignKey(
        ClassEnrollment, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='checkpoint_entries'
    )
    checkpoint_field = models.ForeignKey(
        CheckpointField, 
        on_delete=models.CASCADE, 
        related_name='checkpoint_entries'
    )
    checkpoint_yeargroup = models.ForeignKey(
        CheckpointYearGroup, 
        on_delete=models.CASCADE, 
        related_name='checkpoint_entries'
    )
    grade = models.CharField(
        max_length=20,
        blank=True, 
        null=True
    )
    category = models.CharField(
        max_length=40, 
        blank=True, 
        null=True
    )  
    mark = models.FloatField(
        blank=True, 
        null=True
    )  
    comment = models.TextField(
        blank=True, 
        null=True,
        validators=[MaxLengthValidator(2500)]
    )  
    component = models.ForeignKey(
        Component, 
        on_delete=models.CASCADE, 
        related_name='mock_entries',
        verbose_name='Exam component',
        blank=True, 
        null=True,
    )
    
    is_excluded = models.BooleanField(
        default=False,
    )
    
    is_completed = models.BooleanField(
        default=False,
    )
    
    def save(self, *args, **kwargs):
        if self.is_always_excluded():
            self.is_excluded = True
        super().save(*args, **kwargs)
    
    def is_always_excluded(self)->bool:
        if self.checkpoint_field.kind == CheckpointFieldKind.MOCK:
            return not self.qualification().components.all().exists() 
        return False
        
    def clear(self):
        self.comment = None
        self.mark = None
        self.grade = None
        self.category = None
        
    def value(self):            
        match self.checkpoint_field.kind:
            case CheckpointFieldKind.GRADE:
                if self.qualification().mark_required:
                    return (
                        f'<div class="text-nowrap">{self.mark_formatted} / {self.qualification().mark} &nbsp; ({self.grade})</div>' 
                        if self.mark is not None else None
                    )
                return self.grade
            case CheckpointFieldKind.MARK:
                return (f'<div class="text-nowrap">{self.mark_formatted} / {self.checkpoint_field.maxmark}</div>' 
                        if self.mark is not None else None
                )
            case CheckpointFieldKind.PERCENTAGE:
                return f"{self.mark_formatted} %" if self.mark is not None else None
            case CheckpointFieldKind.COMMENT:
                text, count = truncate_html(self.comment, max_length=20)
                if not text:
                    return None
                return (f'<div class="text-nowrap"> {escape(text)}</div>'
                        f'<div class="text-nowrap">({count} / {self.checkpoint_field.maxlength})</div>')
            case CheckpointFieldKind.CATEGORICAL:
                return self.category
            case CheckpointFieldKind.MOCK:
                if not self.grade:
                    return None
                mark_str=f'&nbsp; ({self.mark_formatted} / {self.component.mark})' if self.mark else ''
                return (
                    f'<div class="text-nowrap">{self.grade} {mark_str}</div>'
                    f'<div class="text-nowrap">{truncate_text(self.component.__str__(), max_length=20)}</div>'
                )


    @property   
    def mark_formatted(self):        
        return int(self.mark) if self.mark.is_integer() else self.mark
        
    def qualification(self):
        eq = self.enrollment_qualification or self.class_enrollment.enrollment_qualification
        return eq.student_qualification.qualification if eq else None
    def bs_hx_targets(self):
        match self.checkpoint_field.kind:
            case CheckpointFieldKind.COMMENT:
                return "#form-modal-large", "#form-container-large"
            case CheckpointFieldKind.MOCK:
                return "#form-modal", "#form-container"
        return "#form-modal-small", "#form-container-small"
            
            
                