import random
from register_app.models import (
    School, Period, Student, Teacher, Enrollment, StudentProgramme, 
    StudentQualification, TeachingClass, EnrollmentQualification
)
from subject_app.models import Qualification
from choices.people import Gender
from faker import Faker
from dataclasses import dataclass
from choices.qualification_tree import Edusystem
from choices.qualification_family import QualificationFamily
from choices. yeargroups import YearGroupLevel
from django.db.models import Max



def get_fictional_teacher_names(n: int)->list[str]:
    fictional_teachers = [
        "Walter White", "Edna Krabappel", "Seymour Skinner", "Ted Mosby", "Master Roshi",
        "Bruce Wayne", "Dolores Umbridge", "Severus Snape", "Saul Goodman", "Frodo Baggins",
        "Barney Stinson", "Albus Dumbledore", "Cersei Lannister", "Kakashi Hatake",
        "Dexter Morgan", "Darth Vader", "Agatha Trunchbull",
        "Qui-Gon Jinn", "Master Yoda", "Charles Xavier", "Annalise Keating", "Arthur Shelby"
    ]

    """Returns a list of n unique teacher names."""
    if n > len(fictional_teachers):
        return fictional_teachers
    
    return random.sample(fictional_teachers, n)



fake = Faker()






@dataclass
class SchoolFactory:
    school: School
    edusystem: Edusystem
    num_students: int=50
    num_teachers: int=10
    num_yeargroups: int=4
    
    
    
    def generate(self):
        self.generate_periods()
        self.generate_teachers()
        self.generate_students()
        self.generate_enrollments()
        self.generate_programmes()
        self.generate_qualifications()
        self.generate_teaching_classes()

    def generate_periods(self):
        periods = [
            Period(
                name= "2023/24 [Fictive]",
                start_date="2023-09-01",
                end_date="2024-06-30",
                school=self.school,
                fake=True
            ),
            Period(
                name= "2024/25 [Fictive]",
                start_date="2024-09-01",
                end_date="2025-06-30",
                school=self.school,
                fake=True
            ),
        ]
        Period.objects.bulk_create(periods)
        self.period_ids = list(self.school.periods.filter(fake=True).values_list("id", flat=True))
        
    def generate_students(self):
        students = []
        for _ in range(self.num_students):
            gender = random.choice([Gender.MALE, Gender.FEMALE])
            first_name = fake.first_name_male() if gender == Gender.MALE else fake.first_name_female()
            last_name = fake.last_name()
            email = f"{first_name}.{last_name}@student.com".lower()
            
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

    def generate_teachers(self):
        teachers = []
        teacher_names = get_fictional_teacher_names(self.num_teachers)
        for teacher_name in teacher_names:
            name_parts = teacher_name.split()
            first_name, last_name = name_parts[0], name_parts[1]
            email = f"{first_name}.{last_name}@teacher.com".lower()

            teachers.append(Teacher(
                school=self.school,
                first_name=first_name,
                last_name=last_name,
                fake=True,
                email=email
            ))
        
        teachers = Teacher.objects.bulk_create(teachers)
        self.teacher_ids = list(self.school.teachers.filter(fake=True).values_list("id", flat=True))
        
        for teacher in teachers:
            teacher.periods.set(self.period_ids)
        
        
    def generate_enrollments(self):
        yeargroups = list(self.school.yeargroups.all()[:self.num_yeargroups]) 
        previous_period_id = self.period_ids[1]
        latest_period_id = self.period_ids[0]
        
        enrollments = [] 
        for student_id in self.student_ids:
            enrollments.append(Enrollment(
                student_id=student_id,
                period_id=previous_period_id,
                yeargroup=random.choice(yeargroups)
            ))
        Enrollment.objects.bulk_create(enrollments)  
        
        enrollments = []  
        for enrollment in Enrollment.objects.filter(
            student__fake=True, 
            period=previous_period_id
        ).select_related("yeargroup"):
            pos = yeargroups.index(enrollment.yeargroup)  
            next_pos = pos-1 if pos > 0 else None
            if next_pos is not None:
                enrollments.append(Enrollment(
                student=enrollment.student,
                period_id=latest_period_id,
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

    def generate_teaching_classes(self):
        qualifications = Qualification.objects.none()  # Start with an empty queryset
        periods = Period.objects.filter(id__in=self.period_ids)

        for period in periods:
            qualifications = qualifications.union(period.qualifications().order_by())

            
        counter = 1
        for qualification in qualifications:
            teacher_id = random.choice(self.teacher_ids)
            for period in periods:
                for yeargroup in self.school.yeargroups.all():
                    eqs = EnrollmentQualification.objects.filter(
                        enrollment__period=period,
                        enrollment__yeargroup=yeargroup,
                        student_qualification__qualification__id=qualification.id
                    )
                    if eqs:
                        tc=TeachingClass.objects.create(
                            period=period, 
                            qualification=qualification,
                            name =f"{qualification.subject} {qualification.get_board_display()} TC {counter}",
                            yeargroup=yeargroup,
                            )
                        tc.enrollment_qualifications.set(eqs)
                        tc.teachers.set([teacher_id])
                        counter=counter+1

    
                        
                
                