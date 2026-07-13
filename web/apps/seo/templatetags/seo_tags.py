import json

from django import template


register = template.Library()


def _localized(value, ar_key, en_key, language_code):
    if language_code == "ar":
        return value.get(ar_key) or value.get(en_key) or ""
    return value.get(en_key) or value.get(ar_key) or ""


@register.simple_tag(takes_context=True)
def page_structured_data(context):
    page = context.get("page")
    request = context.get("request")
    language_code = context.get("LANGUAGE_CODE", "ar")
    if not page or not request:
        return ""

    absolute_url = request.build_absolute_uri(page.url)
    graph = [
        {
            "@type": "WebPage",
            "@id": absolute_url,
            "url": absolute_url,
            "name": getattr(page, "meta_title", "") or page.title,
            "description": getattr(page, "meta_description", ""),
            "inLanguage": language_code,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index + 1,
                    "name": ancestor.title,
                    "item": request.build_absolute_uri(ancestor.url),
                }
                for index, ancestor in enumerate(page.get_ancestors(inclusive=True).live().specific())
                if not ancestor.is_root()
            ],
        },
    ]

    if page.__class__.__name__ == "ProjectDetailPage":
        project = {
            "@type": "Residence" if "barah" in page.slug.lower() else "Place",
            "name": getattr(page, "project_name_ar", "") or page.title,
            "url": absolute_url,
            "address": getattr(page, "project_address", ""),
        }
        if getattr(page, "latitude", None) and getattr(page, "longitude", None):
            project["geo"] = {
                "@type": "GeoCoordinates",
                "latitude": str(page.latitude),
                "longitude": str(page.longitude),
            }
        graph.append(project)

    faq_entities = []
    body = getattr(page, "body", None)
    if body:
        for block in body:
            if block.block_type == "faq":
                for item in block.value.get("faqs", []):
                    faq_entities.append(
                        {
                            "@type": "Question",
                            "name": _localized(item, "question_ar", "question_en", language_code),
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": str(_localized(item, "answer_ar", "answer_en", language_code)),
                            },
                        }
                    )
    if faq_entities:
        graph.append({"@type": "FAQPage", "mainEntity": faq_entities})

    manual_schema = getattr(page, "json_ld_schema", None)
    if manual_schema:
        graph.append(manual_schema)

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
