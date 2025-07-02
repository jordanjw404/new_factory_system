from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_link(context, label, field):
    request = context["request"]
    current_sort = request.GET.get("sort", "")
    direction = "" if current_sort != field else "-"
    new_sort = f"{direction}{field}" if direction else f"-{field}"

    query = request.GET.copy()
    query["sort"] = new_sort
    url = f"?{urlencode(query)}"

    # Add arrows
    arrow = ""
    if current_sort == field:
        arrow = " 🔽"
    elif current_sort == f"-{field}":
        arrow = " 🔼"

    return f'<a href="{url}" class="text-white text-decoration-none">{label}{arrow}</a>'
