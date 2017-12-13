"""
Definition of urls for IdentityAccessManager.
"""

from datetime import datetime
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from app import urls
from restapi import urls as rurls

urlpatterns = patterns('',
    url(r'^',                   include(urls.endpoints)),
    url(r'^',                   include(urls.private_api,   namespace="private_api")),
    url(r'^api/',               include(rurls.endpoints,    namespace='public_api')),
    url(r'^docs/',              include('rest_framework_swagger.urls', namespace="docs")), 
    url(r'^api-auth/',          include('rest_framework.urls',  namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# change the http.conf from /static -> /prosperity4all/identity-access-manager/static
#urlpatterns = patterns('',
#    url(r'^prosperity4all/identity-access-manager/',                   include(urls.endpoints)),
#    url(r'^prosperity4all/identity-access-manager/',                   include(urls.private_api,   namespace="private_api")),
#    url(r'^prosperity4all/identity-access-manager/api/',               include(rurls.endpoints,    namespace='public_api')),
#    url(r'^prosperity4all/identity-access-manager/docs/',              include('rest_framework_swagger.urls', namespace="docs")), 
#    url(r'^prosperity4all/identity-access-manager/api-auth/',          include('rest_framework.urls',  namespace='rest_framework')),
#) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)