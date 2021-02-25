from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def video_status_badge(value):
    if value == 'IDEIA':
        color = 'primary'

    elif value == 'PRODUCAO':
        color = 'danger'

    elif value == 'REVISAO':
        color = 'warning'

    elif value == 'APROVADO':
        color = 'info'

    elif value == 'VIDEO_INVALIDO':
        color = 'danger'

    return mark_safe(f'<span class="badge badge-pill badge-{color}">{value}</span>')
