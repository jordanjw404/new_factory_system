from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_status_display(obj, status_field):
    """Returns the display label for a status field (e.g., 'sales_status')"""
    method_name = f"get_{status_field}_display"
    if hasattr(obj, method_name):
        return getattr(obj, method_name)()
    return getattr(obj, status_field, "-")

@register.filter
def get_target_date(obj, field):
    return getattr(obj, f"{field}_target_date", None)

@register.filter
def get_completed_date(obj, field):
    return getattr(obj, f"{field}_completed_date", None)
