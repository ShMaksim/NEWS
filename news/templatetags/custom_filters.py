from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='censor')
@stringfilter
def censor(value):
    unwanted_words = ['редиска', 'морковка', 'помидор']
    for word in unwanted_words:
        value = value.replace(word, word[0] + '*' * (len(word) - 1))
    return value