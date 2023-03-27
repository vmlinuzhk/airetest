from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.home, name='home'),
    path('bug/<int:bugid>', views.bug, name='bug'),
    path('newbug', views.newbug, name='newbug'),
    path('closebug/<int:bugid>', views.closebug, name='closebug'),
    path('person', views.person, name='person'),
    path('newperson', views.newperson, name='newperson'),
    path('api/bugs', api.bugs, name='api_bugs'),
    path('api/bug/<int:bugid>', api.bug, name='api_bug'),
    path('api/bug', api.newbug, name='api_newbug'),
    path('api/people', api.people, name='api_people'),
    path('api/person/<int:personid>', api.person, name='api_person'),
    path('api/person', api.newperson, name='api_newperson'),
]
