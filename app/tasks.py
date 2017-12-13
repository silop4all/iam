from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from celery import task


@task
def send_email_task(receivers_list, subject, content, html_format=False):
    """Sends email in one or more receivers.

    Args:
        receivers_list: The list of receivers' emails (list)
        subject: The subject of the email (string)
        content: The content of the email (string)
        html_format: Define if the email's content includes HTML code (boolean, optional variable)

    Returns:
        None
    """
    try:
        sender = settings.EMAIL_HOST_USER

        if html_format is True:
            # include HTML code in content
            format = "text/html"
            msg = EmailMultiAlternatives(subject, "", sender, receivers_list)
            msg.attach_alternative(content, format)
            msg.send()
        else:
            send_mail(subject, content, sender,
                      receivers_list, fail_silently=False)
    except Exception as e:
        log.error('Exception in send_email_task. Reason: {}'.format(str(e)))
