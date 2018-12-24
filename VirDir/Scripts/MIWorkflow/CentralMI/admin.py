from django.contrib import admin
from .models import TblWhatwedo, TblIssueAction, TblUatDetail, TblUatStatusMaster, TblAcceptrejectdetail, TblActivity, TblActivityCalendar, TblActivitystatusCalendar, TblAppreciation, TblAssignView, TblAssigneddetail, TblCalendar, TblCalendarHolidays, TblCategorysMaster, TblCompleteddetail, TblConversation, TblDateTypesMaster, TblDeliveryDaysMaster, TblDesignationMaster, TblEmaildetail, TblErrorlog, TblErrortypeMaster, TblEstimationdetail, TblFeedback, TblFeedbackQuestionMaster, TblFrequency, TblGallery, TblGovernance, TblInternaltask, TblInternaltaskchoice, TblInternaltaskstatus, TblLeaveRecord, TblLeaveTypeMaster, TblMember, TblNavbarFooterMaster, TblNavbarHeaderMaster, TblNavbarMaster, TblNavbarView, TblOpenClose, TblYesNo, TblOtDetail, TblOtStatusMaster, TblOverviewdetail, TblPriorityMaster, TblPublicHolidaysMaster, TblRawActivityDetail, TblRawScore, TblRawTeamMaster, TblRawTeamMemberMaster, TblReply, TblRequestdetail, TblRequeststatusdetail, TblRequesttypeMaster, TblShiftUpdate, TblStatusMaster, TblSubcategoryMaster, TblSuccessStories, TblSuggestion, TblTeamMaster, TblTeamMetrics, TblTimeTracker, TblUsefulLinks, TblValidInvalidMaster, TblViewTypeMaster, TblAuthorisedetail, TblCategorysMaster, TblSubcategoryMaster,TblBusinessUnitMaster

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = TblMember
    can_delete = False
    fk_name = 'userid'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('tblmember', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class TblMemberAdmin(admin.ModelAdmin):
    list_display = ('memberid','userid','teamid','designationid','employeeid','dateofjoining','dateofbirth','viewid','individual_view','team_view','bu_view')
    search_fields = ['userid']
admin.site.register(TblMember,TblMemberAdmin)
admin.site.register(TblBusinessUnitMaster)
admin.site.register(TblWhatwedo)
admin.site.register(TblIssueAction)
admin.site.register(TblUatDetail)
admin.site.register(TblUatStatusMaster)
admin.site.register(TblAcceptrejectdetail)
admin.site.register(TblActivity)
admin.site.register(TblActivityCalendar)
admin.site.register(TblActivitystatusCalendar)
admin.site.register(TblAppreciation)
admin.site.register(TblAssignView)
admin.site.register(TblCalendar)
admin.site.register(TblCalendarHolidays)
admin.site.register(TblCategorysMaster)
admin.site.register(TblCompleteddetail)
admin.site.register(TblConversation)
admin.site.register(TblDateTypesMaster)
admin.site.register(TblDeliveryDaysMaster)
admin.site.register(TblDesignationMaster)
admin.site.register(TblEmaildetail)
admin.site.register(TblErrorlog)
admin.site.register(TblErrortypeMaster)
admin.site.register(TblEstimationdetail)
admin.site.register(TblFeedbackQuestionMaster)
admin.site.register(TblFrequency)
admin.site.register(TblGallery)
admin.site.register(TblGovernance)
admin.site.register(TblInternaltask)
admin.site.register(TblInternaltaskchoice)
admin.site.register(TblInternaltaskstatus)
admin.site.register(TblLeaveRecord)
admin.site.register(TblLeaveTypeMaster)
#admin.site.register(TblMember)
class TblNavbarFooterMasterAdmin(admin.ModelAdmin):
    list_display = ('navbar_footer_id','navbar_footer_name','navbar_footer_url','ranking','navbar_header')
    search_fields = ['navbar_footer_name']
admin.site.register(TblNavbarFooterMaster,TblNavbarFooterMasterAdmin)

class TblNavbarHeaderMasterAdmin(admin.ModelAdmin):
    list_display = ('navbar_header_id','navbar_header_name','navbar_header_url','ranking')
    search_fields = ['navbar_header_name']
admin.site.register(TblNavbarHeaderMaster,TblNavbarHeaderMasterAdmin)
admin.site.register(TblNavbarMaster)

class TblNavbarViewAdmin(admin.ModelAdmin):
    list_display = ('navbar_id','view_type','navbar_footer','can_edit','can_view','can_delete')
    search_fields = ['navbar_footer']
admin.site.register(TblNavbarView,TblNavbarViewAdmin)

admin.site.register(TblOpenClose)
admin.site.register(TblYesNo)
admin.site.register(TblOtDetail)
admin.site.register(TblOtStatusMaster)
admin.site.register(TblOverviewdetail)
admin.site.register(TblPriorityMaster)
admin.site.register(TblPublicHolidaysMaster)
admin.site.register(TblRawActivityDetail)
admin.site.register(TblRawScore)
admin.site.register(TblRawTeamMaster)
admin.site.register(TblRawTeamMemberMaster)
admin.site.register(TblReply)
admin.site.register(TblRequestdetail)
admin.site.register(TblRequeststatusdetail)
admin.site.register(TblRequesttypeMaster)
admin.site.register(TblShiftUpdate)
admin.site.register(TblStatusMaster)
admin.site.register(TblSubcategoryMaster)
admin.site.register(TblSuccessStories)
admin.site.register(TblSuggestion)
admin.site.register(TblTeamMaster)
admin.site.register(TblTeamMetrics)
admin.site.register(TblTimeTracker)
admin.site.register(TblUsefulLinks)
admin.site.register(TblValidInvalidMaster)
admin.site.register(TblViewTypeMaster)
admin.site.register(TblAuthorisedetail)
