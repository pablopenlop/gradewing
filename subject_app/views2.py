from django.shortcuts import render, redirect, get_object_or_404
from .read_data import update_subject_data, update_subject_areas 

from .models import Qualification, Component, SubjectArea
from django.http import HttpResponse
from .loader import load_subjects
from register_app.loader import load_yeargroups
from register_app.models import YearGroup, Student
from factories.register_factory import SchoolFactory
from choices.qualification_tree import Edusystem
def subjects(request):
    school = request.user.userprofile.school
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            load_subjects()
        elif action == 'delete':
            Qualification.objects.all().delete()
            Component.objects.all().delete()
        elif action == 'add_areas':
            update_subject_areas()
        elif action == 'delete_areas':
            SubjectArea.objects.all().delete()
        elif action == 'test':
            pass
        elif action == 'yg':
            load_yeargroups()
        elif action == 'yg-delete':
            YearGroup.objects.all().delete()
        
        elif action == 'create-students':
            sf = SchoolFactory(
                school=school, 
                edusystem=Edusystem.IB,
                num_students=400)
            sf.generate()
            print('done')
        elif action == 'delete-students':
            Student.objects.filter(school=school).all().delete()
            print('delete')
            
         
    subjects = Qualification.objects.all()
    papers = Component.objects.all()
    subject_areas = SubjectArea.objects.all()
    yeargroups = YearGroup.objects.all()
    #print(ExamSeriesSelector.mapping)
    context = {'subjects': subjects, 'papers': papers, 'subject_areas': subject_areas,  'yeargroups': yeargroups}
    return render(request, 'subject_app/subjects.html', context)


def subject_table(request):
    subjects = Qualification.objects.all()
    return render(request, 'subject_app/partials/subject_table.html', {'subjects': subjects})

def paper_table(request):
    papers = Component.objects.all()
    return render(request, 'subject_app/partials/paper_table.html', {'papers': papers})

def subject_detail(request, pk):
    subject = get_object_or_404(Qualification, pk=pk)
    return render(request, 'subject_app/partials/subject_detail.html', {'subject': subject})
