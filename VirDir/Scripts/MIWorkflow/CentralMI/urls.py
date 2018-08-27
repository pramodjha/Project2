from django.conf.urls import include,url
from . import views

urlpatterns = [
# 1) Credential
	url(r'^signup_view/', views.Sign_Up_View, name='signup'),
    url(r'^signin_view/', views.Sign_In_View, name='signin'),
	url(r'^signout/', views.Sign_Out, name='signout'),
# 2) Home
	url(r'^$',views.Index, name = 'home'),

# 3) About us
	url(r'^about_team_view/',views.About_Team_View, name = 'aboutteam'),
	url(r'^what_we_do_view/',views.What_We_Do_View, name = 'whatwedo'),
	url(r'^governance_process_view/',views.Governance_Process_View, name = 'governanceprocess'),
	url(r'^success_stories_view/',views.Success_Stories_View, name = 'successstories'),
	url(r'^comm_sugg_view/',views.Comm_Sugg_View, name = 'commsugg'),
# 4) Workflow
	# View
	url(r'^request_view/',views.All_Request_View, name = 'allrequest'),
	url(r'^request_unapproved_view/',views.Unapproved_View, name = 'unapproved'),
	url(r'^request_approved_view/',views.Approved_View, name = 'approved'),
	url(r'^request_assigned_view/',views.Assigned_View, name = 'assigned'),
	url(r'^request_overview_view/',views.Overview_View, name = 'overview'),
	url(r'^request_estimate_view/',views.Estimate_View, name = 'estimate'),
	url(r'^request_wip_view/',views.Wip_View, name = 'wip'),
	url(r'^request_completed_view/',views.Completed_View, name = 'completed'),
	url(r'^request_rejected_view/',views.Rejected_View, name = 'rejected'),
	url(r'^check_status_view/',views.Check_Status_View, name = 'checkstatus'),
	url(r'^thankyou_view/(?P<requestid>\d+)$',views.Thank_You_Page_View, name = 'ty'),

	# form
	url(r'^request_form/',views.Request_Form, name = 'loginrequest'),
	url(r'^request_form/',views.Request_Form, name = 'addrequest'),
	url(r'^authorised_form/(?P<requestid>\d+)$',views.Authorised_Form, name = 'authform'),
	url(r'^assigned_form/(?P<requestid>\d+)$',views.Requestassigneddetail_Form, name = 'assignedform'),
	url(r'^overview_form/(?P<requestid>\d+)$',views.Overview_Form, name = 'overviewform'),
	url(r'^estimation_form/(?P<requestid>\d+)$',views.Estimation_Form, name = 'estimationform'),
	url(r'^estimation_acceptance_form/(?P<requestid>\d+)$',views.EstimationAcceptance_Form, name = 'estimationformar'),
	url(r'^completed_form/(?P<requestid>\d+)$',views.Completed_Form, name = 'completedform'),

# 5) Reports/Activity
	# Report
	url(r'^reports_detail_view/',views.Report_Detail_View, name = 'allreports'),
	url(r'^report_add_form/',views.Report_Add_Form, name = 'report'),
	url(r'^report_add_form/',views.Report_Add_Form, name = 'addreport'),
	url(r'^report_edit_form/(?P<requestid>\d+)$', views.Report_Edit_Form, name='editreport'),
	# Feedback
	url(r'^feedback_detail_view/',views.Feedback_Detail_View, name = 'feedbackdetail'),
	url(r'^feedback_question_view/(?P<activityid>\d+)$',views.Feedback_Question_View, name = 'viewfeedbackquestion'),
	url(r'^feedback_add_form/(?P<feedbackquestionid>\d+)$', views.Feedback_Add_Form, name='addfeedback'),
	url(r'^feedback_edit_form/(?P<feedbackid>\d+)$', views.Feedback_Edit_Form, name='editfeedback'),
	# Error log
	url(r'^error_detail_view/',views.Errorlog_Detail_View, name = 'errordetail'),
	url(r'^errorlog_add_form/(?P<reportid>\d+)$',views.Errorlog_Add_Form, name = 'errorlog'),
	url(r'^errorlog_edit_form/(?P<requestid>\d+)$', views.Errorlog_Edit_Form, name='editerrorlog'),

# 6) TimeTracker
	url(r'^sd/', views.setdate, name='sdate'),
	url(r'^tracker_view/', views.TimeTracker_View, name='timetracker'),
#	url(r'^tracker_view/', views.TimeTracker_View, name='tracker'),
	url(r'^tracker_edit_form/(?P<requestid>\d+)$', views.Tracker_Edit_Form, name='edittracker'),
	url(r'^ot_detail_view/',views.Ot_Detail_View, name = 'otdetail'),
	url(r'^ot_add_form/(?P<trackerid>\d+)$',views.Ot_Add_Form, name = 'otform'),
	url(r'^ot_edit_form/(?P<requestid>\d+)$', views.Ot_Edit_Form, name='editot'),
# 7) Employee Detail
	url(r'^staff_detail_view/',views.Staff_Detail_View, name = 'viewDetail'),
	url(r'^staff_edit_form/',views.Staff_Edit_Form, name = 'editstaffdetail'),
	url(r'^staff_edit_manager_form/(?P<id>\d+)$',views.Staff_Edit_Manager_Form, name = 'editstaffbymanager'),

# 8) Internal Task
	url(r'^internal_task_detail_view/',views.Internal_Task_Detail_View, name = 'internaltaskdetail'),
	url(r'^internal_task_add_form/',views.Internal_Task_Add_Form, name = 'addinternaltaskdetail'),
	url(r'^internal_task_edit_form/(?P<taskid>\d+)$',views.Internal_Task_Edit_Form, name = 'editinternaltaskdetail'),
	url(r'^internal_task_choice_view/(?P<taskid>\d+)$',views.Internal_Task_Choice_view, name = 'viewinternaltaskoption'),
	url(r'^internal_task_choice_add_form/(?P<taskid>\d+)$',views.Internal_Choice_Add_Form, name = 'addinternaltaskoption'),
	url(r'^internal_task_choice_edit_form/(?P<choiceid>\d+)$',views.Internal_Choice_Edit_Form, name = 'editinternaltaskoption'),
	url(r'^internal_task_and_choice_view/(?P<taskid>\d+)$',views.Internal_Task_And_Choice_View, name = 'internaltaskwithchoice'),
	url(r'^internal_task_and_choice_edit_form/(?P<taskstatusid>\d+)$',views.Internal_Task_And_Choice_Edit_Form, name = 'internaltaskwithchoiceedit'),
	url(r'^internal_task_completion_view/(?P<internaltaskid>\d+)$',views.Internal_Task_Completion_View, name = 'internaltaskcompetionview'),

#	url(r'^rupdate/(?P<requestid>\d+)$',views.RequestdetailUpdate, name = 'rupdate'),

# 9) Data Analysis
	url(r'^summary_tracker/',views.Summary_Tracker, name = 'summary'),
	url(r'^extract_data/',views.Filter_Data, name = 'extractdatafilter'),
	url(r'^extract_data1/',views.Filter_Data, name = 'extractdatafilter1'),

#### Ajax call
	url(r'^ajax/load-subcategories/', views.Load_Subcategories, name='ajax_load_subcategories'),
	url(r'^ajax/load-activity/', views.Load_Activity, name='ajax_load_activity'),
	url(r'^ajax/mimember_load_ajax/', views.Load_Mimember, name='ajax_load_mimember'),
	url(r'^ajax/load-datevalues/', views.Load_Datevalues, name='ajax_load_datavalues'),
	url(r'^ajax/load-tables/', views.Load_Tables, name='ajax_load_tables'),
	url(r'^ajax/load-signup/', views.Load_Signup, name='ajax_load_signup'),

## Export to excel
	url(r'^export_to_excel/', views.Workflow_Summary, name='exporttoexcel'),

# 10)
url(r'^request_type_view/', views.Requesttype_View, name='requesttype'),
url(r'^request_priority_view/', views.Requestpriority_View, name='requestpriority'),
url(r'^request_assign_view/', views.Requestassigned_View, name='requestassigned'),
url(r'^request_complete_view/', views.Requestcompleted_View, name='requestcompleted'),

# 11)
url(r'^Core_NonCore_view/', views.CoreNonCore_View, name='corenoncore'),
url(r'^activity_timetracker_view/', views.Activitytimetracker_View, name='activitytimetracker'),

# 12)
url(r'^ot_view/', views.Ot_View, name='otuserwise'),
url(r'^error_userwise_View/', views.Erroruserwise_View, name='erroruserwise'),
url(r'^Error_reportwise_View/', views.Errorreportwise_View, name='errorreportwise'),
url(r'^report_due/', views.report_due, name='reportdue'),
url(r'^add_to_timetracker/(?P<activityid>\d+)$', views.Add_To_Timetracker, name='addtotimetracker'),


 url(r'^export/csv/$', views.export_users_csv, name='export_users_csv'),
	]
