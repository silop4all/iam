from django.conf.urls import patterns, url, include
from restapi.views import *

endpoints = patterns(
    '',
    url(r'^oauth2/userinfo$',      ProfileAPIview.as_view(),    name="extended_userinfo"),
    url(r'^oauth2/roles$',         RoleAPIview.as_view(),       name="user_roles"),
    url(r'^users$',                UserListAPIview.as_view(),   name="register_user"),
)