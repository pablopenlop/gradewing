from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from choices import QT, QK, Ser, Tier, Board, SG, MT, GS, Month

class Qualification(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    group = models.CharField(
        max_length=20,
        choices=SG.choices(),
        default=SG.NONE.UNDEFINED,
    )
    first_assessment = models.SmallIntegerField(
       blank=True, 
       null=True,
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)
        ]
    )
    last_assessment = models.SmallIntegerField(
       blank=True, 
       null=True,
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)
        ]
    )
    modular = models.BooleanField(default=False)
    kind = models.CharField(
        max_length=30,
        choices=QK.choices(),
        default=QK.NONE.UNDEFINED,
    )
    name = models.CharField(
        max_length=30,
        choices=QT.choices(),
        default=QT.NONE.UNDEFINED,
    )
    suite = models.CharField(
        max_length=30,
        choices=QT.suite_choices(),
        default=QT.NONE.UNDEFINED,
    )

    board = models.CharField(
        max_length=30,
        choices=Board.choices,
        default=Board.UNDEFINED,
    )

    grading = models.CharField(
        max_length=30,
        choices=GS.choices(),
        default=GS.NONE.UNDEFINED,
    )
    mark = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000)
        ]
    )
    mark_type = models.CharField(
        max_length=10,
        choices=MT.choices,
        default=MT.NONE,
    )
    tier = models.CharField(
        max_length=12,
        choices=Tier.choices,
        default=Tier.NONE,
    )
    glh = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000)
        ]
    )
    series = models.JSONField(blank=True, null=True, default=list)
    sbs = models.BooleanField(default=False)
    seed = models.BooleanField(default=True)
    current = models.BooleanField(default=True)
    sub_qualification = models.OneToOneField(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='super_qualification'
    )
    school = models.ForeignKey(
        'register_app.School', 
        on_delete=models.CASCADE, 
        related_name='qualifications', 
        null=True,
    )

    core = models.BooleanField(default=False)
    mark_secondary = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ]
    )
    mark_secondary_type = models.CharField(
        max_length=10,
        choices=MT.choices,
        default=MT.NONE,
    )

    class Meta:
        ordering = ['title'] 

    def __str__(self):
        return self.title
    
    def get_series(self):
        return Ser.choices_from_values(self.series)
    
    def has_no_examseries(self)->bool:
        series = self.get_series()
        return True if series == [Ser.Flex.ALL] else False

    def get_form_series(self):
        if self.has_no_examseries():
            return Month.choices
        return [(s.value, s.label) for s in self.get_series()]

    
    def get_level(self):
        if self.kind == QK.IB.DP.SL.value or self.kind == QK.IB.DP.HL.value:
            level = self.get_kind_display().replace("DP ", "")
            return level
        return ""

 
    
    def get_board(self):
        if self.board == Board.CIE:
            return "Cambridge"
        return self.get_board_display()

    @property
    def titlee(self):
        return f"{self.get_board()} {self.get_qualification_display()} {self.name} ({self.first_assessment}) [{self.code}]"
        
    @property
    def titlee_noyear(self):
        return f"{self.get_board()} {self.get_qualification_display()} {self.name} ({self.code})"
    


class Component(models.Model):
    name = models.CharField(max_length=150)
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15, blank=True)
    duration = models.CharField(max_length=25, blank=True)
    internal = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)
    series = models.JSONField(blank=True, null=True, default=list)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE, related_name='components')
    mark = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ]
    )
    mark_adjusted = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ]
    )
    mark_type = models.CharField(
        max_length=10,
        choices=MT.choices,
        default=MT.RAW,
    )
    
    mark_adjusted_type = models.CharField(
        max_length=10,
        choices=MT.choices,
        default=MT.NONE,
    )
    weighting = models.CharField(max_length=50)
    grading = models.CharField(
        max_length=30,
        choices=GS.choices(),
        default=GS.NONE.UNDEFINED,
    )
    glh = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000)
        ]
    )

    def __str__(self):
        return self.name
    
    def get_series(self):
        return Ser.choices_from_values(self.series)
    
    def has_no_examseries(self)->bool:
        series = self.get_series()
        return True if series == [Ser.Flex.ALL] else False

    def get_form_series(self):
        if self.has_no_examseries():
            return Month.choices
        return [(s.value, s.label) for s in self.get_series()]
    



""" 
@dataclass
class ExamSeriesSelector:
    board: Board
    qualification: Qualification
    mapping = {
    (Board.EDEXCEL, Qualification.IAS):     (ExamSeries.JANUARY, ExamSeries.SUMMER, ExamSeries.NOVEMBER),
    (Board.EDEXCEL, Qualification.IA2):     (ExamSeries.JANUARY, ExamSeries.SUMMER, ExamSeries.NOVEMBER),
    (Board.EDEXCEL, Qualification.AS):      (ExamSeries.SUMMER,),
    (Board.EDEXCEL, Qualification.A2):      (ExamSeries.SUMMER,),
    (Board.CIE, Qualification.AS):          (ExamSeries.MARCH, ExamSeries.JUNE, ExamSeries.NOVEMBER),
    (Board.CIE, Qualification.A2):          (ExamSeries.MARCH, ExamSeries.JUNE, ExamSeries.NOVEMBER),
    (Board.OXFORD_AQA, Qualification.AS):   (ExamSeries.MAY_JUNE, ExamSeries.NOVEMBER),
    (Board.OXFORD_AQA, Qualification.A2):   (ExamSeries.MAY_JUNE, ExamSeries.NOVEMBER),
}

    def get(self) -> Tuple[str]:
        sessions: Tuple[ExamSeries] = ExamSeriesSelector.mapping.get(
            (self.board, self.qualification), (ExamSeries.MAY_JUNE, ExamSeries.NOVEMBER))
        return tuple(session for session in sessions)
    
"""


""" 
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    series = models.CharField(
        max_length=16,
        choices=ExamSeries.choices,
    )
    year = models.PositiveSmallIntegerField()
    context = models.ForeignKey(StudentSubject, on_delete=models.CASCADE, related_name="exams")
    grade = models.CharField(max_length=3)
    mark_raw = models.PositiveSmallIntegerField()
    mark_ums = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.id

class PaperEntry(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.CharField(max_length=3)
    mark_raw = models.PositiveSmallIntegerField()
    mark_ums = models.PositiveSmallIntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="papers")
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="entries")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['exam', 'paper'], name='unique_exam_paper')
        ]

    def __str__(self):
        return self.id


def get_grade_choices():
    GRADE_CHOICES = {
        "EDEXCEL": [
            ("a*", "A*"),
            ("b", "B"),
            ("c", "C"),
        ],
        "CIE": [
            ("9", "9"),
            ("8", "8"),
        ],
    }
    # Implement your logic to select the appropriate grading system
    # For this example, let's assume we are choosing "EDEXCEL"
    chosen_system = "EDEXCEL"  # or "CIE"
    return GRADE_CHOICES[chosen_system]


class Exam3(models.Model):
    GRADE_SYSTEMS = [
        ('EDEXCEL', 'EDEXCEL'),
        ('CIE', 'CIE'),
    ]

    id = models.AutoField(primary_key=True)
    series = models.CharField(
        max_length=16,
        choices=ExamSeries.choices,
    )
    year = models.PositiveSmallIntegerField()
    context = models.ForeignKey(StudentSubject, on_delete=models.CASCADE, related_name="exams")
    grade_system = models.CharField(max_length=16, choices=GRADE_SYSTEMS)
    grade = models.CharField(max_length=2, choices=get_grade_choices)

    def __str__(self):
        return str(self.id)

"""


      



class SubjectField(models.TextChoices):
    UNDEFINED = 'undefined', 'OTHER'
    ACCOUNTING = 'accounting', 'Accounting'
    ART = 'art', 'Art'
    ARABIC = 'arabic', 'Arabic'
    BIOLOGY = 'biology', 'Biology'
    BIBLICAL_STUDIES = 'biblical_studies', 'Biblical Studies'
    BUSINESS = 'business', 'Business'
    CHEMISTRY = 'chemistry', 'Chemistry'
    CHINESE = 'chinese', 'Chinese'
    CLASSICAL_STUDIES = 'classical_studies', 'Classical Studies'
    COMPUTER_SCIENCE = 'computer_science', 'Computer Science'
    DESIGN_TECHNOLOGY = 'design_technology', 'Design & Technology'
    ECONOMICS = 'economics', 'Economics'
    ENGLISH_LANGUAGE = 'english_language', 'English Language'
    ENGLISH_LITERATURE = 'english_literature', 'English Literature'
    ENVIRONMENTAL_STUDIES = 'environmental_studies', 'Environmental Studies'
    FRENCH = 'french', 'French'
    FURTHER_MATHS = 'further_maths', 'Further Mathematics'
    GEOGRAPHY = 'geography', 'Geography'
    GERMAN = 'german', 'German'
    GREEK = 'greek', 'Greek'
    HISTORY = 'history', 'History'
    ISLAMIC_STUDIES = 'islamic_studies', 'Islamic Studies'
    IT = 'information_technology', 'Information Technology'
    ITALIAN = 'italian', 'Italian'
    LAW = 'law', 'Law'
    LATIN = 'latin', 'Latin'
    MATHEMATICS = 'mathematics', 'Mathematics'
    MARINE_STUDIES = 'marine_studies', 'Marine Studies'
    MEDIA_STUDIES = 'media_studies', 'Media Studies'
    MUSIC = 'music', 'Music'
    PHILOSOPHY = 'philosophy', 'Philosophy'
    PHYSICS = 'physics', 'Physics'
    POLITICS = 'politics', 'Politics'
    PORTUGUESE = 'portuguese', 'Portuguese'
    PSYCHOLOGY = 'psychology', 'Psychology'
    RELIGION = 'religion', 'Religion'
    SOCIOLOGY = 'sociology', 'Sociology'
    SPANISH = 'spanish', 'Spanish'
    SPORTS = 'sports', 'Sports'
    THEATRE = 'theatre', 'Theatre'
    URDU = 'urdu', 'Urdu'



class SubjectArea(models.Model):
    name = models.CharField(
        max_length=30,
        choices=SubjectField.choices,
    )

    def __str__(self):
        return self.get_name_display()
