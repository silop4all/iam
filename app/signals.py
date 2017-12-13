from django.conf import settings
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from app.models import Profile, RegistrationRequest
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def profile_post_save(sender, **kwargs):
    """When the registration of a user is performed, the registration request is marked as completed"""
    try:
        profile = kwargs['instance']
        Profile.objects.filter(pk=profile.id).update(activation=True)
        RegistrationRequest.objects.filter(mail=profile.mail).update(status=True)
    except Exception as e:
        logger.error('Exception while activating the user profile`{}`. Reason : {}'.format(
            profile.mail, str(e)))
