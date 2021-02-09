# https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
# https://django-portuguese.readthedocs.io/en/1.0/howto/custom-template-tags.html

# Pacote de filtros que podem ser uteis (esta sendo usado neste projeto)
# https://pypi.org/project/django-widget-tweaks/

from django import template
from django.template.defaultfilters import register

register = template.Library()


@register.filter
def meufiltro(value, arg):
    return 'novo_valor'
