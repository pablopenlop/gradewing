
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from subject_app.models import Qualification
from choices import QF

from django.db.models import Q

@login_required
def ib_main(request):
    return render(request, 'subject_app/qualifications/ib_main.html')

@login_required
def uki_main(request):
    return render(request, 'subject_app/qualifications/uki_main.html')

@login_required
def ukn_main(request):
    return render(request, 'subject_app/qualifications/ukn_main.html')


@login_required
def get_main_content(request, family_value: str):
    family = QF.choices_from_values(family_value)[0]
    edusystem = QF.get_edusystem_from_choice(family)
    print(edusystem)
    qnames = QF.get_qualification_name_choices(family, values_only=True)
    qualifications = Qualification.objects.filter(
        Q(name__in=qnames) & (Q(seed=True) | Q(school=request.user.userprofile.school))
    )
    context = {'qualifications': qualifications, 'family': family, 'edusystem': edusystem}
    return render(request, 'subject_app/qualifications/partials/qualifications_main_content.html', context)

@login_required
def get_qualification_info(request, pk):
    qualification = get_object_or_404(Qualification, pk=pk)
    context = {'qualification': qualification}
    return render(request, 'subject_app/qualifications/partials/qualification_info.html', context)

