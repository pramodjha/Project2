from django import forms
from .models import TblWhatwedo, TblIssueAction, TblUatDetail, TblUatStatusMaster, TblAcceptrejectdetail, TblActivity, TblActivityCalendar, TblActivitystatusCalendar, TblAppreciation, TblAssignView, TblAssigneddetail, TblCalendar, TblCalendarHolidays, TblCategorysMaster, TblCompleteddetail, TblConversation, TblDateTypesMaster, TblDeliveryDaysMaster, TblDesignationMaster, TblEmaildetail, TblErrorlog, TblErrortypeMaster, TblEstimationdetail, TblFeedback, TblFeedbackQuestionMaster, TblFrequency, TblGallery, TblGovernance, TblInternaltask, TblInternaltaskchoice, TblInternaltaskstatus, TblLeaveRecord, TblLeaveTypeMaster, TblMember, TblNavbarFooterMaster, TblNavbarHeaderMaster, TblNavbarMaster, TblNavbarView, TblOpenClose, TblYesNo, TblOtDetail, TblOtStatusMaster, TblOverviewdetail, TblPriorityMaster, TblPublicHolidaysMaster, TblRawActivityDetail, TblRawScore, TblRawTeamMaster, TblRawTeamMemberMaster, TblReply, TblRequestdetail, TblRequeststatusdetail, TblRequesttypeMaster, TblShiftUpdate, TblStatusMaster, TblSubcategoryMaster, TblSuccessStories, TblSuggestion, TblTeamMaster, TblTeamMetrics, TblTimeTracker, TblUsefulLinks, TblValidInvalidMaster, TblViewTypeMaster, TblAuthorisedetail, TblCategorysMaster, TblSubcategoryMaster,TblBusinessUnitMaster
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta

class ViewListForm():
    class Meta():
        model = TblTeamMetrics
        fields = '__all__'


class UserRegistrationForm(forms.Form):
    username = forms.CharField(required = True, min_length=6,label = 'Username', max_length = 100 )
    employeeid = forms.IntegerField(required=True)
    email = forms.EmailField(required = True, label = 'Email', max_length = 100, widget=forms.EmailInput(attrs={'placeholder': 'email@willistowerswatson.com'}))
    firstname = forms.CharField(required = True, label = 'firstname', max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastname = forms.CharField(required = True, label = 'lastname', max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    designation = forms.ModelChoiceField(required = True, label = 'Designation',queryset=TblDesignationMaster.objects.all())
    Team = forms.ModelChoiceField(queryset=TblTeamMaster.objects.all())
    phone_number = forms.CharField(required = True, label = 'Ph.No.', max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    password = forms.CharField(required = True, label = 'Password', max_length = 100, widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
    passwordagain = forms.CharField(required = True, label = 'Password1', max_length = 100, widget = forms.PasswordInput(attrs={'placeholder': 'Password (Again)'}))

class UploadFileForm(forms.Form):
    file = forms.FileField()

class FilterForm(forms.Form):
     columnname = forms.ModelChoiceField(queryset=TblActivity.objects.all())
     filteroption = forms.ModelChoiceField(queryset=TblActivity.objects.all())
     filterdata = forms.CharField()

class UsersigninForm(forms.Form):
    username = forms.CharField(required = True, label = 'username', max_length = 100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
#    password = forms.CharField(required = True, label = 'Password', max_length = 32, widget = forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

class UsersigninasotherForm(forms.Form):
    username = forms.CharField(required = True, label = 'username', max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Enter Username '}))
    password = forms.CharField(required = True, label = 'Password', max_length = 100, widget = forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

class RequestdetailForm(forms.ModelForm):
    class Meta():
        model = TblRequestdetail
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(RequestdetailForm, self).__init__(*args, **kwargs)
        self.fields['requestraiseddate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()


class AuthorisedetailForm(forms.ModelForm):
    class Meta():
        model = TblAuthorisedetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AuthorisedetailForm, self).__init__(*args, **kwargs)
        self.fields['authoriseddate'].widget = forms.HiddenInput()
        self.fields['authoriserid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()


class OverviewdetailForm(forms.ModelForm):
    class Meta():
        model = TblOverviewdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OverviewdetailForm, self).__init__(*args, **kwargs)
        self.fields['overviewdate'].widget = forms.HiddenInput()
        self.fields['giventoid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['providedbyid'].label = "Provided By"
        self.fields['sopcreatedid'].label = "SOP Created?"


class ActivitystatusCalendarForm(forms.ModelForm):
    class Meta():
        model = TblActivitystatusCalendar
        fields = '__all__'

class EstimationdetailForm(forms.ModelForm):
    class Meta():
        model = TblEstimationdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstimationdetailForm, self).__init__(*args, **kwargs)
        self.fields['estimationdate'].widget = forms.HiddenInput()
        self.fields['estimatedbyid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['estimateddays'].label = "Estimation in Hours"


class StatusdetailForm(forms.ModelForm):
    class Meta():
        model = TblRequeststatusdetail
        exclude = ['requestid']

    def __init__(self, *args, **kwargs):
        super(StatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['statusid'].widget  = forms.HiddenInput()


class RequeststatusdetailForm(forms.ModelForm):
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequeststatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['statusid'].widget  = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()

class RequeststatusdetailForm(forms.ModelForm):
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequeststatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['statusid'].widget  = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()

class UATstatusdetailForm(forms.ModelForm):
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UATstatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()


class AcceptRequeststatusdetailForm(forms.ModelForm):
    statusid = forms.ModelChoiceField(queryset=TblStatusMaster.objects.filter(statusnameid__in=[3,7]),required=False)
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AcceptRequeststatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['statusid'].label = "Status"

class AuthoriserstatusdetailForm(forms.ModelForm):
    statusid = forms.ModelChoiceField(queryset=TblStatusMaster.objects.filter(statusnameid__in=[3,2]),required=False)
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AuthoriserstatusdetailForm, self).__init__(*args, **kwargs)
        self.fields['requeststatusdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['statusid'].label = "Status"



class RequeststatusAcceptanceForm(forms.ModelForm):
    class Meta():
        model = TblRequeststatusdetail
        fields = '__all__'


class AssigneddetailForm(forms.ModelForm):
    class Meta():
        model = TblAssigneddetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AssigneddetailForm, self).__init__(*args, **kwargs)
        self.fields['assigneddate'].widget = forms.HiddenInput()
        self.fields['assignedbyid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['assignedtoid'].label = "Assigned To"


class TblConversationForm(forms.ModelForm):
    class Meta():
        model = TblConversation
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblConversationForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['requestid'].widget = forms.HiddenInput()
        self.fields['userid'].widget  = forms.HiddenInput()


class AcceptrejectdetailForm(forms.ModelForm):
    class Meta():
        model = TblAcceptrejectdetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AcceptrejectdetailForm, self).__init__(*args, **kwargs)
        self.fields['estacceptrejectdate'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()

class CompleteddetailForm(forms.ModelForm):
    class Meta():
        model = TblCompleteddetail
        fields = '__all__'

class RequestcategorysForm(forms.ModelForm):
    class Meta():
        model = TblCategorysMaster
        fields = '__all__'

class TimetrackersForm(forms.ModelForm):
    class Meta():
        model = TblTimeTracker
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimetrackersForm, self).__init__(*args, **kwargs)
        self.fields['trackingdatetime'].widget.attrs['class']  = 'date form-control'
        self.fields['categorysid'].widget.attrs['class']  = 'form-control'
        self.fields['subcategoryid'].widget.attrs['class']  = 'form-control'
        self.fields['activityid'].widget.attrs['class']  = 'form-control'
        self.fields['task'].widget.attrs['class']  = 'form-control'
        self.fields['totaltime'].widget.attrs['class']  = 'form-control'

class TimetrackersEditForm(forms.ModelForm):
    class Meta():
        model = TblTimeTracker
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimetrackersEditForm, self).__init__(*args, **kwargs)
        self.fields['registerdatetime'].widget = forms.HiddenInput()
        self.fields['trackingdatetime'].widget = forms.HiddenInput()
        self.fields['memberid'].widget = forms.HiddenInput()
        self.fields['teamid'].widget = forms.HiddenInput()
        self.fields['startdatetime'].widget = forms.HiddenInput()
        self.fields['stopdatetime'].widget = forms.HiddenInput()
        self.fields['otid'].widget = forms.HiddenInput()


class RequestcategorysForm(forms.ModelForm):
    class Meta():
        model = TblCategorysMaster
        fields = '__all__'

class RequestsubcategoryForm(forms.ModelForm):
    class Meta():
        model = TblSubcategoryMaster
        fields = '__all__'

class TeamdetailForm(forms.ModelForm):
    class Meta():
        model = TblTeamMaster
        fields = '__all__'

class EmaildetailForm(forms.ModelForm):
    class Meta():
        model = TblEmaildetail
        fields = '__all__'

class ErrorlogForm(forms.ModelForm):
    class Meta():
        model = TblErrorlog
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ErrorlogForm, self).__init__(*args, **kwargs)
        self.fields['datetime'].widget  = forms.HiddenInput()
        self.fields['activityid'].widget  = forms.HiddenInput()
        self.fields['occurancedate'].label = "Occurance Date"
        self.fields['occurancedate'].widget.attrs['class']  = 'date'
        self.fields['reportedbyid'].widget  = forms.HiddenInput()
        self.fields['reportedtoid'].widget  = forms.HiddenInput()
        self.fields['errortypeid'].label = "Error Type"
        self.fields['document'].label = "Upload Document (If any)"

class FeedbackForm(forms.ModelForm):
    class Meta():
        model = TblFeedback
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback_date'].widget  = forms.HiddenInput()
        self.fields['feedback_question'].widget  = forms.HiddenInput()
        self.fields['activityid'].widget  = forms.HiddenInput()
        self.fields['feedback_text'].label = "Feedback"

class OtDetailForm(forms.ModelForm):
    class Meta():
        model = TblOtDetail
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(OtDetailForm, self).__init__(*args, **kwargs)
        self.fields['ot_startdatetime'].widget.attrs['class']  = 'datetime'
        self.fields['ot_enddatetime'].widget.attrs['class']  = 'datetime'
        self.fields['timetrackerid'].widget  = forms.HiddenInput()
        self.fields['ot_time'].widget  = forms.HiddenInput()
        self.fields['ot_startdatetime'].label = "Start DateTime"
        self.fields['ot_enddatetime'].label = "End DateTime"
        self.fields['otdocument'].label = "Upload Document (if any)"
        self.fields['statusid'].widget  = forms.HiddenInput()


class OtDetail1Form(forms.ModelForm):
    class Meta():
        model = TblOtDetail
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(OtDetail1Form, self).__init__(*args, **kwargs)
        self.fields['ot_startdatetime'].widget.attrs['disabled']  = True
        self.fields['ot_enddatetime'].widget.attrs['disabled']  = True
        self.fields['otdocument'].widget.attrs['disabled']  = True


REPORT_CHOICES = (
    (1, ("Workflow")),
    (2, ("TimeTracker")),
    (3, ("ErrorLog")),
    (4, ("OT"))
    )

INTERVAL_CHOICES = (
    (1, ("Daily")),
    (2, ("Weekly")),
    (3, ("Monthly")),
    )

TYPE_CHOICES = (
    (1, ("Raw Data")),
    (2, ("Summary")),
    (3, ("Visualistion")),
    )

class SearchForm(forms.Form):
    datachoice = forms.ChoiceField(choices = REPORT_CHOICES, label="Date Choice", initial=1, widget=forms.Select(), required=True)
    datatype = forms.ChoiceField(choices = TYPE_CHOICES, label="Type", initial=1, widget=forms.Select(), required=True)
    interval = forms.ChoiceField(choices = INTERVAL_CHOICES, label="Interval", initial=1, widget=forms.Select(), required=True)
    startdate = forms.DateField(initial=datetime.now() - timedelta(days=1), label="StartDate",required=False)
    enddate = forms.DateField(initial=datetime.now(), required=False,label="EndDate")
    team = forms.ModelChoiceField(queryset=TblTeamMaster.objects.all(),required =False,label="Team")
    member = forms.ModelChoiceField(queryset=TblMember.objects.all(),required =False,label="Member")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['datachoice'].widget.attrs['class']  = 'form-control'
        self.fields['datatype'].widget.attrs['class']  = 'form-control'
        self.fields['startdate'].widget.attrs['class']  = 'date form-control'
        self.fields['startdate'].widget.attrs['class']  = 'date form-control'
        self.fields['enddate'].widget.attrs['class']  = 'date form-control'
        self.fields['team'].widget.attrs['class']  = 'form-control'
        self.fields['member'].widget.attrs['class']  = 'form-control'


class SearchForm1(forms.Form):
    datachoice = forms.ChoiceField(choices = REPORT_CHOICES, label="Date Choice", initial=1, widget=forms.Select(), required=True)
    datatype = forms.ChoiceField(choices = TYPE_CHOICES, label="Type", initial=1, widget=forms.Select(), required=True)
    interval = forms.ChoiceField(choices = INTERVAL_CHOICES, label="Interval", initial=1, widget=forms.Select(), required=True)
    startdate = forms.DateField(initial=datetime.now(), label="StartDate",required=False)
    enddate = forms.DateField(initial=datetime.now(), required=False,label="EndDate")
    team = forms.ModelChoiceField(queryset=TblTeamMaster.objects.all(),required =False,label="Team")
    member = forms.ModelChoiceField(queryset=TblMember.objects.all(),required =False,label="Member")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['datachoice'].widget.attrs['class']  = 'form-control'
        self.fields['datatype'].widget.attrs['class']  = 'form-control hidden'
        self.fields['startdate'].widget.attrs['class']  = 'date form-control'
        self.fields['startdate'].widget.attrs['class']  = 'date form-control'
        self.fields['enddate'].widget.attrs['class']  = 'date form-control'
        self.fields['team'].widget.attrs['class']  = 'form-control'
        self.fields['member'].widget.attrs['class']  = 'form-control'





class FilteredForm(forms.Form):
    bufilter = forms.ModelChoiceField(queryset=TblBusinessUnitMaster.objects.all(),required =False)
    teamfilter = forms.ModelChoiceField(queryset=TblTeamMaster.objects.all(),required =False)
    memberfilter = forms.ModelChoiceField(queryset=TblMember.objects.all(),required =False)
    def __init__(self, *args, **kwargs):
        super(FilteredForm, self).__init__(*args, **kwargs)
        self.fields['teamfilter'].widget.attrs['class']  = 'form-control mb-2'
        self.fields['memberfilter'].widget.attrs['class']  = 'form-control'


class ViewForm(forms.Form):
    VIEW_CHOICES = (
        (1, ("Overall View")),
        (2, ("Team View")),
        (3, ("MY View")),
        )
    viewchoice = forms.ChoiceField(choices = VIEW_CHOICES, label="Select View", initial=3, widget=forms.Select(), required=True)

class ActivityForm(forms.ModelForm):
    class Meta():
        model = TblActivity
        fields = '__all__'
        widgets = { 'registereddate': forms.HiddenInput(),}

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['registereddate'].label = "Registered Date"

class MemberForm(forms.ModelForm):
    class Meta():
        model = TblMember
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['userid'].widget  = forms.HiddenInput()
        self.fields['dateofjoining'].label = "Date of Joining"
        self.fields['dateofbirth'].label = "Date of Birth"
        self.fields['phonenumber'].label = "Ph. No"
        self.fields['aboutme'].label = "About Me"
        self.fields['dateofjoining'].widget.attrs['class']  = 'date'
        self.fields['dateofbirth'].widget.attrs['class']  = 'date'

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget  = forms.HiddenInput()
        self.fields['last_login'].widget  = forms.HiddenInput()
        self.fields['is_superuser'].widget  = forms.HiddenInput()
        self.fields['groups'].widget  = forms.HiddenInput()
        self.fields['user_permissions'].widget  = forms.HiddenInput()
        self.fields['username'].widget  = forms.HiddenInput()
        self.fields['is_staff'].widget  = forms.HiddenInput()
        self.fields['is_active'].widget  = forms.HiddenInput()
        self.fields['date_joined'].widget  = forms.HiddenInput()




class InternaltaskForm(forms.ModelForm):
    class Meta():
        model = TblInternaltask
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(InternaltaskForm, self).__init__(*args, **kwargs)
        self.fields['internaltaskdatetime'].widget  = forms.HiddenInput()
        self.fields['internaltaskquestion'].label = "Question"
        self.fields['statusid'].label = "Status"
        self.fields['ownerid'].widget =  forms.HiddenInput()
        self.fields['targetdate'].label = "Target Date"
        self.fields['targetdate'].widget.attrs['class']  = 'date form-control'
        self.fields['link'].label = "Link"


class InternaltaskchoiceForm(forms.ModelForm):
    class Meta():
        model = TblInternaltaskchoice
        fields = '__all__'

class InternaltaskstatusForm(forms.ModelForm):
    class Meta():
        model = TblInternaltaskstatus
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(InternaltaskstatusForm, self).__init__(*args, **kwargs)
        self.fields['internaltaskstatusdatetime'].widget  = forms.HiddenInput()
        self.fields['memberid'].widget  = forms.HiddenInput()
        self.fields['internaltaskid'].widget  = forms.HiddenInput()
        self.fields['internaltaskchoiceid'].widget  = forms.HiddenInput()


class SuccessStoriesForm(forms.ModelForm):
    class Meta():
        model = TblSuccessStories
        fields = '__all__'


class GovernanceForm(forms.ModelForm):
    class Meta():
        model = TblGovernance
        fields = '__all__'


class SuggestionForm(forms.ModelForm):
    class Meta():
        model = TblSuggestion
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(SuggestionForm, self).__init__(*args, **kwargs)
        self.fields['suggestiondatetime'].widget = forms.HiddenInput()
        self.fields['suggestedbyid'].widget = forms.HiddenInput()


class ReplyForm(forms.ModelForm):
    class Meta():
        model = TblReply
        fields = '__all__'

class WhatwedoForm(forms.ModelForm):
    class Meta():
        model = TblWhatwedo
        fields = '__all__'

class TblLeaveRecordForm(forms.ModelForm):
    class Meta():
        model = TblLeaveRecord
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblLeaveRecordForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['userid'].widget = forms.HiddenInput()
        self.fields['leave_date'].widget.attrs['class']  = 'date form-control'


class TblAppreciationForm(forms.ModelForm):
    class Meta():
        model = TblAppreciation
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblAppreciationForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()

class TblRawActivityDetailForm(forms.ModelForm):
    class Meta():
        model = TblRawActivityDetail
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblRawActivityDetailForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['raw_activity'].label = "Activity"
        self.fields['raw_activity_description'].label = "Activity Description"
        self.fields['raw_activity_img'].label = "Upload Img"
        self.fields['raw_activity_scheduled'].label = "ACtivity Scheduled"
        self.fields['raw_statusid'].label = "Status"


class TblRawScoreForm(forms.ModelForm):
    class Meta():
        model = TblRawScore
        fields = '__all__'

class TblRawTeamMasterForm(forms.ModelForm):
    class Meta():
        model = TblRawTeamMaster
        fields = '__all__'

class TblRawTeamMemberMasterForm(forms.ModelForm):
    class Meta():
        model = TblRawTeamMemberMaster
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblRawTeamMemberMasterForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()


class TblTeamMetricsForm(forms.ModelForm):
    class Meta():
        model = TblTeamMetrics
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblTeamMetricsForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['teamid'].widget = forms.HiddenInput()
        self.fields['requesttypeid'].widget = forms.HiddenInput()

class TblRawScoreForm(forms.ModelForm):
    class Meta():
        model = TblRawScore
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblRawScoreForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['raw_teamid'].widget = forms.HiddenInput()


class TblUsefulLinksForm(forms.ModelForm):
    class Meta():
        model = TblUsefulLinks
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(TblUsefulLinksForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['memberid'].widget = forms.HiddenInput()


class UatDetailForm(forms.ModelForm):
    class Meta():
        model = TblUatDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UatDetailForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['uat_statusid'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['testedbyid'].widget  = forms.HiddenInput()
        self.fields['updatedbyid'].widget  = forms.HiddenInput()

class UatDetail1Form(forms.ModelForm):
    class Meta():
        model = TblUatDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UatDetail1Form, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['requestid'].widget  = forms.HiddenInput()
        self.fields['testedbyid'].widget  = forms.HiddenInput()
        self.fields['updatedbyid'].widget  = forms.HiddenInput()
        self.fields['uat_statusid'].label = "UAT Status"


class IssueActionForm(forms.ModelForm):
    class Meta():
        model = TblIssueAction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IssueActionForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['updatedbyid'].widget  = forms.HiddenInput()

class ShiftupdateForm(forms.ModelForm):
    class Meta():
        model = TblShiftUpdate
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ShiftupdateForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['recordedbyid'].widget = forms.HiddenInput()

class GalleryForm(forms.ModelForm):
    class Meta():
        model = TblGallery
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields['uploadedbyid'].widget = forms.HiddenInput()

class PublicholidaysForm(forms.ModelForm):
    class Meta():
        model = TblPublicHolidaysMaster
        fields = '__all__'
