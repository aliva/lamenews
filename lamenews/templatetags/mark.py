import markdown

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = Library()

@register.filter(is_safe=True)
@stringfilter
def mark(text):
    return mark_safe(markdown.markdown(text))
