from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from subject_app.models import Qualification
from register_app.edusystem import QualificationSuite as QS



@login_required
def get_main_content(request, suite_value: str):
    suite = QS.choices_from_values(suite_value)[0]
    qualifications = Qualification.objects.filter(suite=suite)
    context = {'qualifications': qualifications, 'suite': suite}
    return render(request, 'subject_app/qualifications/partials/qualifications_main_content.html', context)

@login_required
def get_qualification_info(request, pk):
    qualification = get_object_or_404(Qualification, pk=pk)
    print(qualification)
    context = {'qualification': qualification}
    return render(request, 'subject_app/qualifications/partials/qualification_info.html', context)

