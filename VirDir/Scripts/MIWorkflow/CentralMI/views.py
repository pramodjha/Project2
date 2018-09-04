from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView,ListView
from django.db import connection, transaction
from .forms import RequestdetailForm , EstimationdetailForm, OverviewdetailForm, AuthorisedetailForm, RequeststatusdetailForm, AssigneddetailForm, AcceptrejectdetailForm, CompleteddetailForm, UserRegistrationForm, UsersigninForm,  RequestcategorysForm,  TimetrackersForm, RequestcategorysForm, RequestsubcategoryForm, TeamdetailForm, StatusdetailForm, UploadFileForm, ReportsForm,EmaildetailForm,FilterForm, ErrorlogForm, OtDetailForm, FeedbackForm, SearchForm,FilteredForm,ActivityForm,  INTERVAL_CHOICES, MimemberForm, UserForm, InternaltaskForm, InternaltaskchoiceForm, InternaltaskstatusForm, ActivitystatusCalendarForm, ViewForm
from .models import Acceptrejectdetail, Acceptrejectoption, Assigneddetail, Authorisedetail, Authoriserdetail, Completeddetail, Estimationdetail, Mimember, Options, Overviewdetail, Prioritydetail, Requestcategorys, Requestdetail, Requeststatusdetail, Requestsubcategory, Requesttypedetail, Statusdetail, Teamdetail, Timetrackers, Reports, Emaildetail, Errorlog, OtDetail,Activity, FeedbackQuestion,Feedback, AuthUser, Internaltask, Internaltaskchoice, Internaltaskstatus, FeedbackQuestion, ActivitystatusCalendar, Whatwedo, Reply, Suggestion, Governance, SuccessStories
from django.core import serializers
from django.shortcuts import redirect
from django.db import connection
import datetime
import getpass
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, user_passes_test
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
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from  .decorators import user_permission
from django.urls import reverse
from django.http import HttpResponse
#import django-excel as excel
#import pyexcel.ext.xls
import datetime as dt
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")


def export_users_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=filename.csv'
  exportdata.to_csv(path_or_buf=response,index = False, sep=',', encoding='utf-8')
  return response


@login_required
def is_group(request,username):
    try:
        userid = User.objects.get(username=username).id
        group = Group.objects.prefetch_related('user_set')
        group = group.filter(user__in=[userid]).values_list('name',flat=True)
        group = list(group)
    except:
        group = ['None']
    return ', '.join(group)


@login_required
def create_session(request,header=None,footer=None):
    username = request.user.username
    request.session['activeheader'] = header
    request.session['activefooter'] = footer
    activetab = request.session.get('activeheader')
    activetab1 = request.session.get('activefooter')
    try:
        sd = request.session.get('setdate')
        info = vistorinfo_output(username,sd)
        info.get_member_info()
        return activetab, activetab1, username, info, sd
    except:
        sd = None
        info = None
        return activetab, activetab1, username, info, sd

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
def activity_Calendar(request,parameter1=None,parameter2=None):
    #print(parameter1)
    #print(parameter2)
    print("[CentralMI].[dbo].[usp_activity_calendar] " + "'" + parameter1 + "'"  + ","  + "'" + parameter2 + "'")
    cur = connection.cursor()
    ret = cur.execute("[CentralMI].[dbo].[usp_activity_calendar] "  + "'" + parameter1 + "'"  + ","  + "'" + parameter2 + "'")

    def dictfetchall(cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]
    data = dictfetchall(ret)
    return data

@login_required
def session_view(request,username=None):
    group_name = is_group(request,username=username)
    if group_name == 'manager':
        session_teamid = None
        session_memberid = None
    elif group_name == 'technical_leader' or group_name == 'team_leader':
        session_userid = User.objects.get(username=username).id
        session_teamid = Mimember.objects.get(username=session_userid).teamdetail
        session_memberid = None
    elif group_name == 'mi_team':
        session_userid = User.objects.get(username=username).id
        session_teamid = Mimember.objects.get(username=session_userid).teamdetail
        session_memberid = Mimember.objects.get(username=session_userid).mimemberid

    request.session['sessison_team'] = str(session_teamid)
    request.session['sessison_member'] = str(session_memberid)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    return teamid, memberid

@login_required
def HomePage_Data(request,username,info,session_teamid,session_memberid):
    teamid , memberid, form = filterform(request,username=username,session_teamid=session_teamid,session_memberid=session_memberid)
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
    return mv, wv, dv, mvOT, wvOT, dvOT, mvcore, wvcore, dvcore, mvutilisation, wvutilisation, dvutilisation, dv_error, wv_error, mv_error, form


@login_required
def Index(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='')
    group_name = is_group(request,username=username)
    if group_name ==  'manager' or group_name ==  'team_leader' or group_name ==  'technical_leader' or group_name ==  'mi_team':
        try:
            teamid = request.session.get('sessison_team')
            memberid = request.session.get('sessison_member')
        except:
            teamid, memberid = session_view(request,username=username)

        form = FilteredForm(initial={'teamfilter':teamid, 'memberfilter':memberid})
        if request.method == 'POST':
            form =  FilteredForm(request.POST)
            if form.is_valid():
                teamfilter = form.cleaned_data['teamfilter']
                memberfilter = form.cleaned_data['memberfilter']
                teamdetail_id = Teamdetail.objects.get(teamname=teamfilter).teamid
                user_id = User.objects.get(username=memberfilter).id
                mimember_id = Mimember.objects.get(username=user_id).mimemberid
                request.session['sessison_team'] = str(teamdetail_id)
                request.session['sessison_member'] = str(mimember_id)
                teamid = request.session.get('sessison_team')
                memberid = request.session.get('sessison_member')

        teamid = None if teamid == 'None' else teamid
        memberid = None if memberid == 'None' else memberid
        print(teamid)
        print(memberid)

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
        return render(request, 'CentralMI/1d_index.html',{'form':form,'username':username,'activetab':activetab,
        'mv':mv,'wv':wv,'dv':dv,'mvOT':mvOT,'wvOT':wvOT,'dvOT':dvOT,'mvcore':mvcore,'wvcore':wvcore,'dvcore':dvcore,'mvutilisation':mvutilisation,'wvutilisation':wvutilisation,'dvutilisation':dvutilisation,
        'dv_error':dv_error,'wv_error':wv_error,'mv_error':mv_error,'group_name':group_name})
    else:
        return render(request, 'CentralMI/1d_index.html',{'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def report_due(request):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='reportdue')
    session_teamid, session_memberid = session_view(request,view_value=view_value,username=username)
    group_name = is_group(request,username=username)
    if sd == None:
        sd = datetime.today().strftime('%Y-%m-%d')
        datedetail = 'Activity Due is for  today i.e. ' + sd + '. To check for other date please set it in Timetracker'
    else:
        datedetail = 'Activity Due is for the date ' + sd + '. To check for other date please set it in Timetracker'

    data_daily = activity_Calendar(request,parameter1=sd,parameter2='daily')
    data_weekly = activity_Calendar(request,parameter1=sd,parameter2='weekly')
    data_monthly = activity_Calendar(request,parameter1=sd,parameter2='monthly')
    return render(request, 'CentralMI/16a_report_due.html', {'datedetail':datedetail,'model1':data_daily,'model2':data_weekly,'model3':data_monthly,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Add_To_Timetracker(request,activityid):
    view_value = request.session.get('view_value_session')
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='reportdue')
    group_name = is_group(request,username=username)
    frequencyname = Activity.objects.get(activityid=activityid).frequency
    if str(frequencyname) == 'Daily':
        frequencyid = 1
    elif str(frequencyname) == 'Weekly':
        frequencyid = 2
    elif str(frequencyname) == 'Monthly':
        frequencyid = 4
    else:
        frequencyid = None
    checkid = ActivitystatusCalendar.objects.filter(activityid__in=[activityid]).count()
    print(checkid)
    if checkid > 0:
        form = TimetrackersForm(initial={'mimember':info.mimemberid,'teamdetail':info.teamid,'options':2,'trackingdatetime':sd,'requestcategorys':1,'reports':activityid,'requestsubcategory':frequencyid})
#        print(activityid)
        activity_id = ActivitystatusCalendar.objects.filter(activityid=activityid).all().values_list('activitystatuscalendarid',flat = True)
        print(max(activity_id))
        e = ActivitystatusCalendar.objects.get(activitystatuscalendarid=max(activity_id))
        form1 = ActivitystatusCalendarForm(instance=e)
        if request.method == 'POST':
            form = TimetrackersForm(request.POST)
            form1 = ActivitystatusCalendarForm(request.POST,instance=e)
            if all([form.is_valid() , form1.is_valid()]):
                form.save(commit=True)
                form1.save(commit=True)
                return HttpResponseRedirect(reverse('reportdue'))

    else:
        form = TimetrackersForm(initial={'mimember':info.mimemberid,'teamdetail':info.teamid,'options':2,'trackingdatetime':sd,'requestcategorys':1,'reports':activityid,'requestsubcategory':frequencyid})
        form1 = ActivitystatusCalendarForm(initial={'activityid':activityid,'recordenteredby':info.mimemberid})
        if request.method == 'POST':
            form = TimetrackersForm(request.POST)
            form1 = ActivitystatusCalendarForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                form.save(commit=True)
                form1.save(commit=True)
                return HttpResponseRedirect(reverse('reportdue'))
    return render(request, 'CentralMI/16b_add_to_timetracker.html', {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})


def Timetrcker_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    df1 = pd.DataFrame(list(Timetrackers.objects.all().values()))
    df2 = pd.DataFrame(list(Mimember.objects.all().values()))
    df3 = pd.DataFrame(list(Teamdetail.objects.all().values()))
    df4 = pd.DataFrame(list(AuthUser.objects.all().values()))
    df5 = pd.DataFrame(list(Requestcategorys.objects.all().values()))
    df6 = pd.DataFrame(list(Requestsubcategory.objects.all().values()))

    df_merge1 = pd.merge(df1, df2,  how='left', left_on=['mimember_id'], right_on = ['mimemberid'])
    df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['teamdetail_id_y'], right_on = ['teamid'])
    df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['username_id'], right_on = ['id'])
    df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['requestcategorys_id'], right_on = ['requestcategoryid'])
    df_merge5 = pd.merge(df_merge4, df6,  how='left', left_on=['requestsubcategory_id'], right_on = ['requestsubcategoryid'])
    df_merge5['trackingdatetime'] = df_merge5['trackingdatetime'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
    df_merge5['trackingdatetime_monthyear'] = df_merge5['trackingdatetime'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
    df_merge5['trackingdatetime_week'] = df_merge5['trackingdatetime'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge5 = df_merge5[df_merge5['teamname']==team] if team != 'None' else df_merge5
    df_merge5 = df_merge5[df_merge5['username']==member] if member != 'None' else df_merge5
    if interval == 'Daily':
        if view == "core_noncore":
            pivot_daily_corenoncore = pd.pivot_table(df_merge5,index=['trackingdatetime', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
            exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
            #print(exportdata.head(5))
            data = pivot_daily_corenoncore.to_html(classes="table cell-border")
        elif view == "activity":
            pivot_daily_corenoncore = pd.pivot_table(df_merge5,index=['requestcategorys','requestsubcategory'], columns='username', values='totaltime',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
            data = pivot_daily_corenoncore.to_html(classes="table cell-border")
    elif  interval == 'Monthly':
        if view == "core_noncore":
            pivot_monthly_corenoncore = pd.pivot_table(df_merge5,index=['trackingdatetime_monthyear', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
            exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
            data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
        elif view == "activity":
            pivot_monthly_corenoncore = pd.pivot_table(df_merge5,index=['requestcategorys'], columns='username', values='totaltime',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
            data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
    elif  interval == 'Weekly':
        if view == "core_noncore":
            pivot_weekly_corenoncore = pd.pivot_table(df_merge5,index=['trackingdatetime_week', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
            exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
            data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
        elif view == "activity":
            pivot_weekly_corenoncore = pd.pivot_table(df_merge5,index=['requestcategorys'], columns='username', values='totaltime',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
            data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
    return data

def Ot_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    df1 = pd.DataFrame(list(OtDetail.objects.all().values()))
    df2 = pd.DataFrame(list(Timetrackers.objects.all().values()))
    df3 = pd.DataFrame(list(Mimember.objects.all().values()))
    df4 = pd.DataFrame(list(Teamdetail.objects.all().values()))
    df5 = pd.DataFrame(list(AuthUser.objects.all().values()))
    df_merge1 = pd.merge(df1, df2,  how='left', left_on=['timetrackers_id'], right_on = ['timetrackerid'])
    df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['mimember_id'], right_on = ['mimemberid'])
    df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['teamdetail_id_y'], right_on = ['teamid'])
    df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['username_id'], right_on = ['id'])
    df_merge4['ot_startdatetime'] = df_merge4['ot_startdatetime'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
    df_merge4['ot_startdatetime_monthyear'] = df_merge4['ot_startdatetime'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
    df_merge4['ot_startdatetime_week'] = df_merge4['ot_startdatetime'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge4 = df_merge4[df_merge4['teamname']==team] if team != 'None' else df_merge4
    df_merge4 = df_merge4[df_merge4['username']==member] if member != 'None' else df_merge4
    if interval == 'Daily':
        pivot_daily_corenoncore = pd.pivot_table(df_merge4,index=['ot_startdatetime'], columns='username', values='ot_hrs',aggfunc=sum)
        exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
        data = pivot_daily_corenoncore.to_html(classes="table cell-border")
    elif  interval == 'Monthly':
        pivot_monthly_corenoncore = pd.pivot_table(df_merge4,index=['ot_startdatetime_monthyear'], columns='username', values='ot_hrs',aggfunc=sum)
        exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
        data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
    elif  interval == 'Weekly':
        pivot_weekly_corenoncore = pd.pivot_table(df_merge4,index=['ot_startdatetime_week'], columns='username', values='ot_hrs',aggfunc=sum)
        exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
        data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
    return data

def Error_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    df1 = pd.DataFrame(list(Errorlog.objects.all().values()))
    df2 = pd.DataFrame(list(Activity.objects.all().values()))
    df3 = pd.DataFrame(list(Mimember.objects.all().values()))
    df4 = pd.DataFrame(list(Teamdetail.objects.all().values()))
    df5 = pd.DataFrame(list(AuthUser.objects.all().values()))

    df_merge1 = pd.merge(df1, df2,  how='left', left_on=['error_report_id'], right_on = ['activityid'])
    df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['error_reportedto_id'], right_on = ['mimemberid'])
    df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['teamdetail_id'], right_on = ['teamid'])
    df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['username_id'], right_on = ['id'])
    df_merge4['errorlog_date'] = df_merge4['errorlog_date'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
    df_merge4['errorlog_date_monthyear'] = df_merge4['errorlog_date'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
    df_merge4['errorlog_date_week'] = df_merge4['errorlog_date'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge4 = df_merge4[df_merge4['teamname']==team] if team != 'None' else df_merge4
    df_merge4 = df_merge4[df_merge4['username']==member] if member != 'None' else df_merge4

    if interval == 'Daily':
        if view == 'erroruserwise':
            pivot_daily_userwise = pd.pivot_table(df_merge4,index=['errorlog_date'], columns='username', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_userwise.reset_index())
            data = pivot_daily_userwise.to_html(classes="table cell-border")
        elif view == 'errorreportwise':
            pivot_daily_userwise = pd.pivot_table(df_merge4,index=['errorlog_date'], columns='name', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_userwise.reset_index())
            data = pivot_daily_userwise.to_html(classes="table cell-border")
    elif  interval == 'Monthly':
        if view == 'erroruserwise':
            pivot_monthly_userwise = pd.pivot_table(df_merge4,index=['errorlog_date_monthyear'], columns='username', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
            data = pivot_monthly_userwise.to_html(classes="table cell-border")
        elif view == 'errorreportwise':
            pivot_monthly_userwise = pd.pivot_table(df_merge4,index=['errorlog_date_monthyear'], columns='name', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
            data = pivot_monthly_userwise.to_html(classes="table cell-border")
    elif  interval == 'Weekly':
        if view == 'erroruserwise':
            pivot_monthly_userwise = pd.pivot_table(df_merge4,index=['errorlog_date_week'], columns='username', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
            data = pivot_monthly_userwise.to_html(classes="table cell-border")
        elif view == 'errorreportwise':
            pivot_monthly_userwise = pd.pivot_table(df_merge4,index=['errorlog_date_week'], columns='name', values='error_reportedto_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
            data = pivot_monthly_userwise.to_html(classes="table cell-border")
    return data

def Workflow_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    df01 = pd.DataFrame(list(Requestdetail.objects.filter(requestraiseddate__range=[startdate,enddate]).values()))
    df02 = pd.DataFrame(list(Authorisedetail.objects.all().values()))
    df03 = pd.DataFrame(list(Assigneddetail.objects.all().values()))
    df04 = pd.DataFrame(list(Overviewdetail.objects.all().values()))
    df05 = pd.DataFrame(list(Estimationdetail.objects.all().values()))
    df06 = pd.DataFrame(list(Acceptrejectdetail.objects.all().values()))
    df07 = pd.DataFrame(list(Completeddetail.objects.all().values()))
    df08 = pd.DataFrame(list(Prioritydetail.objects.all().values()))
    df09 = pd.DataFrame(list(Requesttypedetail.objects.all().values()))
    df10 = pd.DataFrame(list(Mimember.objects.all().values()))
    df11 = pd.DataFrame(list(AuthUser.objects.all().values()))
    df12 = pd.DataFrame(list(Teamdetail.objects.all().values()))
    df_merge1 = pd.merge(df01, df02,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge2 = pd.merge(df_merge1, df03,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge3 = pd.merge(df_merge2, df04,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge4 = pd.merge(df_merge3, df05,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge5 = pd.merge(df_merge4, df06,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge6 = pd.merge(df_merge5, df07,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
    df_merge7 = pd.merge(df_merge6, df08,  how='left', left_on=['prioritydetail_id'], right_on = ['requestpriorityid'])
    df_merge8 = pd.merge(df_merge7, df09,  how='left', left_on=['requesttypedetail_id'], right_on = ['requesttypeid'])
    df_merge9 = pd.merge(df_merge8, df10,  how='left', left_on=['username_id'], right_on = ['username_id'])
    df_merge10 = pd.merge(df_merge9, df11,  how='left', left_on=['username_id'], right_on = ['id'])
    df_merge11 = pd.merge(df_merge10, df12,  how='left', left_on=['teamdetail_id'], right_on = ['teamid'])
    df_merge11['requestraiseddate'] = df_merge11['requestraiseddate'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
    df_merge11['requestraised_monthyear'] = df_merge11['requestraiseddate'].apply(lambda x:
                                    dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
    df_merge11['assigneddate'] = df_merge11['assigneddate'].apply(lambda x:
                                     dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d')  if pd.notnull(x) else None)
    df_merge11['assigneddate_monthyear'] = df_merge11['assigneddate'].apply(lambda x:
                                     dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m')  if pd.notnull(x) else None)
    df_merge11['completeddate'] = df_merge11['completeddate'].apply(lambda x:
                                     dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d')  if pd.notnull(x) else None)
    df_merge11['completeddate_monthyear'] = df_merge11['completeddate'].apply(lambda x:
                                     dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m')  if pd.notnull(x) else None)
    df_merge11['requestraised_week'] = df_merge11['requestraiseddate'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge11['assigneddate_week'] = df_merge11['assigneddate'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge11['completeddate_week'] = df_merge11['completeddate'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
    df_merge11 = df_merge11[df_merge11['teamname']==team] if team != 'None' else df_merge11
    df_merge11 = df_merge11[df_merge11['username']==member] if member != 'None' else df_merge11
    if interval == 'Daily':
        if view == "requesttype":
            pivot_daily_type = pd.pivot_table(df_merge11,index=['requestraiseddate'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_type.reset_index())
            data = pivot_daily_type.to_html(classes="table cell-border")
        elif view == "requestpriority":
            pivot_daily_priority = pd.pivot_table(df_merge11,index=['requestraiseddate'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_priority.reset_index())
            data = pivot_daily_priority.to_html(classes="table cell-border")
        elif view == "requestassigned":
            pivot_daily_assigned = pd.pivot_table(df_merge11,index=['assigneddate'], columns='assignedto_id', values='assignedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_assigned.reset_index())
            data = pivot_daily_assigned.to_html(classes="table cell-border")
        elif view == "requestcompleted":
            pivot_daily_completed = pd.pivot_table(df_merge11,index=['completeddate'], columns='completedby_id', values='completedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_daily_completed.reset_index())
            data = pivot_daily_completed.to_html(classes="table cell-border")
    elif  interval == 'Monthly':
        if view == "requesttype":
            pivot_monthly_type = pd.pivot_table(df_merge11,index=['requestraised_monthyear'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_type.reset_index())
            data = pivot_monthly_type.to_html(classes="table cell-border")
        elif view == "requestpriority":
            pivot_monthly_priority = pd.pivot_table(df_merge11,index=['requestraised_monthyear'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_priority.reset_index())
            data = pivot_monthly_priority.to_html(classes="table cell-border")
        elif view == "requestassigned":
            pivot_monthly_assigned = pd.pivot_table(df_merge11,index=['assigneddate_monthyear'], columns='assignedto_id', values='assignedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_assigned.reset_index())
            data = pivot_monthly_assigned .to_html(classes="table cell-border")
        elif view == "requestcompleted":
            pivot_monthly_Completed = pd.pivot_table(df_merge11,index=['completeddate_monthyear'], columns='completedby_id', values='completedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_monthly_Completed.reset_index())
            data = pivot_monthly_Completed.to_html(classes="table cell-border")
    elif  interval == 'Weekly':
        if view == "requesttype":
            pivot_weekly_type = pd.pivot_table(df_merge11,index=['requestraised_week'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_weekly_type.reset_index())
            data = pivot_weekly_type.to_html(classes="table cell-border")
        elif view == "requestpriority":
            pivot_weekly_priority = pd.pivot_table(df_merge11,index=['requestraised_week'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
            exportdata = pd.DataFrame(pivot_weekly_priority.reset_index())
            data = pivot_weekly_priority.to_html(classes="table cell-border")
        elif view == "requestassigned":
            pivot_weekly_assigned = pd.pivot_table(df_merge11,index=['assigneddate_week'], columns='assignedto_id', values='assignedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_weekly_assigned.reset_index())
            data = pivot_weekly_assigned .to_html(classes="table cell-border")
        elif view == "requestcompleted":
            pivot_weekly_completed = pd.pivot_table(df_merge11,index=['completeddate_week'], columns='completedby_id', values='completedid',aggfunc=len)
            exportdata = pd.DataFrame(pivot_weekly_completed.reset_index())
            data = pivot_weekly_completed.to_html(classes="table cell-border")
    return data


def setdateforall(request):
    try:
        selecteddate = request.POST.get('trackingdatetime')
        if selecteddate == None:
            currentdate = str(datetime.date.today())
            selecteddate = currentdate
        else:
            selecteddate = selecteddate
    except:
        currentdate = str(datetime.date.today())
        selecteddate = currentdate
    return  selecteddate

@login_required
def setdate(request):
    request.session['setdate'] = setdateforall(request)
    return HttpResponseRedirect(reverse('timetracker'))

def Sign_Up_View(request):
    #activetab, activetab1, username, info, sd = create_session(request, header='signup',footer='')
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
            #print(password)
            #print(passwordagain)
            #print(password == passwordagain)
            if password == passwordagain:
                #print(User.objects.filter(username=username).exists() )
                if not (User.objects.filter(username=username).exists() ):
                    new_user = User.objects.create_user(username, email, password)
                #    print(new_user)
                    new_user.is_active = True
                    new_user.first_name = firstname
                    new_user.last_name = lastname
                    new_user.save()
    #                info_email = sendemail(to_email=email, status="signup")
    #                info_email.sending_email()
                    try:
                        user = authenticate(username = username, password = password)
                        login(request, user)
                        return HttpResponseRedirect(reverse('home'))
                    except:
                        form =  UserRegistrationForm()
                        return render(request,'CentralMI/15a_ErrorPage.html')
                else:
                    form = UserRegistrationForm()
                    return render(request,'CentralMI/15a_ErrorPage.html')
            else:
                form = UserRegistrationForm()
                return render(request,'CentralMI/15a_ErrorPage.html')

        else:
            form = UserRegistrationForm()
            return render(request, 'CentralMI/1a_signup_view.html', {'form' : form,'activetab':activetab})
    else:
        form = UserRegistrationForm()
        return render(request, 'CentralMI/1a_signup_view.html', {'form' : form,'activetab':activetab})


def Sign_In_View(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='signin',footer='')
    except:
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
                    error = 'Error'
                    return render(request, 'CentralMI/1b_signin_view.html', {'form' : form,'activetab':activetab,'error':error})
            else:
                form =  UsersigninForm()
                error = 'Error'
                return render(request, 'CentralMI/1b_signin_view.html', {'form' : form,'activetab':activetab,'error':error})
        else:
            form =  UsersigninForm()
            error = 'Error'
            return render(request, 'CentralMI/1b_signin_view.html', {'form' : form,'activetab':activetab,'error':error})
    else:
        form =  UsersigninForm()
        error = 'NoError'
        return render(request, 'CentralMI/1b_signin_view.html', {'form' : form,'activetab':activetab,'error':error})

def Sign_Out(request):
    request.session.delete()
    logout(request)
    return HttpResponseRedirect(reverse('signin'))

@login_required
def All_Request_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='allrequest')
    group_name = is_group(request,username=username)
    data = Requestdetail.objects.all()
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Unapproved_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='unapproved')
    group_name = is_group(request,username=username)
    approved = list(Authorisedetail.objects.all().values_list('requestdetail', flat=True))
    data = Requestdetail.objects.exclude(requestid__in=approved)
#    data1 = Requestdetail.objects.select_related('username','requesttypedetail','prioritydetail').all()

#    print(data1)
    #data = data_extraction(request,parameter1="'Approval pending'",parameter2="'RequestStage'")
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Approved_View(request):
    activetab, activetab1, username, info, sd= create_session(request,  header='workflow',footer='approved')
    group_name = is_group(request,username=username)
    assigned = list(Assigneddetail.objects.all().values_list('requestdetail', flat=True))
    data = Authorisedetail.objects.select_related('requestdetail').exclude(requestdetail__in=assigned)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Assigned_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='assigned')
    group_name = is_group(request,username=username)
    overviewed = list(Overviewdetail.objects.all().values_list('requestdetail', flat=True))
    data = Assigneddetail.objects.select_related('requestdetail').exclude(requestdetail__in=overviewed)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})


@login_required
def Overview_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='overview')
    group_name = is_group(request,username=username)
    Estimated = list(Estimationdetail.objects.all().values_list('requestdetail', flat=True))
    data = Overviewdetail.objects.select_related('requestdetail').exclude(requestdetail__in=Estimated)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Estimate_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='estimate')
    group_name = is_group(request,username=username)
    Accepted = list(Acceptrejectdetail.objects.all().values_list('requestdetail', flat=True))
    data = Estimationdetail.objects.select_related('requestdetail').exclude(requestdetail__in=Accepted)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})


@login_required
def Wip_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='wip')
    group_name = is_group(request,username=username)
    Accepted = list(Completeddetail.objects.all().values_list('requestdetail', flat=True))
    data = Acceptrejectdetail.objects.select_related('requestdetail').exclude(requestdetail__in=Accepted)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})


@login_required
def Completed_View(request):
    activetab, activetab1, username, info, sd= create_session(request,  header='workflow',footer='completed')
    group_name = is_group(request,username=username)
    Completed = list(Completeddetail.objects.all().values_list('requestdetail', flat=True))
    data = Completeddetail.objects.select_related('requestdetail').filter(requestdetail__in=Completed)
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Rejected_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='workflow',footer='rejected')
    group_name = is_group(request,username=username)
    data = Requeststatusdetail.objects.select_related('statusdetail','requestdetail').filter(statusdetail__in=[3])
#    data = data_extraction(request,parameter1="'Rejected'",parameter2="'All'")
    return render(request, 'CentralMI/3a_request_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})


@login_required
def Errorlog_Add_Form(request,reportid):
    activetab, activetab1, username, info, sd= create_session(request, header='report',footer='')
    group_name = is_group(request,username=username)

    form = ErrorlogForm(initial={'error_report':reportid})
    if request.method == 'POST':
        form = ErrorlogForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('errordetail'))
    return render(request, 'CentralMI/7b_errorlog_add_form.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username})


@login_required
def Errorlog_Detail_View(request):
    activetab, activetab1, username, info, sd= create_session(request, header='report',footer='errordetail')
    group_name = is_group(request,username=username)

    data = Errorlog.objects.all()
    return render(request, 'CentralMI/7a_error_detail_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Errorlog_Edit_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    group_name = is_group(request,username=username)

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
    return render(request, 'CentralMI/7c_errorlog_edit_form.html', {'form':form,'model':model, 'username':username,'activetab':activetab})

def Ot_Detail_View(request):
    activetab, activetab1, username, info, sd= create_session(request, header='timetracker',footer='otdetail')
    group_name = is_group(request,username=username)

    data = OtDetail.objects.all()
    return render(request, 'CentralMI/9a_ot_detail_view.html', {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name})

@login_required
def Ot_Add_Form(request,trackerid):
    activetab, activetab1, username, info, sd = create_session(request,  header='timetracker',footer='otdetail')
    group_name = is_group(request,username=username)
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
    return render(request, 'CentralMI/9b_ot_add_form.html',{'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

from django.apps import apps
@login_required
def Summary_Tracker(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='filterdata')
    reportpage = "mainpage"
    group_name = is_group(request,username=username)
    form = SearchForm()
    if request.method == 'POST':
        form =  SearchForm(request.POST)
        if form.is_valid():
            request.session['reportno'] = form.cleaned_data['datachoice']
            request.session['startdate'] = str(form.cleaned_data['startdate'])
            request.session['interval'] = dict(INTERVAL_CHOICES)[int(form.cleaned_data["interval"])]
            request.session['enddate'] = str(form.cleaned_data['enddate'])
            request.session['team'] = str(form.cleaned_data['team'])
            request.session['member'] = str(form.cleaned_data['member'])
            startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
            return render(request, 'CentralMI/12a_filter_tab.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'reportno':reportno,'reportpage':reportpage})
    return render(request, 'CentralMI/12a_filter_tab.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'reportpage':reportpage})

def Datarequiredforreport(request):
    startdate = request.session.get('startdate')
    enddate = request.session.get('enddate')
    reportno = request.session.get('reportno')
    interval = request.session.get('interval')
    team = request.session.get('team')
    member = request.session.get('member')
    return startdate, enddate, reportno, interval, team, member

def CoreNonCore_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='corenoncore')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='core_noncore')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Activitytimetracker_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='activity')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='activity')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Requesttype_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='requesttype')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    print(team)
    print(member)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requesttype')
    length = len(data)
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name,'length':length})


def Requestpriority_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='requestpriority')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestpriority')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Requestassigned_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='requestassigned')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestassigned')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Requestcompleted_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='requestcompleted')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestcompleted')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Ot_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='otuserwise')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Ot_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view=None)
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Erroruserwise_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='erroruserwise')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='erroruserwise')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Errorreportwise_View(request):
    activetab, activetab1, username, info, sd = create_session(request, header='summary',footer='errorreportwise')
    group_name = is_group(request,username=username)
    startdate, enddate, reportno, interval, team, member = Datarequiredforreport(request)
    data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='errorreportwise')
    return render(request, 'CentralMI/12b_summary_tracker.html',{'data':data,'activetab':activetab,'activetab1':activetab1,'username':username,'reportno':reportno,'group_name':group_name})

def Filter_Data(request):
    activetab, activetab1, username, info, sd= create_session(request, header='extractdatafilter',footer='extractdatafilter1')
    group_name = is_group(request,username=username)
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
            return render(request, 'CentralMI/12a_extract_data.html',{'model':model,'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'reportno':reportno})
        return render(request, 'CentralMI/12a_extract_data.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username})
    return render(request, 'CentralMI/12a_extract_data.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username})

@login_required
def About_Team_View(request):
    activetab, activetab1, username, info, sd= create_session(request, header='home',footer='aboutteam')
    group_name = is_group(request,username=username)
    model = Mimember.objects.all()
    return render(request, 'CentralMI/2a_about_team_view.html',{'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model})

@login_required
def What_We_Do_View(request):
    activetab, activetab1, username, info, sd= create_session(request, header='home',footer='whatwedo')
    group_name = is_group(request,username=username)
    model = Whatwedo.objects.all()
    return render(request, 'CentralMI/2b_what_we_do_view.html',{'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model})

@login_required
def Governance_Process_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='governanceprocess')
    group_name = is_group(request,username=username)
    model = Governance.objects.all()
    return render(request, 'CentralMI/2c_governance_process_view.html',{'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model})

@login_required
def Success_Stories_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='successstories')
    group_name = is_group(request,username=username)

    return render(request, 'CentralMI/2d_success_stories_view.html',{'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username})

@login_required
def Comm_Sugg_View(request):
    activetab, activetab1, username, info, sd = create_session(request,header='home',footer='commsugg')
    group_name = is_group(request,username=username)

    return render(request, 'CentralMI/2e_comm_sugg_view.html',{'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username})

@login_required
def Check_Status_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='checkstatus')
    group_name = is_group(request,username=username)

    userid = User.objects.get(username=username).pk
    model = Requestdetail.objects.filter(username__in=[userid])
    return render(request, 'CentralMI/3b_check_status_view.html',{'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

################## Reports

@login_required
def Report_Detail_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='allreports')
    group_name = is_group(request,username=username)
    model = Activity.objects.all()
    return render(request, 'CentralMI/5a_reports_detail_view.html',{'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Report_Add_Form(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='')
    group_name = is_group(request,username=username)

    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('allreports'))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/5a_report_add_form.html',{'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/5a_report_add_form.html',{'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Report_Edit_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='')
    group_name = is_group(request,username=username)
    e = Activity.objects.get(activityid=requestid)
    model = Activity.objects.filter(activityid=requestid)
    form = ActivityForm(instance=e)
    if request.method == 'POST':
        e = Activity.objects.get(pk=requestid)
        form = ActivityForm(request.POST,request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('allreports'))
    return render(request, 'CentralMI/5c_report_edit_form.html', {'form':form,'model':model, 'username':username,'activetab':activetab})


######################## Feedback

@login_required
def Feedback_Question_View(request,activityid):
    activetab, activetab1, username, info, sd= create_session(request, header='report',footer='')
    group_name = is_group(request,username=username)

    model =  FeedbackQuestion.objects.all()
    request.session['aid'] = activityid
    return render(request, 'CentralMI/6b_feedback_question_view.html',{'model':model,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Feedback_Detail_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='feedbackdetail')
    group_name = is_group(request,username=username)

    model = Feedback.objects.all()
    return render(request, 'CentralMI/6a_feedback_detail_view.html',{'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Feedback_Edit_Form(request,feedbackid):
    activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='feedbackdetail')
    group_name = is_group(request,username=username)

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
    return render(request, 'CentralMI/6c_feedback_edit_form.html',{'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Feedback_Add_Form(request,feedbackquestionid):
    activetab, activetab1, username, info, sd = create_session(request,  header='report',footer='')
    group_name = is_group(request,username=username)

    activityid = request.session.get('aid')
    checkmember = Feedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activity__in=[activityid]).count()
    model1 = Feedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activity__in=[activityid])
    if checkmember > 0:
        feedbackid = Feedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activity__in=[activityid])
        #print(feedbackid)
        e = Feedback.objects.get(feedback_id=feedbackid)
        form = FeedbackForm(instance=e)
        if request.method == 'POST':
            form =  FeedbackForm(request.POST,instance=e)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.save()
                return HttpResponseRedirect(reverse('viewfeedbackquestion',args = (activityid,)))
            else:
                return render(request, 'CentralMI/6d_feedback_add_form.html',{'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid})
    else:
        form = FeedbackForm(initial={'feedback_question':feedbackquestionid,'activity':activityid})
        if request.method == 'POST':
            form = FeedbackForm(request.POST,request.FILES)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.save()
                return HttpResponseRedirect(reverse('viewfeedbackquestion',args = (activityid,)))
            else:
                return render(request, 'CentralMI/6d_feedback_add_form.html',{'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid})
    return render(request, 'CentralMI/6d_feedback_add_form.html',{'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid})

############## Staff
@login_required
def Staff_Detail_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='viewdetail')
    group_name = is_group(request,username=username)
    model1 = User.objects.all()
    model = Mimember.objects.all()
    data = zip(model1,model)
    return render(request, 'CentralMI/10a_staff_detail_view.html',{'model':model,'model1':model1,'data':data,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def My_Detail_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='mydetail')
    group_name = is_group(request,username=username)
    userid = User.objects.get(username=username).pk
    model1 = User.objects.filter(username__in=[username])
    model = Mimember.objects.filter(username__in=[userid])
    data = zip(model1,model)
    return render(request, 'CentralMI/10a_my_detail_view.html',{'model':model,'model1':model1,'data':data,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def Staff_Edit_Form(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='mydetail')
    group_name = is_group(request,username=username)
    userid = User.objects.get(username=username).pk
    e1 = User.objects.get(pk=userid)
    e = Mimember.objects.get(username=userid)
    model1 = User.objects.filter(username__in=username)
    model = Mimember.objects.filter(username__in=[userid])
    form1 = UserForm(instance=e1)
    #print(username)
    form = MimemberForm(instance=e)
    if request.method == 'POST':
        form = MimemberForm(request.POST,request.FILES,instance=e)
        form1 = UserForm (request.POST,instance=e1)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=True)
            inst.save()
            inst1 = form1.save(commit=False)
            inst1.username = username
            inst1.save()
            return HttpResponseRedirect(reverse('mydetail'))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/10b_my_edit_form.html',{'form':form,'form1':form1,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/10b_my_edit_form.html',{'form':form,'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def Staff_Edit_Manager_Form(request,id):
    detail = "managerview"
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='')
    group_name = is_group(request,username=username)
    userid = User.objects.get(id=id).pk
    e1 = User.objects.get(pk=userid)
    model1 = User.objects.filter(username__in=username)
    form1 = UserForm(instance=e1)
    if request.method == 'POST':
        form1 = UserForm (request.POST,instance=e1)
        if  form1.is_valid():
            inst1 = form1.save(commit=True)
            inst1.save()
            return HttpResponseRedirect(reverse('viewDetail'))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/10b_staff_edit_form.html',{'form1':form1,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'detail':detail})
    return render(request, 'CentralMI/10b_staff_edit_form.html',{'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'detail':detail})


############### Internal Task detailview
@login_required
def Internal_Task_Detail_View(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    model = Internaltask.objects.all()
    return render(request, 'CentralMI/11a_internal_task_detail_view.html',{'model':model, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

def Internal_Task_Completion_View(request,internaltaskid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    model = Internaltaskstatus.objects.filter(internaltask_id__in=[internaltaskid])
    return render(request, 'CentralMI/11g_internal_task_completion_view.html',{'model':model, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def Internal_Task_Add_Form(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    userid = User.objects.get(username=username).id
    mimemberid = Mimember.objects.get(username=userid).mimemberid
    form = InternaltaskForm(initial={'owner':mimemberid})
    if request.method == 'POST':
        form = InternaltaskForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('internaltaskdetail'))
    return render(request, 'CentralMI/11b_internal_task_add_form.html',{'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Internal_Task_Edit_Form(request,taskid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    e = Internaltask.objects.get(internaltaskid=taskid)
    form = InternaltaskForm(instance=e)
    if request.method == 'POST':
        form = InternaltaskForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('internaltaskdetail'))
    return render(request, 'CentralMI/11b_internal_task_add_form.html',{'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})



@login_required
def Internal_Task_Choice_view(request,taskid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    model = Internaltaskchoice.objects.filter(internaltask__in=[taskid])
    return render(request, 'CentralMI/11c_internal_task_choice_view.html',{'model':model, 'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def Internal_Choice_Add_Form(request,taskid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    id = taskid
    #print(id)
    form =  InternaltaskchoiceForm(initial={'internaltask':taskid})
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('viewinternaltaskoption',args = (id,)))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/11d_internal_task_choice_add_form.html',{'form':form,'taskid':taskid,'id':id,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/11d_internal_task_choice_add_form.html',{'form':form,'taskid':taskid,'id':id,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def Internal_Choice_Edit_Form(request,choiceid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    e = Internaltaskchoice.objects.get(internaltaskchoiceid=choiceid)
    question = Internaltaskchoice.objects.get(internaltaskchoiceid=choiceid).internaltask
    #print(question)
    taskid = Internaltask.objects.get(internaltaskquestion=question).internaltaskid
    #print(taskid)
#    print(id)
    form =  InternaltaskchoiceForm(instance=e)
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('viewinternaltaskoption',args = (taskid,)))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/11d_internal_task_choice_add_form.html',{'form':form,'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/11d_internal_task_choice_add_form.html',{'form':form,'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})




@login_required
def Internal_Task_And_Choice_View(request,taskid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    #print(taskid)
    userid = User.objects.get(username=username).id
    memberid = Mimember.objects.get(username=userid).mimemberid
    model =  Internaltask.objects.filter(internaltaskid__in=[taskid])
    model1 = Internaltaskchoice.objects.filter(internaltask__in=[taskid])
    checkmember = Internaltaskstatus.objects.filter(internaltask__in=[taskid]).filter(mimember__in=[memberid]).count()
    model2 = Internaltaskstatus.objects.filter(mimember__in=[memberid]).filter(internaltask__in=[taskid])
    if checkmember > 0:
        taskstatusid = Internaltaskstatus.objects.filter(mimember__in=[memberid]).filter(internaltask__in=[taskid])
    #    print(taskstatusid)
        e = Internaltaskstatus.objects.get(internaltaskstatusid=taskstatusid)
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
                return render(request, 'CentralMI/11e_internal_task_and_choice_view.html',{'form':form,'model':model,'model1':model1,'model2':model2,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    else:
        form =  InternaltaskstatusForm(initial={'internaltask':taskid, 'mimember':memberid})
        if request.method == 'POST':
            choice = request.POST['choice']
            taskchoiceid = Internaltaskchoice.objects.filter(internaltaskchoice__in=[choice]).filter(internaltask__in=[taskid])
            e = Internaltaskchoice.objects.get(internaltaskchoiceid=taskchoiceid)
            #print(choice)
            form =  InternaltaskstatusForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.internaltaskchoice = e
                inst.save()
                return HttpResponseRedirect(reverse('internaltaskdetail'))
            else:
                return render(request, 'CentralMI/11e_internal_task_and_choice_view.html',{'form':form,'model':model,'model1':model1,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/11e_internal_task_and_choice_view.html',{'form':form,'checkmember':checkmember,'model':model,'model1':model1,'model2':model2,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Internal_Task_And_Choice_Edit_Form(request,taskstatusid):
    activetab, activetab1, username, info, sd = create_session(request,  header='Details',footer='internaltaskdetail')
    group_name = is_group(request,username=username)

    userid = User.objects.get(username=username).id
    memberid = Mimember.objects.get(username=userid).mimemberid
    #print(taskstatusid)
    internaltaskchoice = Internaltaskstatus.objects.filter(internaltaskstatusid__in=[taskstatusid]).values_list('internaltaskchoice', flat=True)
    #print(internaltaskchoice)
    taskid = Internaltaskstatus.objects.filter(internaltaskstatusid__in=[taskstatusid]).values_list('internaltask', flat=True)
    internaltaskid = Internaltask.objects.get(internaltaskid=taskid).internaltaskid
    print(internaltaskid)
    choice = Internaltaskchoice.objects.filter(internaltaskchoiceid__in=list(internaltaskchoice)).values_list('internaltaskchoice',flat=True)
    choice_string = ', '.join(choice)
    #taskid_string =  ', '.join(taskid)
    model =  Internaltask.objects.filter(internaltaskid__in=list(taskid))
    model1 = Internaltaskchoice.objects.filter(internaltask__in=list(taskid))
    e = Internaltaskstatus.objects.get(internaltaskstatusid=taskstatusid)
    form = InternaltaskstatusForm(instance=e)
    if request.method == 'POST':
        choice = request.POST['choice']
        taskchoiceid = Internaltaskchoice.objects.filter(internaltaskchoice__in=[choice]).filter(internaltask__in=list(taskid)).values_list('internaltaskchoiceid',flat=True)
        #print(taskchoiceid)
        #taskchoiceid = ', '.join(taskchoiceid)
        f = Internaltaskchoice.objects.get(internaltaskchoiceid=taskchoiceid)
        #print(f)
        form =  InternaltaskstatusForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.internaltaskchoice = f
            inst.save()
            return HttpResponseRedirect(reverse('internaltaskwithchoice',args = (internaltaskid,)))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    return render(request, 'CentralMI/11f_internal_task_and_choice_edit_form.html',{'form':form,'model':model,'model1':model1,'choice':choice_string,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})





@login_required
def Request_Form(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='addrequest')
    group_name = is_group(request,username=username)

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
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        return render(request, 'CentralMI/4a_request_form.html',{'form':form,'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    return render(request, 'CentralMI/4a_request_form.html',{'form':form,'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})




@login_required
def Authorised_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='unapproved')
    group_name = is_group(request,username=username)

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
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user= 'Request ID ' + str(requestid) +'  has been ' + str(inst1.statusdetail) ,
        #                L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , now it is with MI-Team to assign ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + 'has been ' + str(inst1.statusdetail) + ' , hence no futher action required',
        #                sub_auth='Thanks for authorising Request ID ' + str(requestid) ,
        #                L1_auth='Request is with MI-Team to Assign ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + ' has been ' + str(inst1.statusdetail) + ' , hence no futher action required' ,
        #                sub_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail),
        #                L1_miteam='Authoriser has '  + str(inst1.statusdetail) + ' the request, assign to appropriate member ' if str(inst1.statusdetail)=='Approved' else ' Request ID ' + str(requestid) + ' has been '  + str(inst1.statusdetail) + ' , hence no futher action required',
        #                sub_manager='Request ID ' + str(requestid) + ' need to be assigned ' if str(inst1.statusdetail)=='Approved' else 'Request ID ' + str(requestid) + ' has been ' + str(inst1.statusdetail) + ' , hence no futher action required',
        #                L1_manager='Request has authorised and it is with MI-Team to assign',
        #                request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('unapproved'))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4b_authorised_form.html',{'form':form, 'form1':form1,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

@login_required
def Requestassigneddetail_Form(request, requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='approved')
    group_name = is_group(request,username=username)
    userid = User.objects.get(username=username).id
    memberid = Mimember.objects.get(username=userid).mimemberid
    print(userid)
    try:
        DataModel= Assigneddetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('approved'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        #print(request_owner)
        form = AssigneddetailForm(initial={'requestdetail':requestid, 'assignedby':memberid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':4,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = AssigneddetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) + ' to ' + str(inst.assignedto),
        #                L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , now it is with MI-Team to Overview ',
        #                sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto),
        #                L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto) + ' ,next step is take Overview',
        #                sub_miteam='Request has been succesfully assigned to '+  str(inst.assignedto),
        #                L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ 'to ' + str(inst.assignedto),
        #                sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' to ' + str(inst.assignedto) ,
        #                L1_manager='Next Step is to take overview of request',
        #                request_status=str(inst1.statusdetail))

                return HttpResponseRedirect(reverse('approved'))

            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4c_assigned_form.html',{'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab})



@login_required
def Overview_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='assigned')
    group_name = is_group(request,username=username)

    userid = User.objects.get(username=username).id
    memberid = Mimember.objects.get(username=userid).mimemberid
    try:
        DataModel= Overviewdetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('assigned'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = OverviewdetailForm(initial={'requestdetail':requestid, 'mimember':memberid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':5,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = OverviewdetailForm(request.POST,request.FILES)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
        #                L1_user= 'Request has been ' + str(inst1.statusdetail) + ' , shortly estimation in hours will be provided ',
        #                sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
        #                L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + '  , shortly estimation in hours will be provided',
        #                sub_miteam='Request ID ' + str(requestid) + ' has been overviewed',
        #                L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ ', please provide the estimation of the same',
        #                sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
        #                L1_manager='Next Step is with MI-Team to provide estimation in hours',
        #                request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('assigned'))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4d_overview_form.html',{'form':form,'form1':form1,'username':username,'activetab1':activetab1,'activetab':activetab})

@login_required
def Estimation_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='overview')
    group_name = is_group(request,username=username)

    userid = User.objects.get(username=username).pk
    memberid = Mimember.objects.get(username=userid).mimemberid

    try:
        DataModel= Estimationdetail.objects.all().get(requestdetail=requestid)
        return HttpResponseRedirect(reverse('overview'))
    except:
        requestfilter = Requestdetail.objects.get(requestid=requestid)
        request_owner = Requestdetail.objects.get(requestid=requestid).username
        form = EstimationdetailForm(initial={'requestdetail':requestid, 'mimember':memberid})
        form1 = RequeststatusdetailForm(initial={'statusdetail':6,'username':userid,'requestdetail':requestid})
        if request.method == 'POST':
            form = EstimationdetailForm(request.POST)
            form1 = RequeststatusdetailForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                inst = form.save(commit=False)
                inst.save()
                inst1 = form1.save(commit=False)
                inst1.save()
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
        #                L1_user= 'Request has been ' + str(inst1.statusdetail) + ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
        #                sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail)  ,
        #                L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) + ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
        #                sub_miteam='Request ID ' + str(requestid) + ' has been' + str(inst1.statusdetail) ,
        #                L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail)+ ' and Estimated time is ' + str(inst.estimateddays) + 'hours',
        #                sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
        #                L1_manager='Next Step is with Requester to Accept/Reject estimation',
        #                request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('overview'))
            else:
                pagename = "estimate"
                errormsg1 = "Something went Wrong"
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4e_estimation_form.html',{'form':form, 'form1':form1, 'username': username,'activetab1':activetab1,'activetab':activetab})

@login_required
def EstimationAcceptance_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='wip')
    group_name = is_group(request,username=username)

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
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user=  str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
        #                L1_user= 'You have accepted the Estimation of your request ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
        #                sub_auth= str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
        #                L1_auth='Request ID ' + str(requestid) + ' moved to WIP ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required' ,
        #                sub_miteam= str(inst1.statusdetail) + 'for Request ID' + str(requestid),
        #                L1_miteam= str(inst1.statusdetail) + ' and it moved to WIP ' if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
        #                sub_manager= str(inst1.statusdetail) + 'for Request ID' + str(requestid) ,
        #                L1_manager="Estimation has been Accepted, it's moved to WIP bucket"  if str(inst1.statusdetail)=='Estimation Accepted' else 'Estimation has been' +  str(inst1.statusdetail) + 'for Request ID' + str(requestid) + ' , hence no futher action required',
        #                request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('estimate'))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4f_estimation_acceptance_form.html',{'form':form, 'form1':form1, 'username': username,'activetab1':activetab1,'activetab':activetab})

@login_required
def Completed_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='workflow',footer='wip')
    group_name = is_group(request,username=username)

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
        #        dataforemail(username= request_owner,
        #                requestid = requestid,
        #                sub_user= 'Request ID ' + str(requestid) +'  has been ' +str(inst1.statusdetail) ,
        #                L1_user= 'Request has been ' + str(inst1.statusdetail) ,
        #                sub_auth='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail)  ,
        #                L1_auth= 'Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail) ,
        #                sub_miteam='Request ID ' + str(requestid) + ' has been' + str(inst1.statusdetail) ,
        #                L1_miteam='Request ID '  + str(requestid) +' has been ' + str(inst1.statusdetail),
        #                sub_manager='Request ID ' + str(requestid) + 'has been' + str(inst1.statusdetail),
        #                L1_manager='Request been completed',
        #                request_status=str(inst1.statusdetail))
                return HttpResponseRedirect(reverse('wip'))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4g_completed_form.html',{'form':form, 'form1':form1, 'username': username,'activetab1':activetab1,'activetab':activetab})



@login_required
def Thank_You_Page_View(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request,  header='loginrequest',footer='checkstatus')
    group_name = is_group(request,username=username)

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
        return render(request, 'CentralMI/3c_thankyou_view.html',{'detail1':model1,'detail2':model2,'detail3':model3,'detail4':model4,'detail5':model5,'detail6':model6,'detail7':model7,'detail8':model8,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
    except:
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})


@login_required
def filterform(request,username,session_teamid,session_memberid):
    form = FilteredForm(initial={'teamfilter':session_teamid, 'memberfilter':session_memberid})
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
    else:
        userid = User.objects.get(username__in=[username]).id
        memberid = Mimember.objects.get(username__in=[userid]).mimemberid
        teamid = Mimember.objects.get(username__in=[userid]).teamdetail
    return teamid , memberid, form



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

class vistorinfo_output(object):
    def __init__(self, username,sd=None, core='Core',noncore='Non-Core',OT_Yes=1,OT_No=2):
        self.username = username
        self.sd = sd
        self.OT_Yes = OT_Yes
        self.OT_No = OT_No
        self.core = core
        self.noncore = noncore


    def get_member_info(self):
        self.user_id = User.objects.get(username=self.username).pk
        self.mimemberid = Mimember.objects.get(username=self.user_id).mimemberid
        self.teamname = Mimember.objects.get(mimemberid=self.mimemberid).teamdetail
        self.teamid = Teamdetail.objects.get(teamname=self.teamname).pk
        self.coreid = Requestsubcategory.objects.filter(core_noncore__in=[self.core]).values_list('pk', flat=True).distinct()
        self.noncoreid = Requestsubcategory.objects.filter(core_noncore__in=[self.noncore]).values_list('pk', flat=True).distinct()
        self.modelTracker = Timetrackers.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd)

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
                #print(start)
                #print(end)
            elif range_type == 'Weekly':
                days_range = ((end - start).days) / 7
                days_range = int(str(days_range).split('.')[0])
                #print(start)
                #print(end)

            elif range_type == 'Monthly':
                days_range = ((end - start).days) / 30
                days_range = int(str(days_range).split('.')[0])
        else:
            days_range = days_range

        #print(days_range)
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
        #print(days_range)

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
                #print(totaldays)

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
def TimeTracker_View(request):
#    try:
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    group_name = is_group(request,username=username)
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
                return render(request, 'CentralMI/13e_rebuilding_tables.html', {'form':form,'model':model, 'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
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
            return render(request, 'CentralMI/13e_rebuilding_tables.html', {'form':form,'model':model, 'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})
        else:
            pagename = "report"
            errormsg1 = "Something went Wrong"
            return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})
    return render(request, 'CentralMI/8a_tracker_view.html', {'form':form, 'model':model,'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name})

#    except:
#        pagename = "report"
#        errormsg1 = "Something went Wrong"
#        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def Tracker_Edit_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    group_name = is_group(request,username=username)

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
    return render(request, 'CentralMI/8b_tracker_edit_form.html', {'form':form,'model':model, 'username':username,'activetab':activetab})


@login_required
def Ot_Edit_Form(request,requestid):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    group_name = is_group(request,username=username)

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
    return render(request, 'CentralMI/9c_ot_edit_form.html', {'form':form,'model':model, 'username':username,'activetab':activetab})

@login_required
def Load_Datevalues(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')

        mimemberid = User.objects.get(username=username).pk
        model = Timetrackers.objects.filter(mimember__in=[mimemberid]).filter(trackingdatetime=sd)
        return render(request, 'CentralMI/13b_rebuilding_datevalues.html', {'model': model,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})

@login_required
def Load_Subcategories(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
        category_id = request.GET.get('categories')
        #print(category_id)
        subcategories = Requestsubcategory.objects.filter(requestcategorys_id=category_id)
        activities = Activity.objects.filter(requestcategorys=category_id)
        #print(activities)
        return render(request, 'CentralMI/13d_rebuilding_subcategories.html', {'subcategories': subcategories,'activities':activities,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})


def Load_view(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='')
    group_name = is_group(request,username=username)

    try:
        view_value_radio = request.GET.get('radioValue')
        print(view_value_radio)
        if view_value_radio == None:
            request.session['view_value_session'] == 'myview'
        else:
            request.session['view_value_session'] = view_value_radio
        view_value = request.session.get('view_value_session')
    except:
        view_value = 'myview'
    if view_value == 'myview':
        session_userid = User.objects.get(username=username).id
        session_teamid = Mimember.objects.get(username=session_userid).teamdetail
        session_memberid = Mimember.objects.get(username=session_userid).mimemberid
    elif view_value == 'teamview':
        session_userid = User.objects.get(username=username).id
        session_teamid = Mimember.objects.get(username=session_userid).teamdetail
        session_memberid = None
    elif view_value == 'overallview':
        session_teamid = None
        session_memberid = None
        render(request, 'CentralMI/13f_rebuilding_index.html',{'session_teamid':session_teamid, 'session_memberid':session_memberid})



@login_required
def Load_Activity(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
        category_id = request.GET.get('categories')
        #print(category_id)
        activities = Activity.objects.filter(requestcategorys=category_id)
        #print(activities)
        return render(request, 'CentralMI/13a_rebuilding_activity.html', {'activities':activities,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})

def Load_Signup(request):
    try:
        username = request.GET.get('username')
        emailid = request.GET.get('emailid')
        password = request.GET.get('password')
        passwordagain = request.GET.get('passwordagain')
        #print(username)
#        print(passwordagain)
#        print(password)
#        print(username)
        try:
            lengthofusername = len(username)
            #print(lengthofusername)
            username_exist = User.objects.filter(username__in=[username]).exists()
            #print(username_exist)
            active_field = 1
        except:
            username_exist = None
            lengthofusername = None
#        print(username_exist)
        try:
            lengthofemail = len(emailid)
            email_exist = User.objects.filter(email__in=[emailid]).exists()
            active_field = 2
        except:
            lengthofemail = None
            email_exist = None

        try:
            lengthofpassword = len(passwordagain)
            #print(lengthofpassword)
            password_match = True if passwordagain == password else False
            #print(password_match)
            active_field = 3
        except:
            lengthofpassword = None
            password_match = None

        #print(password_match)
        #print(passwordagain)
        #print(email_exist)
        #print(lengthofemail)
        #check = username_exist == True or lengthofusername > 5
#        print(check)
        #print(activities)
        return render(request, 'CentralMI/1c_username_check.html', {'active_field':active_field,'username_exist':username_exist,'lengthofusername':lengthofusername,'email_exist':email_exist,'lengthofemail':lengthofemail,'password_match':password_match,'lengthofpassword':lengthofpassword})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})


@login_required
def Load_Mimember(request):
    team_id = request.GET.get('team_id')
    mimembers = Mimember.objects.filter(teamdetail__in=[team_id])
    print(mimembers)
    return render(request, 'CentralMI/13c_rebuilding_mimember.html', {'mimembers': mimembers})

@login_required
def Load_Tables(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
        mimemberid = User.objects.get(username=username).pk
        form = TimetrackersForm(initial={'trackingdatetime':sd})
        model = Timetrackers.objects.filter(mimember__in=[mimemberid])
        return render(request, 'CentralMI/13e_rebuilding_tables.html', {'form':form,'model': model,'activetab':activetab})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})
