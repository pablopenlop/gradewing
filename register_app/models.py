from django.db import models
from django.db.models import Case, When, Value, IntegerField
from choices.qualification_family import QualificationFamily
from choices.yeargroups import YearGroupLevel, YearGroupSystem, YearGroupManager 
from choices.checkpoints import CheckpointScope, CheckpointFieldKind, CheckpointState 
from choices.people import Gender
from choices import QF
from subject_app.models import Qualification
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from choices.qualification_states import QualificationState
from typing import Union
from django.db.models import Count, Q
from math import floor
class StudentQualificationManager(models.Manager):
    def ordered_by_qualifications(self):
        return self.get_queryset().annotate(
            has_sub_qualification=Case(
                When(sub_qualification__isnull=False, then=Value(1)),
                When(super_qualification__isnull=False, then=Value(3)),
                default=Value(2),  # Neither sub_qualification nor super_qualification
                output_field=IntegerField(),
            )
        ).order_by('has_sub_qualification', 'qualification__title')
    
class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="School name")
    yeargroup_system = models.CharField(
        max_length=10,
        choices=YearGroupSystem.choices,
        default= YearGroupSystem.CUSTOM,
    )
    country = CountryField(default='GB')
    def __str__(self):
        return self.name
    

    def teachable_periods(self):
        # Get periods with at least one teacher
        periods = self.periods.filter(teachers__isnull=False).distinct()
        # Filter periods that have qualifications using the qualifications() method
        periods = [p for p in periods if p.qualifications().exists()]
        # Set the queryset for the period field
        return self.periods.filter(id__in=[p.id for p in periods])


class TeacherTag(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_tags')
    name = models.CharField(max_length=30, verbose_name="Teacher tag")
    def __str__(self):
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'school'], name='unique_student_tag')
        ]
        ordering = ['school', 'name']

class StudentTag(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='student_tags')
    name = models.CharField(max_length=30, verbose_name="Student tag")
    def __str__(self):
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'school'], name='unique_teacher_tag')
        ]
        ordering = ['school', 'name']


class YearGroup(models.Model):
    id = models.AutoField(primary_key=True)
    custom_name = models.CharField(max_length=25)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='yeargroups')
    level = models.CharField(
        max_length=10,
        choices=YearGroupLevel.choices,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['level', 'school'], name='unique_level'),
            models.UniqueConstraint(fields=['custom_name', 'school'], name='unique_custom_name')
        ]
        ordering = ['level']
        
    @property
    def name(self):
        if self.school.yeargroup_system==YearGroupSystem.CUSTOM:
            return self.custom_name
        return YearGroupManager.names(system=self.school.yeargroup_system, level=self.level)
    
    def __str__(self):
        return self.name
    
    def index(self):
        return ''.join(filter(str.isdigit,  self.level))
    
 
class Period(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Period ID")
    name = models.CharField(max_length=35, unique=False, verbose_name="Period name")
    start_date = models.DateField(verbose_name="Start date")
    end_date = models.DateField(verbose_name="End date")
    current = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='periods')

    class Meta:
        ordering = ['-start_date'] 
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'school'], 
                name='unique_period_per_school')
        ]
        
    def __str__(self):
        return self.name

    @property
    def period(self):
        return f"{self.start_date.strftime('%d %b. %Y')} – {self.end_date.strftime('%d %b. %Y')}"

    def save(self, *args, **kwargs):
        if self.current:
            Period.objects.filter(school=self.school, current=True).exclude(id=self.id).update(current=False)
        if not Period.objects.filter(school=self.school).exclude(id=self.id).exists():
            self.current = True
        super(Period, self).save(*args, **kwargs)
    
    def qualifications(self):
        return Qualification.objects.filter(student_qualifications__enrollments__period_id=self.id)
    


class Person(models.Model):
    first_name = models.CharField(max_length=40, verbose_name="First name")
    last_name = models.CharField(max_length=40, db_index=True, verbose_name="Last name") 
    email = models.EmailField(blank=True, max_length=50, verbose_name="Email address")
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.UNDEFINED,
        verbose_name="Gender"
    )

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name'] 

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def catalog_name(self):
        return f"{self.last_name}, {self.first_name}"

    def __str__(self):
        return self.catalog_name

class Student(Person):
    id = models.AutoField(primary_key=True, verbose_name="Student ID")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    tags = models.ManyToManyField(StudentTag, related_name='students', blank=True,  verbose_name="Permanent student tags") 
    periods = models.ManyToManyField(Period, related_name='students', blank=True,  through='Enrollment', verbose_name="Academic periods")
    
    def can_enroll(self)->bool:
        used_periods = self.enrollments.count()
        available_periods = self.school.periods.count()
        return used_periods<available_periods
    
    def update_enrollment_tags(self):
        permanent_tags = self.tags.all()
        if permanent_tags:
            enrollments = self.enrollments.filter(tags__in=permanent_tags)
            for enrollment in enrollments:
                enrollment.tags.remove(*permanent_tags)
    
    def can_add_programme(self):
        used_families = self.programmes.count()
        return  used_families < QF.count()
    
    def qualifications(self):
        return StudentQualification.objects.filter(programme__in=self.programmes.all())
    
    def last_enrollment(self):
        return self.enrollments.first()
        
    def external_qualifications(self):
        return self.qualifications().filter(enrollments__isnull=True)

    
    def get_programmes_with_external_qualifications(self):
        """
        Returns a dictionary where the key is the programme and the value is 
        a queryset of external qualifications associated with this student and programme.
        Programmes with zero qualifications are excluded.
        """
        return {
            programme: programme.qualifications.filter(enrollments__isnull=True, programme=programme)
            for programme in self.programmes.all()
            if programme.qualifications.filter(enrollments__isnull=True, programme=programme).exists()
        }



class Teacher(Person):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    periods = models.ManyToManyField(Period, related_name='teachers', blank=True,  verbose_name="Academic periods") 
    tags = models.ManyToManyField(TeacherTag, related_name='teachers', blank=True,  verbose_name="Tags") 

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Enrollment ID")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="enrollments")
    yeargroup = models.ForeignKey(YearGroup, on_delete=models.CASCADE, related_name="enrollments")
    tags = models.ManyToManyField(StudentTag, related_name='enrollments', blank=True,  verbose_name="Student enrollment tags") 

    def __str__(self):
        return self.period.name
    
    def get_programmes(self):
        return set(sq.programme for sq in self.student_qualifications.all())

    def tags_as_list(self)->list:
        return [tag.__str__() for tag in self.student.tags.all()] + [tag.name for tag in self.tags.all()]  
      
    def get_programmes_with_qualifications(self):
        """
        Returns a dictionary where the key is the programme and the value is 
        a queryset of qualifications associated with this enrollment and programme.
        """
        programmes = self.get_programmes()
        programme_qualifications = {
            programme: programme.qualifications.filter(enrollments=self)
            for programme in programmes
        }
        return programme_qualifications
    
    def programmes_as_list(self)->list:
        return [
            f"{programme.__str__()} ({qualifications.count()})" for 
            programme, qualifications in self.get_programmes_with_qualifications().items()
        ]
    
    def on_checkpoint(self, checkpoint_id: int) -> bool:
        return self.checkpoint_yeargroups.filter(checkpoint_id=checkpoint_id).exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'period'], name='unique_student_period')
        ]
        ordering = ['-period__start_date']



class StudentProgramme(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='programmes')
    name = models.CharField(
        verbose_name="Qualification programme",
        max_length=20,
        choices=QualificationFamily.grouped_choices(),
    default=QualificationFamily.NONE.UNDEFINED,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'name'], name='unique_student_name')
        ]
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()
    


class StudentQualification(models.Model):
    id = models.AutoField(primary_key=True)
    qualification = models.ForeignKey(
        'subject_app.Qualification', 
        on_delete=models.CASCADE, 
        related_name="student_qualifications", 
        verbose_name="Qualification title"
    )
    programme = models.ForeignKey(StudentProgramme, on_delete=models.CASCADE, related_name="qualifications")
    enrollments = models.ManyToManyField(
        Enrollment, 
        through="EnrollmentQualification", 
        related_name='student_qualifications', 
        blank=True, 
        verbose_name="Enrollment periods") 
    sub_qualification = models.OneToOneField(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='super_qualification'
    )
    objects = StudentQualificationManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['programme', 'qualification'], name='unique_student_qualification')
        ]

    def __str__(self):
        return f"{self.qualification.title}"
    
    def representative_exam_result(self):
        fqer = self.exam_entries.filter(is_final=True).first()
        return fqer if fqer else self.exam_entries.first()
    
    def is_external(self)->bool:
        return not(self.enrollments.exists())
    
    def state(self)->str:
        if self.exam_entries.filter(is_final=True).exists():
            return QualificationState.AWARDED.value
        elif self.exam_entries.filter(is_final=False).exists():
            return QualificationState.PROVISIONAL.value
        else:
            return QualificationState.PENDING.value

    def has_tag(self):
        return bool(self.qualification.aggregate) or bool(self.super_qualification)
    
    def tag(self):
        if self.qualification.aggregate:
            return {
                'name': 'AGG', 
                'description': 'Aggregate qualification'
            }
        if self.super_qualification:
            return {
                'name': 'SUB', 
                'description': f'''Subqualification included in
                {self.super_qualification.qualification.title}
                '''
            }
        return None

class EnrollmentQualification(models.Model):
    id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(
        Enrollment, 
        on_delete=models.CASCADE, 
        verbose_name="Enrollment", 
        related_name="enrollment_qualifications"
    )
    student_qualification = models.ForeignKey(
        StudentQualification, 
        on_delete=models.CASCADE, 
        verbose_name="Student qualification", 
        related_name="enrollment_qualifications"
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'student_qualification'], 
                name='unique_enrollment_qualification'
            )
        ]
        
    def on_checkpoint(self, checkpoint_id: int) -> bool:
        return self.checkpoint_yeargroups.filter(checkpoint_id=checkpoint_id).exists()
    
    
class TeachingClass(models.Model):
    id = models.AutoField(primary_key=True)
    yeargroup = models.ForeignKey(YearGroup, on_delete=models.CASCADE, verbose_name="Year group (class)", related_name="teaching_classes")
    teachers = models.ManyToManyField(Teacher, related_name='teaching_classes') 
    enrollment_qualifications = models.ManyToManyField(
        EnrollmentQualification, 
        through="ClassEnrollment", 
        blank=True,
        related_name='enrollment_qualifications') 
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Academic period", related_name="teaching_classes")
    qualification = models.ForeignKey('subject_app.Qualification', on_delete=models.CASCADE, related_name="teaching_classes")
    name = models.CharField(max_length=50, verbose_name="Class name") 

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['period', 'name',], 
                name='unique_teaching_class'
            )
        ]
    
    def __str__(self):
        return self.name
    
    def get_teachers_display(self):
        return ", ".join(
            [teacher.full_name for teacher in self.teachers.all()]
        )


class ClassEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    enrollment_qualification = models.ForeignKey(
        EnrollmentQualification, 
        on_delete=models.CASCADE, 
        verbose_name="Enrollment qualification", 
        related_name="class_enrollments"
    )
    teaching_class = models.ForeignKey(
        TeachingClass, 
        on_delete=models.CASCADE, 
        verbose_name="Teaching class", 
        related_name="class_enrollments"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enrollment_qualification', 'teaching_class',], name='unique_class_enrollment')
        ]
        
    def __str__(self):
        return f"""
            {self.enrollment_qualification.enrollment.student} 
        """
        
    def on_checkpoint(self, checkpoint_id: int) -> bool:
        return self.checkpoint_yeargroups.filter(checkpoint_id=checkpoint_id).exists()


class Checkpoint(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Date")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Academic period", related_name="checkpoints")
    name = models.CharField(max_length=50, verbose_name="Checkpoint name") 
    scope = models.CharField(
        max_length=20, 
        verbose_name="Scope",
        choices=CheckpointScope.choices,
        default= CheckpointScope.CLASS_LANDMARK,
    ) 
    teaching_classes = models.ManyToManyField(TeachingClass, related_name='checkpoints', blank=True)
    yeargroups = models.ManyToManyField(
        YearGroup, 
        through="CheckpointYearGroup", 
        related_name='checkpoints', 
        blank=True
    )
    state = models.CharField(
        max_length=10,
        choices=CheckpointState.choices,
        default=CheckpointState.HIDDEN
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'period'], name='unique_checkpoint_name')
        ]

    def __str__(self):
        return self.name
    
    def reorder_fields(self):
        fields = self.checkpoint_fields.order_by('index')
        for i, field in enumerate(fields, start=1):
            if field.index != i:
                field.index = i
                field.save()

    def can_add_fields(self):
        if self.checkpoint_fields.count()<10:
            return True
        return False
    
    def can_add_targets(self):
        if self.yeargroups.count()<self.period.school.yeargroups.count():
            return True
        return False

    def progress(self):

        from gradebook_app.models import CheckpointEntry

        checkpoint_data = CheckpointEntry.objects.filter(
            checkpoint_yeargroup__checkpoint=self, is_excluded=False
        ).aggregate(
            completed_count=Count('id', filter=Q(is_completed=True)),
            total_count=Count('id')
        )

        completed_count = checkpoint_data['completed_count']
        total_count = checkpoint_data['total_count']

        return floor(completed_count/total_count*100)
        
class CheckpointYearGroup(models.Model):
    id = models.AutoField(primary_key=True)
    checkpoint = models.ForeignKey(
        Checkpoint, 
        on_delete=models.CASCADE, 
        related_name="checkpoint_yeargroups"
    )
    yeargroup = models.ForeignKey(
        YearGroup, 
        on_delete=models.CASCADE, 
        verbose_name="Year group", 
        related_name="checkpoint_yeargroups"
    )
    teaching_classes = models.ManyToManyField(
        TeachingClass, 
        blank=True,
        verbose_name="Teaching classes", 
        related_name="checkpoint_yeargroups"
    )
    qualifications = models.ManyToManyField(
        Qualification, 
        blank=True,
        verbose_name="Qualifications", 
        related_name="checkpoint_yeargroups"
    )
    enrollments = models.ManyToManyField(
        Enrollment, 
        blank=True,
        verbose_name="Enrollments", 
        related_name="checkpoint_yeargroups"
    )
    class_enrollments = models.ManyToManyField(
        ClassEnrollment, 
        blank=True,
        verbose_name="Class enrollments", 
        related_name="checkpoint_yeargroups"
    )
    enrollment_qualifications = models.ManyToManyField(
        EnrollmentQualification, 
        blank=True,
        verbose_name="Enrollment qualifications", 
        related_name="checkpoint_yeargroups"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['checkpoint', 'yeargroup'], name='unique_checkpoint_yeargroup')
        ]
        ordering = ['checkpoint', 'yeargroup']
        
    def __str__(self):
        return self.yeargroup.__str__()    
    
    def target_ids(self):
        if self.checkpoint.scope==CheckpointScope.CLASS_LANDMARK:
            return ClassEnrollment.objects.filter(
                teaching_class__period_id=self.checkpoint.period.id, 
                teaching_class__yeargroup_id=self.yeargroup.id).values_list('id', flat=True)
        elif self.checkpoint.scope==CheckpointScope.SUBJECT_BENCHMARK:
            return EnrollmentQualification.objects.filter(
                enrollment__period_id=self.checkpoint.period.id, 
                enrollment__yeargroup_id=self.yeargroup.id).values_list('id', flat=True)
        elif self.checkpoint.scope==CheckpointScope.GENERAL_BENCHMARK:
            return Enrollment.objects.filter(
                period_id=self.checkpoint.period.id, 
                yeargroup_id=self.yeargroup.id).values_list('id', flat=True)
            
    def assigned_target_ids(self):
        if self.checkpoint.scope==CheckpointScope.CLASS_LANDMARK:
            return self.class_enrollments.all().values_list('id', flat=True)
                
        elif self.checkpoint.scope==CheckpointScope.SUBJECT_BENCHMARK:
            return self.enrollment_qualifications.all().values_list('id', flat=True)
        elif self.checkpoint.scope==CheckpointScope.GENERAL_BENCHMARK:
            return self.enrollments.all().values_list('id', flat=True)
    
    
    def target_model(self)-> models.Model:
        if self.checkpoint.scope==CheckpointScope.CLASS_LANDMARK:
            return ClassEnrollment
        elif self.checkpoint.scope==CheckpointScope.SUBJECT_BENCHMARK:
            return EnrollmentQualification
        elif self.checkpoint.scope==CheckpointScope.GENERAL_BENCHMARK:
            return Enrollment
        

    def no_targets_message(self) -> Union[str, None]:
        checks = {
            CheckpointScope.CLASS_LANDMARK: self.yeargroup.teaching_classes.exists(),
            CheckpointScope.SUBJECT_BENCHMARK: self.yeargroup.enrollments.filter(enrollment_qualifications__isnull=False).exists(),
            CheckpointScope.GENERAL_BENCHMARK: self.yeargroup.enrollments.exists(),
        }

        if checks.get(self.checkpoint.scope, False):  
            return None

        messages = {
            CheckpointScope.SUBJECT_BENCHMARK: "There are no subjects studied in this year group.",
            CheckpointScope.CLASS_LANDMARK: "There are no classes registered for this year group.",
            CheckpointScope.GENERAL_BENCHMARK: "There are no students registered in this year group.",
        }

        return messages.get(self.checkpoint.scope)


       
class CheckpointField(models.Model):
    STEP_CHOICES = [
        ('0.01', "0.01"),
        ('0.05', "0.05"),
        ('0.1', "0.1"),
        ('0.5', "0.5"),
        ('1', "1"),
        ('5', "5"),
        ('10', "10"),
    ]
    id = models.AutoField(primary_key=True)
    checkpoint = models.ForeignKey(
        Checkpoint,
        on_delete=models.CASCADE,
        verbose_name="Checkpoint",
        related_name="checkpoint_fields"
    )
    index = models.PositiveIntegerField(verbose_name="Order")  # New index field


    kind = models.CharField(
        max_length=20, 
        verbose_name="Field type",
        choices=CheckpointFieldKind.choices,
    ) 
    name = models.CharField(max_length=30, verbose_name="Field name") 
    minmark = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Min. mark",
        validators=[
            MaxValueValidator(1000),  
            MinValueValidator(0),  
        ],
    )
    maxmark = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Max. mark", 
        validators=[
            MaxValueValidator(10000),  
            MinValueValidator(1),  
        ],
    )
    stepsize = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        verbose_name="Mark step size",
        choices=STEP_CHOICES, 

    )
    minlength = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Min. character count",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(500)
        ]
    )
    maxlength = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Max. character count",
        validators=[
            MinValueValidator(10),
            MaxValueValidator(1500)
        ]
    )
    categories = models.JSONField(blank=True, null=True, default=list, verbose_name="Categories")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'checkpoint'], name='unique_checkpointfield_name')
        ]
        ordering = ['checkpoint', 'index']
    
    def __str__(self):
        return self.name
        

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only on creation
            last_index = CheckpointField.objects.filter(checkpoint=self.checkpoint).count()
            self.index = last_index + 1
        super().save(*args, **kwargs)
        
    def rules(self):
        if self.kind== CheckpointFieldKind.COMMENT:
            return f"Comment between {self.minlength} and {self.maxlength} characters long"
        elif self.kind== CheckpointFieldKind.GRADE:
            return "Grade from the corresponding subject qualification gradeset"
        elif self.kind== CheckpointFieldKind.MOCK:
            return "Mark & grade from the corresponding exam component gradeset"
        elif self.kind== CheckpointFieldKind.MARK:
            return f"Mark between {self.minmark} and {self.maxmark}, rounded to the nearest {self.stepsize}"
        elif self.kind== CheckpointFieldKind.CATEGORICAL:
            return 'Category from: ' + ', '.join(self.categories)
        elif self.kind== CheckpointFieldKind.PERCENTAGE:
            return f"Percentage mark between {self.minmark} and {self.maxmark}, rounded to the nearest {self.stepsize}"

        

    
