from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from user.models import *
# Create your views here.
def action(request):
    action=Action.objects.all()
    return render(request,'action/action.html',{'action':action})
def actionone(request,action_id):
    action=Action.objects.get(id=action_id)
    commen=action.actioncommen_set.all()
    return render(request,'action/actionone.html',{'action':action,'commen':commen})
def actioncommen(request,action_id):
    action=Action.objects.get(id=action_id)
    user=User.objects.get(id=request.session.get('user_id'))
    commen=request.POST['commen']
    ActionCommen.objects.create(user=user,action=action,commen=commen)
    return HttpResponseRedirect(reverse('actionone',args=(action_id,)))
def join(request,action_id):
    action=Action.objects.get(id=action_id)
    print(action)
    user=User.objects.get(id=request.session.get('user_id'))
    if not action.new.filter(name=user.name):
        action.new.add(user)
        return render(request,'action/actionone.html',{'action':action,'message':True})
    else:
        return render(request,'action/actionone.html',{'action':action,'message':False})
