from django import forms
from .models import Student, Assignment, Course


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