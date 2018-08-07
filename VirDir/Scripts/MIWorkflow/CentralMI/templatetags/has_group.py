from django import template
from django.contrib.auth.models import Group


register = template.Library()
@register.filter(name='has_group')
def has_group(user,group_name):
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except:
        return False


#def user_permission(*args):
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
