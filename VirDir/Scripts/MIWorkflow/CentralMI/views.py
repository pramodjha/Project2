from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView,ListView
from django.db import connection, transaction
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
from django.db.models import Q
import getpass

from .forms import RequestdetailForm , EstimationdetailForm, OverviewdetailForm, AuthorisedetailForm, RequeststatusdetailForm, AssigneddetailForm, AcceptrejectdetailForm, CompleteddetailForm, UserRegistrationForm, UsersigninForm,  RequestcategorysForm,  TimetrackersForm, RequestcategorysForm, RequestsubcategoryForm, TeamdetailForm, StatusdetailForm, UploadFileForm, EmaildetailForm,FilterForm, ErrorlogForm, OtDetailForm, FeedbackForm, SearchForm,FilteredForm,ActivityForm,  INTERVAL_CHOICES, MemberForm, UserForm, InternaltaskForm, InternaltaskchoiceForm, InternaltaskstatusForm, ActivitystatusCalendarForm, ViewForm, SuccessStoriesForm, GovernanceForm, SuggestionForm, ReplyForm, WhatwedoForm, TYPE_CHOICES, OtDetail1Form, TblConversationForm, TblLeaveRecordForm, TblAppreciationForm, TblRawActivityDetailForm, TblRawScoreForm, TblRawTeamMasterForm,TblRawTeamMemberMasterForm,TblTeamMetricsForm, TblRawScoreForm, SearchForm1, TblUsefulLinksForm, UatDetailForm, UsersigninasotherForm,AcceptRequeststatusdetailForm, AuthoriserstatusdetailForm, REPORT_CHOICES, TYPE_CHOICES, IssueActionForm, ShiftupdateForm, GalleryForm, UatDetail1Form,ViewListForm

from .models import TblWhatwedo, TblIssueAction, TblUatDetail, TblUatStatusMaster, TblAcceptrejectdetail, TblActivity, TblActivityCalendar, TblActivitystatusCalendar, TblAppreciation, TblAssignView, TblAssigneddetail, TblCalendar, TblCalendarHolidays, TblCategorysMaster, TblCompleteddetail, TblConversation, TblDateTypesMaster, TblDeliveryDaysMaster, TblDesignationMaster, TblEmaildetail, TblErrorlog, TblErrortypeMaster, TblEstimationdetail, TblFeedback, TblFeedbackQuestionMaster, TblFrequency, TblGallery, TblGovernance, TblInternaltask, TblInternaltaskchoice, TblInternaltaskstatus, TblLeaveRecord, TblLeaveTypeMaster, TblMember, TblNavbarFooterMaster, TblNavbarHeaderMaster, TblNavbarMaster, TblNavbarView, TblOpenClose, TblYesNo, TblOtDetail, TblOtStatusMaster, TblOverviewdetail, TblPriorityMaster, TblPublicHolidaysMaster, TblRawActivityDetail, TblRawScore, TblRawTeamMaster, TblRawTeamMemberMaster, TblReply, TblRequestdetail, TblRequeststatusdetail, TblRequesttypeMaster, TblShiftUpdate, TblStatusMaster, TblSubcategoryMaster, TblSuccessStories, TblSuggestion, TblTeamMaster, TblTeamMetrics, TblTimeTracker, TblUsefulLinks, TblValidInvalidMaster, TblViewTypeMaster, TblAuthorisedetail, TblCategorysMaster, TblSubcategoryMaster, AuthUser
from .views_signin_signup import Sign_Up_View_Version1,Sign_Up_View_Version2,Sign_In_View_Version1,Sign_In_View_Version3,Sign_In_View_Version4,Sign_In_View_Version2,Sign_In_As_Other_View_Version1

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")

#--------------- signin_signup-------------------------
def Sign_Up_View(request):
    view_type = 'remote'
    if view_type == 'remote':
        return  Sign_Up_View_Version2(request)
    else:
        return  Sign_Up_View_Version1(request)

def Sign_In_View(request):
    view_type = 'remote'
    if view_type == 'remote':
        return  Sign_In_View_Version2(request)
    else:
        return  Sign_In_View_Version1(request)

def Sign_In_As_Other_View(request):
    view_type = 'remote'
    if view_type == 'remote':
        return  Sign_In_As_Other_View_Version1(request)
    else:
        return  Sign_In_As_Other_View_Version1(request)

#--------------sign_out------------------------------------
def Sign_Out(request):
    request.session.delete()
    logout(request)
    return HttpResponseRedirect(reverse('signin'))
#--------------Store_procedure------------------------------------
@login_required
def activity_Calendar(request,parameter1=None,parameter2=None):
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
#--------------Export to CSV------------------------------------
def export_users_csv(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        exportdata.to_csv(path_or_buf=response,index = False, sep=',', encoding='utf-8')
        return response
    except:
        return HttpResponseRedirect(reverse('filtertab'))
#--------------group_identification------------------------------------
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
#--------------groupid_identification------------------------------------
@login_required
def is_group_id(request,username):
    try:
        userid = User.objects.get(username=username).id
        group = Group.objects.prefetch_related('user_set')
        group = group.filter(user__in=[userid]).values_list('id',flat=True)
        group = list(group)
    except:
        group = 0
    return group
#--------------create_session------------------------------------
@login_required
def create_session(request,header=None,footer=None):
    username = request.user.username
    request.session['activeheader'] = header
    request.session['activefooter'] = footer
    activetab = request.session.get('activeheader')
    activetab1 = request.session.get('activefooter')
    try:
        sd = request.session.get('setdate')
        sd = datetime.strptime(datetime.strftime(datetime.today(), '%y/%m/%d'),'%y/%m/%d') if sd == None else sd
        info = vistorinfo_output(username,sd)
        info.get_member_info()
        return activetab, activetab1, username, info, sd
    except:
        sd = datetime.strptime(datetime.strftime(datetime.today(), '%y/%m/%d'),'%y/%m/%d') if sd == None else sd
        info = None
        return activetab, activetab1, username, info, sd
#--------------create_filter_dictonary------------------------------------
def create_dict_for_filter(request,field_name_list = None,value_list = None):
    filter_dict = {}
    for list_number in range(len(value_list)):
        if value_list[list_number]  != None and value_list[list_number]  != 'None'  :
            filter_dict[field_name_list[list_number]] = value_list[list_number]
    return filter_dict
#--------------set_date_for_timetracker------------------------------------
@login_required
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
#--------------Navbar available for view------------------------------------
@login_required
def navbar(request,view_header=None,username=None):
    model1 = TblMember.objects.all()
    model2 = TblNavbarView.objects.all()
    viewtype = model1.filter(userid__username__in=[username]).values_list('viewid',flat=True)
    header_navbar = model2.filter(view_type__in=list(viewtype)).values_list('navbar_footer_id__navbar_header_id__navbar_header_name',flat=True).distinct().order_by('navbar_footer_id__navbar_header_id__ranking')
    header_url = model2.filter(view_type__in=list(viewtype)).values_list('navbar_footer_id__navbar_header_id__navbar_header_url',flat=True).distinct().order_by('navbar_footer_id__navbar_header_id__ranking')
    footer_navbar = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_header_id__navbar_header_url__in=[view_header]).values_list('navbar_footer_id__navbar_footer_name',flat=True).distinct().order_by('navbar_footer__ranking')
    footer_url = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_header_id__navbar_header_url__in=[view_header]).values_list('navbar_footer_id__navbar_footer_url',flat=True).distinct().order_by('navbar_footer__ranking')
    header_navbar_list = zip(header_navbar,header_url)
    footer_navbar_list = zip(footer_navbar,footer_url)
    return header_navbar_list, footer_navbar_list
#--------------permission available for view------------------------------------
@login_required
def permission(request,view_footer=None,username=None):
    model1 = TblMember.objects.all()
    model2 = TblNavbarView.objects.all()
    viewtype = model1.filter(userid__username__in=[username]).values_list('viewid',flat=True)
    can_edit = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_footer_url__in=[view_footer]).values_list('can_edit',flat=True).distinct()
    can_view = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_footer_url__in=[view_footer]).values_list('can_view',flat=True).distinct()
    can_delete = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_footer_url__in=[view_footer]).values_list('can_delete',flat=True).distinct()
    can_add = model2.filter(view_type__in=list(viewtype)).filter(navbar_footer_id__navbar_footer_url__in=[view_footer]).values_list('can_add',flat=True).distinct()
    return can_edit, can_view, can_delete, can_add
#--------------permission available for view------------------------------------
@login_required
def check_view_level(request,username=None):
    model1 = TblMember.objects.all()
    individual_view = model1.filter(userid__username__in=[username]).values_list('individual_view',flat=True)
    individual_view = individual_view[0]
    team_view = model1.filter(userid__username__in=[username]).values_list('team_view',flat=True)
    team_view = team_view[0]
    bu_view = model1.filter(userid__username__in=[username]).values_list('bu_view',flat=True)
    bu_view = bu_view[0]
    user_id = model1.filter(userid__username__in=[username]).values_list('memberid',flat=True)
    user_id = user_id[0]
    team_id = model1.filter(userid__username__in=[username]).values_list('teamid',flat=True)
    team_id = team_id[0]
    bu_id = model1.filter(userid__username__in=[username]).values_list('teamid__buid',flat=True)
    bu_id = bu_id[0]
    return individual_view, team_view, bu_view,user_id,team_id,bu_id

#--------------Combining_Session Navbar & Permission output------------------------------------
@login_required
def session_navbar_permission(request,view_header=None,view_footer=None,template=None,template_type=None):
    activetab, activetab1, username, info, sd= create_session(request, header=view_header,footer=view_footer)
    group_name = is_group(request,username=username)
    header_navbar_list, footer_navbar_list =navbar(request,view_header=view_header,username=username)
    can_edit, can_view, can_delete, can_add= permission(request,view_footer=view_footer,username=username)
    individual_view, team_view, bu_view,user_id,team_id,bu_id = check_view_level(request,username=username)
    template = template
    template_type = template_type
    return group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id
#--------------Session view as per group------------------------------------
@login_required
def session_view(request,username=None,individual_view=None, team_view=None, bu_view=None):
    individual_view, team_view, bu_view,user_id,team_id,bu_id = check_view_level(request,username=username)
    if bu_view == True:
        try:
            session_buid = request.session.get('sessison_bu')
            session_teamid = request.session.get('sessison_team')
            session_memberid = request.session.get('sessison_member')
        except:
            session_memberid = None
            session_teamid = None
            session_buid = None
    elif team_view == True:
        try:
            session_buid = bu_id
            session_teamid = team_id
            session_memberid = request.session.get('sessison_member')
        except:
            session_memberid = None
            session_teamid = team_id
            session_buid = bu_id
    elif individual_view == True:
        session_memberid = user_id
        session_teamid = team_id
        session_buid = bu_id
    else:
        session_memberid = user_id
        session_teamid = team_id
        session_buid = bu_id
    request.session['sessison_bu'] = str(session_buid)
    request.session['sessison_team'] = str(session_teamid)
    request.session['sessison_member'] = str(session_memberid)
    buid = request.session.get('sessison_bu')
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    print(buid)

    return buid, teamid, memberid

@login_required
def filterform(request,):
    view_header,view_footer = 'home','landingpage'
    template = 'CentralMI/1d_index.html'

    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    if individual_view == True:
        form = FilteredForm(initial={'bufilter':buid,'teamfilter':teamid,'memberfilter':memberid})
    elif team_view == True:
        form = FilteredForm(initial={'bufilter':buid,'teamfilter':teamid,'memberfilter':memberid})
    elif bu_view == True:
        form = FilteredForm(initial={'bufilter':buid})
    else:
        form = FilteredForm(initial={'bufilter':buid,'teamfilter':teamid,'memberfilter':memberid})
    return form

@login_required(login_url='signin')
def Index(request):
    view_header,view_footer = 'home','landingpage'
    template = 'CentralMI/1d_index.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    buid, teamid, memberid = session_view(request,username=username,individual_view=individual_view, team_view=team_view, bu_view=bu_view)
    form =  FilteredForm(initial={'bufilter':buid,'teamfilter':teamid,'memberfilter':memberid})
    if request.method == 'POST':
        form =  FilteredForm(request.POST)
        if form.is_valid():
            teamfilter = form.cleaned_data['teamfilter']
            memberfilter = form.cleaned_data['memberfilter']
            bufilter = form.cleaned_data['bufilter']
            try:
                bu_id = TblMember.objects.filter(userid__username__in=[username]).values_list('teamid__buid',flat=True)
                bu_id = bu_id[0]
                request.session['sessison_bu'] = str(bu_id)
                buid = request.session.get('sessison_bu')
            except:
                request.session['sessison_bu'] = None
                teamid = request.session.get('sessison_bu')
            try:
                teamdetail_id = TblMember.objects.filter(userid__username__in=[username]).values_list('teamid',flat=True)
                teamdetail_id = teamdetail_id[0]
                request.session['sessison_team'] = str(teamdetail_id)
                teamid = request.session.get('sessison_team')
            except:
                request.session['sessison_team'] = None
                teamid = request.session.get('sessison_team')
            try:
                mimember_id = TblMember.objects.filter(userid__username__in=[memberfilter]).values_list('memberid',flat=True)
                mimember_id = mimember_id[0]
                request.session['sessison_member'] = str(mimember_id)
                memberid = request.session.get('sessison_member')
            except:
                request.session['sessison_member'] = None
                memberid = request.session.get('sessison_member')
    buid = None if buid == 'None' else buid
    teamid = None if teamid == 'None' else teamid
    memberid = None if memberid == 'None' else memberid
    filterdict = create_dict_for_filter(request,field_name_list = ['memberid','teamid','teamid__buid'], value_list = [memberid,teamid,buid])
    no_of_member = TblMember.objects.filter(**(filterdict)).count()
    model_team_metrics = TblTeamMetrics.objects.all()
    updates = TblShiftUpdate.objects.exclude(statusid__in=[2])
    issue_action = TblIssueAction.objects.exclude(statusid__in=[2])
    filterdict1 = create_dict_for_filter(request,field_name_list = ['userid','userid__teamid','userid__teamid__buid'], value_list = [memberid,teamid,buid])
    LeaverecordCount = TblLeaveRecord.objects.filter(**(filterdict1)).count()
    dv = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,None],values='memberid',aggregate='totaltime')
    dvcore = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',type='coreandot')
    dvOT = start_end_date(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'core','accepted'],values='timetrackerid__memberid',aggregate='ot_time')
    wv = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=5,range_type='Weekly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,None],values='memberid',aggregate='totaltime')
    wvcore = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=5,range_type='Weekly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',type='coreandot')
    wvOT = start_end_date(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',sd=sd,days_range=5,range_type='Weekly',year_range=0,field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'core','accepted'],values='timetrackerid__memberid',aggregate='ot_time')
    dv_error = start_end_date(request,model=TblErrorlog.objects.all(),datefield='occurancedate',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['reportedtoid','reportedtoid__teamid'], value_list = [memberid,teamid],values='reportedtoid',aggregate='reportedtoid',type="error",calculation_type='count')
    wv_error = start_end_date(request,model=TblErrorlog.objects.all(),datefield='occurancedate',sd=sd,days_range=5,range_type='Weekly',year_range=0,field_name_list = ['reportedtoid','reportedtoid__teamid'], value_list = [memberid,teamid],values='reportedtoid',aggregate='reportedtoid',type="error",calculation_type='count')
    dvutilisation = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',memberid=memberid,teamid=teamid,type="utilisation",no_of_member=no_of_member,averagetime=420,LeaverecordCount=LeaverecordCount)
    wvutilisation = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=5,range_type='Weekly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',memberid=memberid,teamid=teamid,type="utilisation",no_of_member=no_of_member,averagetime=2100,LeaverecordCount=LeaverecordCount)
    dvcore = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=10,range_type='Daily',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',type='coreandot')
    mv = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=6,range_type='Monthly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,None],values='memberid',aggregate='totaltime')
    mvcore = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=6,range_type='Monthly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',type='coreandot')
    mvOT = start_end_date(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',sd=sd,days_range=6,range_type='Monthly',year_range=0,field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'core','accepted'],values='timetrackerid__memberid',aggregate='ot_time')
    mvutilisation = start_end_date(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',sd=sd,days_range=6,range_type='Monthly',year_range=0,field_name_list = ['memberid','teamid','subcategoryid__core_noncore'],value_list = [memberid,teamid,'core'],values='memberid',aggregate='totaltime',memberid=memberid,teamid=teamid,type="utilisation",no_of_member=no_of_member,averagetime=9240,LeaverecordCount=LeaverecordCount)
    mv_error = start_end_date(request,model=TblErrorlog.objects.all(),datefield='occurancedate',sd=sd,days_range=6,range_type='Monthly',year_range=0,field_name_list = ['reportedtoid','reportedtoid__teamid'], value_list = [memberid,teamid],values='reportedtoid',aggregate='reportedtoid',type="error",calculation_type='count')
    context1 = {'model1':updates,'model2':issue_action,'form':form,'username':username,'activetab':activetab,'activetab1':activetab1,
    'mv':mv,'wv':wv,'dv':dv,'mvOT':mvOT,'wvOT':wvOT,'dvOT':dvOT,'mvcore':mvcore,'wvcore':wvcore,'dvcore':dvcore,'mvutilisation':mvutilisation,'wvutilisation':wvutilisation,'dvutilisation':dvutilisation,
    'dv_error':dv_error,'wv_error':wv_error,'mv_error':mv_error,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'model_team_metrics':model_team_metrics,'individual_view':individual_view, 'team_view':team_view, 'bu_view':bu_view,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context1)



@login_required
def add_edit_user_to_group(request):
    view_header = 'Home'
    template = 'CentralMI/group.html'
    model = Group.objects.all()
    model1 = TblViewTypeMaster.objects.all()
    model2 = TblAssignView.objects.all()
    model3 = TblNavbarHeaderMaster.objects.all()
    model4 = TblNavbarFooterMaster.objects.all()
    context = {'model':model,'model1':model1,'model2':model2,'model3':model3,'model4':model4}
    return render(request, template,context)

@login_required
def Edit_Metrics(request,metricsid):
    view_header,view_footer = 'home','landingpage'
    title = 'Add Shift-Update'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblTeamMetrics.objects.get(metrics_id=metricsid)
    form = TblTeamMetricsForm(instance=e)
    if request.method == 'POST':
        form = TblTeamMetricsForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add,'reverseid':metricsid,'redirect_url':redirect_url}
    return render(request, template,context)


@login_required
def report_due(request):
    view_header,view_footer = 'timetracker','reportdue'
    template = 'CentralMI/16a_report_due.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    if sd == None:
        sd = datetime.today().strftime('%Y-%m-%d')
        datedetail = 'Activity Due is for  today i.e. ' + str(sd) + '. To check for other date please set it in Timetracker'
    else:
        datedetail = 'Activity Due is for the date ' + str(sd) + '. To check for other date please set it in Timetracker'
    data_daily = activity_Calendar(request,parameter1=str(sd),parameter2='daily')
    data_weekly = activity_Calendar(request,parameter1=str(sd),parameter2='weekly')
    data_monthly = activity_Calendar(request,parameter1=str(sd),parameter2='monthly')
    context = {'datedetail':datedetail,'model1':data_daily,'model2':data_weekly,'model3':data_monthly,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context)

@login_required
def Add_To_Timetracker(request,activityid):
    view_header,view_footer = 'timetracker','reportdue'
    template = 'CentralMI/16b_add_to_timetracker.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    frequencyname = TblActivity.objects.get(activityid=activityid).frequency
    if str(frequencyname) == 'Daily':
        frequencyid = 1
    elif str(frequencyname) == 'Weekly':
        frequencyid = 2
    elif str(frequencyname) == 'Monthly':
        frequencyid = 4
    else:
        frequencyid = None
    checkid = ActivitystatusCalendar.objects.filter(activityid__in=[activityid]).count()
    if checkid > 0:
        form = TimetrackersForm(initial={'memberid':info.mmemberid,'teamid':info.teamid,'options':2,'trackingdatetime':sd,'requestcategorys':1,'reports':activityid,'subcategoryid':frequencyid})
        activity_id = ActivitystatusCalendar.objects.filter(activityid=activityid).all().values_list('activitystatuscalendarid',flat = True)
        e = ActivitystatusCalendar.objects.get(activitystatuscalendarid=max(activity_id))
        form1 = ActivitystatusCalendarForm(instance=e)
        if request.method == 'POST':
            form = TimetrackersForm(request.POST)
            form1 = ActivitystatusCalendarForm(request.POST,instance=e)
            if all([form.is_valid() , form1.is_valid()]):
                form.save(commit=True)
                form1.save(commit=True)
                return HttpResponseRedirect(reverse(view_footer))

    else:
        form = TimetrackersForm(initial={'memberid':info.memberid,'teamid':info.teamid,'options':2,'trackingdatetime':sd,'requestcategorys':1,'reports':activityid,'subcategoryid':frequencyid})
        form1 = ActivitystatusCalendarForm(initial={'activityid':activityid,'recordenteredby':info.memberid})
        if request.method == 'POST':
            form = TimetrackersForm(request.POST)
            form1 = ActivitystatusCalendarForm(request.POST)
            if all([form.is_valid() , form1.is_valid()]):
                form.save(commit=True)
                form1.save(commit=True)
                return HttpResponseRedirect(reverse(view_footer))
    context =  {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context)



@login_required
def IssueAction_Add_Form(request):
    view_header,view_footer = 'home','landingpage'
    title = 'Add Shift-Update'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    memberid = TblMember.objects.get(userid__username__in=[username]).memberid
    form = IssueActionForm(initial={'updatedbyid':memberid})
    if request.method == 'POST':
        form = IssueActionForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url}
    return render(request, template,context)


@login_required
def IssueAction_Edit_Form(request,issueactionid):
    view_header,view_footer = 'home','landingpage'
    title = 'Edit Shift-Update'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblIssueAction.objects.get(issue_action_id=issueactionid)
    form = IssueActionForm(instance=e)
    if request.method == 'POST':
        form = IssueActionForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add,'redirect_url':redirect_url,'title':title }
    return render(request,template,context)

@login_required
def Shiftupdate_Add_Form(request):
    view_header,view_footer = 'home','landingpage'
    title = 'Add Shift-Update'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    memberid = TblMember.objects.get(userid__username__in=[username]).memberid
    form = ShiftupdateForm(initial={'recordedbyid':memberid})
    if request.method == 'POST':
        form = ShiftupdateForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url}
    return render(request, template ,context)


@login_required
def Shiftupdate_Edit_Form(request,updateid):
    view_header,view_footer = 'home','landingpage'
    title = 'Edit Shift-Update'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblShiftUpdate.objects.get(updateid=updateid)
    form = ShiftupdateForm(instance=e)
    if request.method == 'POST':
        form = ShiftupdateForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url}
    return render(request, template,context)


@login_required
def Gallery_Add_Form(request):
    view_header,view_footer = 'home','gallery'
    title = 'Add Gallery'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    memberid = TblMember.objects.get(userid__username__in=[username]).memberid
    form = GalleryForm(initial={'uploadedbyid':memberid})
    if request.method == 'POST':
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Gallery_Edit_Form(request,imgid ):
    view_header,view_footer = 'home','gallery'
    title = 'Add Gallery'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblGallery.objects.get(imgid =imgid )
    form = GalleryForm(instance=e)
    if request.method == 'POST':
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Gallery_View(request):
    view_header,view_footer = 'home','gallery'
    template = 'CentralMI/gallery.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblGallery.objects.all()
    context = {'model':model,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context )


@login_required
def Raw_View(request):
    view_header,view_footer = 'rawdetail','rawdetail'
    template = 'CentralMI/raw_team.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data1 = TblRawScore.objects.all()
    data2 = TblRawActivityDetail.objects.filter(raw_statusid__in=[1])
    data3 = TblAppreciation.objects.filter(appreciation_status__in=[1])
    context =  {'model1':data1,'model2':data2,'model3':data3,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Raw_Appreciation_Add_Form(request):
    view_header,view_footer = 'rawdetail','rawdetail'
    title = 'Add Appreciation'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    form = TblAppreciationForm()
    if request.method == 'POST':
        form = TblAppreciationForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Raw_Appreciation_Edit_Form(request,appreciationid):
    view_header,view_footer = 'raw','rawdetail'
    title = 'Edit Appreciation'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblAppreciation.objects.get(appreciationid=appreciationid)
    form = TblAppreciationForm(instance=e)
    if request.method == 'POST':
        form = TblAppreciationForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)


@login_required
def Raw_rawactivity_Add_Form(request):
    view_header,view_footer = 'raw','rawdetail'
    title = 'Add Activity'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    form = TblRawActivityDetailForm()
    if request.method == 'POST':
        form = TblRawActivityDetailForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Raw_rawactivity_Edit_Form(request,activityid):
    view_header,view_footer = 'raw','rawdetail'
    title = 'Edit Activity'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblRawActivityDetail.objects.get(raw_activity_id=activityid)
    form = TblRawActivityDetailForm(instance=e)
    if request.method == 'POST':
        form = TblRawActivityDetailForm(request.POST,request.FILES,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)


@login_required
def Raw_Score_Edit_Form(request,activityid):
    view_header,view_footer = 'raw','rawdetail'
    title = 'Edit Score'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    template = 'CentralMI/1d_index.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblRawScore.objects.get(raw_score_id=activityid)
    form = TblRawScoreForm(instance=e)
    if request.method == 'POST':
        form = TblRawScoreForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)


@login_required
def All_Request_View(request):
    view_header,view_footer = 'workflow','allrequest'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data = TblRequestdetail.objects.all()
    header_navbar_list, footer_navbar_list =navbar(request,view_header=view_header,username=username)
    context  = {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Unapproved_View(request):
    view_header,view_footer = 'workflow','unapproved'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    approved = list(TblAuthorisedetail.objects.all().values_list('requestid', flat=True))
    data = TblRequestdetail.objects.exclude(requestid__in=approved)
    context = {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Approved_View(request):
    view_header,view_footer = 'workflow','approved'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    assigned = list(TblAssigneddetail.objects.all().values_list('requestid', flat=True))
    data = TblAuthorisedetail.objects.select_related('requestid').exclude(requestid__in=assigned)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Assigned_View(request):
    view_header,view_footer = 'workflow','assigned'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filter_dict = create_dict_for_filter(request,field_name_list = ['assignedtoid','assignedtoid__teamid'],value_list = [memberid,teamid])
    overviewed = list(TblOverviewdetail.objects.all().values_list('requestid', flat=True))
    data = TblAssigneddetail.objects.select_related('requestid').exclude(requestid__in=overviewed).filter(**filter_dict)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )


@login_required
def Overview_View(request):
    view_header,view_footer = 'workflow','overview'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filter_dict = create_dict_for_filter(request,field_name_list = ['giventoid','giventoid__teamid'],value_list = [memberid,teamid])
    Estimated = list(TblEstimationdetail.objects.all().values_list('requestid', flat=True))
    data = TblOverviewdetail.objects.select_related('requestid').exclude(requestid__in=Estimated).filter(**filter_dict)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Estimate_View(request):
    view_header,view_footer = 'workflow','estimate'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filter_dict = create_dict_for_filter(request,field_name_list = ['estimatedbyid','estimatedbyid__teamid'],value_list = [memberid,teamid])
    Accepted = list(TblAcceptrejectdetail.objects.all().values_list('requestid', flat=True))
    data = TblEstimationdetail.objects.select_related('requestid').exclude(requestid__in=Accepted).filter(**filter_dict)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )


@login_required
def Wip_View(request):
    view_header,view_footer = 'workflow','wip'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filter_dict = create_dict_for_filter(request,field_name_list = ['estimatedbyid','estimatedbyid__teamid'],value_list = [memberid,teamid])
    requestid = list(TblEstimationdetail.objects.filter(**filter_dict).values_list('requestid',flat=True))
    Accepted = list(TblCompleteddetail.objects.all().values_list('requestid', flat=True))
    UAT = list(TblUatDetail.objects.filter(Q(uat_statusid__isnull=True) | Q(uat_statusid__in=[1,None])).values_list('requestid', flat=True))
    data = TblAcceptrejectdetail.objects.select_related('requestid').filter(requestid__in=requestid).exclude(requestid__in=Accepted).exclude(requestid__in=UAT)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def UAT_View(request):
    view_header,view_footer = 'workflow','uat'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filter_dict = create_dict_for_filter(request,field_name_list = ['estimatedbyid','estimatedbyid__teamid'],value_list = [memberid,teamid])
    requestid = TblEstimationdetail.objects.filter(**filter_dict).values_list('requestid',flat=True)
    print(requestid)
    Accepted = list(TblCompleteddetail.objects.all().values_list('requestid', flat=True))
    data = TblUatDetail.objects.select_related('requestid').exclude(uat_statusid__in=[None]).exclude(requestid__in=Accepted).filter(requestid__in=requestid)
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )


@login_required
def Completed_View(request):
    view_header,view_footer = 'workflow','completed'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data = TblUatDetail.objects.select_related('requestid').filter(uat_statusid__uat_status__in=['Pass'])
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Rejected_View(request):
    view_header,view_footer = 'workflow','rejected'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data = TblRequeststatusdetail.objects.select_related('statusid','requestid').filter(statusid__in=[3])
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context )

@login_required
def Errorlog_Add_Form(request,reportid):
    view_header,view_footer = 'report','errordetail'
    title = 'Add Error'
    template = 'CentralMI/form_template.html'
    redirect_url = 'reportsdetail'
    template_type = 'template'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    memberid = TblMember.objects.get(userid__username__in=[username]).memberid
    form = ErrorlogForm(initial={'activityid':reportid,'reportedtoid':memberid})
    if request.method == 'POST':
        form = ErrorlogForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Errorlog_Detail_View(request):
    view_header,view_footer = 'report','errordetail'
    template = 'CentralMI/7a_error_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['reportedtoid','reportedtoid__teamid'], value_list = [memberid,teamid])
    data = TblErrorlog.objects.filter(**(filterdict))
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Errorlog_Edit_Form(request,requestid):
    view_header,view_footer = 'report','errordetail'
    template = 'CentralMI/form_template.html'
    title = 'Edit Error'
    redirect_url = view_footer
    template_type = 'template'
    template = 'CentralMI/3a_request_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblErrorlog.objects.get(error_id=requestid)
    model = TblErrorlog.objects.filter(error_id=requestid)
    form = ErrorlogForm(instance=e)
    if request.method == 'POST':
        e = TblErrorlog.objects.get(error_id=requestid)
        form = ErrorlogForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'model':model, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template, context)

def Ot_Detail_View(request):
    view_header,view_footer = 'timetracker','otdetail'
    template = 'CentralMI/9a_ot_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['timetrackerid__memberid','timetrackerid__teamid'], value_list = [memberid,teamid])
    data = TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]).filter(**(filterdict))
    context = {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context )


@login_required
def Useful_link_View(request):
    view_header,view_footer = 'details','usefullinks'
    template = 'CentralMI/useful_link_detail.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data = TblUsefulLinks.objects.all()
    context =  {'model':data,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)


@login_required
def Useful_link_Add_form(request):
    view_header,view_footer = 'details','usefullinks'
    template = 'CentralMI/form_template.html'
    title = 'Add Link'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    memberid = TblMember.objects.get(userid__username=username).memberid
    print(memberid)
    form = TblUsefulLinksForm(initial={'memberid':memberid})
    if request.method == 'POST':
        form = TblUsefulLinksForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context )

@login_required
def Useful_link_Edit_form(request,linkid):
    view_header,view_footer = 'details','usefullinks'
    template = 'CentralMI/form_template.html'
    title = 'Add Link'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblUsefulLinks.objects.get(linkid=linkid)
    form = TblUsefulLinksForm(instance=e)
    if request.method == 'POST':
        form = TblUsefulLinksForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context )

@login_required
def Raw_Team_View(request):
    view_header,view_footer = 'rawdetail','rawdteamdetail'
    template = 'CentralMI/raw_team_detail.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    data1 = TblRawTeamMemberMaster.objects.filter(raw_team=1).filter(raw_team__valid_invalid__in=[1])
    data2 = TblRawTeamMemberMaster.objects.filter(raw_team=2).filter(raw_team__valid_invalid__in=[1])
    data3 = TblRawTeamMemberMaster.objects.filter(raw_team=3).filter(raw_team__valid_invalid__in=[1])
    data4 = TblRawTeamMemberMaster.objects.filter(raw_team=4).filter(raw_team__valid_invalid__in=[1])
    data5 = TblRawTeamMemberMaster.objects.filter(raw_team=5).filter(raw_team__valid_invalid__in=[1])
    context =  {'model1':data1,'model2':data2,'model3':data3,'model4':data4,'model5':data5,'activetab1':activetab1,'activetab':activetab,'username':username,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Raw_Team_Edit_Form(request,teamid):
    view_header,view_footer = 'rawdetail','rawdteamdetail'
    title = 'Edit Team Member'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblRawTeamMemberMaster.objects.get(raw_team_member_id=teamid)
    form = TblRawTeamMemberMasterForm(instance=e)
    if request.method == 'POST':
        form = TblRawTeamMemberMasterForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context =  {'form':form,'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

@login_required
def Raw_Team_Add_Form(request):
    view_header,view_footer = 'rawdetail','rawdteamdetail'
    title = 'Add Team Member'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    form = TblRawTeamMemberMasterForm()
    if request.method == 'POST':
        form = TblRawTeamMemberMasterForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context =  {'form':form,'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)


@login_required
def Ot_Add_Form(request,trackerid):
    view_header,view_footer = 'timetracker','timetracker'
    title = 'Add OT Form'
    redirect_url =view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    count = TblOtDetail.objects.filter(timetrackerid__in=[trackerid]).count()
    status = list(TblOtDetail.objects.filter(timetrackerid__in=[trackerid]).values_list('statusid',flat=True))
    if status == [2] or status == [3]:
        form = OtDetail1Form(instance=TblOtDetail.objects.get(pk=TblOtDetail.objects.get(timetrackerid=trackerid).pk))
        msg = 'OT field is disabled as OT request has already been Accepted/Rejected'
    else:
        form = OtDetailForm(instance=TblOtDetail.objects.get(pk=TblOtDetail.objects.get(timetrackerid=trackerid).pk)) if count > 0 else OtDetailForm(initial={'timetrackerid':trackerid,'statusid':1})
        msg = ''
    if request.method == 'POST':
        form =  OtDetailForm(request.POST,request.FILES,instance=TblOtDetail.objects.get(ot_id=TblOtDetail.objects.get(timetrackerid=trackerid).ot_id)) if count > 0 else OtDetailForm(request.POST,request.FILES)
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
                inst.ot_time = Totalmin
            except:
                inst.ot_time = 0
                Totalmin = 0
            if Totalmin > 0 and Totalmin != None :
                inst.save()
                inst1 =  TblTimeTracker.objects.get(timetrackerid=trackerid)
                inst1.otid = inst
                inst1.save()
                return HttpResponseRedirect(reverse(view_footer))
                msg = 'OT recorded'
            else:
                msg = "OT time cannot be zero or less"
                context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'msg':msg,'title':title,'redirect_url':redirect_url,'template_type':template_type}
                return render(request,template,context)
    context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'msg':msg,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)

from django.apps import apps

#@login_required
def Filter_Data(request):
    view_header,view_footer = 'data','filtertab'
    activetab, activetab1, username, info, sd = create_session(request, header='data',footer='filtertab')
    reportpage = "mainpage"
    group_name = is_group(request,username=username)
    header_navbar_list, footer_navbar_list =navbar(request,view_header=view_header,username=username)
    form =  SearchForm()
    if request.method == 'POST':
        form =  SearchForm(request.POST)
        if form.is_valid():
            request.session['reportno'] = dict(REPORT_CHOICES)[int(form.cleaned_data['datachoice'])]
            request.session['startdate'] = str(form.cleaned_data['startdate'])
            request.session['interval'] = dict(INTERVAL_CHOICES)[int(form.cleaned_data["interval"])]
            request.session['type'] = dict(TYPE_CHOICES)[int(form.cleaned_data['datatype'])]
            request.session['enddate'] = str(form.cleaned_data['enddate'])
            request.session['team'] = str(form.cleaned_data['team'])
            request.session['member'] = str(form.cleaned_data['member'])
            startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
            return HttpResponseRedirect(reverse(view_footer))


            return HttpResponseRedirect(reverse(view_footer))
    return render(request, 'CentralMI/12a_filter_form.html',{'form':form,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'reportpage':reportpage,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list})


#@login_required
def Data_anlayis(request):
    view_header,view_footer = 'data','filtertab'
    activetab, activetab1, username, info, sd = create_session(request, header='data',footer='filtertab')
    reportpage = "mainpage"
    group_name = is_group(request,username=username)
    header_navbar_list, footer_navbar_list =navbar(request,view_header=view_header,username=username)
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    if type == 'Raw Data':
        startdate, enddate, reportno, type, interval, team, member, data = Rawdata(request)
        view_dict = ''
        value = ''
    elif type == 'Summary':
        value = request.POST.get('button')
        print(value)
        startdate, enddate, reportno, type, interval, team, member, data = Summary_Type(request,report_type=value)
        view_dict = subnavbar(request,reportno)
    else:
        startdate, enddate, reportno, type, interval, team, member, data = Rawdata(request)
        view_dict = ''
        value = ''
    return render(request, 'CentralMI/12a_filter_tab.html',{'data':data,'view_dict':view_dict,'startdate':startdate, 'enddate':enddate, 'reportno':reportno, 'type':type, 'interval':interval, 'team':team, 'member':member ,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'reportpage':reportpage,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,
    'value':value})


def Datarequiredforreport(request):
    startdate = request.session.get('startdate')
    enddate = request.session.get('enddate')
    reportno = request.session.get('reportno')
    interval = request.session.get('interval')
    type = request.session.get('type')
    team = request.session.get('team')
    member = request.session.get('member')
    return startdate, enddate, reportno, type, interval, team, member


def Rawdata(request):
    global exportdata
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    if reportno == 'Workflow':
        data, countofdata = data_formation_workflow(request,startdate=startdate,enddate=enddate,team=team, member=member)
        if countofdata >0:
            data = data[['requestid','requestraiseddate','requestpriority','requestdescription','authoriseddate','assigneddate','overviewdate','estimationdate','estacceptrejectdate']]
            exportdata = data
            data = exportdata.to_html(classes="table cell-border")
        else:
            data = data

    elif reportno == 'TimeTracker':
        print('startdate' + str(startdate) )
        print(enddate)
        data, countofdata = data_formation_Timetracker(request,startdate=startdate,enddate=enddate,team=team, member=member)
        if countofdata >0:
            data =  data[['timetrackerid','registerdatetime','trackingdatetime','username','task','requestcategorys','requestsubcategory','core_noncore','totaltime','comments','description_text']]
            exportdata = data
            data = exportdata.to_html(classes="table cell-border")
        else:
            data = data
    elif reportno == 'ErrorLog':
        data, countofdata = data_formation_error(request,startdate=startdate,enddate=enddate,team=team, member=member)
        if countofdata >0:
            data =  data[['occurancedate','name','username','error_description','description','primaryowner_id','secondaryowner_id']]
            exportdata = data
            data = exportdata.to_html(classes="table cell-border")
        else:
            data = data

    elif reportno == 'OT':
        data, countofdata = data_formation_ot(request,startdate=startdate,enddate=enddate,team=team, member=member)
        if countofdata >0:
            data =  data[['ot_id_x','ot_startdatetime','ot_enddatetime','ot_time','timetrackerid','trackingdatetime','username','task','totaltime']]
            exportdata = data
            data = exportdata.to_html(classes="table cell-border")
        else:
            data = data
    else:
        data, countofdata = data_formation_workflow(request,startdate=startdate,enddate=enddate,team=team, member=member)
        if countofdata >0:
            data = data[['requestid','requestraiseddate','requestpriority','requestdescription','authoriseddate','assigneddate','overviewdate','estimationdate','estacceptrejectdate']]
            exportdata = data
            data = exportdata.to_html(classes="table cell-border")
        else:
            data = data

    return startdate, enddate, reportno, type, interval, team, member, data


def subnavbar(request,reportno=None):
    if reportno == 'Workflow':
        view_dict = {'Requesttype':{'view':'Request Type','url':'data','value':'Request_Type'},
                     'Request_Priority': {'view':'Request Priority','url':'data','value':'Request_Priority'},
                     'Request_Assigned': {'view':'Request Assigned','url':'data','value':'Request_Assigned'}}

    elif reportno == 'TimeTracker':
        view_dict = {'TimeTracker_CoreNonCore':{'view':'Core Non-Core','url':'data','value':'Core_Non-Core'},
                     'TimeTracker_Activity_view': {'view':'Activity View','url':'data','value':'Activity_View'}}
    elif reportno == 'ErrorLog':
            view_dict = {'Error_User_Wise':{'view':'User Wise','url':'data','value':'User_Wise'},
                         'Error_Report_Wise': {'view':'Report Wise','url':'data','value':'Report_Wise'}}
    elif reportno == 'OT':
            view_dict = {'OT_view':{'view':'Request_Type','url':'data','value':'OT_view'}}
    return view_dict

def Summary_Type(request,report_type=None):
    global exportdata
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    if reportno == 'Workflow' and report_type == None:
        report_type = 'Request_Type'
    elif reportno == 'TimeTracker' and report_type == None:
        report_type = 'Core_Non-Core'
    elif reportno == 'ErrorLog' and report_type == None:
        report_type = 'User_Wise'
    elif reportno == 'OT' and report_type == None:
        report_type = 'OT_view'

    if report_type == 'Request_Type':
        print(report_type)
        print(reportno)
        data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requesttype')
        print(data)
    elif report_type == 'Request_Priority':
        data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestpriority')
    elif report_type == 'Request_Assigned':
        data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestassigned')
    elif report_type == 'Core_Non-Core':
        data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='core_noncore')
    elif report_type == 'Activity_View':
        data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='activity')
    elif report_type == 'User_Wise':
        data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='erroruserwise')
    elif report_type == 'Report_Wise':
        data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='errorreportwise')
    elif report_type == 'OT_view':
        data = Ot_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view=None)

    return startdate, enddate, reportno, type, interval, team, member, data


def CoreNonCore_View(request):
    global exportdata
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='core_noncore')
    return startdate, enddate, reportno, type, interval, team, member, data


def Activitytimetracker_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Timetrcker_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='activity')
    return startdate, enddate, reportno, type, interval, team, member, data

def Requesttype_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requesttype')
    return startdate, enddate, reportno, type, interval, team, member, data

def Requestpriority_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestpriority')
    return startdate, enddate, reportno, type, interval, team, member, data

def Requestassigned_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestassigned')
    return startdate, enddate, reportno, type, interval, team, member, data

def Requestcompleted_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Workflow_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='requestcompleted')
    return startdate, enddate, reportno, type, interval, team, member, data

def Ot_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Ot_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view=None)
    return startdate, enddate, reportno, type, interval, team, member, data

def Erroruserwise_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='erroruserwise')
    return startdate, enddate, reportno, type, interval, team, member, data

def Errorreportwise_View(request):
    startdate, enddate, reportno, type, interval, team, member = Datarequiredforreport(request)
    data = Error_Summary(request,startdate=startdate,enddate=enddate,interval=interval,team=team,member=member,view='errorreportwise')
    return startdate, enddate, reportno, type, interval, team, member, data

@login_required
def About_Team_View(request):
    view_header,view_footer = 'home','aboutteam'
    template = 'CentralMI/2a_about_team_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblMember.objects.all()
    context = {'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def What_We_Do_View(request):
    view_header,view_footer = 'home','whatwedo'
    template =  'CentralMI/2b_what_we_do_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblWhatwedo.objects.filter(type__in=['Skill'])
    model1 = TblWhatwedo.objects.filter(type__in=['Geograhic'])
    context = {'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model,'model1':model1,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context)


@login_required
def What_We_Do_Add(request):
    view_header,view_footer = 'home','whatwedo'
    template = 'CentralMI/form_template.html'
    title = 'Add'
    redirect_url = 'whatwedo'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    form = WhatwedoForm()
    if request.method == 'POST':
        form = WhatwedoForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context)

@login_required
def Governance_Process_View(request):
    view_header,view_footer = 'home','governanceprocess'
    template = 'CentralMI/2c_governance_process_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblGovernance.objects.all()
    context = {'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context)

@login_required
def Success_Stories_View(request):
    view_header,view_footer = 'home','successstories'
    template = 'CentralMI/2d_success_stories_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblSuccessStories.objects.all()
    context = {'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template ,context)

@login_required
def Success_Stories_Add(request):
    view_header,view_footer = 'home','successstories'
    template = 'CentralMI/form_template.html'
    title = 'Add Stories'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    form = SuccessStoriesForm()
    if request.method == 'POST':
        form = SuccessStoriesForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)



@login_required
def Conversation_Form(request,requestid):
    view_header,view_footer = 'workflow','ty'
    template = 'CentralMI/form_template_with_parameter.html'
    title = 'Add Your Point'
    redirect_url = 'ty'
    template_type = 'template_with_parameter'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    print(username)
    print(userid)
    print(requestid)
    form = TblConversationForm(initial={'userid':userid,'requestid':requestid})
    if request.method == 'POST':
        print("True")
        form =  TblConversationForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('ty',args = (requestid,)))
    context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'reverseid':requestid,'title':title,'redirect_url':redirect_url,'template_type':template_type,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
    return render(request, template,context)


@login_required
def Comm_Sugg_View(request):
    view_header,view_footer = 'home','commsugg'
    template = 'CentralMI/2e_comm_sugg_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblSuggestion.objects.all()
    context = {'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'username':username,'model':model,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Comm_Sugg_Add(request):
    view_header,view_footer = 'home','commsugg'
    title = 'Add Suggestion'
    template ='CentralMI/form_template.html'
    redirect_url = 'commsugg'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    form = SuggestionForm(initial={'suggestedbyid':userid})
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('commsugg'))
    context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)



@login_required
def Check_Status_View(request):
    view_header,view_footer = 'loginrequest','checkstatus'
    template =  'CentralMI/3b_check_status_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    model = TblRequestdetail.objects.filter(userid__in=[userid])
    #filter_dict = create_dict_for_filter(request,field_name_list = ['estimatedby','estimatedby__teamdetail'],value_list = [memberid,teamid])
    context = {'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context)

@login_required
def Report_Detail_View(request):
    view_header,view_footer = 'report','reportsdetail'
    template = 'CentralMI/5a_reports_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['teamname'], value_list = [teamid])
    model = TblActivity.objects.filter(**(filterdict))
    if memberid !=None and memberid !='None':
        model = TblActivity.objects.filter(Q(primaryowner__in=memberid)|Q(secondaryowner__in=memberid))
    context = {'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Report_Add_Form(request):
    view_header,view_footer = 'reportsdetail','report'
    template = 'CentralMI/5a_report_add_form.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    header_navbar_list, footer_navbar_list =navbar(request,view_header=view_header,username=username)
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST,request.FILES)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'form_header':form_header}
        return render(request, template,context)
    context = {'form':form,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'form_header':form_header}
    return render(request, template,context)

@login_required
def Report_Edit_Form(request,requestid):
    view_header,view_footer = 'report','allreports'
    template = 'CentralMI/5c_report_edit_form.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblActivity.objects.get(activityid=requestid)
    model = TblActivity.objects.filter(activityid=requestid)
    form = ActivityForm(instance=e)
    if request.method == 'POST':
        e = TblActivity.objects.get(pk=requestid)
        form = ActivityForm(request.POST,request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context =  {'form':form,'model':model, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
    return render(request, template,context)


######################## Feedback

@login_required
def Feedback_Question_View(request,activityid):
    view_header,view_footer = 'report','allreports'
    template = 'CentralMI/6b_feedback_question_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model =  TblFeedbackQuestionMaster.objects.all()
    request.session['aid'] = activityid
    context = {'model':model,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Feedback_Detail_View(request):
    view_header,view_footer = 'report','feedbackdetail'
    template ='CentralMI/6a_feedback_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['activityid__teamname'], value_list = [teamid])
    model = TblFeedback.objects.filter(**(filterdict))
    if memberid !=None and memberid !='None':
        model = TblFeedback.objects.filter(Q(activityid__primaryowner__in=memberid)|Q(activityid__secondaryowner__in=memberid))
    context = {'model':model,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template ,context)

@login_required
def Feedback_Edit_Form(request,feedbackid):
    view_header,view_footer = 'report','feedbackdetail'
    title = 'Edit Feedback'
    template ='CentralMI/form_template.html'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblFeedback.objects.get(feedback_id=feedbackid)
    model = TblFeedback.objects.filter(feedback_id=feedbackid)
    form = FeedbackForm(instance=e)
    if request.method == 'POST':
        e = TblFeedback.objects.get(feedback_id=feedbackid)
        form = FeedbackForm(request.POST,request.FILES, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse('feedbackdetail'))
    context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'reverseid':activityid,'template_type':template_type}
    return render(request,template ,context)

@login_required
def Feedback_Add_Form(request,feedbackquestionid):
    view_header,view_footer = 'report','viewfeedbackquestion'
    redirect_url = view_footer
    template = 'CentralMI/dynamic_form_with_parameter.html'
    template_type = 'template_with_parameter'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    activityid = request.session.get('aid')
    checkmember = TblFeedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activityid__in=[activityid]).count()
    model1 = TblFeedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activityid__in=[activityid])
    if checkmember > 0:
        title = 'Edit Feedback'
        feedbackid = TblFeedback.objects.filter(feedback_question__in=[feedbackquestionid]).filter(activityid__in=[activityid]).values_list('feedback_id',flat=True)
        feedbackid = list(feedbackid)
        feedbackid = feedbackid[0]
        e = TblFeedback.objects.get(feedback_id=feedbackid)
        form = FeedbackForm(instance=e)
        if request.method == 'POST':
            form =  FeedbackForm(request.POST,instance=e)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.save()
                return HttpResponseRedirect(reverse(view_footer,args = (activityid,)))
            else:
                context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'reverseid':activityid,'template_type':template_type}
                return render(request, template,context)
    else:
        title = 'Add Feedback'
        form = FeedbackForm(initial={'feedback_question':feedbackquestionid,'activityid':activityid})
        if request.method == 'POST':
            form = FeedbackForm(request.POST,request.FILES)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.save()
                return HttpResponseRedirect(reverse(view_footer,args = (activityid,)))
            else:
                context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'reverseid':activityid,'template_type':template_type}
                return render(request, template,context)
    context = {'form':form,'username':username, 'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'activityid':activityid,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'reverseid':activityid,'template_type':template_type}
    return render(request, template,context)

############## Staff
@login_required
def Staff_Detail_View(request):
    view_header,view_footer = 'details','staffdetail'
    template =  'CentralMI/10a_staff_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['memberid','teamid'], value_list = [memberid,teamid])
    model1 = User.objects.all()
    model = TblMember.objects.filter(**(filterdict))
    data = zip(model1,model)
    context = {'model':model,'model1':model1,'data':data,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request,template,context)

@login_required
def My_Detail_View(request):
    view_header,view_footer = 'details','mydetail'
    template = 'CentralMI/10a_my_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    model1 = User.objects.filter(username__in=[username])
    model = TblMember.objects.filter(userid__in=[userid])
    data = zip(model1,model)
    context = {'model':model,'model1':model1,'data':data,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)


@login_required
def Staff_Edit_Form(request):
    view_header,view_footer = 'details','mydetail'
    title = 'Edit Details'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    e1 = User.objects.get(id=userid)
    print(e1)
    e = TblMember.objects.get(userid=userid)
    model1 = User.objects.filter(username__in=username)
    model = TblMember.objects.filter(userid__in=[userid])
    form1 = UserForm(instance=e1)
    form = MemberForm(instance=e)
    if request.method == 'POST':
        form = MemberForm(request.POST,request.FILES,instance=e)
        form1 = UserForm (request.POST,instance=e1)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=True)
            inst.save()
            inst1 = form1.save(commit=False)
            inst1.username = username
            inst1.save()
            return HttpResponseRedirect(reverse('mydetail'))
    context = {'form':form,'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template':template,'template_type':template_type}
    return render(request, template,context)


@login_required
def Staff_Edit_Manager_Form(request,id):
    view_header,view_footer = 'details','staffdetail'
    title = 'Edit Details'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(id=id).pk
    e1 = User.objects.get(pk=userid)
    model1 = User.objects.filter(username__in=username)
    form1 = UserForm(instance=e1)
    if request.method == 'POST':
        form1 = UserForm (request.POST,instance=e1)
        if  form1.is_valid():
            inst1 = form1.save(commit=True)
            inst1.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template':template,'template_type':template_type}
    return render(request, template,context)


############### Internal Task detailview
@login_required
def Internal_Task_Detail_View(request):
    view_header,view_footer = 'details','internaltaskdetail'
    template = 'CentralMI/11a_internal_task_detail_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblInternaltask.objects.all()
    context = {'model':model, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

def Internal_Task_Completion_View(request,internaltaskid):
    view_header,view_footer = 'details','internaltaskdetail'
    template = 'CentralMI/11g_internal_task_completion_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblInternaltaskstatus.objects.filter(internaltaskid_id__in=[internaltaskid])
    context = {'model':model, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)


@login_required
def Internal_Task_Add_Form(request):
    view_header,view_footer = 'details','internaltaskdetail'
    title = 'Internal Task'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    form = InternaltaskForm(initial={'ownerid':memberid})
    if request.method == 'POST':
        form = InternaltaskForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template':template,'template_type':template_type}
    return render(request, template,context)

@login_required
def Internal_Task_Edit_Form(request,taskid):
    view_header,view_footer = 'details','internaltaskdetail'
    template = 'CentralMI/11b_internal_task_add_form.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblInternaltask.objects.get(internaltaskid=taskid)
    form = InternaltaskForm(instance=e)
    if request.method == 'POST':
        form = InternaltaskForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
    return render(request, template,context)

@login_required
def Leave_Record_Form(request):
    view_header,view_footer = 'details','leaverecorddetail'
    title = 'Add Leave record'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid  = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    form = TblLeaveRecordForm(initial={'userid':memberid})
    if request.method == 'POST':
        form = TblLeaveRecordForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template':template,'template_type':template_type,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Leave_Record_Edit(request,leaveid):
    view_header,view_footer = 'details','leaverecorddetail'
    title = 'Edit Leave record'
    redirect_url = view_footer
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblLeaveRecord.objects.get(leaverecordid=leaveid)
    form = TblLeaveRecordForm(instance=e)
    if request.method == 'POST':
        form = TblLeaveRecordForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form, 'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template':template,'template_type':template_type}
    return render(request, template,context)

@login_required
def Leave_Record_View(request):
    view_header,view_footer = 'details','leaverecorddetail'
    template = 'CentralMI/11a_leave_detail.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    teamid = request.session.get('sessison_team')
    memberid = request.session.get('sessison_member')
    filterdict = create_dict_for_filter(request,field_name_list = ['userid','userid__teamid'], value_list = [memberid,teamid])
    model = TblLeaveRecord.objects.filter(**(filterdict))
    model1 = TblPublicHolidaysMaster.objects.all()
    count = model.values('leave_type__leave_type','userid__userid__username').annotate(dcount=Count('leave_type'))
    context = {'model':model, 'model1':model1,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'count':count,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)

@login_required
def Internal_Task_Choice_view(request,taskid):
    view_header,view_footer = 'details','internaltaskdetail'
    template ='CentralMI/11c_internal_task_choice_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    model = TblInternaltaskchoice.objects.filter(internaltaskid__in=[taskid])
    context = {'model':model, 'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template,context)


@login_required
def Internal_Choice_Add_Form(request,taskid):
    view_header,view_footer = 'details','viewinternaltaskoption'
    template = 'CentralMI/11d_internal_task_choice_add_form.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    id = taskid
    form =  InternaltaskchoiceForm(initial={'internaltask':taskid})
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer,args = (id,)))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        context = {'form':form,'taskid':taskid,'id':id,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
        return render(request, template,context)
    context = {'form':form,'taskid':taskid,'id':id,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
    return render(request, template,context)


@login_required
def Internal_Choice_Edit_Form(request,choiceid):
    view_header,view_footer = 'details','viewinternaltaskoption'
    template = 'CentralMI/form_template_with_parameter.html'
    title = 'Edit Internal Task Choice'
    redirect_url = view_footer
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblInternaltaskchoice.objects.get(internaltaskchoiceid=choiceid)
    question = TblInternaltaskchoice.objects.get(internaltaskchoiceid=choiceid).internaltaskid
    taskid = TblInternaltask.objects.get(internaltaskquestion=question).internaltaskid
    form =  InternaltaskchoiceForm(instance=e)
    if request.method == 'POST':
        form =  InternaltaskchoiceForm(request.POST,instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer,args = (taskid,)))
        else:
            return render(request, 'CentralMI/15a_ErrorPage.html')
    else:
        context = {'form':form,'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'reverseid':choiceid,'redirect_url':redirect_url}
        return render(request, template, context)
    context = {'form':form,'taskid':taskid,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'reverseid':choiceid,'redirect_url':redirect_url}
    return render(request, template,context)


@login_required
def Internal_Task_And_Choice_View(request,taskid):
    view_header,view_footer = 'details','internaltaskdetail'
    template = 'CentralMI/form_template_with_choice.html'
    redirect_url = 'internaltaskwithchoiceedit'
    title = 'Edit Internal Choice'
    template_type = 'template_with_choice'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    model =  TblInternaltask.objects.filter(internaltaskid__in=[taskid])
    model1 = TblInternaltaskchoice.objects.filter(internaltaskid__in=[taskid])
    checkmember = TblInternaltaskstatus.objects.filter(internaltaskid__in=[taskid]).filter(memberid__in=[memberid]).count()
    model2 = TblInternaltaskstatus.objects.filter(memberid__in=[memberid]).filter(internaltaskid__in=[taskid])
    if checkmember > 0:
        taskstatusid = TblInternaltaskstatus.objects.filter(memberid__in=[memberid]).filter(internaltaskid__in=[taskid]).values_list('internaltaskstatusid',flat=True)
        taskstatusid = list(taskstatusid)
        taskstatusid= taskstatusid[0]
        print(taskstatusid)
        e = TblInternaltaskstatus.objects.get(internaltaskstatusid=taskstatusid)
        form = InternaltaskstatusForm(instance=e)
        if request.method == 'POST':
            choice = request.POST['choice']
            e = TblInternaltaskchoice.objects.get(internaltaskchoice=choice)
            form =  InternaltaskstatusForm(request.POST,instance=e)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.internaltaskchoice = e
                inst.save()
                return HttpResponseRedirect(reverse(view_footer))
            else:
                return render(request, template,{'form':form,'model':model,'model1':model1,'model2':model2,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url,'reverseid':taskstatusid,'template_type':template_type})
    else:
        form =  InternaltaskstatusForm(initial={'internaltask':taskid, 'memberid':memberid})
        if request.method == 'POST':
            choice = request.POST['choice']
            taskchoiceid = TblInternaltaskchoice.objects.filter(internaltaskchoice=choice).filter(internaltask=taskid).values_list('internaltaskchoiceid', flat=True)
            taskchoiceid = list(taskchoiceid)
            taskchoiceid = taskchoiceid[0]
            print(taskchoiceid)
            e = Internaltaskchoice.objects.get(internaltaskchoiceid=taskchoiceid)
            print(e)
            form =  InternaltaskstatusForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=True)
                inst.internaltaskchoice = e
                inst.save()
                return HttpResponseRedirect(reverse(view_footer))
    return render(request, template,{'form':form,'checkmember':checkmember,'model':model,'model1':model1,'model2':model2,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url,'template_type':template_type,'reverseid':taskstatusid})

@login_required
def Internal_Task_And_Choice_Edit_Form(request,taskstatusid):
    view_header,view_footer = 'details','internaltaskdetail'
    template = 'CentralMI/form_template_with_choice.html'
    redirect_url = 'internaltaskdetail'
    title = 'Edit Internal Choice'
    template_type = 'template_with_choice'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    internaltaskchoice = TblInternaltaskstatus.objects.filter(internaltaskstatusid__in=[taskstatusid]).values_list('internaltaskchoiceid', flat=True)
    taskid = TblInternaltaskstatus.objects.filter(internaltaskstatusid__in=[taskstatusid]).values_list('internaltaskid', flat=True)
    taskid1 = list(taskid)
    taskid1 = taskid1[0]
    internaltaskid = TblInternaltask.objects.get(internaltaskid=taskid1).internaltaskid
    choice = TblInternaltaskchoice.objects.filter(internaltaskchoiceid__in=list(internaltaskchoice)).values_list('internaltaskchoice',flat=True)
    choice_string = ', '.join(choice)
    model =  TblInternaltask.objects.filter(internaltaskid__in=list(taskid))
    model1 = TblInternaltaskchoice.objects.filter(internaltaskid__in=list(taskid))
    e = TblInternaltaskstatus.objects.get(internaltaskstatusid=taskstatusid)
    form = InternaltaskstatusForm(instance=e)
    if request.method == 'POST':
        choice = request.POST['choice']
        taskchoiceid = TblInternaltaskchoice.objects.filter(internaltaskchoice__in=[choice]).filter(internaltaskid__in=list(taskid)).values_list('internaltaskchoiceid',flat=True)
        taskchoiceid = list(taskchoiceid)
        taskchoiceid = taskchoiceid[0]
        f = TblInternaltaskchoice.objects.get(internaltaskchoiceid=taskchoiceid)
        form =  InternaltaskstatusForm(request.POST,instance=e)
        print(form)
        if form.is_valid():
            print(f)
            inst = form.save(commit=True)
            inst.internaltaskchoiceid = f
            inst.save()
            return HttpResponseRedirect(reverse(view_footer,args = (internaltaskid,)))
    context = {'form':form,'model':model,'model1':model1,'choice':choice_string,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'reverseid':internaltaskid,'template_type':template_type}
    return render(request, template,context)






@login_required
def Request_Form(request):
    view_header,view_footer = 'loginrequest','addrequest'
    title = 'Request Form'
    redirect_url = 'ty'
    template = 'CentralMI/4a_request_form.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    form = RequestdetailForm(initial={'userid':userid})
    form1 = StatusdetailForm(initial={'statusid':1,'userid':userid,'requestid':None})
    if request.method == 'POST':
        form = RequestdetailForm(request.POST,request.FILES)
        form1 = StatusdetailForm (request.POST)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=True)
            inst.save()
            newid = inst.pk
            inst1 = form1.save(commit=False)
            inst1.requestid = inst
            inst1.save()
            return HttpResponseRedirect(reverse(redirect_url,args = (newid,)))
    else:
        context = {'form':form,'form1':form1,  'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list': footer_navbar_list,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)
    return render(request, template,context)


@login_required
def Authorised_Form(request,requestid):
    view_header,view_footer = 'workflow','unapproved'
    title = 'Authorised Form'
    redirect_url = 'unapproved'
    template = 'CentralMI/form_template.html'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    try:
        DataModel= TblAuthorisedetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse(view_footer))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = AuthorisedetailForm(initial={'requestid':requestid, 'authoriserid':userid})
        form1 = AuthoriserstatusdetailForm(initial={'statusid':2,'userid':userid,'requestid':requestid})
        if request.method == 'POST':
            form = AuthorisedetailForm(request.POST)
            form1 = AuthoriserstatusdetailForm(request.POST)
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
                return HttpResponseRedirect(reverse(view_footer))
        context = {'form':form, 'form1':form1,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request,template ,context)

@login_required
def Requestassigneddetail_Form(request, requestid):
    view_header,view_footer = 'workflow','approved'
    title = "Assigned Form"
    template = 'CentralMI/form_template.html'
    redirect_url = 'approved'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    try:
        DataModel= TblAssigneddetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse(view_footer))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = AssigneddetailForm(initial={'requestid':requestid, 'assignedbyid':memberid})
        form1 = RequeststatusdetailForm(initial={'statusid':4,'userid':userid,'requestid':requestid})
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

                return HttpResponseRedirect(reverse(view_footer))
        context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)

@login_required
def Overview_Form(request,requestid):
    view_header,view_footer = 'workflow','assigned'
    title = 'Overview Form'
    template = 'CentralMI/form_template.html'
    redirect_url = 'assigned'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    try:
        DataModel= TblOverviewdetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse('assigned'))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = OverviewdetailForm(initial={'requestid':requestid, 'giventoid':memberid})
        form1 = RequeststatusdetailForm(initial={'statusid':5,'userid':userid,'requestid':requestid})
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
                return HttpResponseRedirect(reverse(view_footer))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)

@login_required
def Estimation_Form(request,requestid):
    view_header,view_footer = 'workflow','overview'
    title = 'Estimation Form'
    template = 'CentralMI/form_template.html'
    redirect_url = 'overview'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    memberid = TblMember.objects.get(userid=userid).memberid
    #print(userid)
    try:
        DataModel= TblEstimationdetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse('overview'))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = EstimationdetailForm(initial={'requestid':requestid, 'estimatedbyid':memberid})
        form1 = RequeststatusdetailForm(initial={'statusid':6,'userid':userid,'requestid':requestid})
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
                return HttpResponseRedirect(reverse(view_footer))
            else:
                pagename = "estimate"
                errormsg1 = "Something went Wrong"
                return render(request, 'CentralMI/15a_ErrorPage.html')
        context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)

@login_required
def EstimationAcceptance_Form(request,requestid):
    view_header,view_footer = 'workflow','estimate'
    title = 'Estimation Acceptance/Rejection Form'
    template = 'CentralMI/form_template.html'
    redirect_url = 'estimate'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)

    userid = User.objects.get(username=username).id
    try:
        DataModel= TblAcceptrejectdetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse('estimate'))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = AcceptrejectdetailForm(initial={'requestid':requestid, 'userid':userid})
        form1 = AcceptRequeststatusdetailForm(initial={'statusid':7,'userid':userid,'requestid':requestid})
        if request.method == 'POST':
            form = AcceptrejectdetailForm(request.POST)
            form1 = AcceptRequeststatusdetailForm(request.POST)
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
                return HttpResponseRedirect(reverse(view_footer))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)


@login_required
def WIP_Form(request,requestid):
    view_header,view_footer = 'workflow','wip'
    title = 'UAT Form'
    template = 'CentralMI/form_template.html'
    redirect_url = 'wip'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    try:
        DataModel= TblUatDetail.objects.filter(uat_statusid__in=1).get(requestid=requestid)
        return HttpResponseRedirect(reverse('wip'))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
        form = UatDetailForm(initial={'requestid':requestid, 'updatedbyid':userid})
        form1 = RequeststatusdetailForm(initial={'statusid':11,'userid':userid,'requestid':requestid})
        if request.method == 'POST':
            form = UatDetailForm(request.POST)
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
                return HttpResponseRedirect(reverse(view_footer))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
        return render(request, template,context)




@login_required
def UAT_Form(request,requestid):
    view_header,view_footer = 'workflow','uat'
    title = 'UAT Form'
    template = 'CentralMI/form_template.html'
    redirect_url = 'uat'
    template_type = 'template'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    userid = User.objects.get(username=username).id
    authuserinstance = AuthUser.objects.get(username=username)
    e = TblUatDetail.objects.filter(uat_statusid=None).get(requestid=requestid)
    #print(e)
    requestfilter = TblRequestdetail.objects.get(requestid=requestid)
    request_owner = TblRequestdetail.objects.get(requestid=requestid).userid
    form  = UatDetail1Form(instance=e)
    #print(form)
    form1 = RequeststatusdetailForm(initial={'statusid':11,'userid':userid,'requestid':requestid})
    if request.method == 'POST':
        form = UatDetail1Form(request.POST,instance=e)
        form1 = RequeststatusdetailForm(request.POST)
        if all([form.is_valid() , form1.is_valid()]):
            inst = form.save(commit=False)
            inst.testedbyid = authuserinstance
            inst.save()
            status = inst.uat_statusid
            inst1 = form1.save(commit=False)
            inst1.save()
            if str(status) == 'Failed':
                stageinst = TblStatusMaster.objects.get(statusnameid=8)
            elif str(status) == 'Pass':
                stageinst = TblStatusMaster.objects.get(statusnameid=9)
            else:
                stageinst = TblStatusMaster.objects.get(statusnameid=11)
            ins = TblRequeststatusdetail.objects.get(requeststatusid=inst1.requeststatusid)
            ins.statusid = stageinst
            ins.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'form1':form1,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'title':title,'redirect_url':redirect_url,'template_type':template_type}
    return render(request, template,context)


@login_required
def Completed_Form(request,requestid):
    view_header,view_footer = 'workflow','wip'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)

    userid = User.objects.get(username=username).id
    try:
        DataModel= TblCompleteddetail.objects.all().get(requestid=requestid)
        return HttpResponseRedirect(reverse('wip'))
    except:
        requestfilter = TblRequestdetail.objects.get(requestid=requestid)
        request_owner = TblRequestdetail.objects.get(requestid=requestid).username

        form = CompleteddetailForm(initial={'requestid':requestid, 'completedby':userid})
        form1 = RequeststatusdetailForm(initial={'statusid':9,'userid':userid,'requestid':requestid})
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
                return HttpResponseRedirect(reverse(view_footer))
            else:
                return render(request, 'CentralMI/15a_ErrorPage.html')
        return render(request, 'CentralMI/4g_completed_form.html',{'form':form, 'form1':form1, 'username': username,'activetab1':activetab1,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list})



@login_required
def Thank_You_Page_View(request,requestid):
    view_header,view_footer = 'loginrequest','checkstatus'
    template = 'CentralMI/3c_thankyou_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    try:
        model1 = TblRequestdetail.objects.all().get(requestid=requestid)
        try:
            model2 = TblAuthorisedetail.objects.all().get(requestid=requestid)
        except:
            model2 = "nothing"
        try:
            model3 = TblYesNo.objects.all().get(requestid=requestid)
        except:
            model3 = "nothing"
        try:
            model4 = TblAssigneddetail.objects.all().get(requestid=requestid)
        except:
            model4 = "nothing"
        try:
            model5 = TblOverviewdetail.objects.all().get(requestid=requestid)
        except:
            model5 = "nothing"
        try:
            model6 = TblEstimationdetail.objects.all().get(requestid=requestid)
        except:
            model6 = "nothing"
        try:
            model7 = TblAcceptrejectdetail.objects.all().get(requestid=requestid)
        except:
            model7 = "nothing"
        try:
            model8 = TblUatDetail.objects.filter(uat_statusid__in=[1]).get(requestid=requestid)
        except:
            model8 = "nothing"
        try:
            model9 = TblConversation.objects.filter(requestid=requestid)
        except:
            model9 = "nothing"
        context = {'detail1':model1,'detail2':model2,'detail3':model3,'detail4':model4,'detail5':model5,'detail6':model6,'detail7':model7,'detail8':model8,'model9':model9,'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
        return render(request, template,context)
    except:
        context = {'username':username,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list}
        return render(request, 'CentralMI/15a_ErrorPage.html',context)



@login_required
def filterform(request,username,session_teamid,session_memberid):
    form = FilteredForm(initial={'teamfilter':session_teamid, 'memberfilter':session_memberid})
    if request.method == 'POST':
        form =  FilteredForm(request.POST)
        if form.is_valid():
            teamfilter = form.cleaned_data['teamfilter']
            memberfilter = form.cleaned_data['memberfilter']
            if teamfilter != None and memberfilter != None:
                teamid = TblTeamMaster.objects.get(teamname__in=[teamfilter]).teamid
                userid = User.objects.get(username__in=[memberfilter]).id
                memberid = TblMember.objects.get(username__in=[userid]).memberid
            elif teamfilter != None and memberfilter == None:
                teamid = TblTeamMaster.objects.get(teamname__in=[teamfilter]).teamid
                memberid = None
            elif teamfilter == None and memberfilter == None:
                teamid = None
                memberid = None
    else:
        userid = User.objects.get(username__in=[username]).id
        memberid = TblMember.objects.get(username__in=[userid]).memberid
        teamid = TblMember.objects.get(username__in=[userid]).teamid
    return teamid , memberid, form



def dataforemail(username=None,requestid=None,sub_user=None,L1_user=None,sub_auth=None,L1_auth=None,sub_miteam=None,L1_miteam=None,sub_manager=None,L1_manager=None,request_status=None):
    userid = User.objects.get(username=username).id
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
        self.requestinst = TblRequestdetail.objects.get(requestid=self.requestid)
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
        self.memberid = TblMember.objects.get(username=self.user_id).memberid
        self.teamid = TblMember.objects.get(memberid=self.memberid).teamid
#        self.coreid = TblSubcategoryMaster.objects.filter(core_noncore__in=[self.core]).values_list('pk', flat=True).distinct()
#        self.noncoreid = TblSubcategoryMaster.objects.filter(core_noncore__in=[self.noncore]).values_list('pk', flat=True).distinct()
#        self.modelTracker = TblTimeTracker.objects.filter(mimember__in=[self.mimemberid]).filter(trackingdatetime=self.sd).select_related()

    def define_day_week_month1(self,start_date=None,end_date=None,days_range=None,range_type=None,year_range=0,report_choice=None,aggregatefield=None,values=None,core_noncore=None,OT=None,utilisation='No',teamdetail=None,member=None,output_type=None):
        #data1 = TblAssigneddetail.objects.all()
        #requestdetail = TblAssigneddetail.objects.get(assignedto=2)
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
            self.memberinteam = TblMember.objects.filter(teamid__in=[teamdetail]).values_list('memberid', flat=True).distinct()
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
                    self.data = TblErrorlog.objects.filter(occurancedate__range=(self.StartDate,self.EndDate)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail != None and member == None:
                    self.data = TblErrorlog.objects.filter(occurancedate__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail == None and member != None:
                    self.data = TblErrorlog.objects.filter(occurancedate__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=[member]).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                elif teamdetail != None and member != None:
                    self.data = TblErrorlog.objects.filter(occurancedate__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                else:
                    self.data = TblErrorlog.objects.filter(occurancedate__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=list(self.memberinteam)).values(self.values).aggregate(Count(self.aggregatefield))
                    self.data = self.data[aggregatefield+'__count']
                self.key.append(str(self.date))
                self.value.append(str(self.data))
                self.result = OrderedDict(zip(self.key, self.value))

            elif output_type == 'timetracker':
                self.key.append(str(1))
                self.value.append(str(2))
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
            self.memberinteam = TblMember.objects.filter(teamid__in=[teamdetail]).values_list('memberid', flat=True).distinct()
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

        if report_choice == '1':
            if teamdetail == None and member == None:
                self.data = TblTimeTracker.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                memberid = TblMember.objects.filter(teamid__in=[teamdetail]).values_list('memberid',flat=True)
                requestid = TblAssigneddetail.objects.filter(assignedtoid__in=list(memberid)).values_list('requestid',flat=True)
                self.data = TblRequestdetail.objects.filter(requestraiseddate__range=(self.StartDate,self.EndDate)).filter(requestid__in=list(requestid)).aggregate(Count(self.aggregatefield))
                self.data = self.data[aggregatefield+'__count']
            elif teamdetail != None and member != None:
                requestid = TblAssigneddetail.objects.filter(assignedtoid__in=[member]).values_list('requestid',flat=True)
                self.data = TblRequestdetail.objects.filter(requestraiseddate__range=(self.StartDate,self.EndDate)).filter(requestid__in=list(requestid)).aggregate(Count(self.aggregatefield))
                self.data = self.data[aggregatefield+'__count']

        elif report_choice == '2':
            if teamdetail == None and member == None:
                self.data = TblTimeTracker.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                self.data = TblTimeTracker.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).filter(teamid__in=[teamdetail]).aggregate(Count(self.aggregatefield))
            elif teamdetail != None and member != None:
                self.data = TblTimeTracker.objects.filter(trackingdatetime__range=(self.StartDate,self.EndDate)).filter(memberid__in=[member]).aggregate(Count(self.aggregatefield))

        elif report_choice == '3':
            if teamdetail == None and member == None:
                self.data = TblErrorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                memberid = TblMember.objects.filter(teamid__in=[teamdetail]).values_list('memberid',flat=True)
                self.data = TblErrorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=list(memberid)).aggregate(Count(self.aggregatefield))
            elif teamdetail != None and member != None:
                self.data = TblErrorlog.objects.filter(errorlog_date__range=(self.StartDate,self.EndDate)).filter(reportedtoid__in=[member]).all()
        elif report_choice == '4':
            if teamdetail == None and member == None:
                self.data = TblOtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).all()
            elif teamdetail != None and member == None:
                timetrackerid = TblTimeTracker.objects.filter(teamid__in=[teamdetail]).values_list('timetrackerid',flat=True)
                self.data = TblOtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).filter(timetrackerid__in=list(timetrackerid)).all()
            elif teamdetail != None and member != None:
                timetrackerid = TblTimeTracker.objects.filter(memberid__in=[member]).values_list('timetrackerid',flat=True)
                self.data = TblOtDetail.objects.filter(ot_startdatetime__range=(self.StartDate,self.EndDate)).filter(timetrackerid__in=list(timetrackerid)).all()
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
def filterbydaterange(request,variable_column=None,fromdate=None,todate=None):
    variable_column = variable_column
    filter = variable_column + '__range'
    return filter

@login_required
def calculation(request,datefield=None,model=None,values=None,fromdate=None,todate=None, field_name_list =None, value_list=None,aggregatefield=None,raw_data=None,calculation_type='sum'):
    filterdict = create_dict_for_filter(request,field_name_list = field_name_list ,value_list = value_list)
    #print(filterdict)
    if calculation_type == 'sum':
        aggregation = Sum(aggregatefield)
        type = '__sum'
    elif calculation_type == 'count':
        aggregation = Count(aggregatefield)
        type = '__count'

    if fromdate != None and todate != None:
        filter =  filterbydaterange(request,variable_column=datefield,fromdate=fromdate,todate=todate)
        daterange = [fromdate,todate]
        if raw_data == 'Y':
            data = model.filter(**{filter: daterange}).filter(**(filterdict)).aggregate(aggregation)
        elif raw_data == 'N':
            data = model.filter(**{filter: daterange}).filter(**(filterdict)).values(values).aggregate(aggregation)
            data = data[aggregatefield + type]
            data = 0 if data == None else data
    else:
        if raw_data == 'Y':
            data = model.filter(**(filterdict))
        elif raw_data == 'N':
            data = model.filter(**(filterdict)).values(values).aggregate(aggregation)
            data = data[aggregatefield + type]
            data = 0 if data == None else data
    return data

def hours_min(request,time_in_min=None,date=None,dict=None):
    key = []
    value = []
    #print(time_in_min)
    hours = 0.00 if time_in_min == 0 else time_in_min/60
    min = 0.00 if time_in_min == 0 else time_in_min % 60
    if  len(str(hours).split('.')[0]) <= 1:
        time = str(hours).split('.')[0].zfill(2)  + ":" +  str(min).split('.')[0].zfill(2)
    else:
        time = str(hours).split('.')[0].zfill(2)  + ":" + str(min).split('.')[0].zfill(2)
    if dict == None:
        key.append(str(date))
        value.append(str(time))
        result = OrderedDict(zip(key,value))
    else:
        result = time
    return result


@login_required
def TimeTracker_View(request):
    view_header, view_footer =  'timetracker', 'timetracker'
    template = 'CentralMI/8a_tracker_view.html'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    starttime = request.POST.get('startdatetime')
    stoptime = request.POST.get('stopdatetime')
    userid = User.objects.get(username__in=[username]).id
    memberid = TblMember.objects.get(userid__in=[userid]).memberid
    teamid = TblMember.objects.get(userid__in=[userid]).teamid
    dv_value = calculation(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',field_name_list = ['memberid','teamid','subcategoryid__core_noncore'], value_list = [memberid,teamid,None] ,values='memberid',aggregatefield='totaltime',fromdate=sd,todate=sd,raw_data='N')
    dvcore_value = calculation(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',field_name_list = ['memberid','teamid','subcategoryid__core_noncore'], value_list = [memberid,teamid,'core'] ,values='memberid',aggregatefield='totaltime',fromdate=sd,todate=sd,raw_data='N')
    dvOT_value = calculation(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'core','accepted'] ,values='timetrackerid__memberid',aggregatefield='ot_time',fromdate=sd,todate=sd,raw_data='N')
    total_core_value = dvcore_value + dvOT_value
    dvAll_value = dv_value + dvOT_value

    dv = hours_min(request,time_in_min=dv_value,date=sd)
    dvOT = hours_min(request,time_in_min=dvOT_value,date=sd)
    dvcore = hours_min(request,time_in_min=dvcore_value,date=sd)
    dvAll = hours_min(request,time_in_min=dvAll_value,date=sd)
    checkhalfday = TblLeaveRecord.objects.filter(userid__userid__username__in=[username]).filter(leave_date__in=[sd]).filter(leave_type__in=[2,4,6]).count()
    checkfulday = TblLeaveRecord.objects.filter(userid__userid__username__in=[username]).filter(leave_date__in=[sd]).filter(leave_type__in=[1,3,5,6,7]).count()
    msg1 = "You cannot fill today's data in time tracker, as you have marked yourself on leave" if checkfulday == 1 else  "ok"
    msg3 = "Hours cannot be more than 24 hrs " if dv_value <= 1440 else  "ok"

    if checkhalfday == 1:
        totaltimeindays = 210
        daystype = "H"
    elif checkfulday == 1:
        totaltimeindays = 0
        daystype = "L"
    else:
        totaltimeindays = 420
        daystype = "F"

    utiliationtext = 'Util.(B+D/' + str(totaltimeindays) + '+B)'
    dvutilisation = 0.00 if dvcore_value == 0 and dvAll_value == 0 else ((total_core_value / (totaltimeindays + dvOT_value)) * 100)
    dvutilisation = round(dvutilisation,2)
    requestid_onassign = TblAssigneddetail.objects.filter(assignedtoid__in=[memberid]).values_list('requestid',flat=True).distinct()
    requestid_onstatus = TblRequeststatusdetail.objects.filter(statusid__in=[4,5,6,7,8]).values_list('requestid',flat=True).distinct()
    requestid_filter = TblRequestdetail.objects.filter(requestid__in=list(requestid_onassign)).filter(requestid__in=list(requestid_onstatus)).values_list('requestid',flat=True).distinct()
    form = TimetrackersForm(initial={'memberid':memberid,'teamid':teamid,'options':2,'trackingdatetime':sd,'startdatetime':starttime,'stopdatetime':stoptime})
    form.fields['requestid'].queryset = TblRequestdetail.objects.filter(requestid__in=requestid_filter)
    form.fields['activityid'].queryset = TblActivity.objects.all()
    model = TblTimeTracker.objects.exclude(valid_invalid__in=[2]).filter(trackingdatetime__in=[sd]).filter(memberid__userid__username__in=[username])
    if checkfulday == 0 and dv_value <= 1440:
        if request.method == 'POST':
            form = TimetrackersForm(request.POST)
            form.fields['requestid'].queryset = TblRequestdetail.objects.filter(requestid__in=requestid_filter)
            form.fields['activityid'].queryset = TblActivity.objects.all()
            if form.is_valid():
                inst = form.save(commit=False)
                inst.memberid
                form = TimetrackersForm(initial={'memberid':memberid,'teamid':teamid,'options':2,'trackingdatetime': sd,'startdatetime':starttime,'stopdatetime':stoptime})
                model = TblTimeTracker.objects.exclude(valid_invalid__in=[2]).filter(trackingdatetime__in=[sd]).filter(memberid__userid__username__in=[username])
                inst.save()
                form = TimetrackersForm(initial={'memberid':memberid,'teamid':teamid,'options':2,'trackingdatetime': sd,'startdatetime':starttime,'stopdatetime':stoptime})
                form.fields['requestid'].queryset = TblRequestdetail.objects.filter(requestid__in=requestid_filter)
                form.fields['activityid'].queryset = TblActivity.objects.all()
                model = TblTimeTracker.objects.exclude(valid_invalid__in=[2]).filter(trackingdatetime__in=[sd]).filter(memberid__userid__username__in=[username])
                dv_value = calculation(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',field_name_list = ['memberid','teamid','subcategoryid__core_noncore'], value_list = [memberid,teamid,None] ,values='memberid',aggregatefield='totaltime',fromdate=sd,todate=sd,raw_data='N')
                dvcore_value = calculation(request,model=TblTimeTracker.objects.exclude(valid_invalid__in=[2]),datefield='trackingdatetime',field_name_list = ['memberid','teamid','subcategoryid__core_noncore'], value_list = [memberid,teamid,'core'] ,values='memberid',aggregatefield='totaltime',fromdate=sd,todate=sd,raw_data='N')
                dvOT_value = calculation(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'core','accepted'] ,values='timetrackerid__memberid',aggregatefield='ot_time',fromdate=sd,todate=sd,raw_data='N')
                total_core_value = dvcore_value + dvOT_value
                dvAll_value = dv_value + dvOT_value
                dv = hours_min(request,time_in_min=dv_value,date=sd)
                dvOT = hours_min(request,time_in_min=dvOT_value,date=sd)
                dvcore = hours_min(request,time_in_min=dvcore_value,date=sd)
                dvAll = hours_min(request,time_in_min=dvAll_value,date=sd)
                dvutilisation = 0.00 if dvcore_value == 0 and dvAll_value == 0 else ((total_core_value / (totaltimeindays + dvOT_value)) * 100)
                dvutilisation = round(dvutilisation,2)
                msg2 = "ok"
                msg1 = "ok"
                context = {'form':form,'model':model, 'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'utiliationtext':utiliationtext, 'daystype':daystype,'msg2':msg2,'msg1':msg1,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
                return render(request, template,context )
            else:
                msg2 = "Category, SubCategory and Totaltime cannot be blank"
                context = {'form':form,'model':model,'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'utiliationtext':utiliationtext, 'daystype':daystype,'msg2':msg2,'msg1':msg1,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
                return render(request, template, context)
        else:
            msg2 = "ok"
            context = {'form':form,'model':model,'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'msg1':msg1,'utiliationtext':utiliationtext, 'daystype':daystype,'msg2':msg2,'msg1':msg1,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
            return render(request, template, context)
    context = {'form':form,'model':model,'username':username,'dv':dv,'dvOT':dvOT,'dvAll':dvAll,'dvcore':dvcore,'dvutilisation':dvutilisation,'activetab':activetab,'activetab1':activetab1,'group_name':group_name,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'msg1':msg1,'utiliationtext':utiliationtext, 'daystype':daystype,'can_edit':can_edit, 'can_view':can_view, 'can_delete':can_delete, 'can_add':can_add}
    return render(request, template, context)

@login_required
def Tracker_Edit_Form(request,requestid):
    view_header, view_footer =  'timetracker', 'timetracker'
    title = 'Edit Tracker'
    template = 'CentralMI/form_template.html'
    redirect_url = 'timetracker'
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblTimeTracker.objects.get(pk=requestid)
    model = TblTimeTracker.objects.filter(pk=requestid)
    form = TimetrackersForm(instance=e)
    if request.method == 'POST':
        e = TblTimeTracker.objects.get(pk=requestid)
        form = TimetrackersForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'model':model, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'reverseid':requestid,'redirect_url':redirect_url}
    return render(request, template, context)


@login_required
def Ot_Edit_Form(request,requestid):
    view_header, view_footer =  'timetracker', 'otdetail'
    template = 'CentralMI/form_template.html'
    redirect_url = view_footer
    group_name, activetab, activetab1, username, info, sd, header_navbar_list, footer_navbar_list,can_edit, can_view, can_delete, can_add,template,template_type,individual_view, team_view, bu_view,user_id,team_id,bu_id = session_navbar_permission(request,view_header=view_header,view_footer=view_footer,template=template)
    e = TblOtDetail.objects.get(pk=requestid)
    model = TblOtDetail.objects.filter(pk=requestid)
    form = OtDetailForm(instance=e)
    if request.method == 'POST':
        e = TblOtDetail.objects.get(pk=requestid)
        form = OtDetailForm(request.POST, instance=e)
        if form.is_valid():
            inst = form.save(commit=True)
            inst.save()
            return HttpResponseRedirect(reverse(view_footer))
    context = {'form':form,'model':model, 'username':username,'activetab':activetab,'header_navbar_list':header_navbar_list,'footer_navbar_list':footer_navbar_list,'redirect_url':redirect_url}
    return render(request, template, context)

@login_required
def Load_Datevalues(request):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    memberid = User.objects.get(username=username).id
    model = TblTimeTracker.objects.filter(memberid__in=[memberid]).filter(trackingdatetime=sd)
    return render(request, 'CentralMI/13b_rebuilding_datevalues.html', {'model': model,'activetab':activetab})

@login_required
def Load_Subcategories(request):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    category_id = request.GET.get('categories')
    print(category_id)
    subcategories = TblSubcategoryMaster.objects.filter(categorysid=category_id)
    activities = TblActivity.objects.filter(requestcategorys=category_id)
    print(subcategories)
    return render(request, 'CentralMI/13d_rebuilding_subcategories.html', {'subcategories': subcategories,'activities':activities,'activetab':activetab})


def Load_view(request):
    activetab, activetab1, username, info, sd = create_session(request,  header='home',footer='')
    group_name = is_group(request,username=username)

    try:
        view_value_radio = request.GET.get('radioValue')
        #print(view_value_radio)
        if view_value_radio == None:
            request.session['view_value_session'] == 'myview'
        else:
            request.session['view_value_session'] = view_value_radio
        view_value = request.session.get('view_value_session')
    except:
        view_value = 'myview'
    if view_value == 'myview':
        session_userid = User.objects.get(username=username).id
        session_teamid = TblMember.objects.get(userid=session_userid).teamid
        session_memberid = TblMember.objects.get(userid=session_userid).memberid
    elif view_value == 'teamview':
        session_userid = User.objects.get(username=username).id
        session_teamid = TblMember.objects.get(username=session_userid).teamid
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
        activities = TblActivity.objects.filter(requestcategorys=category_id)
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
        try:
            lengthofusername = len(username)
            username_exist = User.objects.filter(username__in=[username]).exists()
            active_field = 1
        except:
            username_exist = None
            lengthofusername = None
        try:
            lengthofemail = len(emailid)
            email_exist = User.objects.filter(email__in=[emailid]).exists()
            active_field = 2
        except:
            lengthofemail = None
            email_exist = None
        try:
            lengthofpassword = len(passwordagain)
            password_match = True if passwordagain == password else False
            active_field = 3
        except:
            lengthofpassword = None
            password_match = None
        return render(request, 'CentralMI/1c_username_check.html', {'active_field':active_field,'username_exist':username_exist,'lengthofusername':lengthofusername,'email_exist':email_exist,'lengthofemail':lengthofemail,'password_match':password_match,'lengthofpassword':lengthofpassword})
    except:
        pagename = "report"
        errormsg1 = "Something went Wrong"
        return render(request, 'CentralMI/15a_ErrorPage.html',{'username':username,'pagename':pagename,'errormsg1':errormsg1})


@login_required
def Load_Mimember(request):
    team_id = request.GET.get('team_id')
    member_id = request.GET.get('member_id')
    members = TblMember.objects.filter(teamid__in=[team_id])
    print(team_id)
    print(member_id)
    return render(request, 'CentralMI/13c_rebuilding_mimember.html', {'members': members,'member_id':str(member_id)})


@login_required
def Load_Tables(request):
    activetab, activetab1, username, info, sd = create_session(request, header='timetracker',footer='timetracker')
    memberid = User.objects.get(username=username).id
    form = TimetrackersForm(initial={'trackingdatetime':sd})
    model = TblTimetracker.objects.filter(memberid__in=[memberid])
    return render(request, 'CentralMI/13e_rebuilding_tables.html', {'form':form,'model': model,'activetab':activetab})



#--------------------------------------Data Data_Analysis-------------------------------
@login_required
def start_end_date(request,model=None,datefield=None,sd=None,values=None,aggregate=None,field_name_list=None,value_list=None,days_range=None,range_type=None,year_range=0,type=None,memberid=None,teamid=None,no_of_member=None,averagetime=None,calculation_type='sum',LeaverecordCount=None):
    key = []
    value = []
    cumulativedays = 0
    currentreviseddate = '2018-01-01'
    for i in range(days_range):
        currentdate = datetime.today()
        cd = datetime.strftime(currentdate, '%y/%m/%d')
        cd  = datetime.strptime(cd, '%y/%m/%d')
        if range_type == None:
            No_of_days = i
        elif range_type == 'setdate':
            daystoloop = 1
            if sd != None:
                StartDate = sd
                EndDate  =  sd
            else:
                StartDate = currentdate
                EndDate  = currentdate
            date1 = ''
        elif range_type == 'Daily':
            daystoloop = 1
            No_of_days = i
            StartDate = cd - timedelta(days=No_of_days)
            EndDate  = StartDate
            currentyear = datetime.strftime(StartDate, '%Y')
            currentmonth = datetime.strftime(StartDate, '%m')
            currentdays = datetime.strftime(StartDate, '%d')
            date1 = date(int(currentyear),int(currentmonth),int(currentdays))
        elif range_type == 'Weekly':
            daystoloop = 7
            days = 7
            No_of_days = (7 * i)
            Start = cd - timedelta(days=cd.weekday())
            StartDate = Start - timedelta(days=No_of_days)
            EndDate  = StartDate  + timedelta(days=(days-1))
            currentyear = datetime.strftime(StartDate, '%Y')
            currentmonth = datetime.strftime(StartDate, '%m')
            currentdays = datetime.strftime(StartDate, '%d')
            date1 = date(int(currentyear),int(currentmonth),int(currentdays))
        elif range_type == 'Monthly':
            if currentreviseddate == '2018-01-01':
                currentmonth = datetime.strftime(currentdate, '%m')
                currentyear = datetime.strftime(currentdate, '%Y')
                currentreviseddate = currentdate
            else:
                currentmonth = datetime.strftime(currentreviseddate, '%m')
                currentyear = datetime.strftime(currentreviseddate, '%Y')
            month  = int(currentmonth)
            year  = int(currentyear)
            No_of_daystest = calendar.monthrange(year,month)[1]
            currentdays = datetime.strftime(currentdate, '%d')
            dateforstartofmonth = (str(year)+"-"+str(month)+"-1")
            dateforstartofmonth = datetime.strptime(dateforstartofmonth, '%Y-%m-%d')
            StartDate = dateforstartofmonth
            EndDate = dateforstartofmonth + timedelta(days=(No_of_daystest-1))
            month = str("0")+str(month) if month <= 9 else str(month)
            date1 = str(str(year) + "-" +str(month))
            currentreviseddate = currentreviseddate - timedelta(days=(No_of_daystest))
        if type == None:
            data = calculation(request,model=model,datefield=datefield,field_name_list = field_name_list, value_list = value_list ,values=values,aggregatefield=aggregate,fromdate=StartDate,todate=EndDate,raw_data='N')
            v = hours_min(request,time_in_min=data,date=sd,dict="Yes")
            key.append(str(date1))
            value.append(str(v))
            result = OrderedDict(zip(key, value))
        elif type == "coreandot":
            core = calculation(request,model=model,datefield=datefield,field_name_list = field_name_list, value_list = value_list ,values=values,aggregatefield=aggregate,fromdate=StartDate,todate=EndDate,raw_data='N')
            core_ot = calculation(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'Core','Accepted'],values='timetrackerid__memberid',aggregatefield='ot_time',fromdate=StartDate,todate=EndDate,raw_data='N')
            total_core = core + core_ot
            v = hours_min(request,time_in_min=total_core,date=sd,dict="Yes")
            key.append(str(date1))
            value.append(str(v))
            result = OrderedDict(zip(key, value))
        elif type == "utilisation":
            utilisation_list = [memberid,teamid,None]
            core = calculation(request,model=model,datefield=datefield,field_name_list = field_name_list, value_list = value_list ,values=values,aggregatefield=aggregate,fromdate=StartDate,todate=EndDate,raw_data='N')
            core_ot = calculation(request,model=TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]),datefield='timetrackerid__trackingdatetime',field_name_list = ['timetrackerid__memberid','timetrackerid__teamid','timetrackerid__subcategoryid__core_noncore','statusid__ot_status'], value_list = [memberid,teamid,'Core','Accepted'],values='timetrackerid__memberid',aggregatefield='ot_time',fromdate=StartDate,todate=EndDate,raw_data='N')
            total_core = core + core_ot
            total = calculation(request,model=model,datefield=datefield,field_name_list = field_name_list, value_list = utilisation_list  ,values=values,aggregatefield=aggregate,fromdate=StartDate,todate=EndDate,raw_data='N')
            totalcoreot = (total + core_ot)
            no_of_member = 1 if no_of_member == 0 else no_of_member
            halfdaycode = 2,4,6
            fulldaycode = 1,3,5,7,8
            leave_halfday = calculation(request,model=TblLeaveRecord.objects.all(),datefield='leave_date',field_name_list = ['userid__memberid','userid__teamid','leave_type'], value_list = [memberid,teamid,halfdaycode],values='userid',aggregatefield='userid',fromdate=StartDate,todate=EndDate,raw_data='N',calculation_type='count')
            leave_fullday = calculation(request,model=TblLeaveRecord.objects.all(),datefield='leave_date',field_name_list = ['userid__memberid','userid__teamid','leave_type'], value_list = [memberid,teamid,fulldaycode],values='userid',aggregatefield='userid',fromdate=StartDate,todate=EndDate,raw_data='N',calculation_type='count')
            reduce_time = (leave_halfday * (420/2)) +  (leave_fullday * (420))
            try:
                v = round((total_core/(((no_of_member * averagetime) - reduce_time) + core_ot)) * 100,2)
                v = v if v != 0.0 else '00.00'
                v = "0"+str(v) if str(v).find('.') == 1 else str(v)

                #print(position)

            except:
                v = '00.00'
            key.append(str(date1))
            value.append(str(v))

            result = OrderedDict(zip(key, value))
        elif type == "error":
            data = calculation(request,model=model,datefield=datefield,field_name_list = field_name_list, value_list = value_list ,values=values,aggregatefield=aggregate,fromdate=StartDate,todate=EndDate,raw_data='N')
        #    v = hours_min(request,time_in_min=data,date=sd,dict="Yes")
            key.append(str(date1))
            value.append(str(data))
            result = OrderedDict(zip(key, value))
    return result



@login_required
def data_formation_Timetracker(request,startdate=None,enddate=None,team=None,member=None):
    filter_dict = create_dict_for_filter(request,field_name_list = ['teamid__teamname','memberid__userid__username'],value_list = [team,member])
    countofdata = TblTimeTracker.objects.filter(trackingdatetime__range=[startdate,enddate]).filter(**filter_dict).count()
    if countofdata > 0:
        df1 = pd.DataFrame(list(TblTimeTracker.objects.filter(trackingdatetime__range=[startdate,enddate]).filter(**filter_dict).values()))
        df2 = pd.DataFrame(list(TblMember.objects.all().values()))
        df3 = pd.DataFrame(list(TblTeamMaster.objects.all().values()))
        df4 = pd.DataFrame(list(AuthUser.objects.all().values()))
        df5 = pd.DataFrame(list(Requestcategorys.objects.all().values()))
        df6 = pd.DataFrame(list(TblSubcategoryMaster.objects.all().values()))
        df_merge1 = pd.merge(df1, df2,  how='left', left_on=['mimember_id'], right_on = ['memberid'])
        df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['teamdetail_id_y'], right_on = ['teamid'])
        df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['username_id'], right_on = ['id'])
        df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['requestcategorys_id'], right_on = ['requestcategoryid'])
        df_merge5 = pd.merge(df_merge4, df6,  how='left', left_on=['requestsubcategory_id'], right_on = ['requestsubcategoryid'])
        df_merge5['trackingdatetime'] = df_merge5['trackingdatetime'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
        df_merge5['trackingdatetime_monthyear'] = df_merge5['trackingdatetime'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
        df_merge5['trackingdatetime_week'] = df_merge5['trackingdatetime'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
        data = df_merge5
    else:
        data = 'Data Not Available'
    return data, countofdata

def Timetrcker_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    data, countofdata = data_formation_Timetracker(request,startdate=startdate,enddate=enddate,team=team,member=member)
    if countofdata > 0:

        data = data[data['teamname']==team] if team != 'None' else data
        data = data[data['username']==member] if member != 'None' else data
        print(type(data))
        if interval == 'Daily':
            if view == "core_noncore":
                pivot_daily_corenoncore = pd.pivot_table(data,index=['trackingdatetime', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
                exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
                #print(exportdata.head(5))
                data = pivot_daily_corenoncore.to_html(classes="table cell-border")
            elif view == "activity":
                pivot_daily_corenoncore = pd.pivot_table(data,index=['requestcategorys','requestsubcategory'], columns='username', values='totaltime',aggfunc=sum)
                exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
                data = pivot_daily_corenoncore.to_html(classes="table cell-border")
        elif  interval == 'Monthly':
            if view == "core_noncore":
                pivot_monthly_corenoncore = pd.pivot_table(data,index=['trackingdatetime_monthyear', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
                exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
                data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
            elif view == "activity":
                pivot_monthly_corenoncore = pd.pivot_table(data,index=['requestcategorys'], columns='username', values='totaltime',aggfunc=sum)
                exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
                data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
        elif  interval == 'Weekly':
            if view == "core_noncore":
                pivot_weekly_corenoncore = pd.pivot_table(data,index=['trackingdatetime_week', 'core_noncore'], columns='username', values='totaltime',aggfunc=sum).unstack('core_noncore')
                exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
                data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
            elif view == "activity":
                pivot_weekly_corenoncore = pd.pivot_table(data,index=['requestcategorys'], columns='username', values='totaltime',aggfunc=sum)
                exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
                data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
    else:
        data = "Data Not Available"
    return data
@login_required
def data_formation_ot(request,startdate=None,enddate=None,team=None,member=None):
    filter_dict = create_dict_for_filter(request,field_name_list = ['timetrackerid__teamid__teamname','timetrackerid__memberid__userid__username'],value_list = [team,member])
    countofdata = TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]).filter(ot_startdatetime__range=[startdate,enddate]).filter(**filter_dict).count()
    if countofdata > 0:
        df1 = pd.DataFrame(list(TblOtDetail.objects.exclude(timetrackerid__valid_invalid__in=[2]).filter(ot_startdatetime__range=[startdate,enddate]).filter(**filter_dict).values()))
        df2 = pd.DataFrame(list(TblTimeTracker.objects.exclude(valid_invalid__in=[2]).values()))
        df3 = pd.DataFrame(list(TblMember.objects.all().values()))
        df4 = pd.DataFrame(list(TblTeamMaster.objects.all().values()))
        df5 = pd.DataFrame(list(AuthUser.objects.all().values()))
        df_merge1 = pd.merge(df1, df2,  how='left', left_on=['timetrackers_id'], right_on = ['timetrackerid'])
        df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['mimember_id'], right_on = ['memberid'])
        df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['teamdetail_id_y'], right_on = ['teamid'])
        df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['username_id'], right_on = ['id'])
        df_merge4['ot_startdatetime'] = df_merge4['ot_startdatetime'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
        df_merge4['ot_startdatetime_monthyear'] = df_merge4['ot_startdatetime'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
        df_merge4['ot_startdatetime_week'] = df_merge4['ot_startdatetime'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
        data = df_merge4
    else:
        data = 'Data Not Available'
    return data, countofdata

@login_required
def Ot_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    data, countofdata  = data_formation_ot(request,startdate=startdate,enddate=enddate,team=team,member=member)
    if countofdata > 0:
        data = data[data['teamname']==team] if team != 'None' else data
        data = data[data['username']==member] if member != 'None' else data
        if interval == 'Daily':
            pivot_daily_corenoncore = pd.pivot_table(data,index=['ot_startdatetime'], columns='username', values='ot_time',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_daily_corenoncore.reset_index())
            data = pivot_daily_corenoncore.to_html(classes="table cell-border")
        elif  interval == 'Monthly':
            pivot_monthly_corenoncore = pd.pivot_table(data,index=['ot_startdatetime_monthyear'], columns='username', values='ot_time',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_monthly_corenoncore.reset_index())
            data = pivot_monthly_corenoncore.to_html(classes="table cell-border")
        elif  interval == 'Weekly':
            pivot_weekly_corenoncore = pd.pivot_table(data,index=['ot_startdatetime_week'], columns='username', values='ot_time',aggfunc=sum)
            exportdata = pd.DataFrame(pivot_weekly_corenoncore.reset_index())
            data = pivot_weekly_corenoncore.to_html(classes="table cell-border")
    else:
        data = "Data Not Available"
    return data

@login_required
def data_formation_error(request,startdate=None,enddate=None,team=None,member=None):
    filter_dict = create_dict_for_filter(request,field_name_list = ['reportedtoid__teamdetail__teamname','reportedtoid__username__username'],value_list = [team,member])
    countofdata = TblErrorlog.objects.filter(errorlog_date__range=[startdate,enddate]).filter(**filter_dict).count()
    if countofdata > 0:
        df1 = pd.DataFrame(list(TblErrorlog.objects.filter(errorlog_date__range=[startdate,enddate]).filter(**filter_dict).values()))
        df2 = pd.DataFrame(list(TblActivity.objects.all().values()))
        df3 = pd.DataFrame(list(TblMember.objects.all().values()))
        df4 = pd.DataFrame(list(TblTeamMaster.objects.all().values()))
        df5 = pd.DataFrame(list(AuthUser.objects.all().values()))
        df_merge1 = pd.merge(df1, df2,  how='left', left_on=['error_report_id'], right_on = ['activityid'])
        df_merge2 = pd.merge(df_merge1, df3,  how='left', left_on=['reportedtoid_id'], right_on = ['memberid'])
        df_merge3 = pd.merge(df_merge2, df4,  how='left', left_on=['teamdetail_id'], right_on = ['teamid'])
        df_merge4 = pd.merge(df_merge3, df5,  how='left', left_on=['username_id'], right_on = ['id'])
        df_merge4['errorlog_date'] = df_merge4['errorlog_date'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m/%d'),'%y/%m/%d'))
        df_merge4['errorlog_date_monthyear'] = df_merge4['errorlog_date'].apply(lambda x:
                                        dt.datetime.strptime(dt.datetime.strftime(x,'%y/%m'),'%y/%m'))
        df_merge4['errorlog_date_week'] = df_merge4['errorlog_date'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
        data = df_merge4
    else:
        data = 'Data Not Available'
    return data, countofdata

def Error_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    data, countofdata = data_formation_error(request,startdate=startdate,enddate=enddate,team=team,member=member)
    if countofdata > 0:
        data = data[data['teamname']==team] if team != 'None' else data
        data = data[data['username']==member] if member != 'None' else data

        if interval == 'Daily':
            if view == 'erroruserwise':
                pivot_daily_userwise = pd.pivot_table(data,index=['errorlog_date'], columns='username', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_daily_userwise.reset_index())
                data = pivot_daily_userwise.to_html(classes="table cell-border")
            elif view == 'errorreportwise':
                pivot_daily_userwise = pd.pivot_table(data,index=['errorlog_date'], columns='name', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_daily_userwise.reset_index())
                data = pivot_daily_userwise.to_html(classes="table cell-border")
        elif  interval == 'Monthly':
            if view == 'erroruserwise':
                pivot_monthly_userwise = pd.pivot_table(data,index=['errorlog_date_monthyear'], columns='username', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
                data = pivot_monthly_userwise.to_html(classes="table cell-border")
            elif view == 'errorreportwise':
                pivot_monthly_userwise = pd.pivot_table(data,index=['errorlog_date_monthyear'], columns='name', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
                data = pivot_monthly_userwise.to_html(classes="table cell-border")
        elif  interval == 'Weekly':
            if view == 'erroruserwise':
                pivot_monthly_userwise = pd.pivot_table(data,index=['errorlog_date_week'], columns='username', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
                data = pivot_monthly_userwise.to_html(classes="table cell-border")
            elif view == 'errorreportwise':
                pivot_monthly_userwise = pd.pivot_table(data,index=['errorlog_date_week'], columns='name', values='reportedtoid_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_userwise.reset_index())
                data = pivot_monthly_userwise.to_html(classes="table cell-border")
    else:
        data = "Data Not Available"
    return data

@login_required
def data_formation_workflow(request,startdate=None,enddate=None,team=None,member=None):
    countofdata = TblRequestdetail.objects.filter(requestraiseddate__range=[startdate,enddate]).count()
    if countofdata > 0:
        df01 = pd.DataFrame(list(TblRequestdetail.objects.filter(requestraiseddate__range=[startdate,enddate]).values()))
        df02 = pd.DataFrame(list(TblAuthorisedetail.objects.all().values()))
        df03 = pd.DataFrame(list(TblAssigneddetail.objects.all().values()))
        df04 = pd.DataFrame(list(TblOverviewdetail.objects.all().values()))
        df05 = pd.DataFrame(list(TblEstimationdetail.objects.all().values()))
        df06 = pd.DataFrame(list(TblAcceptrejectdetail.objects.all().values()))
        df08 = pd.DataFrame(list(TblPriorityMaster.objects.all().values()))
        df09 = pd.DataFrame(list(TblRequesttypeMaster.objects.all().values()))
        df10 = pd.DataFrame(list(TblMember.objects.all().values()))
        df11 = pd.DataFrame(list(AuthUser.objects.all().values()))
        df12 = pd.DataFrame(list(TblTeamMaster.objects.all().values()))
        df_merge1 = pd.merge(df01, df02,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
        df_merge2 = pd.merge(df_merge1, df03,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
        df_merge3 = pd.merge(df_merge2, df04,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
        df_merge4 = pd.merge(df_merge3, df05,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
        df_merge5 = pd.merge(df_merge4, df06,  how='left', left_on=['requestid'], right_on = ['requestdetail_id'])
        df_merge7 = pd.merge(df_merge5, df08,  how='left', left_on=['prioritydetail_id'], right_on = ['requestpriorityid'])
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
        df_merge11['requestraised_week'] = df_merge11['requestraiseddate'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
        df_merge11['assigneddate_week'] = df_merge11['assigneddate'].apply(lambda x: x - timedelta(days=x.weekday()) if pd.notnull(x) else None)
        data = df_merge11
    else:
        data =  'Data Not Available'
    return data , countofdata

@login_required
def Workflow_Summary(request,startdate=None,enddate=None,interval=None,view=None,team=None,member=None):
    global exportdata
    data, countofdata = data_formation_workflow(request,startdate=startdate,enddate=enddate,team=team,member=member)
    if countofdata > 0:
        data = data[data['teamname']==team] if team != 'None' else data
        data = data[data['username']==member] if member != 'None' else data
        if interval == 'Daily':
            if view == "requesttype":
                pivot_daily_type = pd.pivot_table(data,index=['requestraiseddate'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_daily_type.reset_index())
                data = pivot_daily_type.to_html(classes="table cell-border")
            elif view == "requestpriority":
                pivot_daily_priority = pd.pivot_table(data,index=['requestraiseddate'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_daily_priority.reset_index())
                data = pivot_daily_priority.to_html(classes="table cell-border")
            elif view == "requestassigned":
                pivot_daily_assigned = pd.pivot_table(data,index=['assigneddate'], columns='assignedto_id', values='assignedid',aggfunc=len)
                exportdata = pd.DataFrame(pivot_daily_assigned.reset_index())
                data = pivot_daily_assigned.to_html(classes="table cell-border")
        elif  interval == 'Monthly':
            if view == "requesttype":
                pivot_monthly_type = pd.pivot_table(data,index=['requestraised_monthyear'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_type.reset_index())
                data = pivot_monthly_type.to_html(classes="table cell-border")
            elif view == "requestpriority":
                pivot_monthly_priority = pd.pivot_table(data,index=['requestraised_monthyear'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_priority.reset_index())
                data = pivot_monthly_priority.to_html(classes="table cell-border")
            elif view == "requestassigned":
                pivot_monthly_assigned = pd.pivot_table(data,index=['assigneddate_monthyear'], columns='assignedto_id', values='assignedid',aggfunc=len)
                exportdata = pd.DataFrame(pivot_monthly_assigned.reset_index())
                data = pivot_monthly_assigned .to_html(classes="table cell-border")
        elif  interval == 'Weekly':
            if view == "requesttype":
                pivot_weekly_type = pd.pivot_table(data,index=['requestraised_week'], columns='requesttype', values='requesttypedetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_weekly_type.reset_index())
                data = pivot_weekly_type.to_html(classes="table cell-border")
            elif view == "requestpriority":
                pivot_weekly_priority = pd.pivot_table(data,index=['requestraised_week'], columns='requestpriority', values='prioritydetail_id',aggfunc=len)
                exportdata = pd.DataFrame(pivot_weekly_priority.reset_index())
                data = pivot_weekly_priority.to_html(classes="table cell-border")
            elif view == "requestassigned":
                pivot_weekly_assigned = pd.pivot_table(data,index=['assigneddate_week'], columns='assignedto_id', values='assignedid',aggfunc=len)
                exportdata = pd.DataFrame(pivot_weekly_assigned.reset_index())
                data = pivot_weekly_assigned .to_html(classes="table cell-border")
    else:
        data = 'Data Not Available'
    return data
