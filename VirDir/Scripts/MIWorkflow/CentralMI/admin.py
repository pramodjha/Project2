from django.contrib import admin
from .models import Acceptrejectdetail, Acceptrejectoption, Assigneddetail, Authorisedetail, Authoriserdetail, Completeddetail, Estimationdetail, Mimember, Options, Overviewdetail, Prioritydetail, Requestcategorys, Requestdetail, Requeststatusdetail, Requestsubcategory, Requesttypedetail, Statusdetail, Teamdetail, Timetrackers, Deliverydays, Frequency, Reports,Emaildetail,TimeDetail,Filteroption,Fielddetail

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
    list_display = ('timetrackerid','registerdatetime','trackingdatetime','mimember','teamdetail','requestcategorys','requestsubcategory','task','requestdetail','options','description_text','totaltime','comments','startdatetime','stopdatetime','reports')
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
