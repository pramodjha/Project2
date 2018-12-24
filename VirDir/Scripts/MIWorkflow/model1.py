# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Calendar(models.Model):
    date = models.DateField(blank=True, null=True)
    calendar_days = models.IntegerField(blank=True, null=True)
    calendar_weekday = models.IntegerField(db_column='calendar_Weekday', blank=True, null=True)  # Field name made lowercase.
    calendar_months = models.IntegerField(blank=True, null=True)
    calendar_days_rest = models.IntegerField(blank=True, null=True)
    working_days = models.IntegerField(blank=True, null=True)
    working_weekday = models.IntegerField(blank=True, null=True)
    working_months = models.IntegerField(blank=True, null=True)
    working_days_rest = models.IntegerField(blank=True, null=True)
    weeknum = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblWhatwedo(models.Model):
    recordid = models.AutoField(primary_key=True)
    data = models.CharField(db_column='Data', max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=100)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbL_whatwedo'


class TblIssueAction(models.Model):
    issue_action_id = models.AutoField(db_column='Issue_Action_id', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField()
    issue = models.CharField(db_column='Issue', max_length=255, blank=True, null=True)  # Field name made lowercase.
    action_taken = models.CharField(db_column='Action_taken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    targetdate = models.DateField(blank=True, null=True)
    updatedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='updatedbyid', blank=True, null=True)
    statusid = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_Issue_Action'


class TblUatDetail(models.Model):
    uatid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    uat_statusid = models.ForeignKey('TblUatStatusMaster', models.DO_NOTHING, db_column='UAT_statusid', blank=True, null=True)  # Field name made lowercase.
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    testedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='testedbyid', blank=True, null=True)
    updatedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='updatedbyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_UAT_detail'


class TblUatStatusMaster(models.Model):
    uat_status_id = models.AutoField(db_column='UAT_status_id', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField()
    uat_status = models.CharField(db_column='UAT_status', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_UAT_status_master'


class TblAcceptrejectdetail(models.Model):
    estacceptrejectid = models.AutoField(primary_key=True)
    estacceptrejectdate = models.DateTimeField()
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_acceptrejectdetail'


class TblActivity(models.Model):
    activityid = models.AutoField(primary_key=True)
    registereddate = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.ForeignKey('TblFrequency', models.DO_NOTHING, db_column='frequency', blank=True, null=True)
    date_types = models.ForeignKey('TblDateTypesMaster', models.DO_NOTHING, db_column='date_types', blank=True, null=True)
    delivery_days = models.IntegerField(blank=True, null=True)
    deliverytime = models.TimeField(blank=True, null=True)
    teamname = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamname', blank=True, null=True)
    primaryowner = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='primaryowner', blank=True, null=True)
    secondaryowner = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='secondaryowner', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    requestcategorys = models.ForeignKey('TblCategorysMaster', models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    activitystatus = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='activitystatus', blank=True, null=True)
    activitydocument = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_activity'


class TblActivityCalendar(models.Model):
    date = models.DateField(blank=True, null=True)
    daytype = models.CharField(max_length=50, blank=True, null=True)
    weekname = models.CharField(max_length=50, blank=True, null=True)
    cd_wd_days = models.IntegerField(db_column='CD_WD_days', blank=True, null=True)  # Field name made lowercase.
    activityid = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_activity_calendar'


class TblActivitystatusCalendar(models.Model):
    activitystatuscalendarid = models.AutoField(primary_key=True)
    activitystatusdate = models.DateTimeField()
    activitystatus = models.ForeignKey('TblStatusMaster', models.DO_NOTHING, db_column='activitystatus', blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)
    activitycalendardate = models.DateField(blank=True, null=True)
    reallocatedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='reallocatedtoid', blank=True, null=True)
    recordenteredbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='recordenteredbyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_activitystatus_calendar'


class TblAppreciation(models.Model):
    appreciationid = models.AutoField(db_column='Appreciationid', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField()
    appreciated_to = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='Appreciated_to', blank=True, null=True)  # Field name made lowercase.
    appreciated_by = models.CharField(db_column='Appreciated_by', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    appreciation_status = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='appreciation_status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_appreciation'


class TblAssignView(models.Model):
    viewassign_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(AuthGroup, models.DO_NOTHING, db_column='group_name')
    view_type = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='view_type')

    class Meta:
        managed = False
        db_table = 'tbl_assign_view'


class TblAssigneddetail(models.Model):
    assignedid = models.AutoField(primary_key=True)
    assigneddate = models.DateTimeField(db_column='assignedDate')  # Field name made lowercase.
    assignedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='assignedtoid', blank=True, null=True)
    assignedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='assignedbyid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_assigneddetail'


class TblAuthorisedetail(models.Model):
    authorisedid = models.AutoField(primary_key=True)
    authoriseddate = models.DateTimeField()
    authoriserid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='authoriserid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_authorisedetail'


class TblAuthoriserdetail(models.Model):
    authoriserid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'tbl_authoriserdetail'


class TblBusinessUnitMaster(models.Model):
    bu_id = models.AutoField(db_column='BU_id', primary_key=True)  # Field name made lowercase.
    business_unit = models.CharField(db_column='Business_Unit', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_business_unit_master'


class TblCalendar(models.Model):
    date = models.DateField(blank=True, null=True)
    days_type = models.CharField(db_column='Days Type', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    daily = models.IntegerField(db_column='Daily', blank=True, null=True)  # Field name made lowercase.
    weekly = models.IntegerField(db_column='Weekly', blank=True, null=True)  # Field name made lowercase.
    monthly = models.IntegerField(db_column='Monthly', blank=True, null=True)  # Field name made lowercase.
    firstdayofmonth = models.DateField(db_column='FIrstDayofmonth', blank=True, null=True)  # Field name made lowercase.
    lastdayofthemonth = models.DateField(db_column='LastDayoftheMonth', blank=True, null=True)  # Field name made lowercase.
    weeknum = models.IntegerField(db_column='WeekNum', blank=True, null=True)  # Field name made lowercase.
    weekname = models.CharField(db_column='WeekName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_calendar'


class TblCalendarHolidays(models.Model):
    calendardate = models.DateTimeField(db_column='CalendarDate', primary_key=True)  # Field name made lowercase.
    calendarfunction = models.IntegerField(db_column='CalendarFunction')  # Field name made lowercase.
    holidaytype = models.CharField(db_column='HolidayType', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_calendar_holidays'
        unique_together = (('calendardate', 'calendarfunction'),)


class TblCategorysMaster(models.Model):
    requestcategoryid = models.AutoField(primary_key=True)
    requestcategorydatetime = models.DateTimeField()
    requestcategorys = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_categorys_master'


class TblCompleteddetail(models.Model):
    completedid = models.AutoField(primary_key=True)
    completeddate = models.DateTimeField()
    completedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='completedbyid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_completeddetail'


class TblConversation(models.Model):
    conversationid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_conversation'


class TblDateTypesMaster(models.Model):
    date_typesid = models.AutoField(primary_key=True)
    date_types = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_date_types_master'


class TblDeliveryDaysMaster(models.Model):
    deliverydaysid = models.AutoField(primary_key=True)
    days = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_delivery_days_master'


class TblDesignationMaster(models.Model):
    designationid = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_designation_master'


class TblEmaildetail(models.Model):
    emailid = models.AutoField(primary_key=True)
    requestdetail = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    emaildate = models.DateTimeField()
    stage = models.TextField()
    emailsubject = models.TextField()
    emailbody = models.TextField()
    emailto = models.TextField()
    emailfrom = models.TextField()
    emailstatus = models.CharField(max_length=255, blank=True, null=True)
    requeststatus = models.CharField(db_column='RequestStatus', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_emaildetail'


class TblErrorlog(models.Model):
    error_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    occurancedate = models.DateField()
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid')
    reportedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='reportedbyid', blank=True, null=True)
    reportedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='reportedtoid')
    errortypeid = models.ForeignKey('TblErrortypeMaster', models.DO_NOTHING, db_column='errortypeid')
    description = models.TextField()
    document = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_errorlog'


class TblErrortypeMaster(models.Model):
    error_typeid = models.AutoField(primary_key=True)
    error_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_errortype_master'


class TblEstimationdetail(models.Model):
    estimationid = models.AutoField(primary_key=True)
    estimationdate = models.DateTimeField()
    estimatedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='estimatedbyid', blank=True, null=True)
    estimateddays = models.IntegerField(blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_estimationdetail'


class TblFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_date = models.DateTimeField()
    feedback_question = models.ForeignKey('TblFeedbackQuestionMaster', models.DO_NOTHING, db_column='feedback_question')
    feedback_text = models.CharField(max_length=255, blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_feedback'


class TblFeedbackQuestionMaster(models.Model):
    feedback_questionid = models.AutoField(primary_key=True)
    feedback_questiondate = models.DateTimeField()
    feedback_question = models.CharField(max_length=255)
    feedback_answerdatatype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_feedback_question_master'


class TblFrequency(models.Model):
    frequencyid = models.AutoField(primary_key=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_frequency'


class TblGallery(models.Model):
    imgid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    uploadedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='uploadedbyid', blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_gallery'


class TblGovernance(models.Model):
    governancedatetime = models.DateTimeField()
    governanceid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamid')
    processimg = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_governance'


class TblInternaltask(models.Model):
    internaltaskid = models.AutoField(primary_key=True)
    internaltaskdatetime = models.DateTimeField()
    internaltaskquestion = models.CharField(db_column='internaltaskQuestion', max_length=255)  # Field name made lowercase.
    statusid = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='statusid', blank=True, null=True)
    ownerid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='ownerid', blank=True, null=True)
    targetdate = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_internaltask'


class TblInternaltaskchoice(models.Model):
    internaltaskchoiceid = models.AutoField(primary_key=True)
    internaltaskchoicedatetime = models.DateTimeField()
    internaltaskchoice = models.CharField(max_length=255)
    internaltaskid = models.ForeignKey(TblInternaltask, models.DO_NOTHING, db_column='internaltaskid')

    class Meta:
        managed = False
        db_table = 'tbl_internaltaskchoice'


class TblInternaltaskstatus(models.Model):
    internaltaskstatusid = models.AutoField(primary_key=True)
    internaltaskstatusdatetime = models.DateTimeField()
    memberid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    internaltaskid = models.ForeignKey(TblInternaltask, models.DO_NOTHING, db_column='internaltaskid', blank=True, null=True)
    internaltaskchoiceid = models.ForeignKey(TblInternaltaskchoice, models.DO_NOTHING, db_column='internaltaskchoiceid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_internaltaskstatus'


class TblLeaveRecord(models.Model):
    leaverecordid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    leave_date = models.DateField()
    userid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='userid')
    leave_type = models.ForeignKey('TblLeaveTypeMaster', models.DO_NOTHING, db_column='leave_type')

    class Meta:
        managed = False
        db_table = 'tbl_leave_record'


class TblLeaveTypeMaster(models.Model):
    leavetypeid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    leave_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_leave_type_master'


class TblMember(models.Model):
    memberid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    teamid = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamid')
    designationid = models.ForeignKey(TblDesignationMaster, models.DO_NOTHING, db_column='designationid', blank=True, null=True)
    employeeid = models.IntegerField(blank=True, null=True)
    dateofjoining = models.DateField(db_column='DateofJoining', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateofBirth', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aboutme = models.TextField(blank=True, null=True)
    viewid = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='viewid', blank=True, null=True)
    individual_view = models.NullBooleanField(db_column='Individual_view')  # Field name made lowercase.
    team_view = models.NullBooleanField()
    bu_view = models.NullBooleanField(db_column='BU_view')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_member'


class TblNavbarFooterMaster(models.Model):
    navbar_footer_id = models.AutoField(primary_key=True)
    navbar_footer_name = models.CharField(max_length=255, blank=True, null=True)
    navbar_footer_url = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    navbar_header = models.ForeignKey('TblNavbarHeaderMaster', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_footer_master'


class TblNavbarHeaderMaster(models.Model):
    navbar_header_id = models.AutoField(primary_key=True)
    navbar_header_name = models.CharField(max_length=255, blank=True, null=True)
    navbar_header_url = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_header_master'


class TblNavbarMaster(models.Model):
    navbar_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(AuthGroup, models.DO_NOTHING, db_column='group_name')
    navbar_header = models.ForeignKey(TblNavbarHeaderMaster, models.DO_NOTHING)
    navbar_footer = models.ForeignKey(TblNavbarFooterMaster, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_master'


class TblNavbarView(models.Model):
    navbar_id = models.AutoField(primary_key=True)
    view_type = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='view_type')
    navbar_footer = models.ForeignKey(TblNavbarFooterMaster, models.DO_NOTHING)
    can_edit = models.NullBooleanField()
    can_view = models.NullBooleanField()
    can_delete = models.NullBooleanField()
    can_add = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tbl_navbar_view'


class TblOpenClose(models.Model):
    activitystatusid = models.AutoField(primary_key=True)
    activitystatus = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_open_close'


class TblOtDetail(models.Model):
    ot_id = models.AutoField(primary_key=True)
    timetrackerid = models.ForeignKey('TblTimeTracker', models.DO_NOTHING, db_column='timetrackerid')
    ot_startdatetime = models.DateTimeField(blank=True, null=True)
    ot_enddatetime = models.DateTimeField(blank=True, null=True)
    ot_time = models.IntegerField(blank=True, null=True)
    statusid = models.ForeignKey('TblOtStatusMaster', models.DO_NOTHING, db_column='statusid')
    otdocument = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_ot_detail'


class TblOtStatusMaster(models.Model):
    ot_statusid = models.AutoField(primary_key=True)
    ot_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_ot_status_master'


class TblOverviewdetail(models.Model):
    overviewid = models.AutoField(primary_key=True)
    overviewdate = models.DateTimeField()
    providedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='providedbyid')
    giventoid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='giventoid', blank=True, null=True)
    sopcreatedid = models.ForeignKey('TblYesNo', models.DO_NOTHING, db_column='sopcreatedid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    document = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_overviewdetail'


class TblPriorityMaster(models.Model):
    requestpriorityid = models.AutoField(primary_key=True)
    requestpriority = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_priority_master'


class TblPublicHolidaysMaster(models.Model):
    holidaysid = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    holidays_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_public_holidays_master'


class TblRawActivityDetail(models.Model):
    raw_activity_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    raw_activity = models.CharField(max_length=50, blank=True, null=True)
    raw_activity_description = models.TextField(blank=True, null=True)
    raw_activity_img = models.CharField(max_length=255, blank=True, null=True)
    raw_activity_scheduled = models.DateField(blank=True, null=True)
    raw_statusid = models.ForeignKey(TblOpenClose, models.DO_NOTHING, db_column='raw_statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_activity_detail'


class TblRawScore(models.Model):
    raw_score_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    raw_teamid = models.ForeignKey('TblRawTeamMaster', models.DO_NOTHING, db_column='raw_teamid', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(db_column='Winner', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_score'


class TblRawTeamMaster(models.Model):
    raw_team_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    raw_team = models.CharField(max_length=255, blank=True, null=True)
    raw_team_icon = models.CharField(max_length=255, blank=True, null=True)
    raw_team_slogan = models.CharField(max_length=255, blank=True, null=True)
    valid_invalid = models.ForeignKey('TblValidInvalidMaster', models.DO_NOTHING, db_column='valid_invalid', blank=True, null=True)
    raw_managementid = models.ForeignKey('TblYesNo', models.DO_NOTHING, db_column='raw_managementid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_master'


class TblRawTeamMemberMaster(models.Model):
    raw_team_member_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    raw_team = models.ForeignKey(TblRawTeamMaster, models.DO_NOTHING, db_column='raw_team', blank=True, null=True)
    raw_member = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='raw_member', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_member_master'


class TblReply(models.Model):
    replydatetime = models.DateTimeField()
    replyid = models.AutoField(primary_key=True)
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    reply = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tbl_reply'


class TblRequestdetail(models.Model):
    requestid = models.AutoField(primary_key=True)
    requestraiseddate = models.DateTimeField()
    requesttypeid = models.ForeignKey('TblRequesttypeMaster', models.DO_NOTHING, db_column='requesttypeid')
    priorityid = models.ForeignKey(TblPriorityMaster, models.DO_NOTHING, db_column='priorityid')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    requestdescription = models.TextField()
    requestdocument = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_requestdetail'


class TblRequeststatusdetail(models.Model):
    requeststatusid = models.AutoField(primary_key=True)
    requeststatusdate = models.DateTimeField()
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    statusid = models.ForeignKey('TblStatusMaster', models.DO_NOTHING, db_column='statusid', blank=True, null=True)
    requestid = models.ForeignKey(TblRequestdetail, models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_requeststatusdetail'


class TblRequesttypeMaster(models.Model):
    requesttypeid = models.AutoField(primary_key=True)
    requesttype = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_requesttype_master'


class TblShiftUpdate(models.Model):
    updateid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    updateinbrief = models.TextField(blank=True, null=True)
    recordedbyid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='recordedbyid', blank=True, null=True)
    statusid = models.ForeignKey(TblOpenClose, models.DO_NOTHING, db_column='statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_shift_update'


class TblStatusMaster(models.Model):
    statusnameid = models.AutoField(primary_key=True)
    statusname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_status_master'


class TblSubcategoryMaster(models.Model):
    requestsubcategoryid = models.AutoField(primary_key=True)
    requestsubcategorydatetime = models.DateTimeField()
    categorysid = models.ForeignKey(TblCategorysMaster, models.DO_NOTHING, db_column='categorysid', blank=True, null=True)
    requestsubcategory = models.CharField(max_length=100, blank=True, null=True)
    core_noncore = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_subcategory_master'


class TblSuccessStories(models.Model):
    storiesdatetime = models.DateTimeField()
    storiesid = models.AutoField(primary_key=True)
    stories = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_success_stories'


class TblSuggestion(models.Model):
    suggestiondatetime = models.DateTimeField()
    suggestionid = models.AutoField(primary_key=True)
    suggestion = models.TextField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    suggestedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='suggestedbyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_suggestion'


class TblTeamMaster(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamdatetime = models.DateTimeField()
    teamname = models.CharField(max_length=100, blank=True, null=True)
    buid = models.ForeignKey(TblBusinessUnitMaster, models.DO_NOTHING, db_column='buid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_team_master'


class TblTeamMetrics(models.Model):
    metrics_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    teamid = models.ForeignKey(TblTeamMaster, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    requesttypeid = models.ForeignKey(TblRequesttypeMaster, models.DO_NOTHING, db_column='requesttypeid', blank=True, null=True)
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    wip = models.IntegerField(db_column='WIP', blank=True, null=True)  # Field name made lowercase.
    uat = models.IntegerField(db_column='UAT', blank=True, null=True)  # Field name made lowercase.
    completed = models.IntegerField(db_column='Completed', blank=True, null=True)  # Field name made lowercase.
    project = models.IntegerField(db_column='Project', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_team_metrics'


class TblTimeTracker(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdatetime = models.DateTimeField()
    trackingdatetime = models.DateField()
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    teamid = models.ForeignKey(TblTeamMaster, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    categorysid = models.ForeignKey(TblCategorysMaster, models.DO_NOTHING, db_column='categorysid', blank=True, null=True)
    subcategoryid = models.ForeignKey(TblSubcategoryMaster, models.DO_NOTHING, db_column='subcategoryid', blank=True, null=True)
    task = models.CharField(max_length=100, blank=True, null=True)
    requestid = models.ForeignKey(TblRequestdetail, models.DO_NOTHING, db_column='requestid', blank=True, null=True)
    description_text = models.CharField(max_length=255, blank=True, null=True)
    totaltime = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    startdatetime = models.DateTimeField(blank=True, null=True)
    stopdatetime = models.DateTimeField(blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)
    otid = models.ForeignKey(TblOtDetail, models.DO_NOTHING, db_column='otid', blank=True, null=True)
    valid_invalid = models.ForeignKey('TblValidInvalidMaster', models.DO_NOTHING, db_column='valid_invalid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_time_tracker'


class TblUsefulLinks(models.Model):
    linkid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    teamid = models.ForeignKey(TblTeamMaster, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_useful_links'


class TblValidInvalidMaster(models.Model):
    valid_invaidid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_valid_invalid_master'


class TblViewTypeMaster(models.Model):
    view_id = models.AutoField(primary_key=True)
    viewname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_view_type_master'


class TblYesNo(models.Model):
    optionsid = models.AutoField(primary_key=True)
    optionsname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_yes_no'
