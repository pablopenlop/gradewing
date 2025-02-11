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
        ordering = ['-year', '-series'] 
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
        ordering = ['-year', '-series'] 
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
        validators=[MaxLengthValidator(2000)]
    )  
    component = models.ForeignKey(
        Component, 
        on_delete=models.CASCADE, 
        related_name='mock_entries',
        blank=True, 
        null=True,
    )
    
    def value(self):
        match self.checkpoint_field.kind:
            case CheckpointFieldKind.GRADE:
                return self.grade
            case CheckpointFieldKind.MARK:
                return f"{self.mark_formatted} / {self.checkpoint_field.maxmark}" if self.mark is not None else None
            case CheckpointFieldKind.PERCENTAGE:
                return f"{self.mark_formatted} %" if self.mark is not None else None
            case CheckpointFieldKind.COMMENT:
                return self.comment
            case CheckpointFieldKind.CATEGORICAL:
                return self.category

    @property   
    def mark_formatted(self):        
        return int(self.mark) if self.mark.is_integer() else self.mark
            
        