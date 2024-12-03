from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Returns True if the user belongs to the given group.
    Usage in templates:
        {% if user|has_group:"GROUP_NAME" %}
            <!-- User is in the group -->
        {% endif %}
    """
    return user.groups.filter(name=group_name).exists()


