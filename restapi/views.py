"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import copy
import uuid

from restapi.models import *
from app.openam import *
from app.serializers import *

from rest_framework import generics, filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView



class ProfileAPIview(APIView):
    """
        Retrieve the extended user profile
        ---
        GET:
            parameters:
              - name: access_token
                paramType: query
                required: true
                type: string
                description: Access token

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
                message: Internal Server Error

            produces:
              - application/json

            serializer: ClientProfileSerializer
             
    """

    serializer_class = ClientProfileSerializer

    def get(self, request, format=None):
        try:
            if 'access_token' in self.request.GET:
                try:
                    authCode = self.request.GET.get('access_token')
                except:
                    return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Access Token is not valid", "message": "Use Authorization: Bearer <access_token>" }, status=status.HTTP_401_UNAUTHORIZED)

                ows = OpenAM()
                state, accessToken = ows.oauth2ValidateAccessToken(authCode)
                if int(state) == 200:
                    userState, userInfo = ows.oauth2UserProfile(authCode)
                    jUserInfo = json.loads(userInfo)
                    instance = Profile.objects.get(username=jUserInfo['sub'])
                    serializer = ClientProfileSerializer(instance)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Access Token is not valid"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Authorization header does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist, e:
            return Response(data={"message": str(e), "code": status.HTTP_404_NOT_FOUND, "reason": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception, ex:
            return Response(data={"message": str(ex), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class RoleAPIview(APIView):
    """
        Retrieve a list of user roles
        ---
        GET:
            parameters:
              - name: access_token
                paramType: query
                required: true
                type: string
                description: Access Token

              - name: client_id
                description: Client ID
                type: string
                paramType: query
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
                message: Internal Server Error

            produces:
              - application/json

            serializer: ApplicationMemberHasRoleSerializer
             
    """

    serializer_class = ApplicationMemberHasRoleSerializer

    def get(self, request, format=None):
        try:
            if 'access_token' in self.request.GET:
                try:
                    authCode = self.request.GET.get('access_token')
                except:
                    return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Access Token is not valid"}, status=status.HTTP_401_UNAUTHORIZED)

                ows = OpenAM()
                state, accessToken = ows.oauth2ValidateAccessToken(authCode)
                if int(state) == 200:
                    userState, userInfo = ows.oauth2UserProfile(authCode)
                    jUserInfo = json.loads(userInfo)
                    user = Profile.objects.get(username=jUserInfo['sub'])
                    appMemberList = ApplicationMembership.objects.filter(member=user)

                    if 'client_id' in self.request.GET:
                        appMemberList = appMemberList.filter(application__client_id__exact=self.request.GET.get('client_id'))
                        if appMemberList.count() == 0:
                            raise ObjectDoesNotExist('Client_id is not valid')
                        appMemberList.values_list('id', flat=True)
                        roles = ApplicationMemberHasRole.objects.filter(application_member__in=appMemberList)
                        serializer = ApplicationMemberHasRoleSerializer(roles, many=True)
                    else: 
                        raise Exception("client_id query parameter is required")

                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Access Token is not valid"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(data={"code": status.HTTP_401_UNAUTHORIZED, "reason": "Authorization header does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist, e:
            return Response(data={"message": str(e), "code": status.HTTP_404_NOT_FOUND, "reason": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception, ex:
            return Response(data={"message": str(ex), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIview(APIView):
    """
        Register a new user
        ---
        POST:
            omit_parameters:
              - form
            parameters:
              - name: JSON structure
                description: Create a user profile
                type: UserProfileSerializer
                paramType: body
                pytype: UserProfileSerializer

            responseMessages:
              - code: 201
                message: Created
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
              - code: 500
                message: Interval Server Error

            consumes:
              - application/json

            serializer: UserProfileSerializer
             
    """
    
    def post(self, request, format=None):
        try:
            payload=self.request.data
            if settings.DEBUG:
                print payload

            temp = copy.deepcopy(payload)
            if 'vat' in temp:
                del temp['vat']
            if 'language' in temp:
                del temp['language']
            serializer = UserProfileSerializer(data=temp)

            if serializer.is_valid():
                ows = OpenAM()
                authentication  = ows.authenticateAdmin()

                tokenId         = json.loads(authentication[1])["tokenId"]
                tokenValidation = ows.isTokenValid(tokenId)
                if int(tokenValidation[0]) != 200:
                    return Response(data=json.loads(tokenValidation[1]), status=tokenValidation[0])

                registration    = ows.registerUser(tokenId, payload)
                if int(registration[0]) == 201:
                    if 'userpassword' in payload:
                        del payload["userpassword"]
                    if 'language' in payload:
                        del payload["language"]
                    profile = Profile(**payload)
                    profile.save()
                    req = RegistrationRequest(
                        uuid=uuid.uuid4().hex,
                        mail=payload['mail'], 
                        status=1
                    )
                    req.save()

                    return Response(data=ProfileSerializer(payload).data, status=registration[0])
                else:
                    return Response(data=json.loads(registration[1]), status=registration[0])
            else:
                return Response(data={"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            return Response(data={"message": str(ex), "code": status.HTTP_400_BAD_REQUEST, "reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)