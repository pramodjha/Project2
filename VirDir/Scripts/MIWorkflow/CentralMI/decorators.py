from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy, resolve






def user_permission(function):
    def wrapper(request,*agrs,**kwgrs):
        username = request.user.username
        any_true = []
        list_authorised =['manager','team_leader']
        for arg in range(len(list_authorised)):
            try:
                count = User.objects.filter(username__in=[username]).filter(groups__name__in=[list_authorised[arg]]).count()
                logic = True if count > 0 else False
            except:
                logic = False
            any_true.append(logic)
        count_true = any_true.count(True)
        has_permission = True if count_true >0 else False
        if has_permission == False:
            return HttpResponseRedirect(reverse('signin'))
        else:
            return function(request,*agrs,**kwgrs)
        #return function(*agrs,**kwgrs)
    return wrapper



#    any_true = []
#    for arg in args:
#        try:
#            count = User.objects.filter(groups__name__in=[arg]).count()
#            logic = True if count > 0 else False
#        except:
#            logic = False
#        any_true.append(logic)
#    count_true = any_true.count(True)
#    has_permission = True if count_true >0 else False
#    return has_permission

#def user_permission(*args):
#    def wrapper(*args):
#        any_true = []
#        for arg in args:
#            try:
#                count = User.objects.filter(groups__name__in=[arg]).count()
#                logic = True if count > 0 else False
#            except:
#                logic = False
#                any_true.append(logic)
#                count_true = any_true.count(True)
#                has_permission = True if count_true >0 else False
#        return wrapper
#    return user_permission(has_permission)

#def user_permission():
#    def wrapper(*args):
#        return 'Hello'
#    return wrapper

#greet = user_permission()
#print(greet)
