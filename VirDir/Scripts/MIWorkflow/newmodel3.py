# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Acceptrejectoption(models.Model):
    acceptrejectoptionid = models.AutoField(db_column='AcceptRejectOptionId', primary_key=True)  # Field name made lowercase.
    acceptrejectoptionname = models.CharField(db_column='AcceptRejectOptionName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AcceptRejectOption'


class Acceptrejectdetail(models.Model):
    estacceptrejectid = models.AutoField(db_column='EstAcceptRejectID', primary_key=True)  # Field name made lowercase.
    estacceptrejectdate = models.DateTimeField(db_column='EstAcceptRejectDate')  # Field name made lowercase.
    estacceptrejectby = models.CharField(db_column='EstAcceptRejectBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    estacceptrejectoption = models.ForeignKey(Acceptrejectoption, models.DO_NOTHING, db_column='EstAcceptRejectOption', blank=True, null=True)  # Field name made lowercase.
    requeststatus = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='RequestStatus', blank=True, null=True)  # Field name made lowercase.
    estacceptrejectintid = models.CharField(db_column='EstAcceptRejectIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AcceptRejectdetail'


class Options(models.Model):
    optionsid = models.AutoField(db_column='OptionsId', primary_key=True)  # Field name made lowercase.
    optionsname = models.CharField(db_column='OptionsName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Options'


class Requestcategory(models.Model):
    requestsubcategoryid = models.AutoField(db_column='RequestSubcategoryID', primary_key=True)  # Field name made lowercase.
    requestsubcategory = models.CharField(db_column='RequestSubCategory', unique=True, max_length=50)  # Field name made lowercase.
    requestcategory = models.CharField(db_column='RequestCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    core_noncore = models.CharField(db_column='Core_NonCore', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RequestCategory'


class Requestprioritydetail(models.Model):
    requestpriorityid = models.AutoField(db_column='RequestPriorityId', primary_key=True)  # Field name made lowercase.
    requestpriorityname = models.CharField(db_column='RequestPriorityName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RequestPrioritydetail'


class RequestSubcategory(models.Model):
    requestsubcategoryid = models.AutoField(db_column='RequestSubCategoryID', primary_key=True)  # Field name made lowercase.
    requestsubcategorydatetime = models.DateTimeField(db_column='RequestSubCategoryDatetime')  # Field name made lowercase.
    requestsubcat = models.CharField(db_column='RequestSubCat', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Request_SubCategory'


class Requestassigneddetail(models.Model):
    requestassignedid = models.AutoField(db_column='RequestAssignedID', primary_key=True)  # Field name made lowercase.
    requestassigneddate = models.DateTimeField(db_column='RequestAssignedDate')  # Field name made lowercase.
    requestassignedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='RequestAssignedBy', blank=True, null=True)  # Field name made lowercase.
    requestassignedto = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='RequestAssignedTo', blank=True, null=True)  # Field name made lowercase.
    requestassignedintid = models.CharField(db_column='RequestAssignedIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Requestassigneddetail'


class Requeststatusdetail(models.Model):
    requeststatusid = models.AutoField(db_column='RequestStatusID', primary_key=True)  # Field name made lowercase.
    requeststatusdate = models.DateTimeField(db_column='RequestStatusDate')  # Field name made lowercase.
    requeststatuschangeby = models.CharField(db_column='RequestStatusChangeBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    requeststatus = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='RequestStatus', blank=True, null=True)  # Field name made lowercase.
    requeststatusintid = models.CharField(db_column='RequestStatusIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Requeststatusdetail'


class Timetracker(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdate = models.DateTimeField()
    trackingdate = models.DateTimeField()
    requestsubcat = models.ForeignKey(Requestcategory, models.DO_NOTHING, db_column='requestsubcat', blank=True, null=True)
    requestid_mir = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestid_mir', blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    request_status = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='request_status', blank=True, null=True)
    timeinvested = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TimeTracker'


class Timetrackers(models.Model):
    timetrackerid = models.AutoField(primary_key=True)
    registerdatetime = models.DateTimeField()
    trackingdatetime = models.DateTimeField()
    mimember = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    teamname = models.ForeignKey('Teamname', models.DO_NOTHING, db_column='teamname', blank=True, null=True)
    requestcategorys = models.ForeignKey('Requestcategorys', models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    requestsubcategory = models.ForeignKey('Requestsubcategory', models.DO_NOTHING, db_column='requestsubcategory', blank=True, null=True)
    task = models.CharField(max_length=100, blank=True, null=True)
    requestdetail = models.ForeignKey('Requestdetail', models.DO_NOTHING, db_column='requestdetail', blank=True, null=True)
    options = models.ForeignKey(Options, models.DO_NOTHING, db_column='Options', blank=True, null=True)  # Field name made lowercase.
    discription = models.CharField(db_column='Discription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totaltime = models.FloatField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    startdatetime = models.DateTimeField(blank=True, null=True)
    stopdatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TimeTrackers'


class Activitydetail(models.Model):
    statusid = models.AutoField(db_column='StatusId', primary_key=True)  # Field name made lowercase.
    statuschangedate = models.DateTimeField(db_column='StatusChangeDate')  # Field name made lowercase.
    activitystatusnameid = models.ForeignKey('Statusdetail', models.DO_NOTHING, db_column='ActivityStatusNameId', blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.
    activityintid = models.CharField(db_column='ActivityIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'activitydetail'


class Adhocactivity(models.Model):
    adhocid = models.AutoField(db_column='AdhocId', primary_key=True)  # Field name made lowercase.
    adhoctypeid = models.ForeignKey('Adhoctypedetail', models.DO_NOTHING, db_column='AdhocTypeId', blank=True, null=True)  # Field name made lowercase.
    adhoctimespent = models.IntegerField(db_column='AdhocTimeSpent', blank=True, null=True)  # Field name made lowercase.
    ahdocrequestedby = models.CharField(db_column='AhdocRequestedBy', max_length=50)  # Field name made lowercase.
    adhocintid = models.CharField(db_column='AdhocIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adhocactivity'


class Adhoctypedetail(models.Model):
    adhoctypeid = models.AutoField(db_column='AdhocTypeId', primary_key=True)  # Field name made lowercase.
    adhoctypename = models.CharField(db_column='AdhocTypeName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adhoctypedetail'


class Assigneddetail(models.Model):
    assignedid = models.AutoField(db_column='AssignedId', primary_key=True)  # Field name made lowercase.
    assignedname = models.CharField(db_column='AssignedName', unique=True, max_length=100)  # Field name made lowercase.

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
    authorisedid = models.AutoField(db_column='AuthorisedId', primary_key=True)  # Field name made lowercase.
    authoriseddate = models.DateTimeField(db_column='AuthorisedDate')  # Field name made lowercase.
    authorisedoptionsid = models.ForeignKey(Options, models.DO_NOTHING, db_column='AuthorisedOptionsId', blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.
    authorisedintid = models.CharField(db_column='AuthorisedIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    authorisedby = models.ForeignKey('Authoriserdetail', models.DO_NOTHING, db_column='Authorisedby', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authorisedetail'


class Authoriserdetail(models.Model):
    authoriserid = models.AutoField(db_column='AuthoriserId', primary_key=True)  # Field name made lowercase.
    authorisername = models.CharField(db_column='AuthoriserName', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authoriserdetail'


class Completeddetail(models.Model):
    completedid = models.AutoField(db_column='CompletedId', primary_key=True)  # Field name made lowercase.
    completeddate = models.DateTimeField(db_column='CompletedDate')  # Field name made lowercase.
    completedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='CompletedBy', blank=True, null=True)  # Field name made lowercase.
    completedintid = models.CharField(db_column='CompletedIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.

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


class Estimationdetail(models.Model):
    estimationid = models.AutoField(db_column='EstimationId', primary_key=True)  # Field name made lowercase.
    estimationdate = models.DateTimeField(db_column='EstimationDate')  # Field name made lowercase.
    estimationtypeid = models.ForeignKey('Estimationtypedetail', models.DO_NOTHING, db_column='EstimationTypeId', blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.
    estimationintid = models.CharField(db_column='EstimationIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    estimatedby = models.ForeignKey('Mimember', models.DO_NOTHING, db_column='EstimatedBy', blank=True, null=True)  # Field name made lowercase.
    proposeddate = models.DateTimeField(db_column='ProposedDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estimationdetail'


class Estimationtypedetail(models.Model):
    estimationtypeid = models.AutoField(db_column='EstimationTypeId', primary_key=True)  # Field name made lowercase.
    estimationtypename = models.CharField(db_column='EstimationTypeName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estimationtypedetail'


class Mimember(models.Model):
    mimemberid = models.AutoField(db_column='MiMemberId', primary_key=True)  # Field name made lowercase.
    mimembername = models.CharField(db_column='MiMemberName', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mimember'


class Overviewdetail(models.Model):
    overviewid = models.AutoField(db_column='OverViewId', primary_key=True)  # Field name made lowercase.
    overviewdate = models.DateTimeField(db_column='OverViewDate')  # Field name made lowercase.
    providedby = models.CharField(db_column='Providedby', max_length=50)  # Field name made lowercase.
    sopcreatedoptionsid = models.ForeignKey(Options, models.DO_NOTHING, db_column='SOPCreatedOptionsId', blank=True, null=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestId', blank=True, null=True)  # Field name made lowercase.
    overviewintid = models.CharField(db_column='OverViewIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    givento = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='Givento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'overviewdetail'


class Priodetail(models.Model):
    prioritynameid = models.AutoField(primary_key=True)
    priorityname = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'priodetail'


class Requestcategorys(models.Model):
    requestcategoryid = models.AutoField(primary_key=True)
    requestcategorydatetime = models.DateTimeField()
    requestcategorys = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requestcategorys'


class Requestdetail(models.Model):
    requestid = models.AutoField(db_column='RequestId', primary_key=True)  # Field name made lowercase.
    requestraiseddate = models.DateTimeField(db_column='RequestRaisedDate')  # Field name made lowercase.
    requesttypeid = models.ForeignKey('Requesttypedetail', models.DO_NOTHING, db_column='RequestTypeId', blank=True, null=True)  # Field name made lowercase.
    requestpriorityid = models.ForeignKey(Requestprioritydetail, models.DO_NOTHING, db_column='RequestPriorityId', blank=True, null=True)  # Field name made lowercase.
    requestowner = models.CharField(db_column='RequestOwner', max_length=100)  # Field name made lowercase.
    requestdescription = models.CharField(db_column='RequestDescription', max_length=255)  # Field name made lowercase.
    dateforcompletion = models.DateTimeField(db_column='DateforCompletion')  # Field name made lowercase.
    requestintid = models.CharField(db_column='RequestIntId', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requestdetail'


class Requestsubcategory(models.Model):
    requestsubcategoryid = models.AutoField(primary_key=True)
    requestsubcategorydatetime = models.DateTimeField()
    requestcategorys = models.ForeignKey(Requestcategorys, models.DO_NOTHING, db_column='requestcategorys', blank=True, null=True)
    requestcubcategory = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requestsubcategory'


class Requesttypedetail(models.Model):
    requesttypeid = models.AutoField(db_column='RequestTypeId', primary_key=True)  # Field name made lowercase.
    requesttypename = models.CharField(db_column='RequestTypeName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requesttypedetail'


class Statusdetail(models.Model):
    statusnameid = models.AutoField(db_column='StatusNameId', primary_key=True)  # Field name made lowercase.
    statusname = models.CharField(db_column='StatusName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'statusdetail'


class Teamname(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamdatetime = models.DateTimeField()
    mimember = models.ForeignKey(Mimember, models.DO_NOTHING, db_column='mimember', blank=True, null=True)
    teamname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teamname'
