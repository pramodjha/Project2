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
from django.db import models

class Acceptrejectdetail(models.Model):
    estacceptrejectid = models.AutoField(primary_key=True)
    estacceptrejectdate = models.DateTimeField(default= datetime.datetime.now())
    estacceptrejectby = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='estacceptrejectby')
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'acceptrejectdetail'


class Acceptrejectoption(models.Model):
    acceptrejectoptionid = models.AutoField(primary_key=True)
    acceptrejectoptionname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'acceptrejectoption'


class Assigneddetail(models.Model):
    assignedid = models.AutoField(primary_key=True)
    assigneddate = models.DateTimeField(db_column='assignedDate',default= datetime.datetime.now())  # Field name made lowercase.
    assignedto = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='assignedto',related_name='assignedto')
    assignedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='assignedby', related_name='assignedby')
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'assigneddetail'

    def __str__(self):
        return str(self.assignedid)


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
        return self.username

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


class Authorisedetail(models.Model):
    authorisedid = models.AutoField(primary_key=True)
    authoriseddate = models.DateTimeField(default= datetime.datetime.now())
    authoriserdetail = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='authoriserdetail')
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')


    def __str__(self):
        return str(self.authoriserdetail)

    class Meta:
        managed = False
        db_table = 'authorisedetail'


class Authoriserdetail(models.Model):
    authoriserid = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')

    class Meta:
        managed = False
        db_table = 'authoriserdetail'


    def __str__(self):
        return str(self.username)

class Completeddetail(models.Model):
    completedid = models.AutoField(primary_key=True)
    completeddate = models.DateTimeField(default= datetime.datetime.now())
    completedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='completedby')
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'completeddetail'


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

class Designationmaster(models.Model):
    designationid = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'designationmaster'

    def __str__(self):
        return self.designation

class Estimationdetail(models.Model):
    estimationid = models.AutoField(primary_key=True)
    estimationdate = models.DateTimeField(default= datetime.datetime.now())
    estimatedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='estimatedby')
    estimateddays = models.IntegerField()
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'estimationdetail'


    def __str__(self):
        return self.estimatedby

class Mimember(models.Model):
    mimemberid = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail')
    designationmaster = models.ForeignKey(Designationmaster, models.DO_NOTHING, db_column='designationmaster', blank=True, null=True)
    employeeid = models.IntegerField(blank=True, null=True)
    dateofjoining = models.DateField(db_column='DateofJoining', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateofBirth', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.IntegerField(db_column='PhoneNumber', blank=True, null=True)  # Field name made lowercase.
    avatar = models.FileField(upload_to='about_team/',blank=True, null=True)  # Field name made lowercase.
    aboutme = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mimember'

    def __str__(self):
        return str(self.username)

class Options(models.Model):
    optionsid = models.AutoField(primary_key=True)
    optionsname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'options'

    def __str__(self):
        return self.optionsname

class Overviewdetail(models.Model):
    overviewid = models.AutoField(primary_key=True)
    overviewdate = models.DateTimeField(default= datetime.datetime.now())
    providedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='providedby')
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember')
    sopcreatedoptionsid = models.ForeignKey(Options, models.DO_NOTHING, db_column='sopcreatedoptionsid')
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')
    document = models.FileField(upload_to='sopdocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'overviewdetail'


    def __str__(self):
        return str(self.overviewid)


class Prioritydetail(models.Model):
    requestpriorityid = models.AutoField(primary_key=True)
    requestpriority = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'prioritydetail'

    def __str__(self):
        return self.requestpriority


class Requestcategorys(models.Model):
    requestcategoryid = models.AutoField(primary_key=True)
    requestcategorydatetime = models.DateTimeField()
    requestcategorys = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'requestcategorys'

    def __str__(self):
        return self.requestcategorys


class Requestdetail(models.Model):
    requestid = models.AutoField(primary_key=True)
    requestraiseddate = models.DateTimeField(default= datetime.datetime.now())
    requesttypedetail = models.ForeignKey('Requesttypedetail', models.DO_NOTHING, db_column='requesttypedetail')
    prioritydetail = models.ForeignKey(Prioritydetail, models.DO_NOTHING, db_column='prioritydetail')
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    requestdescription = models.TextField()
    requestdocument = models.FileField(upload_to='requestdocument/',blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'requestdetail'
    def __str__(self):
        return str(self.requestid)


class Requeststatusdetail(models.Model):
    requeststatusid = models.AutoField(primary_key=True)
    requeststatusdate = models.DateTimeField(default= datetime.datetime.now())
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    statusdetail = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='statusdetail')
    requestdetail = models.ForeignKey(Requestdetail, models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'requeststatusdetail'

    def __str__(self):
        return str(self.requeststatusid)


class Requestsubcategory(models.Model):
    requestsubcategoryid = models.AutoField(primary_key=True)
    requestsubcategorydatetime = models.DateTimeField(default= datetime.datetime.now())
    requestcategorys = models.ForeignKey(Requestcategorys, models.DO_NOTHING, db_column='requestcategorys')
    requestsubcategory = models.CharField(max_length=100)
    core_noncore = models.CharField(max_length=50)


    class Meta:
        managed = False
        db_table = 'requestsubcategory'


    def __str__(self):
        return self.requestsubcategory


class Requesttypedetail(models.Model):
    requesttypeid = models.AutoField(primary_key=True)
    requesttype = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'requesttypedetail'

    def __str__(self):
        return self.requesttype


class Statusdetail(models.Model):
    statusnameid = models.AutoField(primary_key=True)
    statusname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'statusdetail'

    def __str__(self):
        return self.statusname


class Teamdetail(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamdatetime = models.DateTimeField(default= datetime.datetime.now())
    teamname = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'teamdetail'

    def __str__(self):
        return self.teamname


class Frequency(models.Model):
    frequencyid = models.AutoField(primary_key=True)
    frequency = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'frequency'

    def __str__(self):
        return str(self.frequency)

class Deliverydays(models.Model):
    deliverydaysid = models.AutoField(primary_key=True)
    days = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'deliverydays'

    def __str__(self):
        return str(self.days)

class ReportType(models.Model):
    report_typid = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'report_type'
    def __str__(self):
        return str(self.report_type)



class Reports(models.Model):
    reportid = models.AutoField(primary_key=True)
    registereddate = models.DateTimeField(default= datetime.datetime.now())
    name = models.CharField(max_length=255)
    frequency = models.ForeignKey(Frequency, models.DO_NOTHING, db_column='frequency')
    deliverydays = models.ForeignKey(Deliverydays, models.DO_NOTHING, db_column='deliverydays')
    deliverytime = models.DateTimeField(default= datetime.datetime.now())
    primaryowner = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='primaryowner',related_name='primaryowner')
    secondaryowner = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='secondaryowner',related_name='secondaryowner')
    description = models.CharField(max_length=255, blank=True, null=True)
    delivery_time = models.ForeignKey('TimeDetail', models.DO_NOTHING, db_column='delivery_time')
    report_type = models.ForeignKey(ReportType, models.DO_NOTHING, db_column='report_type')

    class Meta:
        managed = False
        db_table = 'reports'

    def __str__(self):
        return str(self.name)


class TimeDetail(models.Model):
    timeid = models.AutoField(primary_key=True)
    time = models.TextField()

    class Meta:
        managed = False
        db_table = 'time_detail'

    def __str__(self):
        return str(self.time)

class Emaildetail(models.Model):
    emailid = models.AutoField(primary_key=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    emaildate = models.DateTimeField()
    stage = models.TextField()
    emailsubject = models.TextField()
    emailbody = models.TextField()
    emailto = models.TextField()
    emailfrom = models.TextField()
    emailstatus = models.CharField(max_length=255, blank=True, null=True)
    requeststatus = models.CharField(db_column='RequestStatus', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emaildetail'

    def __str__(self):
        return str(self.emailid)


class Filteroption(models.Model):
    filterid = models.AutoField(primary_key=True)
    filteroption = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'filteroption'

    def __str__(self):
        return str(self.filteroption)


class Fielddetail(models.Model):
    fieldid = models.AutoField(primary_key=True)
    tablename = models.CharField(max_length=255)
    fieldname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'fielddetail'

    def __str__(self):
        return str(self.fieldname)

class Errortype(models.Model):
    error_typeid = models.AutoField(primary_key=True)
    error_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'errortype'

    def __str__(self):
        return str(self.error_type)



class FeedbackQuestion(models.Model):
    feedback_questionid = models.AutoField(primary_key=True)
    feedback_questiondate = models.DateTimeField(default= datetime.datetime.now())
    feedback_question = models.CharField(max_length=255)
    feedback_answerdatatype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'feedback_question'


    def __str__(self):
        return str(self.feedback_question)

class OtDetail(models.Model):
    ot_id = models.AutoField(primary_key=True)
    timetrackers = models.ForeignKey('Timetrackers', models.DO_NOTHING, db_column='timetrackers')
    ot_startdatetime = models.DateTimeField()
    ot_enddatetime = models.DateTimeField()
    ot_hrs = models.IntegerField(blank=True, null=True)
    ot_status = models.ForeignKey('OtStatus', models.DO_NOTHING, db_column='ot_status')
    otdocument = models.FileField(upload_to='otdocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ot_detail'

    def __str__(self):
        return str(self.timetrackers)

class OtStatus(models.Model):
    ot_statusid = models.AutoField(primary_key=True)
    ot_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ot_status'


    def __str__(self):
        return str(self.ot_status)


class Activity(models.Model):
    activityid = models.AutoField(primary_key=True)
    registereddate = models.DateTimeField(default= datetime.datetime.now())
    name = models.CharField(max_length=255)
    frequency = models.ForeignKey('Frequency', models.DO_NOTHING, db_column='frequency')
    date_types = models.ForeignKey('DateTypes', models.DO_NOTHING, db_column='date_types')
    delivery_days = models.IntegerField()
    deliverytime = models.TimeField()
    teamname = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamname')
    primaryowner = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='primaryowner', related_name='activityprimaryowner')
    secondaryowner = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='secondaryowner',related_name='activitysecondaryowner')
    description = models.CharField(max_length=255)
    requestcategorys = models.ForeignKey('Requestcategorys', models.DO_NOTHING, db_column='requestcategorys')
    activitystatus = models.ForeignKey('Activitystatus', models.DO_NOTHING, db_column='activitystatus')
    activitydocument = models.FileField(upload_to='activitydocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity'

    def __str__(self):
        return str(self.name)


class Errorlog(models.Model):
    error_id = models.AutoField(primary_key=True)
    errorlog_date = models.DateTimeField(default= datetime.datetime.now())
    error_occurancedate = models.DateField(default= datetime.date.today)
    error_report = models.ForeignKey(Activity, models.DO_NOTHING, db_column='error_report')
    error_reportedby = models.CharField(max_length=50)
    error_reportedteam = models.CharField(max_length=50)
    error_reportedto = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='error_reportedto')
    error_type = models.ForeignKey('Errortype', models.DO_NOTHING, db_column='error_type')
    error_description = models.TextField()
    errordocument = models.FileField(upload_to='errordocument/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errorlog'


    def __str__(self):
        return str(self.error_id)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_date = models.DateTimeField(default= datetime.datetime.now())
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING, db_column='feedback_question')
    feedback_text = models.CharField(max_length=255, blank=True, null=True)
    activity = models.ForeignKey(Activity, models.DO_NOTHING, db_column='activity')

    class Meta:
        managed = False
        db_table = 'feedback'

    def __str__(self):
        return str(self.feedback_question)

class Timetrackers(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdatetime = models.DateTimeField(default= datetime.datetime.now())
    trackingdatetime = models.DateTimeField(default= datetime.datetime.now())
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember')
    teamdetail = models.ForeignKey(Teamdetail, models.DO_NOTHING, db_column='teamdetail')
    requestcategorys = models.ForeignKey(Requestcategorys, models.DO_NOTHING, db_column='requestcategorys')
    requestsubcategory = models.ForeignKey(Requestsubcategory, models.DO_NOTHING, db_column='requestsubcategory')
    task = models.CharField(max_length=100, blank=True, null=True)
    requestdetail = models.ForeignKey(Requestdetail, models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    description_text = models.CharField(max_length=255, blank=True, null=True)
    totaltime = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    startdatetime = models.DateTimeField(blank=True, null=True)
    stopdatetime = models.DateTimeField(blank=True, null=True)
    reports = models.ForeignKey(Activity, models.DO_NOTHING, db_column='reports', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetrackers'

    def __str__(self):
        return str(self.timetrackerid)

class ActivityCalendar(models.Model):
    date = models.DateField(blank=True, null=True)
    daytype = models.CharField(max_length=50, blank=True, null=True)
    weekname = models.CharField(max_length=50, blank=True, null=True)
    cd_wd_days = models.IntegerField(db_column='CD_WD_days', blank=True, null=True)  # Field name made lowercase.
    activityid = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_calendar'

class ActivitystatusCalendar(models.Model):
    activitystatuscalendarid = models.AutoField(primary_key=True)
    activitystatusdate = models.DateTimeField(default= datetime.datetime.now())
    activitystatus = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='activitystatus', blank=True, null=True)
    activityid = models.ForeignKey(Activity, models.DO_NOTHING, db_column='activityid', blank=True, null=True)
    activitycalendardate = models.DateField(default= django.utils.timezone.now)
    reallocatedto = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='reallocatedto', blank=True, null=True, related_name='reallocatedto')
    recordenteredby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='recordenteredby', blank=True, null=True, related_name='recordenteredby')

    class Meta:
        managed = False
        db_table = 'activitystatus_calendar'

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
        db_table = 'tbl_Calendar'




class DateTypes(models.Model):
    date_typesid = models.AutoField(primary_key=True)
    date_types = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'date_types'

    def __str__(self):
        return str(self.date_types)

class Activitystatus(models.Model):
    activitystatusid = models.AutoField(primary_key=True)
    activitystatus = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'activitystatus'

    def __str__(self):
        return str(self.activitystatus)



class TblRawActivityDetail(models.Model):
    raw_activity_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_activity = models.CharField(max_length=50, blank=True, null=True)
    raw_activity_description = models.TextField(blank=True, null=True)
    raw_activity_img = models.FileField(upload_to='rawactivity/',blank=True, null=True)
    raw_activity_scheduled = models.DateField()
    raw_activitystatus = models.ForeignKey(Activitystatus, models.DO_NOTHING, db_column='raw_activitystatus', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_activity_detail'

    def __str__(self):
        return str(self.raw_activity)


class TblRawScore(models.Model):
    raw_score_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_team = models.ForeignKey('TblRawTeamMaster', models.DO_NOTHING, db_column='raw_team', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(db_column='Winner', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_score'

    def __str__(self):
        return str(self.raw_team)

class TblRawTeamMaster(models.Model):
    raw_team_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_team = models.CharField(max_length=255, blank=True, null=True)
    raw_team_icon = models.FileField(upload_to='rawteamicon/',blank=True, null=True)
    raw_team_slogan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_master'


    def __str__(self):
        return str(self.raw_team)

class TblRawTeamMemberMaster(models.Model):
    raw_team_member_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    raw_team = models.ForeignKey(TblRawTeamMaster, models.DO_NOTHING, db_column='raw_team', blank=True, null=True)
    raw_member = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='raw_member', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_raw_team_member_master'


    def __str__(self):
        return str(self.raw_team)

class TblTeamMetrics(models.Model):
    metrics_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    metrics_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_team_metrics'

    def __str__(self):
        return str(self.metrics_name)

class TeamMetrics(models.Model):
    metrics_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail', blank=True, null=True)
    metrics_name = models.ForeignKey(TblTeamMetrics, models.DO_NOTHING, db_column='metrics_name', blank=True, null=True)
    requesttype = models.ForeignKey(Requesttypedetail, models.DO_NOTHING, db_column='requesttype', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_metrics'


class Internaltask(models.Model):
    internaltaskid = models.AutoField(primary_key=True)
    internaltaskdatetime = models.DateTimeField(default= datetime.datetime.now())
    internaltaskquestion = models.CharField(db_column='internaltaskQuestion', max_length=255)  # Field name made lowercase.
    status = models.ForeignKey(Activitystatus, models.DO_NOTHING, db_column='status')
    owner = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='Owner')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'internaltask'

    def __str__(self):
        return str(self.internaltaskquestion)


class Internaltaskchoice(models.Model):
    internaltaskchoiceid = models.AutoField(primary_key=True)
    internaltaskchoicedatetime = models.DateTimeField(default= datetime.datetime.now())
    internaltaskchoice = models.CharField(max_length=255)
    internaltask = models.ForeignKey(Internaltask, models.DO_NOTHING, db_column='internaltask')

    class Meta:
        managed = False
        db_table = 'internaltaskchoice'


    def __str__(self):
        return str(self.internaltaskchoice)

class Internaltaskstatus(models.Model):
    internaltaskstatusid = models.AutoField(primary_key=True)
    internaltaskstatusdatetime = models.DateTimeField(default= datetime.datetime.now())
    mimember = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='mimember')
    internaltask = models.ForeignKey(Internaltask, models.DO_NOTHING, db_column='internaltask')
    internaltaskchoice = models.ForeignKey(Internaltaskchoice, models.DO_NOTHING, db_column='internaltaskchoice')

    class Meta:
        managed = False
        db_table = 'internaltaskstatus'

class Whatwedo(models.Model):
    recordid = models.AutoField(primary_key=True)
    data = models.CharField(db_column='Data', max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=100)  # Field name made lowercase.
    image = models.FileField(upload_to='whatwedo/',blank=True, null=True) # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'whatwedo'


    def __str__(self):
        return str(self.data)


class Reply(models.Model):
    replydatetime = models.DateTimeField()
    replyid = models.AutoField(primary_key=True)
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    reply = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'reply'

    def __str__(self):
        return str(self.reply)


class Suggestion(models.Model):
    suggestiondatetime = models.DateTimeField(default= datetime.datetime.now())
    suggestionid = models.AutoField(primary_key=True)
    suggestedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='suggestedby', blank=True, null=True)
    suggestion = models.TextField()
    subject = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'suggestion'

    def __str__(self):
        return str(self.subject)


class SuccessStories(models.Model):
    storiesdatetime = models.DateTimeField(default= datetime.datetime.now())
    storiesid = models.AutoField(primary_key=True)
    stories = models.TextField()

    class Meta:
        managed = False
        db_table = 'success_stories'


    def __str__(self):
        return str(self.stories)


class Governance(models.Model):
    governancedatetime = models.DateTimeField(default= datetime.datetime.now())
    governanceid = models.AutoField(primary_key=True)
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail')
    processimg = models.FileField(upload_to='governanceprocess/',blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'governance'

    def __str__(self):
        return str(self.governanceid)


class TblNavbarFooterMaster(models.Model):
    navbar_footer_id = models.AutoField(primary_key=True)
    navbar_footer_name = models.CharField(max_length=255, blank=True, null=True)
    navbar_header_url = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)

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

class TblConversation(models.Model):
    conversationid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    requestdetail = models.ForeignKey(Requestdetail, models.DO_NOTHING, db_column='requestdetail')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    comments = models.TextField()

    class Meta:
        managed = False
        db_table = 'tbl_conversation'



class TblLeaveRecord(models.Model):
    leaverecordid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    leave_date = models.DateField()
    userid = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='userid')
    leave_type = models.ForeignKey('TblLeaveType', models.DO_NOTHING, db_column='leave_type')

    class Meta:
        managed = False
        db_table = 'tbl_leave_record'

    def __str__(self):
        return str(self.leaverecordid)

class TblLeaveType(models.Model):
    leavetypeid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    leave_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_leave_type'

    def __str__(self):
        return str(self.leave_type)

class UatDetail(models.Model):
    uatid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    uat_status = models.ForeignKey('UatStatus', models.DO_NOTHING, db_column='UAT_status', blank=True, null=True)  # Field name made lowercase.
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')
    testedby = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='testedby', blank=True, null=True, related_name='testedby')
    updatedby = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='updatedby', blank=True, null=True,related_name='updatedby')

    class Meta:
        managed = False
        db_table = 'UAT_detail'

class UatStatus(models.Model):
    uat_status_id = models.AutoField(db_column='UAT_status_id', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField(default= datetime.datetime.now())
    uat_status = models.CharField(db_column='UAT_status', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UAT_status'

    def __str__(self):
        return str(self.uat_status)


class TblAppreciation(models.Model):
    appreciationid = models.AutoField(db_column='Appreciationid', primary_key=True)  # Field name made lowercase.
    date_time = models.DateTimeField(default= datetime.datetime.now())
    appreciated_to = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='Appreciated_to', blank=True, null=True)  # Field name made lowercase.
    appreciated_by = models.CharField(db_column='Appreciated_by', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    appreciation_status = models.ForeignKey(Activitystatus, models.DO_NOTHING, db_column='appreciation_status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_Appreciation'


class TblUsefulLinks(models.Model):
    linkid = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(default= datetime.datetime.now())
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail', blank=True, null=True)
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_useful_links'


class AssignView(models.Model):
    viewassign_id = models.AutoField(primary_key=True)
    group_name = models.ForeignKey('AuthGroup', models.DO_NOTHING, db_column='group_name')
    view_type = models.ForeignKey('ViewType', models.DO_NOTHING, db_column='view_type')

    class Meta:
        managed = False
        db_table = 'assign_view'

    def __str__(self):
        return str(self.group_name)

class TblNavbarView(models.Model):
    navbar_id = models.AutoField(primary_key=True)
    view_type = models.ForeignKey('ViewType', models.DO_NOTHING, db_column='view_type')
    navbar_header = models.ForeignKey(TblNavbarHeaderMaster, models.DO_NOTHING)
    navbar_footer = models.ForeignKey(TblNavbarFooterMaster, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tbl_navbar_view'

    def __str__(self):
        return str(self.navbar_header)


class TeamMetricsData(models.Model):
    metrics_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail', blank=True, null=True)
    requesttype = models.ForeignKey(Requesttypedetail, models.DO_NOTHING, db_column='requesttype', blank=True, null=True)
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    wip = models.IntegerField(db_column='WIP', blank=True, null=True)  # Field name made lowercase.
    uat = models.IntegerField(db_column='UAT', blank=True, null=True)  # Field name made lowercase.
    completed = models.IntegerField(db_column='Completed', blank=True, null=True)  # Field name made lowercase.
    project = models.IntegerField(db_column='Project', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'team_metrics_data'

    def __str__(self):
        return str(self.metrics_id)

class ViewType(models.Model):
    view_id = models.AutoField(primary_key=True)
    viewname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_type'

    def __str__(self):
        return str(self.viewname)
