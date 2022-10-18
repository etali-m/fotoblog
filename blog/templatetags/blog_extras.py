from django import template
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()

@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'you'
    return user.username

@register.filter
def get_posted_at_display(posted_at):
    second_ago = (timezone.now() - posted_at).total_seconds()
    if second_ago <= HOUR:
        return f'Posted {int(second_ago // MINUTE)} minute ago.'
    elif second_ago <= DAY:
        return f'Posted {int(second_ago // HOUR)} hours ago.'
    return f'Posted at {posted_at.strftime("%H:%M %d %b %y")}'