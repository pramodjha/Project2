# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Acceptrejectdetail(models.Model):
    estacceptrejectid = models.AutoField(primary_key=True)
    estacceptrejectdate = models.DateTimeField()
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
    assigneddate = models.DateTimeField(db_column='assignedDate')  # Field name made lowercase.
    assignedto = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='assignedto', blank=True, null=True)
    assignedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='assignedby', blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'assigneddetail'


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


class Authorisedetail(models.Model):
    authorisedid = models.AutoField(primary_key=True)
    authoriseddate = models.DateTimeField()
    authoriserdetail = models.ForeignKey('Authoriserdetail', models.DO_NOTHING, db_column='authoriserdetail', blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'authorisedetail'


class Authoriserdetail(models.Model):
    authoriserid = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')

    class Meta:
        managed = False
        db_table = 'authoriserdetail'


class Completeddetail(models.Model):
    completedid = models.AutoField(primary_key=True)
    completeddate = models.DateTimeField()
    completedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='completedby', blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'completeddetail'


class Deliverydays(models.Model):
    deliverydaysid = models.AutoField(primary_key=True)
    days = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deliverydays'


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
    requeststatus = models.CharField(db_column='RequestStatus', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'emaildetail'


class Estimationdetail(models.Model):
    estimationid = models.AutoField(primary_key=True)
    estimationdate = models.DateTimeField()
    estimatedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='estimatedby', blank=True, null=True)
    estimateddays = models.IntegerField(blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'estimationdetail'


class Frequency(models.Model):
    frequencyid = models.AutoField(primary_key=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frequency'


class Mimember(models.Model):
    mimemberid = models.AutoField(primary_key=True)
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    teamdetail = models.ForeignKey('Teamdetail', models.DO_NOTHING, db_column='teamdetail')

    class Meta:
        managed = False
        db_table = 'mimember'


class Options(models.Model):
    optionsid = models.AutoField(primary_key=True)
    optionsname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'options'


class Overviewdetail(models.Model):
    overviewid = models.AutoField(primary_key=True)
    overviewdate = models.DateTimeField()
    providedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='providedby')
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    sopcreatedoptionsid = models.ForeignKey(Options, models.DO_NOTHING, db_column='sopcreatedoptionsid', blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail')
    document = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'overviewdetail'


class Prioritydetail(models.Model):
    requestpriorityid = models.AutoField(primary_key=True)
    requestpriority = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'prioritydetail'


class Reports(models.Model):
    reportid = models.AutoField(primary_key=True)
    registereddate = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.ForeignKey(Frequency, models.DO_NOTHING, db_column='frequency', blank=True, null=True)
    deliverydays = models.ForeignKey(Deliverydays, models.DO_NOTHING, db_column='deliverydays', blank=True, null=True)
    deliverytime = models.DateTimeField()
    primaryowner = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='primaryowner', blank=True, null=True)
    secondaryowner = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='secondaryowner', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    delivery_time = models.ForeignKey('TimeDetail', models.DO_NOTHING, db_column='delivery_time', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'


class Requestcategorys(models.Model):
    requestcategoryid = models.AutoField(primary_key=True)
    requestcategorydatetime = models.DateTimeField()
    requestcategorys = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requestcategorys'


class Requestdetail(models.Model):
    requestid = models.AutoField(primary_key=True)
    requestraiseddate = models.DateTimeField()
    requesttypedetail = models.ForeignKey('Requesttypedetail', models.DO_NOTHING, db_column='requesttypedetail')
    prioritydetail = models.ForeignKey(Prioritydetail, models.DO_NOTHING, db_column='prioritydetail')
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    requestdescription = models.TextField()

    class Meta:
        managed = False
        db_table = 'requestdetail'


class Requeststatusdetail(models.Model):
    requeststatusid = models.AutoField(primary_key=True)
    requeststatusdate = models.DateTimeField()
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username')
    statusdetail = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='statusdetail', blank=True, null=True)
    requestdetail = models.ForeignKey(Requestdetail, models.DO_NOTHING, db_column='requestdetail')

    class Meta:
        managed = False
        db_table = 'requeststatusdetail'


class Requestsubcategory(models.Model):
    requestsubcategoryid = models.AutoField(primary_key=True)
    requestsubcategorydatetime = models.DateTimeField()
    requestcategorys = models.ForeignKey(Requestcategorys, models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    requestsubcategory = models.CharField(max_length=100, blank=True, null=True)
    core_noncore = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requestsubcategory'


class Requesttypedetail(models.Model):
    requesttypeid = models.AutoField(primary_key=True)
    requesttype = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'requesttypedetail'


class Statusdetail(models.Model):
    statusnameid = models.AutoField(primary_key=True)
    statusname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'statusdetail'


class Teamdetail(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamdatetime = models.DateTimeField()
    teamname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teamdetail'


class TimeDetail(models.Model):
    timeid = models.AutoField(primary_key=True)
    time = models.TextField()

    class Meta:
        managed = False
        db_table = 'time_detail'


class Timetrackers(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdatetime = models.DateTimeField()
    trackingdatetime = models.DateTimeField()
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    teamdetail = models.ForeignKey(Teamdetail, models.DO_NOTHING, db_column='teamdetail', blank=True, null=True)
    requestcategorys = models.ForeignKey(Requestcategorys, models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    requestsubcategory = models.ForeignKey(Requestsubcategory, models.DO_NOTHING, db_column='requestsubcategory', blank=True, null=True)
    task = models.CharField(max_length=100, blank=True, null=True)
    requestdetail = models.ForeignKey(Requestdetail, models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    options = models.ForeignKey(Options, models.DO_NOTHING, db_column='options', blank=True, null=True)
    description_text = models.CharField(max_length=255, blank=True, null=True)
    totaltime = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    startdatetime = models.DateTimeField(blank=True, null=True)
    stopdatetime = models.DateTimeField(blank=True, null=True)
    reports = models.ForeignKey(Reports, models.DO_NOTHING, db_column='reports', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetrackers'
