from django import template

register = template.Library()

@register.filter()
def censor(value):
    if not isinstance(value,str):
        raise TypeError(f"unresolved type '{type(value)}' expected type 'str'")
    for word in value.split():
        if word == 'редиска':
            return value
        else:
            value = value.replace('редиска', 'p****')
            return value




