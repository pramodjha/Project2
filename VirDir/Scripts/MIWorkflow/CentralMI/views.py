from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView,ListView
from django.db import connection, transaction
from .forms import RequestdetailForm , EstimationdetailForm, OverviewdetailForm, AuthorisedetailForm, RequeststatusdetailForm, AssigneddetailForm, AcceptrejectdetailForm, CompleteddetailForm, UserRegistrationForm, UsersigninForm,  RequestcategorysForm,  TimetrackersForm, RequestcategorysForm, RequestsubcategoryForm, TeamdetailForm, StatusdetailForm, UploadFileForm, ReportsForm,EmaildetailForm,FilterForm, ErrorlogForm, OtDetailForm, FeedbackForm, SearchForm,FilteredForm,ActivityForm,  INTERVAL_CHOICES, MimemberForm, UserForm, InternaltaskForm, InternaltaskchoiceForm, InternaltaskstatusForm
from .models import Acceptrejectdetail, Acceptrejectoption, Assigneddetail, Authorisedetail, Authoriserdetail, Completeddetail, Estimationdetail, Mimember, Options, Overviewdetail, Prioritydetail, Requestcategorys, Requestdetail, Requeststatusdetail, Requestsubcategory, Requesttypedetail, Statusdetail, Teamdetail, Timetrackers, Reports, Emaildetail, Errorlog, OtDetail,Activity, FeedbackQuestion,Feedback, AuthUser, Internaltask, Internaltaskchoice, Internaltaskstatus
from django.core import serializers
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy, resolve
from django.db import connection
import datetime
import getpass
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import JsonResponse
import datetime
from datetime import datetime, timedelta, date
from django.db.models import Count, Avg, Sum
import numpy as np
import calendar
import os
from collections import OrderedDict
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pandas as pd
from django.http import JsonResponse
from django.template.loader import render_to_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")

@login_required
def Report_create(request):
    form = ActivityForm()
    context = {'form': form}
    html_form = render_to_string('books/includes/partial_book_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})

@login_required
def create_session(request,header=None,footer=None,loginpage=None):
    username = request.user.username
    sd = request.session.get('setdate')
    info = vistorinfo_output(username,sd)
    info.getinfo()
    info.is_member()
    try:
        authority = info.permission
    except:
        authority = ''
    request.session['activeheader'] = header
    request.session['activefooter'] = footer
    activetab = request.session.get('activeheader')
    activetab1 = request.session.get('activefooter')
    return authority, activetab, activetab1, username, info, sd

@login_required
def create_session_onerror(request,header=None,footer=None,loginpage=None):
    username = request.user.username
    authority = ''
    request.session['activeheader'] = header
    request.session['activefooter'] = footer
    activetab = request.session.get('activeheader')
    activetab1 = request.session.get('activefooter')
    return authority, activetab, activetab1, username


@login_required
def data_extraction(request,parameter1=None,parameter2=None):
    #print(parameter1)
    cur = connection.cursor()
    ret = cur.execute("[CentralMI].[dbo].[uspjoin] " + parameter1 + ","  + parameter2)
    def dictfetchall(cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]
    data = dictfetchall(ret)
    return data

@login_required
def setdate(request):
    try:
        selecteddate = request.POST.get('trackingdatetime')
        #print(selecteddate)
        if selecteddate == None:
            currentdate = str(datetime.date.today())
            selecteddate = currentdate
        selecteddate = selecteddate
        request.session['setdate'] = selecteddate
        return HttpResponseRedirect(reverse('timetracker'))
    except:
        return render(request, 'CentralMI/ErrorPage.html')

def sign_up(request):
    #authority, activetab, activetab1, username, info, sd = create_session(request, header='signup',footer='')
    activetab = 'signup'
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            passwordagain =  userObj['passwordagain']
            firstname =  userObj['firstname']
            lastname =  userObj['lastname']
            print(password)
            print(passwordagain)
            if password == passwordagain:
                if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                    new_user = User.objects.create_user(username, email, password)
                    new_user.is_active = True
                    new_user.first_name = firstname
                    new_user.last_name = lastname
                    new_user.save()
    #                info_email = sendemail(to_email=email, status="signup")
    #                info_email.sending_email()
                    try:
                        user = authenticate(username = username, password = password)
                        login(request, user)
                        return HttpResponseRedirect(reverse('lp'))
                    except:
                        form =  UserRegistrationForm()
                        return render(request,'CentralMI/ErrorPage.html')
                else:
                    form = UserRegistrationForm()
                    return render(request,'CentralMI/ErrorPage.html')
            else:
                form = UserRegistrationForm()
                return render(request,'CentralMI/ErrorPage.html')

        else:
            form = UserRegistrationForm()
            return render(request, 'CentralMI/signup.html', {'form' : form,'activetab':activetab})
    else:
        form = UserRegistrationForm()
        return render(request, 'CentralMI/signup.html', {'form' : form,'activetab':activetab})


def sign_in(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request, header='signin',footer='')
    except:
        authority = ''
        activetab = 'signin'

    tab = request.session.get('tabname')
    if request.method == 'POST':
        form =  UsersigninForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            password =  userObj['password']

            #print(password)
            if (User.objects.filter(username=username).exists()):
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    form =  UsersigninForm()
                return render(request,'CentralMI/ErrorPage.html')
            else:
                form =  UsersigninForm()
                return render(request,'CentralMI/ErrorPage.html')
        else:
            form =  UsersigninForm()
            return render(request, 'CentralMI/signin.html', {'form' : form,'activetab':activetab,'authority':authority})
    else:
        form =  UsersigninForm()
        return render(request, 'CentralMI/signin.html', {'form' : form,'activetab':activetab,'authority':authority})

def sign_out(request):
    #if request.method == 'POST':
    request.session.delete()
    logout(request)
    return HttpResponseRedirect(reverse('signin'))

@login_required
def All_request(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='allrequest')
    data = data_extraction(request,parameter1="'All'",parameter2="'All'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})

@login_required
def unapproved(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='unapproved')
    data = data_extraction(request,parameter1="'Approval pending'",parameter2="'RequestStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})

@login_required
def approved(request):
    authority, activetab, activetab1, username, info, sd= create_session(request,  header='workflow',footer='approved')
    data = data_extraction(request,parameter1="'Approved'",parameter2="'AuthorisedStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def assigned(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='assigned')
    data = data_extraction(request,parameter1="'Assigned'",parameter2="'AssignedStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def overview(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='overview')
    data = data_extraction(request,parameter1="'Overviewed'",parameter2="'OverviewStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})

@login_required
def estimate(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='estimate')
    data = data_extraction(request,parameter1="'Estimated'",parameter2="'EstimateStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def wip(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='wip')
    data = data_extraction(request,parameter1="'Estimation Accepted'",parameter2="'WIPStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def completed(request):
    authority, activetab, activetab1, username, info, sd= create_session(request,  header='workflow',footer='completed')
    data = data_extraction(request,parameter1="'Completed'",parameter2="'CompletedStage'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})

@login_required
def rejected(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='rejected')
    data = data_extraction(request,parameter1="'Rejected'",parameter2="'All'")
    return render(request, 'CentralMI/DetailView.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def Error_Log(request,reportid):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='report',footer='')
    form = ErrorlogForm(initial={'error_report':reportid})
    if request.method == 'POST':
        form = ErrorlogForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('errordetail'))
    return render(request, 'CentralMI/ErrorLog.html',{'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def Error_detail(request):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='report',footer='errordetail')
    data = Errorlog.objects.all()
    return render(request, 'CentralMI/errordetail.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})

@login_required
def EditError_Log(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
    e = Errorlog.objects.get(pk=requestid)
    model = Errorlog.objects.filter(pk=requestid)
    form = ErrorlogForm(instance=e)
    if request.method == 'POST':
        e = Errorlog.objects.get(pk=requestid)
        form = ErrorlogForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('errordetail'))
    return render(request, 'CentralMI/ErrorLogEdit.html', {'form':form,'model':model, 'username':username,'authority':authority,'activetab':activetab})

def modelview(request):
    form = FilteredForm()
    return render(request, 'CentralMI/modeltest.html',{'form':form})

@login_required
def ot_form(request,trackerid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='timetracker',footer='otdetail')
    form = OtDetailForm(initial={'timetrackers':trackerid,'ot_status':1})
    if request.method == 'POST':
        form =  OtDetailForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            startdate = form.cleaned_data['ot_startdatetime']
            enddate = form.cleaned_data['ot_enddatetime']
            try:
                time = str(enddate-startdate).split(':')
                timehours = time[0]
                timemin = time[1]
                timesec = time[2]
                Totalmin = (int(timehours) * 60) + int(timemin) + (int(timesec)/60)
                inst.ot_hrs = Totalmin
            except:
                inst.ot_hrs = 0
            inst.save()
            return HttpResponseRedirect(reverse('otdetail'))
    return render(request, 'CentralMI/otform.html',{'form':form,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})

def OT_detail(request):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='timetracker',footer='otdetail')
    data = OtDetail.objects.all()
    return render(request, 'CentralMI/otdetail.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'authority':authority,'username':username})


@login_required
def summary_tracker(request):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='extractdatafilter',footer='summary')
    form = SearchForm()
    if request.method == 'POST':
        form =  SearchForm(request.POST)
        if form.is_valid():
            reportno = form.cleaned_data['datachoice']
            startdate = form.cleaned_data['startdate']
            interval = dict(INTERVAL_CHOICES)[int(form.cleaned_data["interval"])]
            enddate = form.cleaned_data['enddate']
            team = form.cleaned_data['team']
            member = form.cleaned_data['member']
            print(interval)
            model = info.define_day_week_month2(report_choice='2',start_date=startdate,end_date=enddate,range_type=interval,values='requestraiseddate',aggregatefield='requestid',core_noncore=None,OT=None,teamdetail=team,member=member,output_type='extract_summary')
            return render(request, 'CentralMI/summary.html',{'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})
    return render(request, 'CentralMI/summary.html',{'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})


def filterdata(request):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='extractdatafilter',footer='extractdatafilter1')
    form = SearchForm()
    if request.method == 'POST':
        form =  SearchForm(request.POST)
        if form.is_valid():
            reportno = form.cleaned_data['datachoice']
            startdate = form.cleaned_data['startdate']
            enddate = form.cleaned_data['enddate']
            team = form.cleaned_data['team']
            member = form.cleaned_data['member']
            if team == None and member == None:
                if reportno == str(2):
                    model = Requestdetail.objects.filter(requestraiseddate__range=[startdate, enddate])
                elif reportno == str(3):
                    model = Timetrackers.objects.filter(trackingdatetime__range=[startdate, enddate])
                elif reportno == str(4):
                    model = Errorlog.objects.filter(error_occurancedate__range=[startdate, enddate])
                elif reportno == str(5):
                    model = OtDetail.objects.filter(ot_startdatetime__range=[startdate, enddate])
                elif reportno == str(1):
                    model=  ''
                else:
                    model = ''
            elif team != None and member == None:
                teamno = Teamdetail.objects.filter(teamname__in=[team]).values_list('teamid',flat=True).distinct()
                userno = Mimember.objects.filter(teamdetail__in=list(teamno)).values_list('mimemberid',flat=True).distinct()
                trackerid = Timetrackers.objects.filter(mimember__in=list(userno)).values_list('timetrackerid',flat=True).distinct()
                if reportno == str(2):
                    model = Requestdetail.objects.filter(username__in=list(userno)).filter(requestraiseddate__range=[startdate, enddate])
                elif reportno == str(3):
                    model = Timetrackers.objects.filter(mimember__in=list(userno)).filter(trackingdatetime__range=[startdate, enddate])
                elif reportno == str(4):
                    model = Errorlog.objects.filter(error_reportedto__in=list(userno)).filter(error_occurancedate__range=[startdate, enddate])
                elif reportno == str(5):
                    model = OtDetail.objects.filter(timetrackers__in=list(trackerid)).filter(ot_startdatetime__range=[startdate, enddate])
                elif reportno == str(1):
                    model=  ''
                else:
                    model = ''
            elif team != None and member != None:
#                print(member)
                memberid = User.objects.get(username__in=[member]).id
                trackerid = Timetrackers.objects.filter(mimember__in=[member]).values_list('timetrackerid',flat=True).distinct()
                if reportno == str(2):
                    model = Requestdetail.objects.filter(username__in=[memberid]).filter(requestraiseddate__range=[startdate, enddate])
                elif reportno == str(3):
                    model = Timetrackers.objects.filter(mimember__in=[member]).filter(trackingdatetime__range=[startdate, enddate])
                elif reportno == str(4):
                    model = Errorlog.objects.filter(error_reportedto__in=[member]).filter(error_occurancedate__range=[startdate, enddate])
                elif reportno == str(5):
                    model = OtDetail.objects.filter(timetrackers__in=list(trackerid)).filter(ot_startdatetime__range=[startdate, enddate])
                elif reportno == str(1):
                    model=  ''
                else:
                    model = ''

            #print(enddate)
            return render(request, 'CentralMI/extract_data.html',{'model':model,'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno})
        return render(request, 'CentralMI/extract_data.html',{'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})
    return render(request, 'CentralMI/extract_data.html',{'form':form,'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})




@login_required
def about_team(request):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='home',footer='aboutteam')
    return render(request, 'CentralMI/about_team.html',{'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def whatwedo(request):
    authority, activetab, activetab1, username, info, sd= create_session(request, header='home',footer='whatwedo')
    return render(request, 'CentralMI/about_team.html',{'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def governanceprocess(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='governanceprocess')
    return render(request, 'CentralMI/about_team.html',{'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def successstories(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='successstories')
    return render(request, 'CentralMI/about_team.html',{'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def comm_sugg(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,header='home',footer='comm_sugg')
    return render(request, 'CentralMI/about_team.html',{'authority':authority,'activetab':activetab,'activetab1':activetab1,'username':username})

@login_required
def ReportForm(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='')
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('allreports'))
        else:
            return render(request, 'CentralMI/ErrorPage.html')
    else:
        return render(request, 'CentralMI/Reports.html',{'form':form,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/Reports.html',{'form':form,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def EditReport(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
    e = Activity.objects.get(pk=requestid)
    model = Activity.objects.filter(pk=requestid)
    form = ActivityForm(instance=e)
    if request.method == 'POST':
        e = Activity.objects.get(pk=requestid)
        form = ActivityForm(request.POST,request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('allreports'))
    return render(request, 'CentralMI/ReportsEdit.html', {'form':form,'model':model, 'username':username,'authority':authority,'activetab':activetab})


@login_required
def check_status(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='checkstatus')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='loginrequest',footer='checkstatus')

    userid = User.objects.get(username=username).pk
    model = Requestdetail.objects.filter(username__in=[userid])
    return render(request, 'CentralMI/check_status.html',{'model':model,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})

@login_required
def Report_Detail(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='allreports')
    model = Activity.objects.all()
    return render(request, 'CentralMI/allreports.html',{'model':model,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})

@login_required
def feedback(request,reportid,id=1):
    id_cumulative = 0
    authority, activetab, activetab1, username, info, sd= create_session(request, header='report',footer='')
    #exist = Feedback.objects.filter(activity__in=[reportid]).count()
#    if exist > 0:
#        return HttpResponseRedirect(reverse('allreports'))
#    else:
    #request.session['reportid'] = reportid
    questionlen = FeedbackQuestion.objects.count()
    #activeid = request.session.get('reportid')
    form = FeedbackForm(initial={'activity':reportid,'feedback_question':id})
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            id_cumulative = int(int(id_cumulative) + 1)
            id = id_cumulative
            if id > questionlen:
                return HttpResponseRedirect(reverse('allreports'))
            else:
                print(reportid)
                print(id)
                return HttpResponseRedirect(reverse('feedback', args={reportid,id}))
    return render(request, 'CentralMI/feedback.html',{'form':form,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})

@login_required
def Feedback_Detail(request):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='feedbackdetail')
    model = Feedback.objects.all()
    return render(request, 'CentralMI/feedbackdetail.html',{'model':model,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})

@login_required
def Feedback_Detail_id(request,reportid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='feedbackdetail')
    model = Feedback.objects.filter(activity__in=[reportid])
    return render(request, 'CentralMI/feedbackdetail.html',{'model':model,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})


@login_required
def EditFeedback(request,feedbackid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='feedbackdetail')
    e = Feedback.objects.get(pk=feedbackid)
    model = Feedback.objects.filter(pk=feedbackid)
    form = FeedbackForm(instance=e)
    if request.method == 'POST':
        e = Feedback.objects.get(pk=feedbackid)
        form = FeedbackForm(request.POST,request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('feedbackdetail'))
    return render(request, 'CentralMI/editfeedbackform.html',{'form':form,'username':username,'authority':authority, 'activetab':activetab,'activetab1':activetab1})

@login_required
def RequestFormTemplate(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='addrequest')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='loginrequest',footer='addrequest')

    userid = User.objects.get(username=username).pk
    form = RequestdetailForm(initial={'username':userid})
    form1 = StatusdetailForm(initial={'statusdetail':1,'username':userid,'requestdetail':None})
    if request.method == 'POST':
        form = RequestdetailForm(request.POST,request.FILES)
        form1 = StatusdetailForm (request.POST)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=True)
            inst.save()
            newid = inst.pk
            inst1 = form1.save(commit=False)
            inst1.requestdetail = inst
            inst1.save()
#            dataforemail(username=inst.username,
#                        requestid = inst.requestid,
#                        sub_user='Request registered successfully',
#                        L1_user='Your request is sent for approval to Authoriser, any update on your request will be sent through email ',
#                        sub_auth='Please Authorise the request',
#                        L1_auth='A request has been raised, pending for your approval',
#                        sub_miteam='Request raised, pending for approval ',
#                        L1_miteam='New request has been raised, however peding for Approval',
#                        sub_manager='Request raised, pending for approval ',
#                        L1_manager='New request has been raised, however peding for Approval',
#                        request_status='Pending for Approval')
            return HttpResponseRedirect(reverse('ty',args = (newid,)))
        else:
            return render(request, 'CentralMI/ErrorPage.html')
    else:
        return render(request, 'CentralMI/RequestForm.html',{'form':form,'form1':form1,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/RequestForm.html',{'form':form,'form1':form1,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})

@login_required
def view_staff_detail(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='viewdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='viewdetail')
    print(authority)
    if authority == "Group2":
        model1 = User.objects.all()
        model = Mimember.objects.all()
        data = zip(model1,model)
    elif authority == "Group4":
        userid = User.objects.get(username=username).pk
        model1 = User.objects.filter(username__in=[username])
        model = Mimember.objects.filter(username__in=[userid])
        data = zip(model1,model)
    return render(request, 'CentralMI/Employee_Detail.html',{'model':model,'model1':model1,'data':data,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def edit_staff_detail(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='')
    userid = User.objects.get(username=username).pk
    e1 = User.objects.get(pk=userid)
    print(e1)
    e = Mimember.objects.get(username=userid)
    model1 = User.objects.filter(username__in=username)
    model = Mimember.objects.filter(username__in=[userid])
    form1 = UserForm(instance=e1)
    print(username)
    form = MimemberForm(instance=e)
    if request.method == 'POST':
        form = MimemberForm(request.POST,instance=e)
        form1 = UserForm (request.POST,instance=e1)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=True)
            inst.save()
            inst1 = form1.save(commit=False)
            inst1.username = username
            inst1.save()
            return HttpResponseRedirect(reverse('viewDetail'))
        else:
            return render(request, 'CentralMI/ErrorPage.html')
    else:
        return render(request, 'CentralMI/EditStaffDetail.html',{'form':form,'form1':form1,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/EditStaffDetail.html',{'form':form,'form1':form1,  'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})



@login_required
def internal_task_detail(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    model = Internaltask.objects.all()
    return render(request, 'CentralMI/InternalTaskDetail.html',{'model':model, 'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def view_internal_task(request,taskid):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    model = Internaltaskchoice.objects.filter(internaltask__in=[taskid])
    return render(request, 'CentralMI/InternalTaskChoiceView.html',{'model':model, 'taskid':taskid,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def add_internal_task_detail(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    userid = User.objects.get(username=username).id
    mimemberid = Mimember.objects.get(username=userid).mimemberid
    form = InternaltaskForm(initial={'owner':mimemberid})
    if request.method == 'POST':
        form = InternaltaskForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('internaltaskdetail'))
    return render(request, 'CentralMI/addinternaltask.html',{'form':form, 'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})

@login_required
def edit_internal_task_detail(request,taskid):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    e = Internaltask.objects.get(internaltaskid=taskid)
    form = InternaltaskForm(instance=e)
    if request.method == 'POST':
        form = InternaltaskForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('internaltaskdetail'))
    return render(request, 'CentralMI/addinternaltask.html',{'form':form, 'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})



@login_required
def edit_internal_choice(request,choiceid):
    print(choiceid)
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    e = Internaltaskchoice.objects.get(internaltaskchoiceid=choiceid)
    question = Internaltaskchoice.objects.get(internaltaskchoiceid=choiceid).internaltask
    print(question)
    taskid = Internaltask.objects.get(internaltaskquestion=question).internaltaskid
    print(taskid)
#    print(id)
    form =  InternaltaskchoiceForm(instance=e)
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('viewinternaltaskoption',args = (taskid,)))
        else:
            return render(request, 'CentralMI/ErrorPage.html')
    else:
        return render(request, 'CentralMI/InternalTaskChoiceEdit.html',{'form':form,'taskid':taskid,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/InternalTaskChoiceEdit.html',{'form':form,'taskid':taskid,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def add_internal_choice(request,taskid):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    id = taskid
    print(id)
    form =  InternaltaskchoiceForm(initial={'internaltask':taskid})
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('viewinternaltaskoption',args = (id,)))
        else:
            return render(request, 'CentralMI/ErrorPage.html')
    else:
        return render(request, 'CentralMI/InternalTaskChoiceEdit.html',{'form':form,'taskid':taskid,'id':id,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/InternalTaskChoiceEdit.html',{'form':form,'taskid':taskid,'id':id,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})


@login_required
def internal_task_with_choice(request,taskid):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='Details',footer='internaltaskdetail')
    model =  Internaltask.objects.filter(internaltaskid__in=[taskid])
    model1 = Internaltaskchoice.objects.filter(internaltask__in=[taskid])
    userid = User.objects.get(username=username).id
    memberid = Mimember.objects.get(username=userid).mimemberid
    checkmember = Internaltaskstatus.objects.filter(mimember__in=[memberid]).count()
    model2 = Internaltaskstatus.objects.filter(mimember__in=[memberid])
    print(model2)
    print(checkmember)
    if checkmember > 0:
        e = Internaltaskstatus.objects.get(mimember__in=[memberid])
        form = InternaltaskstatusForm(instance=e)
        #print(form)
        if request.method == 'POST':
            choice = request.POST['choice']
            e = Internaltaskchoice.objects.get(internaltaskchoice=choice)
            form =  InternaltaskstatusForm(request.POST,instance=e)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.internaltaskchoice = e
                inst.save()
                return HttpResponseRedirect(reverse('internaltaskdetail'))
            else:
                return render(request, 'CentralMI/internaltaskwithchoice.html',{'form':form,'model':model,'model1':model1,'model2':model2,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})

    else:
        form =  InternaltaskstatusForm(initial={'internaltask':taskid, 'mimember':memberid})
        if request.method == 'POST':
            choice = request.POST['choice']
            e = Internaltaskchoice.objects.get(internaltaskchoice=choice)
            print(choice)
            form =  InternaltaskstatusForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.internaltaskchoice = e
                inst.save()
                return HttpResponseRedirect(reverse('internaltaskdetail'))
            else:
                return render(request, 'CentralMI/internaltaskwithchoice.html',{'form':form,'model':model,'model1':model1,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    return render(request, 'CentralMI/internaltaskwithchoice.html',{'form':form,'model':model,'model1':model1,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})






@login_required
def AuthorisedFormTemplate(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='unapproved')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Authorisedetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('unapproved'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = AuthorisedetailForm(initial={'requestdetail':requestid, 'Authorisedetail':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':2,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = AuthorisedetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user= 'Request ID ' + str(requestid) +'  has been ' + str(inst1.statusdetail) ,
                        L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , now it is with MI-Team to assign ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + 'has been ' + str(inst1.statusdetail) + ' , hence no futher action required',
                        sub_auth='Thanks for authorising Request ID ' + str(requestid) ,
                        L1_auth='Request is with MI-Team to Assign ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + ' has been ' + str(inst1.statusdetail) + ' , hence no futher action required' ,
                        sub_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail),
                        L1_miteam='Authoriser has '  + str(inst1.statusdetail) + ' the request, assign to appropriate member ' if str(inst1.statusdetail)=='Approved' else ' Request ID ' + str(requestid) + ' has been '  + str(inst1.statusdetail) + ' , hence no futher action required',
                        sub_manager='Request ID ' + str(requestid) + ' need to be assigned ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + ' has been ' + str(inst1.statusdetail) + ' , hence no futher action required',
                        L1_manager='Request has authorised and it is with MI-Team to assign',
                        request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('unapproved'))
            else:
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/AuthorisedForm.html',{'form':form, 'form1':form1,'authority':authority,'activetab':activetab,'activetab1':activetab1})

@login_required
def RequestassigneddetailFormTemplate(request, requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='approved')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Assigneddetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('approved'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        #print(request_owner)
        form = AssigneddetailForm(initial={'requestdetail':requestid, 'assignedby':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':4,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = AssigneddetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) + ' to ' + str(inst.assignedto),
                        L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , now it is with MI-Team to Overview ',
                        sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto),
                        L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto) + ' ,next step is take Overview',
                        sub_miteam='Request has been succesfully assigned to '+  str(inst.assignedto),
                        L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ 'to ' + str(inst.assignedto),
                        sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto) ,
                        L1_manager='Next Step is to take overview of request',
                        request_status=str(inst1.statusdetail))

                return HttpResponseRedirect(reverse('approved'))

            else:
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/AssignedForm.html',{'form':form,'form1':form1,'authority':authority,'activetab1':activetab1,'activetab':activetab})



@login_required
def OverviewFormTemplate(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='assigned')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Overviewdetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('assigned'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = OverviewdetailForm(initial={'requestdetail':requestid, 'mimember':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':5,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = OverviewdetailForm(request.POST,request.FILES)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
                        L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , shortly estimation in hours will be provided ',
                        sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
                        L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + '  , shortly estimation in hours will be provided',
                        sub_miteam='Request ID ' + str(requestid) + ' has been overviewed',
                        L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ ', please provide the estimation of the same',
                        sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
                        L1_manager='Next Step is with MI-Team to provide estimation in hours',
                        request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('assigned'))
            else:
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/OverviewForm.html',{'form':form,'form1':form1,'username':username,'authority':authority,'activetab1':activetab1,'activetab':activetab})

@login_required
def EstimationFormTemplate(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='overview')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Estimationdetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('overview'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = EstimationdetailForm(initial={'requestdetail':requestid, 'mimember':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':6,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = EstimationdetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
                        L1_user= 'Request has been ' + str(inst1.statusdetail) + ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
                        sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail)  ,
                        L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
                        sub_miteam='Request ID ' + str(requestid) + ' has been' + str(inst1.statusdetail) ,
                        L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
                        sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
                        L1_manager='Next Step is with Requester to Accept/Reject estimation',
                        request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('overview'))
            else:
                pagename = "estimate"
                errormsg1 = "Something went Wrong"
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/EstimationForm.html',{'form':form, 'form1':form1, 'username': username,'authority':authority,'activetab1':activetab1,'activetab':activetab})

@login_required
def EstimationAcceptanceFormTemplate(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='wip')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Acceptrejectdetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('estimate'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = AcceptrejectdetailForm(initial={'requestdetail':requestid, 'estacceptrejectby':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':7,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = AcceptrejectdetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user=  str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
                        L1_user= 'You have accepted the Estimation of your request ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
                        sub_auth= str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
                        L1_auth='Request ID ' + str(requestid) + ' moved to WIP ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required' ,
                        sub_miteam= str(inst1.statusdetail) + 'for Request ID' + str(requestid),
                        L1_miteam= str(inst1.statusdetail) + ' and it moved to WIP ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
                        sub_manager= str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
                        L1_manager="Estimation has been Accepted, it's moved to WIP bucket"  if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
                        request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('estimate'))
            else:
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/EstAcceptRejectForm.html',{'form':form, 'form1':form1, 'username': username,'authority':authority,'activetab1':activetab1,'activetab':activetab})

@login_required
def CompletedFormTemplate(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='wip')
    userid = User.objects.get(username=username).pk
    try:
        DataModel= Completeddetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('wip'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username

        form = CompleteddetailForm(initial={'requestdetail':requestid, 'completedby':userid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':9,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = CompleteddetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
                dataforemail(username= request_owner,
                        requestid = requestid,
                        sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
                        L1_user= 'Request has been ' + str(inst1.statusdetail) ,
                        sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail)  ,
                        L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) ,
                        sub_miteam='Request ID ' + str(requestid) + ' has been' + str(inst1.statusdetail) ,
                        L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail),
                        sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
                        L1_manager='Request been completed',
                        request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('wip'))
            else:
                return render(request, 'CentralMI/ErrorPage.html')
        return render(request, 'CentralMI/CompletedForm.html',{'form':form, 'form1':form1, 'username': username,'activetab1':activetab1,'authority':authority,'activetab':activetab})



@login_required
def typage(request,requestid):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='checkstatus')
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='loginrequest',footer='')

    try:
        model1 = Requestdetail.objects.all().get(requestid=requestid)
        try:
            model2 = Authorisedetail.objects.all().get(requestdetail=requestid)
        except:
            model2 = "nothing"
        try:
            model3 = Options.objects.all().get(requestdetail=requestid)
        except:
            model3 = "nothing"
        try:
            model4 = Assigneddetail.objects.all().get(requestdetail=requestid)
        except:
            model4 = "nothing"
        try:
            model5 = Overviewdetail.objects.all().get(requestdetail=requestid)
        except:
            model5 = "nothing"
        try:
            model6 = Estimationdetail.objects.all().get(requestdetail=requestid)
        except:
            model6 = "nothing"
        try:
            model7 = Acceptrejectdetail.objects.all().get(requestdetail=requestid)
        except:
            model7 = "nothing"
        try:
            model8 = Completeddetail.objects.all().get(requestdetail=requestid)
        except:
            model8 = "nothing"
        return render(request, 'CentralMI/ThankYou.html',{'detail1':model1,'detail2':model2,'detail3':model3,'detail4':model4,'detail5':model5,'detail6':model6,'detail7':model7,'detail8':model8,'username':username,'authority':authority,'activetab':activetab,'activetab1':activetab1})
    except:
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1,'activetab':activetab,'activetab1':activetab1})


def RequestdetailUpdate(request,requestid):
    instance = get_object_or_404(Requestdetail, requestid=requestid)
    form = RequestdetailForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        form = RequestdetailForm(request.POST)
        if form.is_valid():
            estimate = form.save(commit=True)
            estimate.save()
            return render(request, 'CentralMI/RequestForm.html', {'form':form})
        else:
            pagename = "report"
            errormsg1 = "Something went Wrong"
            return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})
    return render(request, 'CentralMI/RequestForm.html',{'form':form})

@login_required
def filterform(request,username,authority):
    form = FilteredForm()
    if authority == "Group2":
        if request.method == 'POST':
            form =  FilteredForm(request.POST)
            if form.is_valid():
                teamfilter = form.cleaned_data['teamfilter']
                memberfilter = form.cleaned_data['memberfilter']
                if teamfilter != None and memberfilter != None:
                    teamid = Teamdetail.objects.get(teamname__in=[teamfilter]).teamid
                    userid = User.objects.get(username__in=[memberfilter]).id
                    memberid = Mimember.objects.get(username__in=[userid]).mimemberid
                elif teamfilter != None and memberfilter == None:
                    teamid = Teamdetail.objects.get(teamname__in=[teamfilter]).teamid
                    memberid = None
                elif teamfilter == None and memberfilter == None:
                    teamid = None
                    memberid = None
                #form.fields['memberfilter'] =  Mimember.objects.all()
            else:
                teamid = None
                memberid = None
                form = FilteredForm()
                print("error")
        else:
            teamid = None
            memberid = None
            form = FilteredForm()
    else:
        userid = User.objects.get(username__in=[username]).id
        memberid = Mimember.objects.get(username__in=[userid]).mimemberid
        teamid = Mimember.objects.get(username__in=[userid]).teamdetail
    return teamid , memberid, form


@login_required
def landingpage(request):
    username = request.user.username
    return render(request, 'CentralMI/landingpage.html',{'username':username})


@login_required
def index(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='')
        teamid , memberid, form = filterform(request,username=username,authority=authority)
        mv = info.define_day_week_month1(days_range=3,range_type='Monthly',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        wv = info.define_day_week_month1(days_range=5,range_type='Weekly',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        dv = info.define_day_week_month1(days_range=5,range_type='Daily',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        mvOT = info.define_day_week_month1(days_range=3,range_type='Monthly',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=1,teamdetail=teamid,member=memberid,output_type='timetracker')
        wvOT = info.define_day_week_month1(days_range=5,range_type='Weekly',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=1,teamdetail=teamid,member=memberid,output_type='timetracker')
        dvOT= info.define_day_week_month1(days_range=5,range_type='Daily',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=1,teamdetail=teamid,member=memberid,output_type='timetracker')
        mvcore = info.define_day_week_month1(days_range=3,range_type='Monthly',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        wvcore = info.define_day_week_month1(days_range=5,range_type='Weekly',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        dvcore = info.define_day_week_month1(days_range=5,range_type='Daily',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
        mvutilisation = info.define_day_week_month1(days_range=3,range_type='Monthly',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,utilisation='Yes',teamdetail=teamid,member=memberid,output_type='timetracker')
        wvutilisation = info.define_day_week_month1(days_range=5,range_type='Weekly',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,utilisation='Yes',teamdetail=teamid,member=memberid,output_type='timetracker')
        dvutilisation = info.define_day_week_month1(days_range=5,range_type='Daily',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,utilisation='Yes',teamdetail=teamid,member=memberid,output_type='timetracker')
        dv_error = info.define_day_week_month1(days_range=5,range_type='Daily',values='error_reportedto',aggregatefield='error_occurancedate',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='error')
        wv_error = info.define_day_week_month1(days_range=5,range_type='Weekly',values='error_reportedto',aggregatefield='error_occurancedate',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='error')
        mv_error = info.define_day_week_month1(days_range=3,range_type='Monthly',values='error_reportedto',aggregatefield='error_occurancedate',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='error')
        form = FilteredForm()
        #form.cleaned_data['memberfilter'] = Mimember.objects.all()
        #load_mimember()
        return render(request, 'CentralMI/index.html',{'form':form,'username':username,'authority':authority,'activetab':activetab,'authority':authority,
        'mv':mv,'wv':wv,'dv':dv,'mvOT':mvOT,'wvOT':wvOT,'dvOT':dvOT,'mvcore':mvcore,'wvcore':wvcore,'dvcore':dvcore,'mvutilisation':mvutilisation,'wvutilisation':wvutilisation,'dvutilisation':dvutilisation,
        'dv_error':dv_error,'wv_error':wv_error,'mv_error':mv_error})
    except:
        authority, activetab, activetab1, username = create_session_onerror(request,header='home',footer='')
        return render(request, 'CentralMI/landingpage.html',{'username':username,'authority':authority,'activetab':activetab,'authority':authority})



def dataforemail(username=None,requestid=None,sub_user=None,L1_user=None,sub_auth=None,L1_auth=None,sub_miteam=None,L1_miteam=None,sub_manager=None,L1_manager=None,request_status=None):
    userid = User.objects.get(username=username).pk
    user = User.objects.get(pk=userid)
    user_email = user.email
    requester_email = sendemail(to_email=user_email, name=username,sent_to="requester", len=1,requestid= str(requestid),subject=sub_user,line1=L1_user,request_status=request_status,linktext='Click link to check detail of your request',link='http://127.0.0.1:8000/CMI/status')
    requester_email.sending_email()
    auth_groups = User.objects.filter(groups__name='authoriser').values_list('email',flat=True)
    auth_email = sendemail(to_email=auth_groups,name='Authoriser', sent_to="authoriser",len=len(auth_groups),requestid= str(requestid),subject=sub_auth,line1=L1_auth,request_status=request_status,linktext='Click link to Authorise Request',link='http://127.0.0.1:8000/CMI/')
    auth_email.sending_email()
    miteam_groups = User.objects.filter(groups__name='miteam').values_list('email',flat=True)
    miteam_groups = sendemail(to_email=miteam_groups,name='MI-team', sent_to="miteam",len=len(miteam_groups),requestid= str(requestid),subject=sub_miteam,line1=L1_miteam,request_status=request_status,linktext='Click link to check detail of your Request',link='http://127.0.0.1:8000/CMI/')
    miteam_groups.sending_email()
    manager_groups = User.objects.filter(groups__name='manager').values_list('email',flat=True)
    manager_groups = sendemail(to_email=manager_groups,name='Manager', sent_to="manager",len=len(manager_groups),requestid= str(requestid),subject=sub_manager,line1=L1_manager,request_status=request_status,linktext='To know more click the link',link='http://127.0.0.1:8000/CMI/')
    manager_groups.sending_email()

class sendemail(object):
    def __init__(self, name=None, password=None, len=None, to_email='jha.pramod234@gmail.com',requestid=None,sent_to=None,request_status=None,subject=None,line1=None,line2=None,line3=None,linktext=None,link=None):
        if len == 1:
            self.to_email = [to_email]
        else:
            self.to_email = list(to_email)
        self.requestid = int(requestid)
        self.sent_to = sent_to
        self.name = name
        self.password = password
        self.subject = subject
        self.emailbody = line1
        self.linktext = linktext
        self.link = link
        self.request_status=request_status
        self.currentdatetime = datetime.now()

    def sending_email(self):
        self.requestinst = Requestdetail.objects.get(requestid=self.requestid)
        try:
            from_email = settings.EMAIL_HOST_USER
            html_content = render_to_string('CentralMI\email.html', {'requestid':self.requestid,'username':self.name,'line1':self.emailbody, 'request_status':self.request_status,'linktext':self.linktext,'link':self.link})
            text_content = strip_tags(html_content)
            instance = Emaildetail(requestdetail=self.requestinst,emaildate=self.currentdatetime,stage=self.sent_to,emailsubject=self.subject,emailbody=self.emailbody,emailto=self.to_email,emailfrom=from_email,emailstatus='Success',requeststatus=self.request_status)
            instance.save()
            msg = EmailMultiAlternatives(self.subject,text_content, from_email, self.to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            instance = Emaildetail(requestdetail=self.requestinst,emaildate=self.currentdatetime,stage=self.sent_to,emailsubject=self.subject,emailbody=self.emailbody,emailto=self.to_email,emailfrom=from_email,emailstatus='Failed',requeststatus=self.request_status)
            instance.save()

from django.contrib.auth.models import Group
class vistorinfo_output(object):
    def __init__(self, username,sd=None, core='Core',noncore='Non-Core',OT_Yes=1,OT_No=2):
        self.username = username
        self.sd = sd
        self.OT_Yes = OT_Yes
        self.OT_No = OT_No
        user_id = User.objects.get(username=self.username).pk
        self.mimemberid = Mimember.objects.get(username=user_id).mimemberid
        self.core = core
        self.noncore = noncore

    def is_member(self):
        for grpname in ['Group1','Group2','Group3','Group4']:
            self.groupname = Group.objects.get(name=grpname).user_set.filter(username=self.username)
            try:
                self.groupname = self.groupname[0]
                self.permission = grpname
            except:
                self.groupname = None


    def getinfo(self):
        self.mimemberid = self.mimemberid
        self.teamname = Mimember.objects.get(mimemberid=self.mimemberid).teamdetail
        self.teamid = Teamdetail.objects.get(teamname=self.teamname).pk
        self.coreid = Requestsubcategory.objects.filter(core_noncore__in=[self.core]).values_list('pk', flat=True).distinct()
        self.noncoreid = Requestsubcategory.objects.filter(core_noncore__in=[self.noncore]).values_list('pk', flat=True).distinct()
        self.modelTracker = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd)


    def sumcalculationindividual(self,core_noncore=None,OT=None,aggregatefield='totaltime'):
        """ For Core enter 'Core' in parameter and for Non-Core enter 'noncore'"""
        """ For OT enter 'Yes' in parameter and 'No' for without OT"""
        if core_noncore != None:
            self.core_noncore_id = Requestsubcategory.objects.filter(core_noncore__in=[core_noncore]).values_list('pk', flat=True).distinct()
        if core_noncore == None and OT == None:
            self.summarising = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd ).aggregate(Sum(aggregatefield))
        elif core_noncore == None and OT != None:
            self.summarising = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd ).filter(options=OT).aggregate(Sum(aggregatefield))
        elif core_noncore != None and OT == None:
            self.summarising = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd ).filter(requestsubcategory__in=list(self.core_noncore_id)).aggregate(Sum(aggregatefield))
        else:
            self.summarising = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd ).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).aggregate(Sum(aggregatefield))

        self.summarising1 = self.summarising[aggregatefield+'__sum']
        if self.summarising1 == None:
            self.summarising1 = 0
        elif self.summarising1 > 60:
            self.summarising1 = str(round(self.summarising1/60,0)).split('.')[0]  + ":" + str(self.summarising1 % 60)
        else:
            self.summarising1
        return self.summarising, self.summarising1

    def Topdata(self,grouping_column='trackingdatetime',core_noncore=None,OT=None,aggregatefield='totaltime',topn=5):
        if core_noncore != None:
            self.core_noncore_id = Requestsubcategory.objects.filter(core_noncore__in=[core_noncore]).values_list('pk', flat=True).distinct()
        if core_noncore == None and OT == None:
            self.Topdata = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).values(grouping_column).annotate(sum=Sum(self.aggregatefield)).order_by(grouping_column).reverse()
            self.Topdata = self.Topdata[":" + topn]
        elif core_noncore == None and OT != None:
            self.Topdata = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(options=OT).values(grouping_column).annotate(sum=Sum(self.aggregatefield)).order_by(grouping_column).reverse()
            self.Topdata = self.Topdata[":" + topn]
        elif core_noncore != None and OT == None:
            self.Topdata = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(requestsubcategory__in=list(self.core_noncore_id)).values(grouping_column).annotate(sum=Sum(self.aggregatefield)).order_by(grouping_column).reverse()
            self.Topdata = self.Topdata[":" + topn]
        else:
            self.Topdata = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).values(grouping_column).annotate(sum=Sum(self.aggregatefield)).order_by(grouping_column).reverse()
            self.Topdata = self.Topdata[":" + topn]
        return self.Topdata

    def sqlconnection(self,storeprocedurename,parameter1,parameter2):
        cur = connection.cursor()
        result = cur.execute("" + storeprocedurename + "'" + parameter1 + "','" + parameter2 + "'")

        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
                ]
        self.length = len(dictfetchall(result))
        return self.length

    def define_day_week_month1(self,start_date=None,end_date=None,days_range=None,range_type=None,year_range=0,report_choice=None,aggregatefield=None,values=None,core_noncore=None,OT=None,utilisation='No',teamdetail=None,member=None,output_type=None):
        #data1 = Assigneddetail.objects.all()
        #requestdetail = Assigneddetail.objects.get(assignedto=2)
        #print(requestdetail)
        #print(data1)

        # start_date, starting range of data
        # end_date, ending range of data
        self.key = []
        self.value = []
        self.cumulativedays = 0
        if start_date != None and end_date != None:
            start = datetime.strftime(start_date, '%y/%m/%d')
            start = datetime.strptime(start, '%y/%m/%d')
            end = datetime.strftime(end_date, '%y/%m/%d')
            end = datetime.strptime(end, '%y/%m/%d')
            if range_type == 'Daily':
                days_range = (end - start).days
                print(start)
                print(end)
            elif range_type == 'Weekly':
                days_range = ((end - start).days) / 7
                days_range = int(str(days_range).split('.')[0])
                print(start)
                print(end)

            elif range_type == 'Monthly':
                days_range = ((end - start).days) / 30
                days_range = int(str(days_range).split('.')[0])
        else:
            days_range = days_range

        print(days_range)
        for i in range(days_range):
            self.values = values
            self.aggregatefield = aggregatefield
            #if start_date != None:
            #    self.currentdate = end_date
            #else:
            self.currentdate = datetime.today()
            self.cd = datetime.strftime(self.currentdate, '%y/%m/%d')
            self.cd  = datetime.strptime(self.cd, '%y/%m/%d')
            self.memberinteam = Mimember.objects.filter(teamdetail__in=[teamdetail]).values_list('mimemberid', flat=True).distinct()
            if range_type == None:
                self.No_of_days = i
            elif range_type == 'setdate':
                self.daystoloop = 1
                if self.sd != None:
                    self.StartDate = self.sd
                    self.EndDate  =  self.sd
                else:
                    self.StartDate = self.currentdate
                    self.EndDate  = self.currentdate
                self.date = ''
            elif range_type == 'Daily':
                self.daystoloop = 1
                self.No_of_days = i
                self.StartDate = self.cd - timedelta(days=self.No_of_days)
                self.EndDate  = self.StartDate
                self.currentyear = datetime.strftime(self.StartDate, '%Y')
                self.currentmonth = datetime.strftime(self.StartDate, '%m')
                self.currentdays = datetime.strftime(self.StartDate, '%d')
                self.date = date(int(self.currentyear),int(self.currentmonth),int(self.currentdays))
            elif range_type == 'Weekly':
                self.daystoloop = 7
                self.days = 7
                self.No_of_days = (7 * i)
                self.Start = self.cd - timedelta(days=self.cd.weekday())
                self.StartDate = self.Start - timedelta(days=self.No_of_days)
                self.EndDate  = self.StartDate  + timedelta(days=(self.days))
                self.currentyear = datetime.strftime(self.StartDate, '%Y')
                self.currentmonth = datetime.strftime(self.StartDate, '%m')
                self.currentdays = datetime.strftime(self.StartDate, '%d')
                self.date = date(int(self.currentyear),int(self.currentmonth),int(self.currentdays))
            elif range_type == 'Monthly':
                self.currentmonth = datetime.strftime(self.currentdate, '%m')
                self.currentyear = datetime.strftime(self.currentdate, '%Y')
                self.month  = int(self.currentmonth) - i
                self.year  = int(self.currentyear) - year_range
                self.No_of_daystest = calendar.monthrange(self.year,self.month)[1]
                self.currentdays = datetime.strftime(self.currentdate, '%d')
                self.days  = (int(self.currentdays) -1)
                self.daystoloop = calendar.monthrange(self.year,self.month)[1]
                self.No_of_days = calendar.monthrange(self.year,self.month)[1]
                self.cumulativedays = (self.cumulativedays + self.No_of_days) -1
                self.StartDate = self.cd - timedelta(days=(self.days + (self.cumulativedays)))
                self.EndDate  = self.StartDate + timedelta(days=(self.No_of_days -2))
                self.date = self.month

            if output_type == 'error':
                if teamdetail == None and member == None:
                    self.data = Errorlog.objects.filter(error_occurancedate__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail != None and member == None:
                    self.data = Errorlog.objects.filter(error_occurancedate__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail == None and member != None:
                    self.data = Errorlog.objects.filter(error_occurancedate__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=[member]).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail != None and member != None:
                    self.data = Errorlog.objects.filter(error_occurancedate__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                else:
                    self.data = Errorlog.objects.filter(error_occurancedate__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                self.key.append(str(self.date))
                self.value.append(str(self.data))
                self.result = OrderedDict(zip(self.key, self.value))

            elif output_type == 'timetracker':
                if teamdetail == None and member == None:
                    memberlen = 1
                elif teamdetail != None and member == None:
                    memberlen = Mimember.objects.filter(teamdetail__in=[teamdetail]).count()
                elif teamdetail != None and member != None:
                    memberlen = 1

                if core_noncore != None:
                    self.core_noncore_id = Requestsubcategory.objects.filter(core_noncore__in=[core_noncore]).values_list('pk', flat=True).distinct()
                if core_noncore == None and OT == None:
                    if teamdetail == None and member == None:
                        self.data = Timetrackers.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member == None:
                        self.data = Timetrackers.objects.filter(teamdetail__in=[teamdetail]).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail == None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(teamdetail__in=[teamdetail]).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    else:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']

                elif core_noncore == None and OT != None:
                    if teamdetail == None and member == None:
                        self.data = Timetrackers.objects.filter(options=OT).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member == None:
                        self.data = Timetrackers.objects.filter(teamdetail__in=[teamdetail]).filter(options=OT).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail == None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(options=OT).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(teamdetail__in=[teamdetail]).filter(options=OT).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    else:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(options=OT).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']

                elif core_noncore != None and OT == None:
                    if teamdetail == None and member == None:
                        self.data = Timetrackers.objects.filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member == None:
                        self.data = Timetrackers.objects.filter(teamdetail__in=[teamdetail]).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail == None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(teamdetail__in=[teamdetail]).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    else:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                else:
                    if teamdetail == None and member == None:
                        self.data = Timetrackers.objects.filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member == None:
                        self.data = Timetrackers.objects.filter(teamdetail__in=[teamdetail]).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail == None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    elif teamdetail != None and member != None:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(teamdetail__in=[teamdetail]).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']
                    else:
                        self.data = Timetrackers.objects.filter(mimember__in=[member]).filter(options=OT).filter(requestsubcategory__in=list(self.core_noncore_id)).filter(trackingdatetime__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Sum(self.aggregatefield))
                        self.data = self.data[aggregatefield+'__sum']


                if utilisation == 'No':
                    if self.data == None:
                        self.hours = 0.00
                        self.min = 00
                    else:
                        self.hours = self.data/60
                        self.min = self.data % 60

                    if  len(str(self.hours).split('.')[0]) <= 1:
                        self.hours = str(self.hours).split('.')[0].zfill(2)

                    if  len(str(self.min)) <= 1:
                        self.min = str(self.min).zfill(2)
                    self.hoursmin = str(self.hours).split('.')[0]  + ":" + str(self.min)
                else:
                    if self.data == None:
                        self.hours = 00
                        self.min = 00
                    else:
                        self.hours = str(round((self.data/((420*memberlen)*self.daystoloop))*100,2)).split('.')[0]
                        self.min = str(round((self.data/((420*memberlen)*self.daystoloop))*100,1)).split('.')[1]

                    self.hoursmin = str(self.hours).zfill(2)  + "." + str(self.min)  + " %"
                self.key.append(str(self.date))
                self.value.append(str(self.hoursmin))
                self.result = OrderedDict(zip(self.key, self.value))
        return self.result


    def define_day_week_month2(self,start_date=None,end_date=None,days_range=None,range_type=None,year_range=0,report_choice=None,aggregatefield=None,values=None,core_noncore=None,OT=None,utilisation='No',teamdetail=None,member=None,output_type=None):
        self.key = []
        self.value = []
        self.cumulativedays = 0
        if start_date != None and end_date != None:
            start = datetime.strftime(start_date, '%y/%m/%d')
            start = datetime.strptime(start, '%y/%m/%d')
            end = datetime.strftime(end_date, '%y/%m/%d')
            end = datetime.strptime(end, '%y/%m/%d')
            if range_type == 'Daily':
                days_range = (end - start).days
            elif range_type == 'Weekly':
                days_range = ((end - start).days) / 7
                days_range = int(str(days_range).split('.')[0])
            elif range_type == 'Monthly':
                days_range = ((end - start).days) / 30
                days_range = int(str(days_range).split('.')[0])
        else:
            days_range = days_range
        print(days_range)

        for i in range(days_range ):
            self.values = values
            self.aggregatefield = aggregatefield
            self.currentdate = start_date
            self.cd = datetime.strftime(self.currentdate, '%y/%m/%d')
            self.cd  = datetime.strptime(self.cd, '%y/%m/%d')
            self.memberinteam = Mimember.objects.filter(teamdetail__in=[teamdetail]).values_list('mimemberid', flat=True).distinct()
            if range_type == None:
                self.No_of_days = i
            elif range_type == 'setdate':
                self.daystoloop = 1
                if self.sd != None:
                    self.StartDate = self.sd
                    self.EndDate  =  self.sd
                else:
                    self.StartDate = self.currentdate
                    self.EndDate  = self.currentdate
                self.date = ''
            elif range_type == 'Daily':
                self.daystoloop = 1
                self.No_of_days = i
                self.StartDate = self.cd + timedelta(days=self.No_of_days)
                self.EndDate  = self.StartDate
                self.currentyear = datetime.strftime(self.StartDate, '%Y')
                self.currentmonth = datetime.strftime(self.StartDate, '%m')
                self.currentdays = datetime.strftime(self.StartDate, '%d')
                self.date = date(int(self.currentyear),int(self.currentmonth),int(self.currentdays))
            elif range_type == 'Weekly':
                self.daystoloop = 7
                self.days = 7
                self.No_of_days = (7 * i)
                self.Start = self.cd + timedelta(days=self.cd.weekday())
                self.StartDate = self.Start + timedelta(days=self.No_of_days)
                self.EndDate  = self.StartDate  + timedelta(days=(self.days))
                self.currentyear = datetime.strftime(self.StartDate, '%Y')
                self.currentmonth = datetime.strftime(self.StartDate, '%m')
                self.currentdays = datetime.strftime(self.StartDate, '%d')
                self.date = date(int(self.currentyear),int(self.currentmonth),int(self.currentdays))
            elif range_type == 'Monthly':

                totaldays = ((end - start).days)
                print(totaldays)

                if days_range == 1:
                    self.currentmonth = datetime.strftime(self.currentdate, '%m')
                    self.currentyear = datetime.strftime(self.currentdate, '%Y')
                    self.currentdays = datetime.strftime(self.currentdate, '%d')
                    self.month  = int(self.currentmonth)
                    self.year  = int(self.currentyear)
                    self.daystoloop = calendar.monthrange(self.year,self.month)[1]
                    self.daystoloop = self.daystoloop - int(self.currentdays)
                    self.cumulativedays = self.cumulativedays +  self.daystoloop
                    self.StartDate = self.currentdate
                    self.EndDate = self.StartDate + timedelta(days=(self.cumulativedays))
                else:
                    self.StartDate = self.cd + timedelta(days=(self.cumulativedays))
                    self.month = int(datetime.strftime(self.StartDate, '%m'))
                    self.year = int(datetime.strftime(self.StartDate, '%Y'))
                    self.daystoloop = calendar.monthrange(self.year,self.month)[1]
                    self.EndDate = self.StartDate + timedelta(days=(self.cumulativedays))
                    self.cumulativedays = self.cumulativedays +  self.daystoloop

        if report_choice == '2':
            if teamdetail == None and member == None:
                self.data = Timetrackers.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                memberid = Mimember.objects.filter(teamdetail__in=[teamdetail]).values_list('mimemberid',flat=True)
                requestid = Assigneddetail.objects.filter(assignedto__in=list(memberid)).values_list('requestdetail',flat=True)
                self.data = Requestdetail.objects.filter(requestraiseddate__range=(self.StartDate,self.EndDate)).filter(requestid__in=list(requestid)).aggregate(Count(self.aggregatefield))
                self.data = self.data[aggregatefield+'__count']
            elif teamdetail != None and member != None:
                requestid = Assigneddetail.objects.filter(assignedto__in=[member]).values_list('requestdetail',flat=True)
                self.data = Requestdetail.objects.filter(requestraiseddate__range=(self.StartDate,self.EndDate)).filter(requestid__in=list(requestid)).aggregate(Count(self.aggregatefield))
                self.data = self.data[aggregatefield+'__count']

        elif report_choice == '3':
            if teamdetail == None and member == None:
                self.data = Timetrackers.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                self.data = Timetrackers.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).filter(teamdetail__in=[teamdetail]).aggregate(Count(self.aggregatefield))
            elif teamdetail != None and member != None:
                self.data = Timetrackers.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).filter(mimember__in=[member]).aggregate(Count(self.aggregatefield))

        elif report_choice == '4':
            if teamdetail == None and member == None:
                self.data = Errorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                memberid = Mimember.objects.filter(teamdetail__in=[teamdetail]).values_list('mimemberid',flat=True)
                self.data = Errorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=list(memberid)).aggregate(Count(self.aggregatefield))
            elif teamdetail != None and member != None:
                self.data = Errorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).filter(error_reportedto__in=[member]).all()
        elif report_choice == '5':
            if teamdetail == None and member == None:
                self.data = OtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                timetrackerid = Timetrackers.objects.filter(teamdetail__in=[teamdetail]).values_list('timetrackerid',flat=True)
                self.data = OtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).filter(timetrackers__in=list(timetrackerid)).all()
            elif teamdetail != None and member != None:
                timetrackerid = Timetrackers.objects.filter(mimember__in=[member]).values_list('timetrackerid',flat=True)
                self.data = OtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).filter(timetrackers__in=list(timetrackerid)).all()
        else:
            self.key.append(str(1))
            self.value.append(str(1))
#        self.key.append(str(1))
#        self.value.append(str(1))
#    self.result = OrderedDict(zip(self.key, self.value))



#def looping_into_interval(output=output,data=data,interval=interval):
#    self.key = []
#    self.value = []
#    if data == '2':
#        if interval == '1':


        return days_range




@login_required
def TimeTracker(request):
#    try:
    authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
    starttime = request.POST.get('startdatetime')
    stoptime = request.POST.get('stopdatetime')
    userid = User.objects.get(username__in=[username]).id
    memberid = Mimember.objects.get(username__in=[userid]).mimemberid
    teamid = Mimember.objects.get(username__in=[userid]).teamdetail
    dv = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
    dvOT = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=1,teamdetail=teamid,member=memberid,output_type='timetracker')
    dvAll = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=None,teamdetail=teamid,member=memberid,output_type='timetracker')
    dvcore = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
    dvutilisation = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,utilisation='Yes',teamdetail=teamid,member=memberid,output_type='timetracker')
    requestid_onassign = Assigneddetail.objects.filter(assignedto__in=[info.mimemberid]).values_list('requestdetail',flat=True).distinct()
    requestid_onstatus = Requeststatusdetail.objects.filter(statusdetail__in=[4,5,6,7,8]).values_list('requestdetail',flat=True).distinct()
    requestid_filter = Requestdetail.objects.filter(requestid__in=list(requestid_onassign)).filter(requestid__in=list(requestid_onstatus)).values_list('requestid',flat=True).distinct()
    form = TimetrackersForm(initial={'mimember':info.mimemberid,'teamdetail':info.teamid,'options':2,'trackingdatetime':sd,'startdatetime':starttime,'stopdatetime':stoptime})
    form.fields['requestdetail'].queryset = Requestdetail.objects.filter(requestid__in=requestid_filter)
    form.fields['reports'].queryset = Activity.objects.all()
    model = info.modelTracker
    if request.method == 'POST':
        form = TimetrackersForm(request.POST)
        form.fields['requestdetail'].queryset = Requestdetail.objects.filter(requestid__in=requestid_filter)
        form.fields['reports'].queryset = Activity.objects.all()
        if form.is_valid():
            inst = form.save(commit=False)
            inst.mimember
            if inst.requestcategorys == None or inst.requestsubcategory == None or inst.totaltime == None or (inst.requestdetail!=None and inst.reports!=None):
                form = TimetrackersForm(initial={'mimember':info.mimemberid,'teamdetail':info.teamid,'options':2,'trackingdatetime': sd,'startdatetime':starttime,'stopdatetime':stoptime})
                model = info.modelTracker
                return render(request, 'CentralMI/rebuilding_tables.html', {'form':form,'model':model, 'username':username,'authority':authority,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1})
            else:
                inst.save()
            form = TimetrackersForm(initial={'mimember':info.mimemberid,'teamdetail':info.teamid,'options':2,'trackingdatetime': sd,'startdatetime':starttime,'stopdatetime':stoptime})
            form.fields['requestdetail'].queryset = Requestdetail.objects.filter(requestid__in=requestid_filter)
            form.fields['reports'].queryset = Activity.objects.all()
            model = info.modelTracker
            dv = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
            dvOT = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=1,teamdetail=teamid,member=memberid,output_type='timetracker')
            dvAll = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore=None,OT=None,teamdetail=teamid,member=memberid,output_type='timetracker')
            dvcore = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,teamdetail=teamid,member=memberid,output_type='timetracker')
            dvutilisation = info.define_day_week_month1(days_range=1,range_type='setdate',values='mimember',aggregatefield='totaltime',core_noncore='core',OT=2,utilisation='Yes',teamdetail=teamid,member=memberid,output_type='timetracker')
            return render(request, 'CentralMI/rebuilding_tables.html', {'form':form,'model':model, 'username':username,'authority':authority,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1})
        else:
            pagename = "report"
            errormsg1 = "Something went Wrong"
            return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})
    return render(request, 'CentralMI/Tracker.html', {'form':form, 'model':model,'username':username,'authority':authority,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1})

#    except:
#        pagename = "report"
#        errormsg1 = "Something went Wrong"
#        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def EditTracker(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
    e = Timetrackers.objects.get(pk=requestid)
    model = Timetrackers.objects.filter(pk=requestid)
    form = TimetrackersForm(instance=e)
    if request.method == 'POST':
        e = Timetrackers.objects.get(pk=requestid)
        form = TimetrackersForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('timetracker'))
    return render(request, 'CentralMI/TrackerEdit.html', {'form':form,'model':model, 'username':username,'authority':authority,'activetab':activetab})


@login_required
def EditOT(request,requestid):
    authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
    e = OtDetail.objects.get(pk=requestid)
    model = OtDetail.objects.filter(pk=requestid)
    form = OtDetailForm(instance=e)
    if request.method == 'POST':
        e = OtDetail.objects.get(pk=requestid)
        form = OtDetailForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('otdetail'))
    return render(request, 'CentralMI/otformEdit.html', {'form':form,'model':model, 'username':username,'authority':authority,'activetab':activetab})



@login_required
def ViewTracker(request,requestid):
    try:
        activetab = 'timetracker'
        username = request.user.username
        sd = request.session.get('setdate')
        info = vistorinfo_output(username,sd)
        info.getinfo()
        info.is_member()
        model = Timetrackers.objects.filter(pk=requestid)
        if request.method == 'POST':
            return render(request, 'CentralMI/TrackerView.html', {'model':model, 'username':username,'authority':authority,'activetab':activetab})
        return render(request, 'CentralMI/TrackerView.html', {'model':model, 'username':username,'authority':authority,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def load_datevalues(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
        mimemberid = User.objects.get(username=username).pk
        model = Timetrackers.objects.filter(mimember__in=[mimemberid]).filter(trackingdatetime=sd)
        return render(request, 'CentralMI/rebuilding_datevalues.html', {'model': model,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def load_subcategories(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
        category_id = request.GET.get('categories')
        #print(category_id)
        subcategories = Requestsubcategory.objects.filter(requestcategorys_id=category_id)
        activities = Activity.objects.filter(requestcategorys=category_id)
        #print(activities)
        return render(request, 'CentralMI/rebuilding_subcategories.html', {'subcategories': subcategories,'activities':activities,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def load_activity(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
        category_id = request.GET.get('categories')
        #print(category_id)
        activities = Activity.objects.filter(requestcategorys=category_id)
        #print(activities)
        return render(request, 'CentralMI/rebuilding_activity.html', {'activities':activities,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def load_mimember(request):
    mimember_id = request.GET.get('mimemberid')
    mimembers = Mimember.objects.filter(teamdetail__in=[mimember_id])
    print('load_member')
    print(mimembers)
    return render(request, 'CentralMI/rebuilding_mimember.html', {'mimembers': mimembers})

@login_required
def load_tables(request):
    try:
        authority, activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='tracker')
        mimemberid = User.objects.get(username=username).pk
        form = TimetrackersForm(initial={'trackingdatetime':sd})
        model = Timetrackers.objects.filter(mimember__in=[mimemberid])
        return render(request, 'CentralMI/rebuilding_datevalues.html', {'form':form,'model': model,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/ErrorPage.html',{'username':username,'authority':authority,'pagename':pagename,'errormsg1':errormsg1})
