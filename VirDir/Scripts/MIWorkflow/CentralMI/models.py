# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import datetime
import django
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'

    def __str__(self):
        return str(self.name)

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

    def __str__(self):
        return str(self.username)


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

    def __str__(self):
        return str(self.group)

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

    def __str__(self):
        return str(self.recordid)


class TblIssueAction(models.Model):
    issue_action_id = models.AutoField(db_column='Issue_Action_id', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField(default= datetime.datetime.now())
    issue = models.CharField(db_column='Issue', max_length=255, blank=True, null=True)  # Field name made lowercase.
    action_taken = models.CharField(db_column='Action_taken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    targetdate = models.DateField(blank=True, null=True,default= datetime.date.today)
    updatedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='updatedbyid', blank=True, null=True)
    statusid = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_Issue_Action'


    def __str__(self):
        return str(self.issue_action_id)


class TblUatDetail(models.Model):
    uatid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    uat_statusid = models.ForeignKey('TblUatStatusMaster', models.DO_NOTHING, db_column='UAT_statusid', blank=True, null=True)  # Field name made lowercase.
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    testedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='testedbyid', blank=True, null=True,related_name='testedbyid')
    updatedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='updatedbyid', blank=True, null=True,related_name='updatedbyid')

    class Meta:
        managed = False
        db_table = 'tbl_UAT_detail'

    def __str__(self):
        return str(self.uatid)


class TblUatStatusMaster(models.Model):
    uat_status_id = models.AutoField(db_column='UAT_status_id', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField(default= datetime.datetime.now())
    uat_status = models.CharField(db_column='UAT_status', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_UAT_status_master'

    def __str__(self):
        return str(self.uat_status)

class TblAcceptrejectdetail(models.Model):
    estacceptrejectid = models.AutoField(primary_key=True)
    estacceptrejectdate = models.DateTimeField(default= datetime.datetime.now())
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_acceptrejectdetail'

    def __str__(self):
        return str(self.estacceptrejectid)

class TblActivity(models.Model):
    activityid = models.AutoField(primary_key=True)
    registereddate = models.DateTimeField(default= datetime.datetime.now())
    name = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.ForeignKey('TblFrequency', models.DO_NOTHING, db_column='frequency', blank=True, null=True)
    date_types = models.ForeignKey('TblDateTypesMaster', models.DO_NOTHING, db_column='date_types', blank=True, null=True)
    delivery_days = models.IntegerField(blank=True, null=True)
    deliverytime = models.TimeField(blank=True, null=True)
    teamname = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamname', blank=True, null=True)
    primaryowner = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='primaryowner', blank=True, null=True,related_name='primaryowner')
    secondaryowner = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='secondaryowner', blank=True, null=True,related_name='secondaryowner')
    description = models.CharField(max_length=255, blank=True, null=True)
    requestcategorys = models.ForeignKey('TblCategorysMaster', models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    activitystatus = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='activitystatus', blank=True, null=True)
    activitydocument = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_activity'

    def __str__(self):
        return str(self.name)


class TblActivityCalendar(models.Model):
    date = models.DateField(blank=True, null=True,default= datetime.date.today)
    daytype = models.CharField(max_length=50, blank=True, null=True)
    weekname = models.CharField(max_length=50, blank=True, null=True)
    cd_wd_days = models.IntegerField(db_column='CD_WD_days', blank=True, null=True)  # Field name made lowercase.
    activityid = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_activity_calendar'

    def __str__(self):
        return str(self.date)

class TblActivitystatusCalendar(models.Model):
    activitystatuscalendarid = models.AutoField(primary_key=True)
    activitystatusdate = models.DateTimeField(default= datetime.datetime.now())
    activitystatus = models.ForeignKey('TblStatusMaster', models.DO_NOTHING, db_column='activitystatus', blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)
    activitycalendardate = models.DateField(blank=True, null=True)
    reallocatedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='reallocatedtoid', blank=True, null=True,related_name='reallocatedtoid')
    recordenteredbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='recordenteredbyid', blank=True, null=True,related_name='recordenteredbyid')

    class Meta:
        managed = False
        db_table = 'tbl_activitystatus_calendar'

    def __str__(self):
        return str(self.activitystatuscalendarid)

class TblAppreciation(models.Model):
    appreciationid = models.AutoField(db_column='Appreciationid', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField(default= datetime.datetime.now())
    appreciated_to = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='Appreciated_to', blank=True, null=True)  # Field name made lowercase.
    appreciated_by = models.CharField(db_column='Appreciated_by', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    appreciation_status = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='appreciation_status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_appreciation'

    def __str__(self):
        return str(self.appreciationid)

class TblAssignView(models.Model):
    viewassign_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(AuthGroup, models.DO_NOTHING, db_column='group_name')
    view_type = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='view_type')

    class Meta:
        managed = False
        db_table = 'tbl_assign_view'

    def __str__(self):
        return str(self.view_type)


class TblAssigneddetail(models.Model):
    assignedid = models.AutoField(primary_key=True)
    assigneddate = models.DateTimeField(db_column='assignedDate',default= datetime.datetime.now())  # Field name made lowercase.
    assignedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='assignedtoid', blank=True, null=True,related_name='assignedtoid')
    assignedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='assignedbyid', blank=True, null=True,related_name='assignedbyid')
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_assigneddetail'

    def __str__(self):
        return str(self.assignedid)

class TblAuthorisedetail(models.Model):
    authorisedid = models.AutoField(primary_key=True)
    authoriseddate = models.DateTimeField(default= datetime.datetime.now())
    authoriserid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='authoriserid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_authorisedetail'

    def __str__(self):
        return str(self.authorisedid)

class TblAuthoriserdetail(models.Model):
    authoriserid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'tbl_authoriserdetail'

    def __str__(self):
        return str(self.authoriserid)

class TblCalendar(models.Model):
    date = models.DateField(blank=True, null=True,default= datetime.date.today)
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

    def __str__(self):
        return str(self.date)


class TblCalendarHolidays(models.Model):
    calendardate = models.DateTimeField(db_column='CalendarDate', primary_key=True)  # Field name made lowercase.
    calendarfunction = models.IntegerField(db_column='CalendarFunction')  # Field name made lowercase.
    holidaytype = models.CharField(db_column='HolidayType', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_calendar_holidays'
        unique_together = (('calendardate', 'calendarfunction'),)

    def __str__(self):
        return str(self.calendardate)


class TblCategorysMaster(models.Model):
    requestcategoryid = models.AutoField(primary_key=True)
    requestcategorydatetime = models.DateTimeField(default= datetime.datetime.now())
    requestcategorys = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_categorys_master'

    def __str__(self):
        return str(self.requestcategorys)


class TblCompleteddetail(models.Model):
    completedid = models.AutoField(primary_key=True)
    completeddate = models.DateTimeField(default= datetime.datetime.now())
    completedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='completedbyid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_completeddetail'

    def __str__(self):
        return str(self.completedid)

class TblConversation(models.Model):
    conversationid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_conversation'

    def __str__(self):
        return str(self.conversationid)

class TblDateTypesMaster(models.Model):
    date_typesid = models.AutoField(primary_key=True)
    date_types = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_date_types_master'

    def __str__(self):
        return str(self.date_types)


class TblDeliveryDaysMaster(models.Model):
    deliverydaysid = models.AutoField(primary_key=True)
    days = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_delivery_days_master'

    def __str__(self):
        return str(self.deliverydaysid)

class TblDesignationMaster(models.Model):
    designationid = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_designation_master'

    def __str__(self):
        return str(self.designation)

class TblEmaildetail(models.Model):
    emailid = models.AutoField(primary_key=True)
    requestdetail = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    emaildate = models.DateTimeField(default= datetime.datetime.now())
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

    def __str__(self):
        return str(self.emailid)


class TblErrorlog(models.Model):
    error_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default= datetime.datetime.now())
    occurancedate = models.DateField(default= django.utils.timezone.now)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid')
    reportedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='reportedbyid', blank=True, null=True)
    reportedtoid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='reportedtoid')
    errortypeid = models.ForeignKey('TblErrortypeMaster', models.DO_NOTHING, db_column='errortypeid')
    description = models.TextField()
    document = models.FileField(upload_to='errordocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_errorlog'

    def __str__(self):
        return str(self.error_id)


class TblErrortypeMaster(models.Model):
    error_typeid = models.AutoField(primary_key=True)
    error_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_errortype_master'

    def __str__(self):
        return str(self.error_type)


class TblEstimationdetail(models.Model):
    estimationid = models.AutoField(primary_key=True)
    estimationdate = models.DateTimeField(default= datetime.datetime.now())
    estimatedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='estimatedbyid', blank=True, null=True)
    estimateddays = models.IntegerField(blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_estimationdetail'

    def __str__(self):
        return str(self.estimationid)

class TblFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_date = models.DateTimeField(default= datetime.datetime.now())
    feedback_question = models.ForeignKey('TblFeedbackQuestionMaster', models.DO_NOTHING, db_column='feedback_question')
    feedback_text = models.CharField(max_length=255, blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_feedback'

    def __str__(self):
        return str(self.feedback_id)

class TblFeedbackQuestionMaster(models.Model):
    feedback_questionid = models.AutoField(primary_key=True)
    feedback_questiondate = models.DateTimeField(default= datetime.datetime.now())
    feedback_question = models.CharField(max_length=255)
    feedback_answerdatatype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_feedback_question_master'

    def __str__(self):
        return str(self.feedback_question)

class TblFrequency(models.Model):
    frequencyid = models.AutoField(primary_key=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_frequency'

    def __str__(self):
        return str(self.frequency)


class TblGallery(models.Model):
    imgid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    uploadedbyid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='uploadedbyid', blank=True, null=True)
    img = models.FileField(upload_to='gallery/',blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_gallery'

    def __str__(self):
        return str(self.imgid)

class TblGovernance(models.Model):
    governancedatetime = models.DateTimeField(default= datetime.datetime.now())
    governanceid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamid')
    processimg = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_governance'

    def __str__(self):
        return str(self.governanceid)

class TblInternaltask(models.Model):
    internaltaskid = models.AutoField(primary_key=True)
    internaltaskdatetime = models.DateTimeField(default= datetime.datetime.now())
    internaltaskquestion = models.CharField(db_column='internaltaskQuestion', max_length=255)  # Field name made lowercase.
    statusid = models.ForeignKey('TblOpenClose', models.DO_NOTHING, db_column='statusid', blank=True, null=True)
    ownerid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='ownerid', blank=True, null=True)
    targetdate = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_internaltask'

    def __str__(self):
        return str(self.internaltaskquestion)

class TblInternaltaskchoice(models.Model):
    internaltaskchoiceid = models.AutoField(primary_key=True)
    internaltaskchoicedatetime = models.DateTimeField(default= datetime.datetime.now())
    internaltaskchoice = models.CharField(max_length=255)
    internaltaskid = models.ForeignKey(TblInternaltask, models.DO_NOTHING, db_column='internaltaskid')

    class Meta:
        managed = False
        db_table = 'tbl_internaltaskchoice'

    def __str__(self):
        return str(self.internaltaskchoice)

class TblInternaltaskstatus(models.Model):
    internaltaskstatusid = models.AutoField(primary_key=True)
    internaltaskstatusdatetime = models.DateTimeField(default= datetime.datetime.now())
    memberid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    internaltaskid = models.ForeignKey(TblInternaltask, models.DO_NOTHING, db_column='internaltaskid', blank=True, null=True)
    internaltaskchoiceid = models.ForeignKey(TblInternaltaskchoice, models.DO_NOTHING, db_column='internaltaskchoiceid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_internaltaskstatus'

    def __str__(self):
        return str(self.internaltaskstatusid)

class TblLeaveRecord(models.Model):
    leaverecordid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    leave_date = models.DateField(default= datetime.date.today)
    userid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='userid')
    leave_type = models.ForeignKey('TblLeaveTypeMaster', models.DO_NOTHING, db_column='leave_type')

    class Meta:
        managed = False
        db_table = 'tbl_leave_record'

    def __str__(self):
        return str(self.leaverecordid)

class TblLeaveTypeMaster(models.Model):
    leavetypeid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    leave_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_leave_type_master'


    def __str__(self):
        return str(self.leave_type)

class TblMember(models.Model):
    memberid = models.AutoField(primary_key=True)
    userid = models.OneToOneField(User, on_delete=models.CASCADE, db_column='userid')
    teamid = models.ForeignKey('TblTeamMaster', models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    designationid = models.ForeignKey(TblDesignationMaster, models.DO_NOTHING, db_column='designationid', blank=True, null=True)
    employeeid = models.IntegerField(blank=True, null=True)
    dateofjoining = models.DateField(db_column='DateofJoining', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateofBirth', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aboutme = models.FileField(upload_to='about_team/',blank=True, null=True)
    viewid = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='viewid', blank=True, null=True)
    individual_view = models.BooleanField(db_column='Individual_view')  # Field name made lowercase.
    team_view = models.BooleanField()
    bu_view = models.BooleanField(db_column='BU_view')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_member'

    def __str__(self):
        return str(self.userid)

class TblNavbarFooterMaster(models.Model):
    navbar_footer_id = models.AutoField(primary_key=True)
    navbar_footer_name = models.CharField(max_length=255, blank=True, null=True)
    navbar_footer_url = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    navbar_header = models.ForeignKey('TblNavbarHeaderMaster', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_footer_master'

    def __str__(self):
        return str(self.navbar_footer_name)

class TblNavbarHeaderMaster(models.Model):
    navbar_header_id = models.AutoField(primary_key=True)
    navbar_header_name = models.CharField(max_length=255, blank=True, null=True)
    navbar_header_url = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_header_master'

    def __str__(self):
        return str(self.navbar_header_name)

class TblNavbarMaster(models.Model):
    navbar_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey(AuthGroup, models.DO_NOTHING, db_column='group_name')
    navbar_header = models.ForeignKey(TblNavbarHeaderMaster, models.DO_NOTHING)
    navbar_footer = models.ForeignKey(TblNavbarFooterMaster, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_master'

    def __str__(self):
        return str(self.navbar_id)


class TblNavbarView(models.Model):
    navbar_id = models.AutoField(primary_key=True)
    view_type = models.ForeignKey('TblViewTypeMaster', models.DO_NOTHING, db_column='view_type')
    navbar_footer = models.ForeignKey(TblNavbarFooterMaster, models.DO_NOTHING)
    can_edit = models.BooleanField()
    can_view = models.BooleanField()
    can_delete = models.BooleanField()
    can_add = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tbl_navbar_view'

    def __str__(self):
        return str(self.navbar_footer)


class TblOpenClose(models.Model):
    activitystatusid = models.AutoField(primary_key=True)
    activitystatus = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_open_close'

    def __str__(self):
        return str(self.activitystatus)


class TblOtDetail(models.Model):
    ot_id = models.AutoField(primary_key=True)
    timetrackerid = models.ForeignKey('TblTimeTracker', models.DO_NOTHING, db_column='timetrackerid')
    ot_startdatetime = models.DateTimeField(blank=True, null=True)
    ot_enddatetime = models.DateTimeField(blank=True, null=True)
    ot_time = models.IntegerField(blank=True, null=True)
    statusid = models.ForeignKey('TblOtStatusMaster', models.DO_NOTHING, db_column='statusid')
    otdocument = models.FileField(upload_to='otdocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_ot_detail'

    def __str__(self):
        return str(self.statusid)

class TblOtStatusMaster(models.Model):
    ot_statusid = models.AutoField(primary_key=True)
    ot_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_ot_status_master'

    def __str__(self):
        return str(self.ot_status)

class TblOverviewdetail(models.Model):
    overviewid = models.AutoField(primary_key=True)
    overviewdate = models.DateTimeField(default= datetime.datetime.now())
    providedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='providedbyid')
    giventoid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='giventoid', blank=True, null=True)
    sopcreatedid = models.ForeignKey('TblYesNo', models.DO_NOTHING, db_column='sopcreatedid', blank=True, null=True)
    requestid = models.ForeignKey('TblRequestdetail', models.DO_NOTHING, db_column='requestid')
    document = models.FileField(upload_to='sopdocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_overviewdetail'

    def __str__(self):
        return str(self.overviewid)

class TblPriorityMaster(models.Model):
    requestpriorityid = models.AutoField(primary_key=True)
    requestpriority = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_priority_master'

    def __str__(self):
        return str(self.requestpriority)

class TblPublicHolidaysMaster(models.Model):
    holidaysid = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    holidays_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_public_holidays_master'

    def __str__(self):
        return str(self.holidaysid)


class TblRawActivityDetail(models.Model):
    raw_activity_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_activity = models.CharField(max_length=50, blank=True, null=True)
    raw_activity_description = models.TextField(blank=True, null=True)
    raw_activity_img =  models.FileField(upload_to='rawactivity/',blank=True, null=True)
    raw_activity_scheduled = models.DateField(blank=True, null=True,default= datetime.date.today)
    raw_statusid = models.ForeignKey(TblOpenClose, models.DO_NOTHING, db_column='raw_statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_activity_detail'

    def __str__(self):
        return str(self.raw_activity_id)


class TblRawScore(models.Model):
    raw_score_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_teamid = models.ForeignKey('TblRawTeamMaster', models.DO_NOTHING, db_column='raw_teamid', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(db_column='Winner', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_score'

    def __str__(self):
        return str(self.raw_score_id)

class TblRawTeamMaster(models.Model):
    raw_team_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_team = models.CharField(max_length=255, blank=True, null=True)
    raw_team_icon = models.CharField(max_length=255, blank=True, null=True)
    raw_team_slogan = models.CharField(max_length=255, blank=True, null=True)
    valid_invalid = models.ForeignKey('TblValidInvalidMaster', models.DO_NOTHING, db_column='valid_invalid', blank=True, null=True)
    raw_managementid = models.ForeignKey('TblYesNo', models.DO_NOTHING, db_column='raw_managementid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_master'

    def __str__(self):
        return str(self.raw_team)

class TblRawTeamMemberMaster(models.Model):
    raw_team_member_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_team = models.ForeignKey(TblRawTeamMaster, models.DO_NOTHING, db_column='raw_team', blank=True, null=True)
    raw_member = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='raw_member', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_member_master'

    def __str__(self):
        return str(self.raw_team)


class TblReply(models.Model):
    replydatetime = models.DateTimeField(default= datetime.datetime.now())
    replyid = models.AutoField(primary_key=True)
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    reply = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tbl_reply'

    def __str__(self):
        return str(self.replyid)


class TblRequestdetail(models.Model):
    requestid = models.AutoField(primary_key=True)
    requestraiseddate = models.DateTimeField(default= datetime.datetime.now())
    requesttypeid = models.ForeignKey('TblRequesttypeMaster', models.DO_NOTHING, db_column='requesttypeid')
    priorityid = models.ForeignKey(TblPriorityMaster, models.DO_NOTHING, db_column='priorityid')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    requestdescription = models.TextField()
    requestdocument = models.FileField(upload_to='requestdocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_requestdetail'

    def __str__(self):
        return str(self.requestid)


class TblRequeststatusdetail(models.Model):
    requeststatusid = models.AutoField(primary_key=True)
    requeststatusdate = models.DateTimeField(default= datetime.datetime.now())
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    statusid = models.ForeignKey('TblStatusMaster', models.DO_NOTHING, db_column='statusid', blank=True, null=True)
    requestid = models.ForeignKey(TblRequestdetail, models.DO_NOTHING, db_column='requestid')

    class Meta:
        managed = False
        db_table = 'tbl_requeststatusdetail'

    def __str__(self):
        return str(self.statusid)


class TblRequesttypeMaster(models.Model):
    requesttypeid = models.AutoField(primary_key=True)
    requesttype = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_requesttype_master'

    def __str__(self):
        return str(self.requesttype)

class TblShiftUpdate(models.Model):
    updateid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    updateinbrief = models.TextField(blank=True, null=True)
    recordedbyid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='recordedbyid', blank=True, null=True)
    statusid = models.ForeignKey(TblOpenClose, models.DO_NOTHING, db_column='statusid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_shift_update'

    def __str__(self):
        return str(self.updateid)

class TblStatusMaster(models.Model):
    statusnameid = models.AutoField(primary_key=True)
    statusname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_status_master'

    def __str__(self):
        return str(self.statusname)


class TblSubcategoryMaster(models.Model):
    requestsubcategoryid = models.AutoField(primary_key=True)
    requestsubcategorydatetime = models.DateTimeField(default= datetime.datetime.now())
    categorysid = models.ForeignKey(TblCategorysMaster, models.DO_NOTHING, db_column='categorysid', blank=True, null=True)
    requestsubcategory = models.CharField(max_length=100, blank=True, null=True)
    core_noncore = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_subcategory_master'

    def __str__(self):
        return str(self.requestsubcategory)


class TblSuccessStories(models.Model):
    storiesdatetime = models.DateTimeField(default= datetime.datetime.now())
    storiesid = models.AutoField(primary_key=True)
    stories = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_success_stories'

    def __str__(self):
        return str(self.storiesdatetime)

class TblSuggestion(models.Model):
    suggestiondatetime = models.DateTimeField(default= datetime.datetime.now())
    suggestionid = models.AutoField(primary_key=True)
    suggestion = models.TextField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    suggestedbyid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='suggestedbyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_suggestion'

    def __str__(self):
        return str(self.suggestionid)

class TblBusinessUnitMaster(models.Model):
    bu_id = models.AutoField(db_column='BU_id', primary_key=True)  # Field name made lowercase.
    business_unit = models.CharField(db_column='Business_Unit', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_business_unit_master'

    def __str__(self):
        return str(self.business_unit)


class TblTeamMaster(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamdatetime = models.DateTimeField(default= datetime.datetime.now())
    teamname = models.CharField(max_length=100, blank=True, null=True)
    buid = models.ForeignKey(TblBusinessUnitMaster, models.DO_NOTHING, db_column='buid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_team_master'

    def __str__(self):
        return str(self.teamname)

class TblTeamMetrics(models.Model):
    metrics_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
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

    def __str__(self):
        return str(self.metrics_id)

class TblTimeTracker(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdatetime = models.DateTimeField(default= datetime.datetime.now())
    trackingdatetime = models.DateField(default= datetime.date.today)
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    teamid = models.ForeignKey(TblTeamMaster, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    categorysid = models.ForeignKey(TblCategorysMaster, models.DO_NOTHING, db_column='categorysid')
    subcategoryid = models.ForeignKey(TblSubcategoryMaster, models.DO_NOTHING, db_column='subcategoryid')
    task = models.CharField(max_length=100)
    requestid = models.ForeignKey(TblRequestdetail, models.DO_NOTHING, db_column='requestid', blank=True, null=True)
    description_text = models.CharField(max_length=255, blank=True, null=True)
    totaltime = models.IntegerField()
    comments = models.CharField(max_length=255, blank=True, null=True)
    startdatetime = models.DateTimeField(blank=True, null=True)
    stopdatetime = models.DateTimeField(blank=True, null=True)
    activityid = models.ForeignKey(TblActivity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)
    otid = models.ForeignKey(TblOtDetail, models.DO_NOTHING, db_column='otid', blank=True, null=True)
    valid_invalid = models.ForeignKey('TblValidInvalidMaster', models.DO_NOTHING, db_column='valid_invalid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_time_tracker'

    def __str__(self):
        return str(self.timetrackerid)


class TblUsefulLinks(models.Model):
    linkid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    teamid = models.ForeignKey(TblTeamMaster, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    memberid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='memberid', blank=True, null=True)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_useful_links'

    def __str__(self):
        return str(self.linkid)


class TblValidInvalidMaster(models.Model):
    valid_invaidid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_valid_invalid_master'

    def __str__(self):
        return str(self.type)


class TblViewTypeMaster(models.Model):
    view_id = models.AutoField(primary_key=True)
    viewname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_view_type_master'

    def __str__(self):
        return str(self.viewname)


class TblYesNo(models.Model):
    optionsid = models.AutoField(primary_key=True)
    optionsname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tbl_yes_no'

    def __str__(self):
        return str(self.optionsname)
