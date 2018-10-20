from django.contrib import admin
from .models import Acceptrejectdetail, Acceptrejectoption, Assigneddetail, Authorisedetail, Authoriserdetail, Completeddetail, Estimationdetail, Mimember, Options, Overviewdetail, Prioritydetail, Requestcategorys, Requestdetail, Requeststatusdetail, Requestsubcategory, Requesttypedetail, Statusdetail, Teamdetail, Timetrackers, Deliverydays, Frequency, Reports,Emaildetail,TimeDetail,Filteroption,Fielddetail, Errortype, Errorlog, Feedback, FeedbackQuestion, OtDetail, OtStatus,ReportType, Activitystatus,Designationmaster, Internaltask, Internaltaskstatus, Internaltaskchoice,Whatwedo, Reply, Suggestion, Governance, SuccessStories, TblNavbarFooterMaster, TblNavbarHeaderMaster, TblNavbarMaster, TblLeaveRecord, TblLeaveType,TblAppreciation, TblRawActivityDetail, TblRawScore, TblRawTeamMaster,TblRawTeamMemberMaster,TblTeamMetrics,TeamMetrics, TblRawScore, UatDetail, UatStatus,AssignView,TblNavbarView,TeamMetricsData,ViewType,ValidInvalid,  IssueAction , Shiftupdate , Gallery, Publicholidays


admin.site.register(IssueAction)
admin.site.register(Shiftupdate)
admin.site.register(Gallery)
admin.site.register(Publicholidays)

admin.site.register(ValidInvalid)
admin.site.register(Mimember)
admin.site.register(Estimationdetail)
admin.site.register(Completeddetail)
admin.site.register(Authoriserdetail)
class AuthorisedetailAdmin(admin.ModelAdmin):
    list_display = ('authorisedid','authoriseddate','authoriserdetail','requestdetail')
    search_fields = ['authorisedid']

admin.site.register(Authorisedetail,AuthorisedetailAdmin)
admin.site.register(Assigneddetail)
admin.site.register(Acceptrejectoption)
admin.site.register(Acceptrejectdetail)

class TimetrackersAdmin(admin.ModelAdmin):
    list_display = ('timetrackerid','registerdatetime','trackingdatetime','mimember','teamdetail','requestcategorys','requestsubcategory','task','requestdetail','description_text','totaltime','comments','startdatetime','stopdatetime','reports')
    search_fields = ['timetrackerid']

admin.site.register(Timetrackers,TimetrackersAdmin)
admin.site.register(Teamdetail)
admin.site.register(Statusdetail)
admin.site.register(Requesttypedetail)
admin.site.register(Requestsubcategory)
admin.site.register(Requeststatusdetail)

class RequestdetailAdmin(admin.ModelAdmin):
    list_display = ('requestid','requestraiseddate','requesttypedetail','prioritydetail','username','requestdescription')
    search_fields = ['requestid']
admin.site.register(Requestdetail,RequestdetailAdmin)
admin.site.register(Requestcategorys)
admin.site.register(Prioritydetail)
admin.site.register(Overviewdetail)
admin.site.register(Options)
admin.site.register(Reports)
admin.site.register(Frequency)
admin.site.register(Deliverydays)
admin.site.register(Emaildetail)
admin.site.register(TimeDetail)
admin.site.register(Fielddetail)
admin.site.register(Filteroption)
admin.site.register(Errortype)
admin.site.register(Errorlog)
admin.site.register(Feedback)
admin.site.register(FeedbackQuestion)
admin.site.register(OtDetail)
admin.site.register(OtStatus)
admin.site.register(ReportType)
admin.site.register(Activitystatus)
admin.site.register(Designationmaster)
admin.site.register(Internaltask)
admin.site.register(Internaltaskchoice)
admin.site.register(Internaltaskstatus)
admin.site.register(Whatwedo)
admin.site.register(Reply)
admin.site.register(Suggestion)
admin.site.register(Governance)
admin.site.register(SuccessStories)
admin.site.register(TblNavbarFooterMaster)
admin.site.register(TblNavbarHeaderMaster)
class TblNavbarMasterAdmin(admin.ModelAdmin):
    list_display = ('navbar_id','group_name','navbar_header_id','navbar_footer_id')
    search_fields = ['navbar_id']

admin.site.register(TblNavbarMaster,TblNavbarMasterAdmin)
admin.site.register(TblLeaveRecord)
admin.site.register(TblLeaveType)
admin.site.register(TblAppreciation)
admin.site.register(TblRawActivityDetail)
admin.site.register(TblRawTeamMaster)
admin.site.register(TblRawTeamMemberMaster)
admin.site.register(TblRawScore)
admin.site.register(TblTeamMetrics)
admin.site.register(TeamMetrics)
admin.site.register(UatDetail)
admin.site.register(UatStatus)

admin.site.register(AssignView)
#admin.site.register(TblNavbarView)
class TblNavbarViewAdmin(admin.ModelAdmin):
    list_display = ('navbar_id','view_type','navbar_header','navbar_footer')
    search_fields = ['navbar_id']
admin.site.register(TblNavbarView,TblNavbarViewAdmin)


admin.site.register(TeamMetricsData)
admin.site.register(ViewType)
