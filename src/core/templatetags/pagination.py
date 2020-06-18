from django import template

register = template.Library()


@register.filter(name='paginate')
def paginate(pages):
    return range(1, pages + 1)
