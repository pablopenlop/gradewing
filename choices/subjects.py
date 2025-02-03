from django.db import models
from .choices import ComplexChoices

class SubjectGroup(ComplexChoices):
    class IB:
        class DP(models.TextChoices):
            LAL = "ib.g1.lal", "Group 1. Studies in Language and Literature"
            LA = "ib.g2.la", "Group 2. Language Acquisition"
            INDIV_SOC = "ib.g3.indiv", "Group 3. Individuals & Societies"
            SCIENCES = "ib.g4.science", "Group 4. Sciences"
            MATHS = "ib.g5.maths", "Group 5. Mathematics"
            ARTS = "ib.g6.arts", "Group 6.  The Arts"
            INTER = "ib.g7.inter", "Interdisciplinary"
            CORE = "ib.g0.dpcore", "DP Core"
        class CP(models.TextChoices):
            CORE = "ib_cpcore", "CP Core"
        class MYP(models.TextChoices):
            LA = "ib.myp.la", "Language Acquisition"
            LAL = "ib.myp.lal", "Language & Literature"
            INDIVIDUALS = "ib.myp.ind", "Individuals & Societies"
            MATHS = "ib.myp.maths", "Mathematics"
            SCIENCES = "ib.myp.science", "Sciences"
            ARTS = "ib.myp.arts", "Arts"
            PHE = "ib.myp.phe", "Physical & Health Education"
            DESIGN = "ib.myp.design", "Design"
            INTER = "ib.myp.inter", "Interdisciplinary"
            PROJECT = "ib.myp.project", "Personal Project"

    class UK(models.TextChoices):
        PROFESSIONAL = "uk.prof", "Creative and professional"
        ENGLISH = "uk.english", "English language and literature"
        HUMANITIES = "uk.humanities", "Humanities and social sciences"
        LANGUAGES = "uk.languages", "Languages"
        MATHS = "uk.maths", "Mathematics"
        SCIENCES = "uk.sciences", "Sciences"
        HEALTH = "uk.sh", "Sport & Health"
        ICT = "uk.ict", "ICT & Computing"
        PROJECT = "uk_project", "Project"

        
    @classmethod
    def grouped_choices(cls):
        choices =  [
            ("UK", list(cls.UK.choices)),
            ("IB DP & IB CP", list(cls.IB.DP.choices)),
            ("IB MYP", list(cls.IB.MYP.choices)),
        ]
        return choices
    

