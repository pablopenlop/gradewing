import random
from register_app.models import School, Student, Enrollment, StudentProgramme, StudentQualification
from subject_app.models import Qualification
from choices.people import Gender
from faker import Faker
from dataclasses import dataclass
from choices.qualification_tree import Edusystem
from choices.qualification_family import QualificationFamily
from choices. yeargroups import YearGroupLevel
from django.db.models import Max



fake = Faker()

@dataclass
class SchoolFactory:
    school: School
    edusystem: Edusystem
    num_students: int=50
    num_yeargroups: int=4
    
    
    
    def generate(self):
        self.generate_periods()
        self.generate_students()
        self.generate_enrollments()
        self.generate_programmes()
        self.generate_qualifications()

    def generate_periods(self):
        return
    def generate_students(self):
        students = []
        for _ in range(self.num_students):
            gender = random.choice([Gender.MALE, Gender.FEMALE])
            first_name = fake.first_name_male() if gender == Gender.MALE else fake.first_name_female()
            last_name = fake.last_name()
            email = f"{first_name}.{last_name}@example.com".lower()
            
            students.append(Student(
                school=self.school,
                gender=gender,
                first_name=first_name,
                last_name=last_name,
                fake=True,
                email=email
            ))
        
        Student.objects.bulk_create(students)
        self.student_ids = list(self.school.students.filter(fake=True).values_list("id", flat=True))

    
    def generate_enrollments(self):
        yeargroups = list(self.school.yeargroups.all()[:self.num_yeargroups]) 
        periods = list(self.school.periods.all()) 
        previous_period = periods[1] if len(periods) > 1 else None 
        latest_period = periods[0] 
        
        enrollments = [] 
        for student_id in self.student_ids:
            enrollments.append(Enrollment(
                student_id=student_id,
                period=previous_period,
                yeargroup=random.choice(yeargroups)
            ))
        Enrollment.objects.bulk_create(enrollments)  
        
        enrollments = []  
        for enrollment in Enrollment.objects.filter(
            student__fake=True, 
            period=previous_period
        ).select_related("yeargroup"):
            pos = yeargroups.index(enrollment.yeargroup)  
            next_pos = pos-1 if pos > 0 else None
            if next_pos is not None:
                enrollments.append(Enrollment(
                student=enrollment.student,
                period=latest_period,
                yeargroup=yeargroups[next_pos]
            ))
        Enrollment.objects.bulk_create(enrollments)  
        self.enrollment_ids = [e.id for e in enrollments]
            

    def generate_programmes(self):
        ygs = self.school.yeargroups.all()
        upper_ygs = ygs[:2]
        middle_ygs = ygs[2:]
        students=Student.objects.filter(id__in=self.student_ids).all()
        programmes= []
        for student in students:
            if student.enrollments.filter(yeargroup__in=upper_ygs).exists():
                programmes.append(StudentProgramme(
                    name= self.programme_provider("upper"),
                    student=student
                ))
            if student.enrollments.filter(yeargroup__in=middle_ygs).exists():
                programmes.append(StudentProgramme(
                    name= self.programme_provider("middle"),
                    student=student
                ))
        StudentProgramme.objects.bulk_create(programmes)  
    
    def generate_qualifications(self):
        programmes = StudentProgramme.objects.filter(student_id__in=self.student_ids).all()
        for programme in programmes:
            yeargroups = QualificationFamily.compatible_yeargroup_levels(programme.name)
            potential_enrollments = programme.student.enrollments.filter(yeargroup__level__in=yeargroups).all()
            for qualification in self.qualifications_provider(programme=programme.name):
                student_qualification = StudentQualification.objects.create(
                    qualification=qualification,
                    programme=programme
                )
                student_qualification.enrollments.set(potential_enrollments)

                
            
            
            
                       
    def programme_provider(self, stage):
        PROGRAMME_MAP = {
            Edusystem.IB: {'middle': QualificationFamily.IB.MYP, 'upper': QualificationFamily.IB.DP},
            Edusystem.UKN: {'middle': QualificationFamily.UKN.GCSE, 'upper': QualificationFamily.UKN.AL},
            Edusystem.UKI: {'middle': QualificationFamily.UKI.IGCSE, 'upper': QualificationFamily.UKI.IAL},
        }
        programmes = PROGRAMME_MAP[self.edusystem]
        return programmes[stage]
                
    def qualifications_provider(self, programme: QualificationFamily):
        QUALIFICATION_MAP = {
            QualificationFamily.IB.MYP: (
                ['IBMYP-105', 'IBMYP-106'], 
                ['IBMYP-204', 'IBMYP-208'], 
                ['IBMYP-300'], 
                ['IBMYP-400', 'IBMYP-404'], 
                ['IBMYP-500'], 
                ['IBMYP-900'], 
                ['IBMYP-901'], 
            ),
             QualificationFamily.IB.DP: (
                ['IBDP-DP'], 
                ['IBDP-CPM'], 
                ['IBDP-EE'], 
                ['IBDP-TOK'], 
                ['IBDP-CAS'], 
                ['112711', '112752'],
                ['112839', '112739'],
                ['117712', '100334'],
                ['100340', '100129'],
                ['100058'],
                ['100680', '149712']
                
            )
             
        }
        codes = QUALIFICATION_MAP[programme]
        codes = [random.choice(sublist) for sublist in codes]
        qualifications = []
        for code in codes:
            latest_spec = Qualification.objects.filter(code=code).aggregate(Max('first_assessment'))['first_assessment__max']
            qualification = Qualification.objects.filter(code=code, first_assessment=latest_spec)
            qualifications.append(random.choice(qualification))
        return qualifications

