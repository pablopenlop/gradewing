from register_app.models import (
    Period, Checkpoint, CheckpointYearGroup, Student, Enrollment, 
    StudentProgramme, StudentQualification, 
)
from gradebook_app.models import QualificationExamResult, ComponentExamResult
from dataclasses import dataclass
from django.db.models import Model
from django.urls import reverse

DELETE_DATA = {
    Period: {
        "form_id": "period-delete-form",
        "action": lambda: reverse("school-period-delete"),
        "title": "Delete academic period?",
        "body": "",
    },
    Student: {
        "form_id": "student-delete-form",
        "action": lambda: reverse("student-delete"),
        "title": "Delete student record?",
        "body": "",
    },
    Checkpoint: {
        "form_id": "checkpoint-delete-form",
        "action": lambda: reverse("checkpoint-delete"),
        "title": "Delete checkpoint?",
        "body": "",
    },
    CheckpointYearGroup: {
        "form_id": "checkpoint-yeargroup-delete-form",
        "action": lambda: reverse("checkpoint-yeargroup-delete"),
        "title": "Remove yeargroup from checkpoint?",
        "body": "",
    },
    Enrollment: {
        "form_id": "student-enrollment-delete-form",
        "action": lambda: reverse("student-enrollment-delete"),
        "title": "Delete enrollment?",
        "body": "",
    },
    StudentProgramme: {
        "form_id": "student-programme-delete-form",
        "action": lambda: reverse("student-programme-delete"),
        "title": "Delete programme?",
        "body": "",
    },
    StudentQualification: {
        "form_id": "student-qualification-delete-form",
        "action": lambda: reverse("student-qualification-delete"),
        "title": "Delete qualification?",
        "body": "",
    },
    QualificationExamResult: {
        "form_id": "qualification-exam-result-delete-form",
        "action": lambda: reverse("delete-qualification-exam-result"),
        "title": "Delete qualification exam result?",
        "body": "",
    },
    ComponentExamResult: {
        "form_id": "component-exam-result-delete-form",
        "action": lambda: reverse("delete-component-exam-result"),
        "title": "Delete component exam result?",
        "body": "",
    },
}



@dataclass
class DeleteForm:
    model: Model
    delete_id: str = ""

    def __post_init__(self):
        data = DELETE_DATA[self.model]
        self.action = data["action"]
        self.title = data["title"]
        self.body = data["body"]
        self.form_id = data["form_id"]
        


    
    