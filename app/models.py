"""
Definition of models.
"""

from datetime import datetime
from django.db import models
from django.utils import timezone
from app.utilities import getLogoPath


class Manager(models.Model):
    """Manager"""

    username = models.CharField(
        max_length=64, blank=False, unique=True, null=False)
    password = models.CharField(
        max_length=128, blank=False, unique=True, null=False)
    token = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        db_table = "iam_manager"


class Profile(models.Model):
    """ User profile """

    GENDER_CHOICES = (
        ('U', 'Not available'),
        ('M', 'sir'),
        ("W", "madam")
    )

    name = models.CharField(max_length=127, blank=True, null=True)
    surname = models.CharField(max_length=127, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='U')
    username = models.CharField(
        max_length=255, blank=False, unique=True, null=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True,
                             null=True, default="00000000000000")
    skills = models.CharField(max_length=10, null=False, default="low")
    activation = models.BooleanField(blank=False, null=False, default=False)
    crowd_fund_participation = models.BooleanField(
        blank=False, null=False, default=False)
    crowd_fund_notification = models.BooleanField(
        blank=False, null=False, default=False)
    logo = models.ImageField(
        upload_to='app/users/logos', blank=True, null=True)

    class Meta:
        ordering = ["username"]
        db_table = "iam_profile"

    def __unicode__(self):
        """ Get the username of user """
        return "%s" % (self.username)


class RegistrationRequest(models.Model):
    mail = models.EmailField(max_length=255, blank=False, null=False)
    uuid = models.CharField(max_length=255, blank=False, null=False)
    status = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        ordering = ["mail"]
        db_table = "iam_registration_request"


class Application(models.Model):
    """ Application """

    client_id = models.CharField(max_length=255, blank=False, null=False)
    client_access_token = models.CharField(
        max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    callback_url = models.CharField(max_length=500, blank=False, null=False)
    callback_url2 = models.CharField(max_length=500, blank=False, null=True)
    #logo        = models.ImageField(upload_to=getLogoPath, blank=False, null=True)

    class Meta:
        db_table = "iam_application"


class ApplicationOwner(models.Model):
    """Associate application with its owner"""

    user = models.ForeignKey(Profile)
    application = models.ForeignKey(Application)

    class Meta:
        db_table = "iam_application_ownership"


class Role(models.Model):
    """ Role in general """

    type = models.CharField(max_length=64, blank=False,
                            null=False, unique=True)
    description = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        ordering = ["type"]
        db_table = "iam_role"


class ApplicationRole(models.Model):
    """ Role per application """

    application = models.ForeignKey(Application)
    role = models.ForeignKey(Role)

    class Meta:
        ordering = ["application"]
        db_table = "iam_application_role"


class ApplicationMembership(models.Model):
    """ Members per application """

    application = models.ForeignKey(Application)
    member = models.ForeignKey(Profile)

    class Meta:
        ordering = ["application"]
        unique_together = [
            ("application", "member"),
        ]
        db_table = "iam_application_membership"


class ApplicationMemberHasRole(models.Model):
    """ Role for the members per application """

    application_role = models.ForeignKey(ApplicationRole)
    application_member = models.ForeignKey(
        ApplicationMembership, related_name="member_roles")

    class Meta:
        db_table = "iam_application_member_hasrole"
