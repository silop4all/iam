
import json
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from app.openam import *

import logging
logger = logging.getLogger(__name__)


class TokenValidationMiddleware(object):
    """
    "TokenValidation" middleware performs the following operations:

        - Check if the tokenId provided from the openAM exists

        - Validate the openAM tokenId, if exist. 
          If tokenId is not valid, the user is directed to the login page.
    """

    def process_request(self, request):
        try:
            appAccessList = [
                reverse('signup_request_form'),
                reverse('signup_form'),
                reverse('login_form'),
                reverse('authorize_app_form'),
            ]
            privateApiAccessList = [
                reverse('private_api:authorize_direct_app_url'),
                reverse('private_api:authenticate_url'),
                reverse('private_api:pre_registration_url'),
                reverse('private_api:users_url'),
                reverse('private_api:logout_url'),
                reverse('private_api:requests_url'),
            ]
            publicApiAccessList = [
                reverse('docs:django.swagger.base.view'),
                reverse('docs:django.swagger.resources.view'),
                reverse('public_api:extended_userinfo'),
                reverse('public_api:user_roles'),
                reverse('public_api:register_user'),
            ]

            whiteList = appAccessList + privateApiAccessList + publicApiAccessList

            if request.path not in whiteList:
                # logger.warn(request.COOKIES['tokenId'])

                if 'tokenId' not in request.COOKIES:
                    raise Exception('OpenAM tokenId does not exist 1')
                elif 'username' not in request.COOKIES:
                    raise Exception('OpenAM username does not exist 2')
                else:
                    ows = OpenAM()
                    httpCode, response = ows.validateTokenId(request.COOKIES['tokenId'])
                    data = json.loads(response)
                    # logger.warn(data)

                    if not data['valid']:
                        raise Exception('OpenAM tokenId is not valid 3')
                    if int(httpCode) != 200:
                        raise Exception('OpenAM tokenId is not valid 4')
            
        except Exception, ex:
            logger.exception(str(ex))
            return redirect(reverse('private_api:logout_url')) 
