from django import template
from django.utils.translation import ugettext as _

register = template.Library()


def account_state_icon(state):
    """Highlight the state of user account

    Args:
        state (str): The state of the user's account

    Returns:
        str: A set of HTML classes.
    """
    state_lowercase = state.lower()

    if state_lowercase == "active":
        return 'fa fa-circle text-success'
    else:
        return 'fa fa-circle text-danger'
register.filter('account_state_icon', account_state_icon)


def user_gender(gender):
    """Get the full gender of user.

    Args:
        gender (str): the gender of user (M or W)

    Returns:
        str: a term by the given gender.
    """
    gender_lowercase = gender.lower()

    if gender_lowercase == "m":
        return 'Male'
    elif gender_lowercase == "w":
        return 'Female'
    else:
        return 'Not Available'
register.filter('user_gender', user_gender)


def user_gender_icon(gender):
    """Get the icon per gender.

    Args:
        gender (str): the gender of user (M or W)

    Returns:
        str: A set of HTML classes.
    """
    gender_lowercase = gender.lower()

    if gender_lowercase == "m":
        return 'fa fa-male fa-fw text-primary'
    elif gender_lowercase == "w":
        return 'fa fa-female fa-fw text-danger'
    else:
        return 'fa fa-user fa-fw'
register.filter('user_gender_icon', user_gender_icon)


def yes_or_no(input):
    """Convert True or False in Yes or No.

    Args:
        input (bool): True or False

    Returns:
        str: Yes for True, No for False
    """
    if input:
        return 'Yes'
    else:
        return 'No'
register.filter('yes_or_no', yes_or_no)


def user_city_country(obj):
    """Get the location (city, country) of the user

    Args:
        obj (object): The user profile

    Returns:
        str: The city and country of user (if exist)
    """
    location = list()

    if obj.city:
        location.append(obj.city)
    if obj.country:
        location.append(obj.country)

    if len(location):
        return ", ".join(str(i) for i in location)
    return 'Not available'

register.filter('user_city_country', user_city_country)
