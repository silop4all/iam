from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from app.openam import *
import json

def tokenRequired(function):
    """
    Check if the user has valid tokenId
    """
    def wrap(request, *args, **kwargs):

        if 'tokenId' not in request.COOKIES:
            return redirect(reverse('logout_url'))
        elif 'username' not in request.COOKIES:
            return redirect(reverse('logout_url'))
        else:
            ows = OpenAM()
            stat, response = ows.validateTokenId(request.COOKIES['tokenId'])
            data = json.loads(response)
            if not data['valid']:
                return redirect(reverse('logout_url'))
            if int(stat) != 200:
                return redirect(reverse('logout_url'))
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


def tokenRequiredView(View): 
    """
    Check if the user has valid tokenId
    Decorator for class-based views 
    """
    View.dispatch = method_decorator(tokenRequired)(View.dispatch)
    return View