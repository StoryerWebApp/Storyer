from django.urls import path

from . import views

app_name = 'storyer'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login_faculty', views.login_faculty, name='login_faculty'),
    path('signup', views.signup, name='signup'),
    path('signup_faculty', views.signup_faculty, name='signup_faculty'),
    path('student_detail/<int:student_id>/',
         views.student_detail, name='student_detail'),
    path('groups/<int:student_id>/', views.pick_groups, name='pick_groups'),
    path('faculty_landing/<int:faculty_id>/<int:course_id>/', 
         views.faculty_landing, name='faculty_landing'),
    path('faculty_landing/<int:faculty_id>/', 
         views.faculty_landing, name='faculty_landing'),
    path('faculty_change_course/<int:faculty_id>/<int:course_id>/', 
         views.faculty_change_course, name='faculty_change_course'),
    path('faculty_check_assignments/<int:faculty_id>/<int:course_id>/', 
         views.faculty_check_assignments, name='faculty_check_assignments'),
    path('faculty_create_assignment/<int:faculty_id>/<int:course_id>/', 
         views.faculty_create_assignment, name='faculty_create_assignment'),
    path('faculty_create_course/<int:faculty_id>/', 
         views.faculty_create_course, name='faculty_create_course'),
    path('faculty_create_course/<int:faculty_id>/<int:course_id>/', 
         views.faculty_create_course, name='faculty_create_course'),
    path('faculty_create_group/<int:faculty_id>/<int:course_id>/', 
         views.faculty_create_group, name='faculty_create_group'),
    path('faculty_edit_groups/<int:faculty_id>/<int:course_id>/', 
         views.faculty_edit_groups, name='faculty_edit_groups'),
    path('faculty_student_info/<int:faculty_id>/<int:course_id>/<int:student_id>/', 
         views.faculty_student_info, name='faculty_student_info'),
]
