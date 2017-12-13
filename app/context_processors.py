from django.conf import settings
from datetime import date


def iam_processor(request):
    """
    Return global variables for the app application
    """

    return {
        'YEAR': date.today().year,
    }
