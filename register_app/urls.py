from django.urls import path
from register_app.views import student_views, teacher_views, school_views, class_views, checkpoint_view


urlpatterns = [
    # CHECKPOINT VIEWS
    path('checkpoints/', checkpoint_view.checkpoints, name='checkpoints'),
    path('checkpoints/table/', checkpoint_view.checkpoints_table, name='checkpoints-table'),
    path('checkpoints/headerbar/', checkpoint_view.checkpoints_headerbar, name='checkpoints-headerbar'),
    path('checkpoints/preform-1/', checkpoint_view.get_checkpoint_preform_1, name='checkpoint-preform-1'),
    path('checkpoints/preform-2/', checkpoint_view.get_checkpoint_preform_2, name='checkpoint-preform-2'),
    path('checkpoints/form/<int:checkpoint_id>/', checkpoint_view.get_checkpoint_form, name='checkpoint-form'),
    path('checkpoints/add/', checkpoint_view.save_checkpoint, name='checkpoint-save'),
    path('checkpoints/delete/', checkpoint_view.delete_checkpoint, name='checkpoint-delete'),
    path('checkpoints/delete-form/<int:checkpoint_id>/', checkpoint_view.checkpoint_delete_form, name='checkpoint-delete-form'),
    path('checkpoints/editor/<int:checkpoint_id>/', checkpoint_view.checkpoint_editor, name='checkpoint-editor'),
    path('checkpoints/editor/<int:checkpoint_id>/details-card/', checkpoint_view.checkpoint_editor_details_card, name='checkpoint-details-card'),
    path('checkpoints/editor/<int:checkpoint_id>/fields-card/', checkpoint_view.checkpoint_editor_fields_card, name='checkpoint-fields-card'),
    path('checkpoints/editor/<int:checkpoint_id>/field/<int:checkpointfield_id>/form/<str:field_kind>', checkpoint_view.checkpoint_field_form, name='checkpoint-field-form'),
    path('checkpoints/editor/field/form/save', checkpoint_view.save_checkpoint_field, name='checkpoint-field-save'),
    path('checkpoints/editor/field/delete', checkpoint_view.delete_checkpoint_field, name='checkpoint-field-delete'),
    path('checkpoints/editor/reorder-fields/', checkpoint_view.reorder_checkpoint_field, name='checkpoint-reorder-fields'),
    path('checkpoints/<int:checkpoint_id>/fields-table/', checkpoint_view.checkpoint_fields_table, name='checkpoint-fields-table'),
    path('checkpoints/editor/<int:checkpoint_id>/targets-card/', checkpoint_view.checkpoint_editor_targets_card, name='checkpoint-targets-card'),
    path('checkpoints/editor/<int:checkpoint_id>/yeargroup/form/', checkpoint_view.checkpoint_yeargroup_form, name='checkpoint-yeargroup-form'),
    path('checkpoints/editor/yeargroup/save/', checkpoint_view.save_checkpoint_yeargroup, name='checkpoint-yeargroup-save'),
    path('checkpoints/editor/yeargroup/<int:cpyg_id>/delete-form', checkpoint_view.checkpoint_yeargroup_delete_form, name='checkpoint-yeargroup-delete-form'),
    path('checkpoints/editor/yeargroup/delete/', checkpoint_view.delete_checkpoint_yeargroup, name='checkpoint-yeargroup-delete'),
    path('checkpoints/editor/yeargroup/<int:cpyg_id>/targets/table/', checkpoint_view.targets_table, name='checkpoint-yeargroup-targets-table'),
    path('checkpoints/editor/yeargroup/<int:cpyg_id>/targets/data/', checkpoint_view.targets_data, name='checkpoint-yeargroup-targets-data'),
    path('checkpoints/editor/yeargroup/<int:cpyg_id>/targets/update/', checkpoint_view.update_targets, name='checkpoint-yeargroup-targets-update'),


    # TEACHER VIEWS
    path('teachers/', teacher_views.teachers, name='teachers'),
    path('teachers/table/', teacher_views.teachers_table, name='teachers-table'),
    path('teachers/headerbar/', teacher_views.teachers_headerbar, name='teachers-headerbar'),
    path('teachers/form/<int:teacher_id>/', teacher_views.get_teacher_form, name='teacher-form'),
    path('teachers/form/save/', teacher_views.save_teacher_form, name='teacher-form-save'),
    path('teachers/delete/', teacher_views.delete_teacher, name='teacher-delete'),


    # TEACHING CLASS VIEWS
    path('teaching-classes/', class_views.classes, name='classes'),
    path('teaching-classes/table/', class_views.classes_table, name='classes-table'),
    path('teaching-classes/headerbar/', class_views.classes_headerbar, name='classes-headerbar'),
    path('teaching-classes/preform-1/', class_views.get_class_preform_1, name='class-preform-1'),
    path('teaching-classes/preform-2/', class_views.get_class_preform_2, name='class-preform-2'),
    path('teaching-classes/form/<int:class_id>/', class_views.get_class_form, name='class-form'),
    path('teaching-classes/form/save', class_views.save_class_form, name='class-form-save'),
    path('teaching-classes/delete/', class_views.delete_class, name='class-delete'),


    #path('teachers/form/save/', teacher_views.save_teacher_form, name='teacher-form-save'),
    #path('teachers/delete', teacher_views.delete_teacher, name='teacher-delete'),
    
    # STUDENT VIEWS
    path('students/', student_views.students, name='students'),
    path('students/headerbar/', student_views.students_headerbar, name='students-headerbar'),
    path('students-json/', student_views.students_json, name='students-json'),
    path('students/table/', student_views.students_table, name='students-table'),
    path('students/infocard/<int:pk>/', student_views.get_student_infocard, name='student-infocard'),
    path('students/<int:student_id>/delete-form/', student_views.student_delete_form, name='student-delete-form'),
    path('students/delete/', student_views.delete_student, name='student-delete'),
    
    path('students/editor/<int:student_id>/form/', student_views.student_general_form, name='student-general-form'),
    path('students/editor/general-save/', student_views.save_student_general, name='student-general-save'),
    path('students/editor/<int:student_id>/', student_views.student_editor, name='student-editor'),
    path('students/editor/<int:student_id>/general-card', student_views.student_general_card, name='student-general-card'),
    path('students/editor/<int:student_id>/enrollments-card', student_views.student_enrollments_card, name='student-enrollments-card'),
    path('students/editor/<int:student_id>/enrollment-form/<int:enrollment_id>', student_views.student_enrollment_form, name='student-enrollment-form'),
    path('students/editor/enrollment/save', student_views.save_student_enrollment, name='student-enrollment-save'),
    path('students/editor/enrollment/<int:enrollment_id>/delete-form', student_views.student_enrollment_delete_form, name='student-enrollment-delete-form'),
    path('students/editor/enrollment/delete', student_views.delete_student_enrollment, name='student-enrollment-delete'),
    path('students/editor/<int:student_id>/qualifications-card', student_views.student_qualifications_card, name='student-qualifications-card'),
    path('students/editor/<int:student_id>/programme-form', student_views.student_programme_form, name='student-programme-form'),
    path('students/editor/programme-save', student_views.save_student_programme, name='student-programme-save'),
    path('students/editor/programme/<int:programme_id>/delete-form', student_views.student_programme_delete_form, name='student-programme-delete-form'),
    path('students/editor/programme/delete', student_views.delete_student_programme, name='student-programme-delete'),
    path('students/editor/<int:programme_id>/<int:sq_id>/qualification-form', student_views.student_qualification_form, name='student-qualification-form'),
    path('students/editor/qualification/<int:sq_id>/delete-form', student_views.student_qualification_delete_form, name='student-qualification-delete-form'),
    path('students/editor/qualification/save', student_views.save_student_qualification, name='student-qualification-save'),
    path('students/editor/qualification/delete', student_views.delete_student_qualification, name='student-qualification-delete'),


    # SCHOOL VIEWS
    path('school/', school_views.school, name='school'),
    path('school/profile/', school_views.school_card, name='school-school-card'),
    path('school/profile/form/', school_views.school_form, name='school-school-form'),
    path('school/profile/save/', school_views.save_school, name='school-school-save'),
    path('school/yeargroups/', school_views.yeargroups_card, name='school-yeargroups-card'),
    path('school/yeargroups/custom-rename-form/<int:yeargroup_id>/', school_views.custom_yeargroup_form, name='rename-custom-yeargroup-form'),
    path('school/yeargroups/set-yeargroup-system/', school_views.set_yeargroup_system, name='set-yeargroup-system'),
    path('school/academic-periods/', school_views.periods_card, name='school-periods-card'),
    path('school/academic-periods/form/<int:period_id>/', school_views.get_period_form, name='school-period-form'),
    path('school/academic-periods/delete-form/<int:period_id>/', school_views.period_delete_form, name='school-period-delete-form'),

    path('school/academic-periods/save/', school_views.save_period, name='school-period-save'),
    path('school/academic-periods/delete/', school_views.delete_period, name='school-period-delete'),
    path('school/academic-periods/current-period/<int:period_id>/', school_views.set_current_period, name='set-current-period'),
    path('school/tags/card/', school_views.tags_card, name='school-tags-card'),
    path('school/tags/<str:tag_type>/form/', school_views.get_tags_form, name='new-tags-form'),
    path('school/tags/<str:tag_type>/add/', school_views.add_tags, name='add-tags'),
    path('school/tags/actions-form/<str:tag_type>/<int:tag_id>/', school_views.get_tag_actions_form, name='tag-actions-form'),
    path('school/tags/actions-form/action/<str:tag_type>/', school_views.save_tag, name='save-tag-form'),
    path('school/tags/delete-form/<str:tag_type>/<int:tag_id>/', school_views.delete_tag_form, name='tag-delete-form'),
    path('school/tags/delete/', school_views.delete_tag, name='tag-delete'),

    # PERIOD VIEWS
    # path('periods/', period_views.periods, name='periods'),
    # path('periods/save/', period_views.save_period, name='save-period'),
    # path('periods/delete/', period_views.delete_period, name='delete-period'),
    # path('periods/current/<int:period_id>/', period_views.set_current_period, name='set-current-period'),
    # path('periods/active/', period_views.set_active_period, name='set-active-period'),

    # path('periods/<int:period_id>/', period_views.period_details, name='period-details'),
    # path('periods/form/', period_views.get_period_form, name='period-form'),



    #path('students/', views.students, name='students'),
    #path('students/delete/', views.delete_students, name='delete-students'),
    #path('students/add/', views.add_student, name='add-student'),
    #path('students/add2/', views.add_student2, name='add2-student'),
    #path('students/add/', views.add_student, name='add-student'),
    #path('students/form/', views.get_student_form, name='student-form'),
    #path('students/period-form/', views.get_studentperiod_form, name='student-period-form'),
    #path('students/save-details/', views.save_student_details, name='save-student-details'),
    #path('students/save-period/', views.save_student_period, name='save-student-period'),
    #path('students/<int:pk>/', views.student_details, name='student-details'),
    #path('students/add-qualification/', views.add_qualification_students, name='add-qualification-students'),

    

    # path('programmes/', views2.programmes, name='programmes'),

    # path('teachers/', views2.teachers, name='teachers'),
    # #path('teachers/add/', views.add_teacher, name='add-teacher'),
    # path('teachers/delete/', views2.delete_teachers, name='teachers-delete'),

    # path('courses/', views2.courses, name='courses'),
    # path('courses/add/', views2.add_course, name='courses-add'),
    # path('courses/delete/', views2.delete_courses, name='courses-delete'),
    # path('courses/add/enrollments/<int:period_id>/', views2.add_course_enrollments, name='courses-add-enrollments'),
    # path('student/addold/', views2.add_student_old, name='add-student-old'),

]
#path('students/<int:id>/delete/', views.delete_student, name='delete-student'),