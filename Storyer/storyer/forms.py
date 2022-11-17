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

class GroupCreateForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=250)
    description = forms.CharField(label="Group Description", widget=forms.Textarea(attrs={"rows":10, "cols":40}))

# TODO: needs to generate a dropdown of choices for a given faculty member's courses
class CourseChangeForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Course.objects.all()