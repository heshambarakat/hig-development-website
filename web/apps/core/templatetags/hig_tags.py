from django import template


register = template.Library()


@register.filter
def dir_for_language(language_code):
    return "rtl" if language_code == "ar" else "ltr"


@register.simple_tag(takes_context=True)
def language_switch_url(context):
    request = context.get("request")
    language = context.get("LANGUAGE_CODE", "ar")
    target = "en" if language == "ar" else "ar"
    if not request:
        return f"/{target}/"
    parts = request.path.strip("/").split("/")
    if parts and parts[0] in {"ar", "en"}:
        parts[0] = target
        return "/" + "/".join(parts) + "/"
    return f"/{target}/"
