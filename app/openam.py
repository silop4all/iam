import sys
import httplib
import urllib
import json
from traceback import print_exc
from base64 import b64decode, b64encode
from django.conf import settings
from django.shortcuts import redirect
from app.models import *

import logging
logger = logging.getLogger(__name__)


class OpenAM(object):
    """ 
        OpenAM class 

        Methods:
            - authenticateAdmin(): authenticate OpenAM admin
            - authenticate(): authenticate any OpenAM user
            - registerUser(): register new user in Openam on behalf of OpenAM admin
            - isTokenValid(): validate a tokenId (text format)
            - validateTokenId(): validate a tokenId (JSON format) (similar to isTokenValid)
            - logout(): logout and terminate the existence of openAM session/tokenId


        Basic endpoints:
            - /openam/json/authenticate
            - /openam/json/groups
            - /openam/json/users
            - /openam/json/agents
            - /openam/json/sessions

            - /openam/json/dashboard*
            - /openam/json/applications*
            - /openam/json/policies*

            - /openam/identity/isTokenValid
            - /openam/identity/getCookieNameForToken
            - /openam/oauth2/authorize
            - /openam/oauth2/connect/register
            - /openam/oauth2/access_token
            - /openam/oauth2/tokeninfo
            - /openam/frrest/oauth2/client
            - /openam/frrest/oauth2/token

    """

    user = 'amadmin'

    def __init__(self):
        """ Class constructor """
        self.base = self.openamURL()
        self.password = b64decode(Manager.objects.get(
            username__exact=OpenAM.user).password)
        self.staticClient = b64encode("iamClient:1qaz@WSX")
        self.tokenId = Manager.objects.get(username__exact=OpenAM.user).token

    def openamURL(self):
        """Retrieve the url of OpenAM in format IP:PORT"""
        try:
            return str(settings.OPENAM["IP"]) + ":" + str(settings.OPENAM["PORT"])
        except:
            return "83.235.169.221:80"

    def authenticateAdmin(self):
        """ Authenticate OpenAM admin 

            No payload required while the response body based on JSON format.

            Normal response - 200 OK:
                {
                    "tokenId": <tokenId>,
                    "successUrl": <url>
                }

            Erroneous response - 401 UNAUTHORIZED:
                {
                    "code": 401,
                    "reason": "Unauthorized",
                    "message": "Authentication Failed!!"
                }
        """

        try:
            endpoint = "/openam/json/authenticate"

            headers = {
                "Content-type": "application/json",
                "X-OpenAM-Username": OpenAM.user,
                "X-OpenAM-Password": self.password
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, "", headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def registerGroup(self, adminTokenId, name):
        """ Group registration """

        try:
            endpoint = "/openam/json/groups?_action=create"

            headers = {
                "iplanetDirectoryPro": str(adminTokenId),
                "Content-type": "application/json"
            }

            group = {"username": name}
            payload = json.dumps(group, separators=(',', ':'), indent=4)
            if settings.DEBUG:
                print payload

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def retrieveGroup(self, adminToken, name):
        """Retrieve group info in OpenAM"""
        try:
            endpoint = "/openam/json/groups/" + str(name)

            headers = {
                "Content-type": "application/json",
                "iplanetDirectoryPro": str(adminToken),
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def addUserToGroup(self, adminTokenId, name, universalIdList):
        """ Associate user with an existing group """

        try:
            endpoint = "/openam/json/groups/" + str(name)

            headers = {
                "iplanetDirectoryPro": str(adminTokenId),
                "Content-type": "application/json"
            }

            d = {"uniquemember": universalIdList}
            payload = json.dumps(d, separators=(',', ':'), indent=4)

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("PUT", endpoint, payload, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def authenticate(self, username, password):
        """"Authenticate a user with session (tokenId) generation"""

        try:
            endpoint = "/openam/json/authenticate"

            headers = {
                "X-OpenAM-Username": str(username),
                "X-OpenAM-Password": str(password),
                "Content-type": "application/json"
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, None, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def authenticateWithoutSession(self, username, password):
        """"Authenticate a user without session (tokenId) generation"""

        try:
            endpoint = "/openam/json/authenticate?noSession=true"

            headers = {
                "X-OpenAM-Username": str(username),
                "X-OpenAM-Password": str(password),
                "Content-type": "application/json"
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, None, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def registerUser(self, adminTokenId, data):
        """ User registration 

        Args:
            adminTokenId (string): the admin token id
            data (dict): the user profile
        """

        try:
            endpoint = "/openam/json/users/?_action=create"

            headers = {
                "iplanetDirectoryPro": str(adminTokenId),
                "Content-type": "application/json"
            }

            # address = ''
            # address += data['address'] + ", " if 'address' in data else ''
            # address += data['postcode'] + ", " if 'postcode' in data else ''
            # address += data['city'] + ", " if 'city' in data else ''
            # address += data['country'] if 'country' in data else ''
            # gender = 'm' if data['gender'] == 'M' else 'f'
            # if settings.DEBUG:
            #     print address

            # OpenAM requires the username, the userpassword and the mail
            # fields.
            d = {
                "username": data["username"],
                "userpassword": data["userpassword"],
                "mail": data["mail"],
                "sunIdentityServerPPCommonNameCN": data["username"],
                # "sn": data['surname'],
                # "givenName": data["name"],
                # 'telephoneNumber': data['phone'] if 'phone' in data else None,
                # "postalAddress": address,
                # "sunIdentityServerPPCommonNameSN": data['surname'],
                # "sunIdentityServerPPCommonNameFN": data['name'],
                # "sunIdentityServerPPLegalIdentityGender":  "urn:liberty:id-sis-pp:gender:" + str(gender),
                # "sunIdentityServerPPDemographicsBirthDay": None,
                # "sunIdentityServerPPAddressCard": address if address != "" else None,
                # "sunIdentityServerPPDemographicsDisplayLanguage": data['language'] if 'language' in data else None,
                # "sunIdentityServerPPLegalIdentityVATIdValue": data["vat"] if 'vat' in data else None,
                # "sunIdentityServerPPEmploymentIdentityJobTitle": "job title",
                # "sunIdentityServerPPEmploymentIdentityOrg": "organization"
            }

            payload = json.dumps(d, separators=(',', ':'), indent=4)
            logger.warn(payload)

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except Exception, e:
            logger.error(str(e))
            return 500, str(e)

    def retrieveUserProfile(self, username, tokenid):
        """Retrieve user profile in OpenAM"""
        try:
            endpoint = "/openam/json/users/" + str(username)

            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "iplanetDirectoryPro": str(tokenid),
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def retrieveIdFromToken(self, tokenId):
        """Retrieve username from tokenId in OpenAM"""
        try:
            endpoint = "/openam/json/users?_action=idFromSession"

            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "iplanetDirectoryPro": str(tokenid),
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, None, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def updateUserProfile(self, username, adminTokenId, data):
        """Update user profile in OpenAM"""
        try:
            endpoint = "/openam/json/users/" + str(username)

            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "iplanetDirectoryPro": str(adminTokenId),
            }

            address = ''
            address += data['address'] + ", " if 'address' in data else ''
            address += data['postcode'] + ", " if 'postcode' in data else ''
            address += data['city'] + ", " if 'city' in data else ''
            address += data['country'] if 'country' in data else ''

            gender = 'm' if data['gender'] == 'M' else 'f'

            d = {
                "mail": data["mail"],
                "sn": data['surname'],
                "givenName": data["name"],
                'telephoneNumber': data['phone'] if 'phone' in data else None,
                "postalAddress": address,
                "sunIdentityServerPPCommonNameSN": data['surname'],
                "sunIdentityServerPPCommonNameFN": data['name'],
                "sunIdentityServerPPLegalIdentityGender":  "urn:liberty:id-sis-pp:gender:" + str(gender),
                "sunIdentityServerPPDemographicsBirthDay": None,
                "sunIdentityServerPPAddressCard": address if address != "" else None,
                "sunIdentityServerPPDemographicsDisplayLanguage": data['language'] if 'language' in data and data['language'] != "" else [],
                "sunIdentityServerPPLegalIdentityVATIdValue": data["vat"] if 'vat' in data and data['vat'] != "" else []
            }
            payload = json.dumps(d, separators=(',', ':'), indent=4)

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("PUT", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def isTokenValid(self, tokenId):
        """ Validate openAM tokenId (text response) """
        try:
            endpoint = "/openam/identity/isTokenValid"

            headers = {
                "Content-type": "application/x-www-form-urlencoded",
            }
            payload = "tokenid=" + tokenId

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except Exception, e:
            if settings.DEBUG:
                print_exc()
            return 500, str(e)

    def validateTokenId(self, tokenId):
        """ Validate openAM tokenId (JSON response) """
        try:
            endpoint = "/openam/json/sessions/" + \
                str(tokenId) + "?_action=validate"
            headers = {
                "Content-type": "application/json",
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            d = response.read()
            # logger.warn(response.status)
            # logger.warn(d)
            return response.status, d
        except Exception, e:
            logger.exception(str(e))
            print_exc()
            return 500, str(e)

    def changePassword(self, username, tokenId, data):
        try:
            endpoint = "/openam/json/users/" + \
                str(username) + "?_action=changePassword"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "iplanetDirectoryPro": str(tokenId)
            }

            d = {
                "currentpassword": str(data['currentpassword']),
                "userpassword": str(data['userpassword'])
            }

            payload = json.dumps(d, separators=(',', ':'), indent=4)
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2AuthorizeCode(self, tokenId, clientId, redirectUri):
        try:
            endpoint = "/openam/oauth2/authorize"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Cookie": "iplanetDirectoryPro=" + str(tokenId)
            }

            if settings.DEBUG:
                print headers

            payload = "response_type=code"
            #payload += "&scope=openid profile cn mail"
            payload += "&scope=openid email profile"
            payload += "&client_id=" + str(clientId)
            payload += "&redirect_uri=" + str(redirectUri)
            payload += "&save_consent=1&decision=Allow"

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            header = response.getheader('location')
            if settings.DEBUG:
                print response.getheaders()
            return response.status, header

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2AccessTokenCode(self, clientId, clientSecret, code, redirectUri):
        try:
            endpoint = "/openam/oauth2/access_token"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Authorization": "Basic " + b64encode(clientId + ":" + clientSecret)
            }

            payload = "grant_type=authorization_code"
            payload += "&code=" + str(code)
            payload += "&redirect_uri=" + str(redirectUri)

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            print response.status, response.read()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2AccessTokenPwd(self, username, password):
        try:
            endpoint = "/openam/oauth2/access_token"

            # basic -> iamCLient id:pwd
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + str(self.staticClient)
            }

            _username = OpenAM.user if username == None else username
            _password = self.password if password == None else password
            payload = "grant_type=password"
            payload += "&username=" + str(_username)
            payload += "&password=" + str(_password)
            payload += "&scope=openid"

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2RegisterClient(self, adminBearerToken, redirectUriList, clientName, clientDescriptionList, clientUri, contactsList):
        """"Register a new client in OpenAM 

            Required: the bearer_token of the OpenAM admin

            Payload example:             
            {
                "redirect_uris": [
                    "http://myapp.org"
                ],
                "client_name": "my_dyn_client"
            }

            Response example:
                {
                    "application_type": "web",
                    "redirect_uris": [
                        "http://myapp.org"
                    ],
                    "registration_client_uri": "http://192.168.1.41:8080/openam/oauth2/connect/register?client_id=a75f96c3-89bf-4133-8d2d-3ca2bc3b583b",
                    "scopes": [
                        "openid"
                    ],
                    "client_secret": "067fb6c7-cae6-402d-8899-f646558223de",
                    "client_type": "Confidential",
                    "registration_access_token": "f2ea63a3-4de7-471c-84d3-a34daf6d3d4b",
                    "subject_type": "Public",
                    "id_token_signed_response_alg": "HS256",
                    "client_id_issued_at": 1465995245,
                    "client_id": "a75f96c3-89bf-4133-8d2d-3ca2bc3b583b",
                    "client_secret_expires_at": 0,
                    "client_name": "my_dyn_client",
                    "response_types": [
                        "code"
                    ]
                }
        """

        try:
            endpoint = "/openam/oauth2/connect/register"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + str(adminBearerToken)
            }

            data = {
                "application_type": "Web",
                "client_type": "Confidential",
                "client_name": clientName,
                "client_description": clientDescriptionList,
                "client_uri": clientUri,
                "contacts": contactsList,
                "display_name": [clientName],
                "redirect_uris": redirectUriList,
                "scopes": [
                    "openid",
                    "email",
                    "profile"
                ]
            }

            payload = json.dumps(data, separators=(',', ':'), indent=4)
            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2RegisterClientfrrest(self, adminTokenId, clientId, clientSecret, redirectUriList, clientName, clientDescriptionList):
        """"OpenAM administrator can register a new client after his success authentication"""

        try:
            endpoint = "/openam/frrest/oauth2/client/?_action=create"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(adminTokenId)
            }

            data = {
                "client_id": [clientId],
                "userpassword": [clientSecret],
                "realm": ["/"],
                "com.forgerock.openam.oauth2provider.clientType": ["Confidential"],
                "com.forgerock.openam.oauth2provider.redirectionURIs": redirectUriList,
                "com.forgerock.openam.oauth2provider.name": [clientName],
                "com.forgerock.openam.oauth2provider.description": clientDescriptionList,
                "com.forgerock.openam.oauth2provider.responseTypes": ["code"]
            }

            payload = json.dumps(data, separators=(',', ':'), indent=4)
            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, payload, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2DeleteClientfrrest(self, adminTokenId, clientId):
        """ Delete an existing client """

        try:
            endpoint = "/openam/frrest/oauth2/client/" + str(clientId)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(adminTokenId)
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("DELETE", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2ActiveAccessTokensffrest(self, tokenId):
        """"Retrieve the active access tokens per user"""

        try:
            endpoint = "/openam/frrest/oauth2/token/?_queryId=access_token"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(tokenId)
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2RevokeAccessTokenffrest(self, id, tokenId):
        """"Destroy a specific active access token"""

        try:
            endpoint = "/openam/frrest/oauth2/token/" + id + "?_action=revoke"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(tokenId)
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2ValidateAccessToken(self, accessTokenId):
        """"Retrieve infor for a specific access token"""

        try:
            endpoint = "/openam/oauth2/tokeninfo?access_token=" + \
                str(accessTokenId)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def oauth2UserProfile(self, accessTokenId):
        """Retrieve the default OpenAM user profile based on access token"""

        try:
            endpoint = "/openam/oauth2/userinfo"
            headers = {
                "Authorization": "Bearer " + str(accessTokenId),
                "Content-Type": "application/json"
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def retrieveClient(self, adminTokenId, clientId):
        """"Retrieve the client information"""

        try:
            endpoint = "/openam/json/agents/" + str(clientId)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(adminTokenId)
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, None, headers)
            # Response
            response = conn.getresponse()
            return response.status, response.read()

        except Exception, ex:
            if settings.DEBUG:
                print_exc()
            return 500, str(ex)

    def updateClient(self, adminTokenId, clientId, data):
        """Update an existing client"""

        try:
            endpoint = "/openam/json/agents/" + str(clientId)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "cookie": "iPlanetDirectoryPro=" + str(adminTokenId)
            }

            d = {
                "com.forgerock.openam.oauth2provider.clientName": [
                    data["name"]
                ],
                "com.forgerock.openam.oauth2provider.name": [
                    '[0]=' + str(data['name'])
                ],
                "com.forgerock.openam.oauth2provider.redirectionURIs": [
                    '[0]=' + str(data["callback_url"])
                ],
                "com.forgerock.openam.oauth2provider.contacts": [
                    '[0]=' + str(data["mail"])
                ],
                "com.forgerock.openam.oauth2provider.description": [
                    "[0]=" + str(data["description"])
                ]
            }
            if 'callback_url2' in data:
                d["com.forgerock.openam.oauth2provider.redirectionURIs"].append(
                    '[1]=' + str(data['callback_url2']))
            payload = json.dumps(d, separators=(',', ':'), indent=4)

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("PUT", endpoint, payload, headers)

            # Response
            response = conn.getresponse()
            return response.status, response.read()
        except:
            print_exc()
            return 500, ""

    def retrieveCookieName(self):
        """Retrieve the default name of the cookie name in OpenAM"""

        try:
            endpoint = "/openam/identity/getCookieNameForToken"

            headers = {
                "Content-type": "application/json",
                "Accept": "application/json"
            }

            # Request
            conn = httplib.HTTPConnection(self.base)
            conn.request("GET", endpoint, "", headers)

            # Response
            response = conn.getresponse()
            data = response.read()
            name = data.split('=')[1]
            return response.status, name
        except:
            print_exc()
            return 500, ""

    def logout(self, tokenId):
        """Terminate an existing session (tokenId) in OpenAM"""

        try:
            endpoint = "/openam/json/sessions/?_action=logout"

            headers = {
                "iplanetDirectoryPro": str(tokenId),
                "Content-Type": "application/json"
            }

            conn = httplib.HTTPConnection(self.base)
            conn.request("POST", endpoint, "", headers)
            response = conn.getresponse()
            data = response.read()
            return response.status, data

        except:
            print_exc()
            return 500, ""


if __name__ == '__main__':
    print OpenAM.__doc__
    ows = OpenAM()
    print ows.user
