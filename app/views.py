from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponseServerError, JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from django.db.models import Avg, Sum, Q
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings

from rest_framework import generics, filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from app.models import *
from app.openam import *
from app.serializers import *
from app.utilities import *
from app.decorators import *
from app.FileStorage import *

from functools import wraps
from datetime import datetime   # date/time module
import json                     # json lib
import urllib
from traceback import print_exc
import pycountry
import copy

import logging
logger = logging.getLogger(__name__)


class LoginView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            if 'tokenId' in request.COOKIES:
                ows = OpenAM()
                state, response = ows.validateTokenId(
                    request.COOKIES['tokenId'])
                jResponse = json.loads(response)
                if jResponse['valid'] == True:
                    return redirect(reverse('dashboard_form'), permanent=True)

            return render(request,
                          'app/login.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Sign In",
                                                              'error': None
                                                          }))

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            # return Response(data={"message": str(e), "code":
            # status.HTTP_400_BAD_REQUEST, "reason": "Bad request"},
            # status=status.HTTP_400_BAD_REQUEST)
            raise Http404


class AuthorizeApplicationView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            if 'client_id' in request.GET and 'redirect_uri' in request.GET:
                app = Application.objects.get(
                    client_id__exact=request.GET['client_id'])

                return render(request,
                              'app/authorization.html',
                              context_instance=RequestContext(request,
                                                              {
                                                                  'title': "Sign In",
                                                                  "client_id": request.GET['client_id'],
                                                                  "redirect_uri": request.GET['redirect_uri'],
                                                                  "app": app
                                                              }))
            else:
                return redirect(reverse('login_form'), permanent=True)

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            raise Http404


class EmailForm(View):

    template = 'app/registration/preprocess.html'

    def get(self, request):
        """Render the template in which candidate user can enter his email account for further information"""
        try:
            assert isinstance(request, HttpRequest)
            return render(request, self.template,
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Register your account"
                                                          }))

        except Exception, e:
            logger.exception(str(e))
            raise Http404


class RegistrationView(View):

    template = 'app/registration/index.html'

    def get(self, request):
        """Render the template where the user is able to complete the registration"""
        try:
            assert isinstance(request, HttpRequest)

            mail = None
            data = request.GET
            if 'activationId' in data.keys() and 'email' in data.keys():
                mail = data['email']
                if not RegistrationRequest.objects.filter(uuid=data['activationId'], mail=data['email'], status=0).count():
                    return redirect(reverse('signup_request_form'))
            else:
                return redirect(reverse('signup_request_form'))

            # update operation between 2 integer
            from random import randint
            literal = str(randint(0, 6)) + "+" + str(randint(0, 4))

            return render(request, self.template,
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Register your account",
                                                              'CountriesList': pycountry.countries,
                                                              'LanguagesList': pycountry.languages,
                                                              'literal': literal,
                                                              'openam_url': settings.OPENAM_HOST,
                                                              'mail': mail
                                                          }))

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            raise Http404


class ProfileView(View):

    template = 'app/dashboard/profile-preview.html'

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)
            username = request.COOKIES.get('username')
            tokenId = request.COOKIES.get('tokenId')

            iamp = Profile.objects.get(username__exact=username)
            ows = OpenAM()
            status, data = ows.retrieveUserProfile(username, tokenId)
            openamp = json.loads(data)

            preferedLang = "Not available"
            if 'sunIdentityServerPPDemographicsDisplayLanguage'in openamp:
                preferedLang = pycountry.languages.get(iso639_3_code=str(
                    openamp['sunIdentityServerPPDemographicsDisplayLanguage'][0])).name

            return render(request, self.template,
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "My account",
                                                              'iamp': iamp,
                                                              'prefered_language': preferedLang,
                                                              'openamp': openamp,
                                                              'username': username,
                                                              'logoPrefixUrl': settings.LOGO_URL
                                                          })
                          )

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            raise Http404


class ProfileUpdateView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)
            username = request.COOKIES.get('username')
            tokenId = request.COOKIES.get('tokenId')

            iamp = Profile.objects.get(username__exact=username)
            ows = OpenAM()
            status, data = ows.retrieveUserProfile(username, tokenId)
            openamp = json.loads(data)

            return render(request,
                          'app/dashboard/profile-update.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Edit your account",
                                                              'iamp': iamp,
                                                              'openamp': openamp,
                                                              'username': username,
                                                              'CountriesList': getCountriesList(),
                                                              'LanguagesList': pycountry.languages,
                                                              'logoPrefixUrl': settings.LOGO_URL
                                                          })
                          )

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            raise Http404


class ProfileChangePwdView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            return render(request,
                          'app/dashboard/profile-change-pwd.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Change your password",
                                                              'username': request.COOKIES.get('username')
                                                          }))

        except Exception, e:
            logger.exception(str(e))
            print_exc()
            raise Http404


class DashboardView(View):

    template = 'app/dashboard/index.html'

    def get(self, request):
        try:
            user = Profile.objects.get(
                username__exact=request.COOKIES.get('username'))
            membership = ApplicationMembership.objects.filter(
                member__id=user.id).values_list('application', flat=True)
            applications = Application.objects.all()

            return render(request, self.template,                          
                          context_instance=RequestContext(request,
                                                          {

                                                              'title': "Welcome on P4all IAM",
                                                              'applications': applications,
                                                              'membership': membership,
                                                              'username': request.COOKIES.get('username')
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationListView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            return render(request,
                          'app/dashboard/applications.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "My applications",
                                                              'username': request.COOKIES.get('username'),
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationCreateView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            return render(request,
                          'app/dashboard/application-registration.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Register your application",
                                                              'username': request.COOKIES.get('username'),
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationPreView(View):

    def get(self, request, clientId):
        try:
            assert isinstance(request, HttpRequest)

            ows = OpenAM()
            authentication = ows.authenticateAdmin()
            tokenId = json.loads(authentication[1])["tokenId"]
            state, app = ows.retrieveClient(tokenId, clientId)

            return render(request,
                          'app/dashboard/application-preview.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "View your application",
                                                              'application': Application.objects.get(client_id__exact=clientId),
                                                              'username': request.COOKIES.get('username'),
                                                              'clientId': clientId,
                                                              'clientSecret': json.loads(app)['userpassword'][0],
                                                              'clientType': json.loads(app)['com.forgerock.openam.oauth2provider.clientType'][0],
                                                              'clientContact': json.loads(app)['com.forgerock.openam.oauth2provider.contacts'][0].split('=')[1],
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationUpdateView(View):

    def get(self, request, clientId):
        try:
            assert isinstance(request, HttpRequest)

            ows = OpenAM()
            authentication = ows.authenticateAdmin()
            tokenId = json.loads(authentication[1])["tokenId"]
            state, app = ows.retrieveClient(tokenId, clientId)

            return render(request,
                          'app/dashboard/application-registration.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Edit your application",
                                                              'application': Application.objects.get(client_id__exact=clientId),
                                                              'username': request.COOKIES.get('username'),
                                                              'clientId': clientId,
                                                              'mail': json.loads(app)['com.forgerock.openam.oauth2provider.contacts'][0].split('=')[1],
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationRolesView(View):

    def get(self, request, clientId):
        try:
            assert isinstance(request, HttpRequest)

            roles = Role.objects.all()
            app = Application.objects.get(client_id=clientId)
            appRoles = ApplicationRole.objects.filter(
                application=app).values_list('role', flat=True)

            return render(request,
                          'app/dashboard/application-roles.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Manage roles",
                                                              'username': request.COOKIES.get('username'),
                                                              'app': app,
                                                              'roles': roles,
                                                              'appRoles':  appRoles
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationAuthMembersView(View):

    def get(self, request, clientId):
        try:
            assert isinstance(request, HttpRequest)
            app = Application.objects.get(client_id=clientId)
            membershipList = ApplicationMembership.objects.filter(
                application__id=app.id).values_list('member', flat=True)
            members = Profile.objects.filter(pk__in=membershipList)

            return render(request,
                          'app/dashboard/application-authorized-members.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Members",
                                                              'username': request.COOKIES.get('username'),
                                                              'app': app,
                                                              'members': members,
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class ApplicationsListView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            applications = Application.objects.all()
            appOwnerList = ApplicationOwner.objects.filter(user__username=request.COOKIES.get(
                'username')).values_list('application', flat=True)
            appMemberList = ApplicationMembership.objects.filter(
                member__username=request.COOKIES.get('username')).values_list('application', flat=True)

            return render(request,
                          'app/dashboard/authorized-applications.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Available Applications",
                                                              'username': request.COOKIES.get('username'),
                                                              'apps': applications,
                                                              'appOwnerList': appOwnerList,
                                                              'appMemberList': appMemberList
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class AuthorizedApplicationRolesView(View):

    def get(self, request, clientId):
        try:
            assert isinstance(request, HttpRequest)
            member = Profile.objects.get(
                username=request.COOKIES.get('username'))
            application = Application.objects.get(client_id=clientId)
            applicationRoles = ApplicationRole.objects.filter(
                application=application)
            try:
                applicationMember = ApplicationMembership.objects.get(
                    member=member, application=application)
            except ApplicationMembership.DoesNotExist:
                applicationMember = None
            memberHasRoles  = ApplicationMemberHasRole.objects.filter(application_role__in=applicationRoles.values_list('id', flat=True), application_member=applicationMember).\
                values_list('application_role', flat=True)

            return render(request,
                          'app/dashboard/authorized-applications-member-has-role.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Declare your role(s)",
                                                              'username': member.username,
                                                              'application': application,
                                                              'applicationRoles': applicationRoles,
                                                              'applicationMember': applicationMember,
                                                              'memberHasRoles':  memberHasRoles
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class AuthorizedApplicationsView(View):

    def get(self, request):
        try:
            assert isinstance(request, HttpRequest)

            return render(request,
                          'app/dashboard/authorized-applications-active-tokens.html',
                          context_instance=RequestContext(request,
                                                          {
                                                              'title': "Authorized applications",
                                                              'username': request.COOKIES.get('username')
                                                          }))

        except ObjectDoesNotExist, oe:
            logger.exception(str(oe))
            raise Http404
        except Exception, e:
            logger.exception(str(e))
            return HttpResponseServerError(str(e))


class UploadUserLogo(View):

    def post(self, request, username):
        """
        Update cover image of user
        """
        try:
            if 'logo' in request.FILES:
                fd = request.FILES['logo']
                if fd:
                    media = MediaStorage(settings.LOGO_PATH, username, fd.name)
                    if not media:
                        raise Exception('Error in logo object')
                    if not media.validateImage():
                        return JsonResponse(data={"message": 'The type of image <{}> is not allowed'.format(fd.name.split('.')[-1]), "code": status.HTTP_403_FORBIDDEN, "reason": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

                    path = settings.LOGO_URL + username + "/" + fd.name
                    media.mkdir()
                    media.flushdir()
                    if media.save(fd):
                        Profile.objects.filter(
                            username__exact=username).update(logo=path)
                        return JsonResponse(data={"message": "The image {} has been uploaded".format(fd.name), "path": path}, status=status.HTTP_200_OK)
                    #raise Exception("The image {} did not upload".format(fd.name))
                else:
                    raise Exception('Not found logo in request')
        except Exception, e:
            return JsonResponse({"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            print_exc()
            return JsonResponse({"message": 'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrepareRegistration(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        """Store the user mail for validation and notify user via an email for the registration process.
        Prevent duplicated entries through the middleware `RegistrationPermissionMiddleware`.
        """
        try:
            import uuid
            payload = request.data
            mail = payload['mail']
            if mail is None:
                raise Exception("The email is invalid")
            if RegistrationRequest.objects.filter(mail=mail, status=True).exists():
                raise Exception("You have already created an account for the email {}. Check your inbox.".format(mail)) 
            if RegistrationRequest.objects.filter(mail=mail, status=False).exists():
                raise Exception("There is an active registration request for the email {}. Check your inbox.".format(mail))            

            payload['uuid'] = uuid.uuid4().hex
            serializer = RegistrationRequestSerializer(data=payload)
            if serializer.is_valid():
                registration = RegistrationRequest(**payload)
                registration.save()

                link = getHostURL()
                link += reverse('signup_form')
                link += "?activationId=" + \
                    str(registration.uuid) + "&email=" + \
                    str(urllib.quote_plus(registration.mail))

                subject = "[P4ALL-IAM] P4ALL IAM Registration"
                body = "<div>Dear user,<br><br>"
                body += "Please goto the link below to continue the registration process:<br>"
                body += '<a href="' + link + '">Signup now</a><br><br>'
                body += "Sincerely,<br>The administrator team<br>---</div>"
                sendEmail([registration.mail], subject, body, True)

                return JsonResponse(data={}, status=200)
            else:
                return JsonResponse(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception, e:
            logger.exception(str(e))
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class MemberAuthentication(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            payload = request.data
            ows = OpenAM()
            authS, authB = ows.authenticate(
                payload['username'], payload['password'])
            resData = json.loads(authB)

            response = JsonResponse(data=resData, status=authS)
            setCookie(response, 'tokenId', resData['tokenId'], 120)
            setCookie(response, 'username', payload['username'], 120)

            #profileS, profileD = ows.retrieveUserProfile(payload['username'], resData['tokenId'])
            # if int(profileS) == 200:
            #    profile = json.loads(profileD)
            #    if len(profile['mail']):
            #        setCookie(response, 'mail', str(profile['mail'][0]), 120)
            return response
        except Exception, e:
            print_exc()
            logger.exception(str(e))
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class MembersListAPIView(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        """"Register a new user.

        If the user has been registered successfully in the OpenAM, the user is also stored in the IAM db.
        Also, a signal is triggered to activate the user profile and to prevent new registration requests in the future by the given email.

        The user is notified with an email.

        """
        try:
            payload = request.data
            temp = copy.deepcopy(payload)
            serializer = SubProfileSerializer(data=temp)

            if serializer.is_valid():
                ows = OpenAM()
                authentication = ows.authenticateAdmin()

                tokenId = json.loads(authentication[1])["tokenId"]
                tokenValidation = ows.isTokenValid(tokenId)
                if int(tokenValidation[0]) != 200:
                    return JsonResponse(data=json.loads(tokenValidation[1]), status=tokenValidation[0])

                registration = ows.registerUser(tokenId, payload)
                if int(registration[0]) == 201:
                    del payload["userpassword"]
                    payload['surname'] = payload['username']
                    profile = Profile(**payload)
                    profile.save()

                    link = getHostURL()
                    link += reverse('login_form')

                    subject = "[P4ALL-IAM] P4ALL IAM Registration"
                    body = "<div>Dear " + profile.username + ",<br><br>"
                    body += "Your registration has completed successfully. Follow the link below to obtain access on your account:<br>"
                    body += '<a href="' + link + '">Login</a><br><br>'
                    body += "Sincerely,<br>The administrator team<br>---</div>"
                    sendEmail([profile.mail], subject, body, True)

                return JsonResponse(data={}, status=registration[0])
            else:
                return JsonResponse(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            logger.exception(str(e))
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Check if the enterred username/mail has been taken from another user during the registration"""
        try:
            if "username" in self.request.GET:
                if Profile.objects.filter(username__iexact=self.request.GET.get('username')).count():
                    return Response(data='The username value has already taken', status=status.HTTP_200_OK)
                else:
                    return Response(data='true', status=status.HTTP_200_OK)

            elif "mail" in self.request.GET:
                query = Profile.objects.filter(
                    mail__iexact=self.request.GET.get('mail'))
                if 'username' in request.COOKIES:
                    if query.exclude(username__exact=request.COOKIES.get('username')).count():
                        return Response(data='The email value has is already taken', status=status.HTTP_200_OK)
                else:
                    if query.count():
                        return Response(data='The email value has already taken', status=status.HTTP_200_OK)

                return Response(data='true', status=status.HTTP_200_OK)
            else:
                params = ""
                for i in self.request.GET.keys():
                    params += i + ", "
                param = params.replace(',', "")
                message = param
                message += " query parameters are not supported" if len(
                    self.request.GET.keys()) > 2 else " query parameter is not supported"
                raise Exception(message)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class MemberChangePasswordAPIView(viewsets.ViewSet):

    def update(self, request, username, *args, **kwargs):
        """Change the password of a registered user since user is logged in"""
        try:
            payload = request.data

            ows = OpenAM()
            pwsState, response = ows.changePassword(
                username, request.COOKIES['tokenId'], payload)

            # retrieve and terminate all active tokens
            state, accessTokenList = ows.oauth2ActiveAccessTokensffrest(request.COOKIES[
                                                                        'tokenId'])
            accessTokenListJson = json.loads(accessTokenList)
            result = accessTokenListJson['result']
            for i in result:
                id = i['id'][0]
                if settings.DEBUG:
                    print "DELETE access_token: " + id
                ows.oauth2RevokeAccessTokenffrest(
                    id, request.COOKIES['tokenId'])

            return JsonResponse(data=json.loads(response), status=pwsState)
        except Exception, e:
            logger.exception(str(e))
            print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class Members(viewsets.ViewSet):

    def update(self, request, username, *args, **kwargs):
        try:
            payload = request.data
            if settings.DEBUG:
                print payload

            temp = copy.deepcopy(payload)
            if 'vat' in temp:
                del temp['vat']
            if 'language' in temp:
                del temp['language']
            serializer = ProfileUpdateSerializer(data=temp)

            if serializer.is_valid():
                ows = OpenAM()
                authentication = ows.authenticateAdmin()

                tokenId = json.loads(authentication[1])["tokenId"]
                tokenValidation = ows.isTokenValid(tokenId)
                if int(tokenValidation[0]) != 200:
                    return JsonResponse(data=json.loads(tokenValidation[1]), status=tokenValidation[0])

                state, response = ows.updateUserProfile(
                    username, tokenId, payload)

                if int(state) == 200:
                    if 'crowd_fund_participation' in temp:
                        temp['crowd_fund_participation'] = int(
                            temp['crowd_fund_participation'])
                    if 'crowd_fund_notification' in temp:
                        temp['crowd_fund_notification'] = int(
                            temp['crowd_fund_notification'])
                    profile = Profile.objects.filter(
                        username=username).update(**temp)

                    # retrieve and terminate all active tokens
                    state, accessTokenList = ows.oauth2ActiveAccessTokensffrest(request.COOKIES[
                                                                                'tokenId'])
                    accessTokenListJson = json.loads(accessTokenList)
                    result = accessTokenListJson['result']
                    for i in result:
                        id = i['id'][0]
                        if settings.DEBUG:
                            print "DELETE access_token: " + id
                        ows.oauth2RevokeAccessTokenffrest(
                            id, request.COOKIES['tokenId'])

                return JsonResponse(data={}, status=state)
            else:
                return JsonResponse(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class Logout(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        try:
            response = HttpResponseRedirect(reverse('login_form'))

            if 'tokenId' in request.COOKIES:
                ows = OpenAM()
                st, msg = ows.logout(request.COOKIES['tokenId'])
                response.delete_cookie('tokenId')

            if 'username' in request.COOKIES:
                response.delete_cookie('username')

            if 'mail' in request.COOKIES:
                response.delete_cookie('mail')
            return response

        except Exception, e:
            print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class Requests(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        try:
            if "mail" in self.request.GET:
                if RegistrationRequest.objects.filter(mail__iexact=self.request.GET.get('mail')).count():
                    return Response(data='The email is already taken', status=status.HTTP_200_OK)
                else:
                    return Response(data='true', status=status.HTTP_200_OK)
            else:
                params = ""
                for i in self.request.GET.keys():
                    params += i + ", "
                param = params.replace(',', "")
                message = param
                message += " query parameters are not supported" if len(
                    self.request.GET.keys()) > 2 else " query parameter is not supported"
                raise Exception(message)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class DirectClientAuthorization(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            payload = request.data

            ows = OpenAM()
            # authenticate user
            state, message = ows.authenticate(
                payload['username'], payload['password'])
            authenticate = json.loads(message)

            # revoke existing access tokens for current user
            state2, accessTokenList = ows.oauth2ActiveAccessTokensffrest(authenticate[
                                                                         'tokenId'])
            jAccessTokenList = json.loads(accessTokenList)
            for i in range(0, jAccessTokenList['resultCount']):
                if jAccessTokenList['result'][i]['clientID'][0] == payload["client_id"]:
                    revoke = ows.oauth2RevokeAccessTokenffrest(jAccessTokenList['result'][i][
                                                               'id'][0], authenticate['tokenId'])

            # generate code for app
            response = ows.oauth2AuthorizeCode(authenticate["tokenId"], payload[
                                               "client_id"], payload["redirect_uri"])
            res = JsonResponse(data={"link": response[
                               1], "code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            setCookie(res, 'tokenId', authenticate['tokenId'], 120)
            setCookie(res, 'username', payload['username'], 120)
            return res
            # return redirect(response[1], permanent=True)
        except Exception, e:
            print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ClientAuthorization(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        try:
            payload = request.GET
            app = Application.objects.get(client_id=payload['client_id'])
            print app.callback_url

            ows = OpenAM()
            response = ows.oauth2AuthorizeCode(
                request.COOKIES['tokenId'], app.client_id, app.callback_url)

            return redirect(response[1], permanent=True)
        except Exception, e:
            print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ClientsList(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            payload = request.data
            if settings.DEBUG:
                print payload

            ows = OpenAM()
            accessToken = ows.oauth2AccessTokenPwd(None, None)
            res = json.loads(accessToken[1])
            if int(accessToken[0]) != 200:
                return JsonResponse(data=res, status=accessToken[0])

            # register app
            redirectUriList = []
            redirectUriList.append(payload["callback_url"])
            if 'callback_url2' in payload:
                redirectUriList.append(payload["callback_url2"])
            app = ows.oauth2RegisterClient(res['access_token'], redirectUriList, payload[
                                           "name"], [payload["description"]], payload["url"], [payload['mail']])
            response = json.loads(app[1])
            print response, type(response)

            if int(app[0]) == 201:
                mail = payload['mail']
                del payload['mail']
                payload['client_id'] = response['client_id']
                payload['client_access_token'] = response[
                    'registration_access_token']
                client = Application(**payload)
                client.save()

                user = Profile.objects.get(
                    username=request.COOKIES['username'])
                appOwner = ApplicationOwner(
                    user_id=user.id,
                    application_id=client.id
                )
                appOwner.save()

                link = getHostURL()
                subject = "[P4ALL-IAM] P4ALL IAM Client Registration"
                body = "<div>Dear user,<br><br>"
                body += "The registration of the " + \
                    str(payload[
                        'name']) + "  application has completed successfully in the openAM.<br>"
                body += "To use OpenAM as an authentication server, please use:<br> - client_id: <strong>" + \
                    str(payload['client_id']) + "</strong> <br> - client_secret: <strong>" + str(
                        response['client_secret']) + "</strong>.<br><br>"
                body += "Sincerely,<br>The administrator team<br>---</div>"
                sendEmail([mail], subject, body, True)

            return JsonResponse(data=json.loads(app[1]), status=app[0])
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            ows = OpenAM()
            state, accessTokenList = ows.oauth2ActiveAccessTokensffrest(request.COOKIES[
                                                                        'tokenId'])
            return JsonResponse(data=json.loads(accessTokenList), status=state)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationAPIView(viewsets.ViewSet):

    def update(self, request, clientId, *args, **kwargs):
        """
        Update an existing client in both IAM and OpenAM 

        """
        try:
            payload = request.data
            if settings.DEBUG:
                print payload

            serializer = ApplicationUpdateSerializer(data=payload)
            if serializer.is_valid():
                ows = OpenAM()
                state, response = ows.authenticateAdmin()
                if int(state) != 200:
                    return JsonResponse(data=jToken, status=state)
                tokenId = json.loads(response)["tokenId"]

                # update OpenAM client
                state, client = ows.updateClient(tokenId, clientId, payload)
                if int(state) in [200]:
                    del payload['mail']
                    Application.objects.filter(
                        client_id=clientId).update(**payload)
                    return JsonResponse(data=json.loads(client), status=state)
                else:
                    return JsonResponse(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, clientId, *args, **kwargs):
        """
        Remove an existing client from IAM and OpenAM
        """
        try:
            ows = OpenAM()
            state, token = ows.authenticateAdmin()
            jToken = json.loads(token)
            if int(state) != 200:
                return JsonResponse(data=jToken, status=state)

            fstate, response = ows.oauth2DeleteClientfrrest(
                jToken['tokenId'], clientId)
            if int(fstate) == 200:
                app = Application.objects.get(client_id=clientId)
                appToUser = ApplicationOwner.objects.get(application_id=app.id)
                appToUser.delete()
                app.delete()

            return JsonResponse(data=json.loads(response), status=fstate)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class GenericRolesListAPIView(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        """Register a new role in IAM db and, in parallel, a new group in OpenAM"""
        try:
            payload = request.data
            if settings.DEBUG:
                print payload

            serializer = RoleSerializer(data=payload)

            if serializer.is_valid():
                ows = OpenAM()
                authentication = ows.authenticateAdmin()

                tokenId = json.loads(authentication[1])["tokenId"]
                tokenValidation = ows.isTokenValid(tokenId)
                if int(tokenValidation[0]) != 200:
                    return JsonResponse(data=json.loads(tokenValidation[1]), status=tokenValidation[0])

                registration = ows. registerGroup(tokenId, payload['type'])
                if int(registration[0]) == 201:
                    role = Role(**payload)
                    role.save()
                return JsonResponse(data={}, status=registration[0])
            else:
                return JsonResponse(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Check if a specific role name exists"""
        try:

            if "type" in self.request.GET:
                if Role.objects.filter(type__iexact=self.request.GET.get('type')).count():
                    return Response(data='This name has already taken', status=status.HTTP_200_OK)
                else:
                    return Response(data='true', status=status.HTTP_200_OK)
            else:
                params = ""
                for i in self.request.GET.keys():
                    params += i + ", "
                param = params.replace(',', "")
                message = param
                message += " query parameters are not supported" if len(
                    self.request.GET.keys()) > 2 else " query parameter is not supported"
                raise Exception(message)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationMemberAPIView(viewsets.ViewSet):

    def create(self, request, clientId, username, *args, **kwargs):
        """Associate a register user with a specific application"""
        try:
            membership = ApplicationMembership(
                application_id=Application.objects.get(
                    client_id__exact=clientId).id,
                member_id=Profile.objects.get(username__exact=username).id
            )
            membership.save()

            return JsonResponse(data={}, status=status.HTTP_201_CREATED)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, clientId, username, *args, **kwargs):
        """Remove a user from a specific application"""
        try:
            membership = ApplicationMembership.objects.get(application=Application.objects.get(
                client_id__exact=clientId), member=Profile.objects.get(username__exact=username))
            membership.delete()
            return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationRolesAPIView(viewsets.ViewSet):

    def update(self, request, clientId, *args, **kwargs):
        """Update the roles that an application supports"""
        try:
            newRoles = request.data
            app = Application.objects.get(client_id__exact=clientId)
            existingRoles = ApplicationRole.objects.filter(
                application=app).values_list('role', flat=True)

            # add the role that does not exist
            for nrole in list(set(newRoles) - set(existingRoles)):
                ApplicationRole(application_id=app.id, role_id=nrole).save()
            # delete the existing but not selected role
            for drole in list(set(existingRoles) - set(newRoles)):
                roleRm = ApplicationRole.objects.get(
                    application_id=app.id, role_id=drole)
                roleRm.delete()

            return JsonResponse(data={}, status=status.HTTP_200_OK)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationMemberHasRoleAPIView(viewsets.ViewSet):

    def update(self, request, clientId, username, *args, **kwargs):
        """Update the roles that a specific application's member has"""
        try:
            payload = request.data
            newRoles = payload['roles']
            existingRoles = ApplicationMemberHasRole.objects.filter(application_member__id=int(
                payload['application_member'])).values_list('application_role', flat=True)

            # add the role that does not exist
            for nrole in list(set(newRoles) - set(existingRoles)):
                ApplicationMemberHasRole(
                    application_role_id=ApplicationRole.objects.get(
                        pk=nrole).id,
                    application_member_id=ApplicationMembership.objects.get(
                        pk=int(payload['application_member'])).id
                ).save()

            # delete the existing but not selected role
            for drole in list(set(existingRoles) - set(newRoles)):
                ApplicationMemberHasRole.objects.get(
                    application_role__id=drole).delete()

            return JsonResponse(data={}, status=status.HTTP_200_OK)
        except Exception, e:
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ActiveAccessTokenListAPIView(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        """Retrieve the list of the active authorized applications' access token  from OpenAM"""
        try:
            ows = OpenAM()
            state, accessTokenList = ows.oauth2ActiveAccessTokensffrest(request.COOKIES[
                                                                        'tokenId'])
            return JsonResponse(data=json.loads(accessTokenList), status=state)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class ActiveAccessTokenAPIView(viewsets.ViewSet):

    def destroy(self, request, id, *args, **kwargs):
        try:
            ows = OpenAM()
            state, response = ows.oauth2RevokeAccessTokenffrest(
                id, request.COOKIES['tokenId'])
            return JsonResponse(data=json.loads(response), status=state)
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return JsonResponse(data={"message": str(e), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class MyApplicationsList(generics.ListAPIView):
    """
    Retrieve list of applications per owner
    ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: username
                paramType: path
                type: integer
                description: Primary key
                required: true

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
    """
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = Profile.objects.get(username=username)
        appIdList = ApplicationOwner.objects.filter(
            user=user).values_list('application_id', flat=True)
        queryset = Application.objects.filter(id__in=appIdList)
        return queryset


class RolesList(generics.ListAPIView):
    """
    LIst of supported roles
    ---
        GET:
            omit_parameters:
              - form

            parameters:
              - name: Authorization
                paramType: header
                required: true
                type: string
                description: Basic token

            responseMessages:
              - code: 200
                message: OK
              - code: 204
                message: No content
              - code: 301
                message: Moved permanently
              - code: 400
                message: Bad Request
              - code: 401
                message: Unauthorized
              - code: 403
                message: Forbidden
              - code: 404
                message: Not found
              - code: 409
                message: Conflict
              - code: 500
                message: Interval Server Error

            produces:
              - application/json
    """
    serializer_class = RoleSerializer

    def list(self, request, format=None):
        try:
            if self.request.META.get('HTTP_AUTHORIZATION') not in [None, "", " "]:
                try:
                    authType, authCode = self.request.META.get(
                        'HTTP_AUTHORIZATION').split(" ")
                except Exception, ex:
                    return Response(data={"message": "Authorization: " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)

                #ows = OpenAM()
                #accessToken = ows.oauth2ValidateAccessToken(authCode)
                # if int(accessToken[0]) == 200:
                #    instance = Profile.objects.get(username=username)
                #    serializer = ClientProfileSerializer(instance)
                #    return Response(data=serializer.data, status=status.HTTP_200_OK)
                # else:
                # return Response(data={"code": status.HTTP_401_UNAUTHORIZED,
                # "reason": "Access Token is not valid"},
                # status=status.HTTP_401_UNAUTHORIZED)
                queryset = Role.objects.all()
                serializer = RoleSerializer(queryset)
                return Response(data=[serializer.data], status=status.HTTP_200_OK)
            else:
                return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Authorization header does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist, e:
            return Response(data={"message": str(e), "code": status.HTTP_404_NOT_FOUND, "reason": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception, ex:
            return Response(data={"message": str(ex), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
