from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.http import HttpResponse

from storyer.models import Student, Assignment, Faculty, Course, Group
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm, CourseCreateForm, CourseChangeForm


def index(request):
    return render(request, 'index.html')


def signup(request):
    # if a user submit a form from the webpage
    if request.method == "POST":
        context = {}
        # get the data and check if its empty before trying to put it into a form model
        post_data = request.POST or None
        if post_data is not None:
            signup_form = SignupForm(post_data)
            # if the data was parsed correctly and could be put into a form object without issue
            if signup_form.is_valid():
                signup_form = signup_form.cleaned_data
                # as long as this email from the form doesnt exist for another student
                if not Student.objects.filter(email=signup_form['email']).exists():
                    # put the first and last name together
                    name = (signup_form['first_name'].replace(" ", "").title(
                    ))+" "+signup_form['last_name'].replace(" ", "").title()
                    # put the data into a new Student in the models
                    new_student = Student(
                        name=name, email=signup_form['email'], password=signup_form['password'])
                    # save the new Student and then display the view for student_detail
                    new_student.save()
                    return student_detail(request, new_student.id)
                else:
                    context.update({"exists": True})
        context.update({'error_message': True})
        return render(request, 'initial.html', context)

    return render(request, 'initial.html')

def signup_faculty(request):
    if request.method == "POST":
        context = {}
        post_data = request.POST or None
        if post_data is not None:
            signup_form = SignupForm(post_data)
            if signup_form.is_valid():
                signup_form = signup_form.cleaned_data
                if not Faculty.objects.filter(email=signup_form['email']).exists():
                    name = (signup_form['first_name'].replace(" ", "").title(
                    ))+" "+signup_form['last_name'].replace(" ", "").title()
                    new_faculty = Faculty(
                        name=name, email=signup_form['email'], password=signup_form['password'])
                    new_faculty.save()
                    redirect('storyer:faculty_landing', faculty_id=new_faculty.id)
                else:
                    context.update({"exists": True})
        context.update({'error_message': True})
        return render(request, 'initial_faculty.html', context)

    return render(request, 'initial_faculty.html')


# student login only
def login(request):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            login_form = LoginForm(post_data)
            if login_form.is_valid():
                login_form = login_form.cleaned_data
                # look for student in user list
                student = Student.objects.filter(
                    email=login_form['email'], password=login_form['password']).first()
                if student is not None:
                    return student_detail(request, student.id)
        context = {'error_message': True}
        return render(request, 'login.html', context)

    return render(request, 'login.html')

# faculty login only
def login_faculty(request):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            login_form = LoginForm(post_data)
            if login_form.is_valid():
                login_form = login_form.cleaned_data
                # look for student in user list
                faculty = Faculty.objects.filter(
                    email=login_form['email'], password=login_form['password']).first()
                if faculty is not None:
                    # TODO: display a default course for the faculty
                    course = Course.objects.filter(creator=faculty).first()
                    if course is not None:
                        return redirect('storyer:faculty_landing', faculty_id=faculty.id, course_id=course.id)
                    return redirect('storyer:faculty_landing', faculty_id=faculty.id)
        
        context = {'error_message': True}
        return render(request, 'login_faculty.html', context)

    return render(request, 'login_faculty.html')



def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student_detail.html', {'student': student})


def pick_groups(request, student_id):
    assignment_list = Assignment.objects.order_by('title')
    student = get_object_or_404(Student, pk=student_id)
    context = {
        'student': student,
        'group_list': assignment_list,
    }
    return render(request, 'pick_groups.html', context)


def faculty_landing(request, faculty_id, course_id=None):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = None
    # add course details as well if one is given
    if course_id is not None:
        course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_landing.html', {'faculty':faculty, 'course':course})

def faculty_change_course(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    # also give a list of all courses
    course_list = faculty.course_set.all()

    post_data = request.POST or None
    if post_data is not None:
        context = {}
        course_change_form = CourseChangeForm(post_data)
        if course_change_form.is_valid():
            course_change_form = course_change_form.cleaned_data  
            name = course_change_form['name']
            new_course = Course.objects.get(name=name, creator=faculty)
            return redirect('storyer:faculty_landing', faculty_id=faculty.id, course_id=new_course.id)
        else:
            print(course_change_form.errors.as_data())
            context.update({'error_message': True})

    return render(request, 'faculty_change_course.html', {'faculty':faculty, 'course':course, 'course_list':course_list})

def faculty_check_assignments(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_check_assignments.html', {'faculty':faculty, 'course':course})

def faculty_create_assignment(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_create_assignment.html', {'faculty':faculty, 'course':course})

def faculty_create_course(request, faculty_id, course_id=None):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    # retain course info if faculty already has one set to view
    course = None
    if course_id is not None:
        course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        context = {}
        post_data = request.POST or None
        if post_data is not None:
            course_create_form = CourseCreateForm(post_data)
            if course_create_form.is_valid():
                course_create_form = course_create_form.cleaned_data  
                name = course_create_form['name']
                code = course_create_form['code']
                # check if a course this faculty member has created already exists with the same name, 
                # as well as the code hasn't been used before at all
                if not Course.objects.filter(code=code).exists() and not faculty.course_set.filter(name=name).exists():
                    new_course = Course(name=name, code=code, creator=faculty)
                    new_course.save()
                    return redirect('storyer:faculty_landing', faculty_id=faculty.id, course_id=new_course.id)
                else:
                    context.update({"exists": True})
            else:
                print(course_create_form.errors.as_data())
        context.update({'error_message': True})
        return render(request, 'faculty_create_course.html', {'faculty' : faculty, 'course':course})

    return render(request, 'faculty_create_course.html', {'faculty' : faculty, 'course':course})

def faculty_create_group(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_create_group.html', {'faculty':faculty, 'course':course})

def faculty_edit_groups(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_edit_groups.html', {'faculty':faculty, 'course':course})

def faculty_student_info(request, faculty_id, course_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'faculty_student_info.html', {'faculty':faculty, 'course':course})
