from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import json
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from register_app.forms import PeriodForm
from register_app.models import Period 


@login_required
def periods(request):
    periods = Period.objects.filter(school=request.user.userprofile.school).order_by('-start_date')
    current_period = Period.objects.get(school=request.user.userprofile.school, current=True)
    return render(
        request, 
        'register_app/periods/periods.html', 
        {'periods': periods, 'current_period': current_period}
    )

@login_required
def get_period_form(request):
    period_id = request.GET.get('period-id')
    print("period_id:", period_id)
    try:
        period = Period.objects.get(id=period_id)
        form = PeriodForm(
            instance=period, 
            initial={'id': period.id}
        )
    except:
        form = PeriodForm(initial={'school': request.user.userprofile.school})
        print("New period Form")
    return render(
        request, 
        'register_app/periods/partials/period_form.html', 
        {'form': form}
    )

@login_required
def period_details(request, period_id):
    period = get_object_or_404(Period, pk=period_id)
    return render(
        request, 
        'register_app/periods/partials/period_details.html', 
        {'period': period}
    )


@require_POST
def save_period(request):
    period_id = request.POST.get('id')
    period = get_object_or_404(Period, id=period_id) if period_id else None
    if period:
        form = PeriodForm(request.POST, instance=period)
    else:
        form = PeriodForm(request.POST)
    if form.is_valid():
        
        period = form.save()
        print("SUCCESS", period.id)
        #messages.success(request, 'Academic Period added successfully!')
        periods = Period.objects.all().order_by('-start_date')
        return JsonResponse({
            'success': True, 
            'periodId': period.id 
        }) 
    else:
        return JsonResponse({
            'success': False,
            'html': render_to_string('register_app/periods/partials/period_form.html', 
            {'form': form}, 
            request=request)
        })
    
@require_POST
def set_current_period(request, period_id):
    periods = Period.objects.filter(school=request.user.userprofile.school).order_by('-start_date')
    try:
        current_period = Period.objects.get(id=period_id)
    except:
        current_period=Period.objects.first()
    else:
        current_period.current = True
        current_period.save()
    return render(
        request, 
        'register_app/periods/partials/period_cards.html', 
        {'periods': periods,
         'active_period_id': current_period.id}
    )


def set_active_period(request):
    periods = Period.objects.filter(school=request.user.userprofile.school).order_by('-start_date')
    active_id = int(request.GET.get('active_id'))
    print(active_id)

    return render(
        request, 
        'register_app/periods/partials/period_cards.html', 
        {'periods': periods,
         'active_period_id': active_id}
    )


@require_POST
def delete_period(request):
    id_value = request.POST.get('confirm-delete')
    print("id val", id_value)
    period = get_object_or_404(Period, id=id_value)
    if not period.current:
        period.delete()
        messages.success(request, 'Academic Period added successfully!')
        
    return redirect('periods')
