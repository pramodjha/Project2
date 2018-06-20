from django import forms
from .models import Acceptrejectdetail, Acceptrejectoption, Assigneddetail, Authorisedetail, Authoriserdetail, Completeddetail, Estimationdetail, Mimember, Options, Overviewdetail, Prioritydetail, Requestcategorys, Requestdetail, Requeststatusdetail, Requestsubcategory, Requesttypedetail, Statusdetail, Teamdetail, Timetrackers, Reports,Emaildetail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime


class UserRegistrationForm(forms.Form):
    username = forms.CharField(required = True, label = 'Username', max_length = 32, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}) )
    email = forms.EmailField(required = True, label = 'Email', max_length = 32, widget=forms.EmailInput(attrs={'placeholder': 'Enter Email ID'}))
    password = forms.CharField(required = True, label = 'Password', max_length = 32, widget = forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    firstname = forms.CharField(required = True, label = 'firstname', max_length = 32, widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
    lastname = forms.CharField(required = True, label = 'lastname', max_length = 32, widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))

class UploadFileForm(forms.Form):
    file = forms.FileField()

class FilterForm(forms.Form):
     columnname = forms.ModelChoiceField(queryset=Reports.objects.all())
     filteroption = forms.ModelChoiceField(queryset=Reports.objects.all())
     filterdata = forms.CharField()

class UsersigninForm(forms.Form):
    username = forms.CharField(required = True, label = 'username', max_length = 32, widget=forms.TextInput(attrs={'placeholder': 'Enter Username '}))
    password = forms.CharField(required = True, label = 'Password', max_length = 32, widget = forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

class RequestdetailForm(forms.ModelForm):
    class Meta():
        model = Requestdetail
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(RequestdetailForm, self).__init__(*args, **kwargs)
        self.fields['requestraiseddate'].widget.attrs['id']  = 'hiddenfield'


class AuthorisedetailForm(forms.ModelForm):
    class Meta():
        model = Authorisedetail
        fields = '__all__'

class OverviewdetailForm(forms.ModelForm):
    class Meta():
        model = Overviewdetail
        fields = '__all__'

class EstimationdetailForm(forms.ModelForm):
    class Meta():
        model = Estimationdetail
        fields = '__all__'


class StatusdetailForm(forms.ModelForm):
    class Meta():
        model = Requeststatusdetail
        exclude = ['requestdetail']
    def __init__(self, *args, **kwargs):
        super(StatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget.attrs['id']  = 'hiddenfield'
        self.fields['username'].widget.attrs['id']  = 'hiddenfield'
        self.fields['statusdetail'].widget.attrs['id']  = 'hiddenfield'



class RequeststatusdetailForm(forms.ModelForm):
    class Meta():
        model = Requeststatusdetail
        fields = '__all__'

class AssigneddetailForm(forms.ModelForm):
    class Meta():
        model = Assigneddetail
        fields = '__all__'

class AcceptrejectdetailForm(forms.ModelForm):
    class Meta():
        model = Acceptrejectdetail
        fields = '__all__'

class CompleteddetailForm(forms.ModelForm):
    class Meta():
        model = Completeddetail
        fields = '__all__'

class RequestcategorysForm(forms.ModelForm):
    class Meta():
        model = Requestcategorys
        fields = '__all__'


class TimetrackersForm(forms.ModelForm):
    class Meta():
        model = Timetrackers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimetrackersForm, self).__init__(*args, **kwargs)
        self.fields['trackingdatetime'].widget.attrs['class']  = 'datetime-input'


class RequestcategorysForm(forms.ModelForm):
    class Meta():
        model = Requestcategorys
        fields = '__all__'

class RequestsubcategoryForm(forms.ModelForm):
    class Meta():
        model = Requestsubcategory
        fields = '__all__'

class TeamdetailForm(forms.ModelForm):
    class Meta():
        model = Teamdetail
        fields = '__all__'


class ReportsForm(forms.ModelForm):
    class Meta():
        model = Reports
        fields = '__all__'
    deliverytime = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.today())
    #deliverytime = forms.DateField(
    #    widget=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datetime-input'}),
    #    input_formats=('%m/%d/%Y', ))

class EmaildetailForm(forms.ModelForm):
    class Meta():
        model = Emaildetail
        fields = '__all__'
