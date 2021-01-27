from django.urls import path
from action import views
urlpatterns=[
        path('action/',views.action,name='action'),
        path('actionone/<int:action_id>',views.actionone,name='actionone'),
        path('actioncommen/<int:action_id>',views.actioncommen,name='actioncommen'),
        path('join/<int:action_id>',views.join,name='join')
        ]
