from django import forms
from .models import Student, Assignment, Course, Group


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=50)

class CourseCreateForm(forms.Form):
    name = forms.CharField(label="Course Name", max_length=250)
    code = forms.CharField(label="Course Code", max_length=25)

class GroupCreateForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=250)
    description = forms.CharField(label="Group Description", widget=forms.Textarea(attrs={"rows":10, "cols":40}))

class CourseChangeForm(forms.Form):
    class Meta:
        model = Course
        fields = ['course',]

    def __init__(self, faculty, *args, **kwargs):
        # call standard __init__
        super().__init__(*args, **kwargs)
        #extend __init__
        self.fields['course'] = forms.ChoiceField(choices=Course.objects.filter(creator=faculty).values_list('id', 'name'))

class StudentGroupChangeForm(forms.Form):
    class Meta:
        model = Course
        fields = ['group',]

    def __init__(self, course, *args, **kwargs):
        # call standard __init__
        super().__init__(*args, **kwargs)
        #extend __init__
        self.fields['group'] = forms.ChoiceField(label="Change Student's Group:", choices=course.group_set.values_list('id', 'name'))

class AssignmentCreateForm(forms.Form):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'group',]

    def __init__(self, course, *args, **kwargs):
        # call standard __init__
        super().__init__(*args, **kwargs)
        #extend __init__
        self.fields['title']  = forms.CharField(label="Assignment Title", max_length=250)
        self.fields['description'] = forms.CharField(label="Assignment Description", widget=forms.Textarea(attrs={"rows":10, "cols":40}))
        self.fields['group'] = forms.ChoiceField(choices=Group.objects.filter(course=course).values_list('id', 'name'))