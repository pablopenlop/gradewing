from django.urls import path
from . import views2
from subject_app.views import qualifications_view, uki_view

urlpatterns = [
    path('qualifications/ib/', qualifications_view.ib_main, name='ib-main'),
    path('qualifications/uk-international/', qualifications_view.uki_main, name='uki-main'),
    path('qualifications/uk-national/', qualifications_view.ukn_main, name='ukn-main'),

    path('qualifications/family-main-content/<str:family_value>/', qualifications_view.get_main_content, name='family-main-content'),
    path('qualifications/qualification-info/<int:pk>/', qualifications_view.get_qualification_info, name='qualification-info'),

    path('qualifications/all', views2.subjects, name='subjects'),
    path('qualifications/all/<int:pk>/', views2.subject_detail, name='subject-detail'),
    path('qualifications/all/subject-table/', views2.subject_table, name='subject-table'),
    path('qualifications/all/paper-table/', views2.paper_table, name='paper-table'),
    
    
]
