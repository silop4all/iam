
from os import path
from django.conf import settings
from pytz import timezone
from django.core.mail import EmailMultiAlternatives, send_mail
from traceback import print_exc
from datetime import datetime, timedelta
import pycountry


def setCookie(response, key, value, minutes_expire=120):
    try:
        max_age = 120 if minutes_expire is None else minutes_expire
        max_age *= 60 * 60
        expires = datetime.strftime(
            datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        #response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
        response.set_cookie(key, value, max_age=max_age, expires=expires)
    except:
        print_exc()


def sendEmail(receivers_list, subject, content, html_format=False):
    """Sends email in one or more receivers as a celery task.

    Args:
        receivers_list: The list of receivers' emails (list)
        subject: The subject of the email (string)
        content: The content of the email (string)
        html_format: Define if the email's content includes HTML code (boolean, optional variable)

    Returns:
        None
    """
    from app.tasks import send_email_task
    subject = "[Identity & Access Manager] %s" % subject
    send_email_task.apply_async(
        (receivers_list, str(subject), str(content), html_format),)


def getHostURL():
    return str(settings.HOST["PROTOCOL"]) + "://" + str(settings.HOST["IP"]) + ":" + str(settings.HOST["PORT"])


def getCountriesList():

    list = pycountry.countries
    countriesList = []

    for i in list:
        countriesList.append(i.name)
    return countriesList


def getLogoPath(instance, filename):
    return path.join('logos', str(instance.id), filename)
