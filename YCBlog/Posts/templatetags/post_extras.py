from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import re

register = Library()

@stringfilter
def spacify(value, autoescape=None):

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return mark_safe(re.sub('\s','&'+'nbsp;',re.sub('\n', '<br/>', esc(value))))

spacify.needs_autoescape = True

def cut_post_content(value):
    string_list = value.split('</p>')

    string_list = string_list[0:min(5,len(string_list))]

    value = '</p>'.join(string_list)+'</p>'
    
    return value


register.filter('spacify',spacify)
register.filter('cut_post_content',cut_post_content)