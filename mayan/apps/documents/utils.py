import logging

import pycountry

from django.utils.translation import gettext_lazy as _

from .settings import setting_language_codes

logger = logging.getLogger(name=__name__)


def get_language(language_code):
    language = getattr(
        pycountry.languages.get(alpha_3=language_code), 'name', None
    )

    if language:
        return _(language)
    else:
        return _(message='Unknown language "%s"') % language_code


def get_language_choices():
    result = []

    for iso639_3 in setting_language_codes.value:
        entry = pycountry.languages.get(alpha_3=iso639_3)
        if entry:
            label = _(entry.name)
            result.append(
                (iso639_3, label)
            )
        else:
            logger.warning('Unknown language code "%s".', iso639_3)

    return sorted(
        result, key=lambda x: x[1]
    )
