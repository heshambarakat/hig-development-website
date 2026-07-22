from django.http import JsonResponse
from django.shortcuts import redirect, render

from apps.core.models import NewWebContent


def healthcheck(request):
    return JsonResponse({"status": "ok"})


NEWWEB_COPY = {
    "ar": {
        "dir": "rtl",
        "other_lang": "EN",
        "other_url": "/en/",
        "title": "HIG Development | WE KNOW THE ROUTE",
        "description": "تصور جديد لموقع HIG Development يعرض الشركة ومشاريعها السكنية والتجارية بأسلوب فاخر.",
        "nav": ["من نحن", "المشاريع", "مجلس الإدارة", "الرؤى", "تواصل"],
        "menu": "القائمة",
        "close": "إغلاق",
        "hotline": "الخط الساخن: 01144815252",
        "hero_title": "WE KNOW\nTHE ROUTE.",
        "hero_text": "نطور وجهات سكنية وتجارية واضحة الهوية، قوية الموقع، ومصممة لقيمة طويلة المدى.",
        "explore": "استكشف المشاريع",
        "request": "اطلب تواصل",
        "scroll": "اسحب",
        "who_label": "من نحن",
        "who_title": "نضع معيارًا واضحًا للثقة في التطوير العقاري.",
        "who_text": "HIG Development شركة تطوير عقاري مصرية تجمع بين خبرة التطوير وجذور مقاولات قوية من El Hosary Contracting. فلسفة الشركة تبدأ من اختيار الموقع الصحيح، تخطيط واضح، وتنفيذ يحترم العميل.",
        "learn_more": "اعرف المزيد",
        "stats": ["سنوات خبرة", "مشروع في محفظة الخبرات", "مليون جنيه أعمال مقاولات", "مبنى ضمن خبرات الإسكان"],
        "values": [
            ("جودة استثنائية", "جودة تبدأ من الفكرة والتخطيط، وتظهر في التفاصيل، المواد، وتجربة الاستخدام اليومية."),
            ("التزام", "خبرة مقاولات وتنفيذ تساعد HIG على تحويل الوعود إلى مراحل واضحة قابلة للمتابعة."),
            ("موثوقية", "الثقة قبل البيع؛ وضوح في الموقع، البيانات، التواصل، وقيمة المشروع طويلة المدى."),
            ("مرونة", "قراءة واقعية للسوق ومحاور التنمية، مع تطوير مشاريع تلائم احتياجات السكن والاستثمار."),
        ],
        "latest": "أحدث الإطلاقات",
        "barah_tagline": "مساحة ترد الروح.",
        "barah_text": "وجهة سكنية في حدائق أكتوبر بالقرب من شارع زويل ومحاور الواحات والفيوم، بمفهوم قائم على المساحة، الخصوصية، والراحة العائلية.",
        "commercial": "تجاري",
        "residential": "سكني",
        "caza_text": "وجهة تجارية في نطاق زويل وحدائق أكتوبر، مبنية على وضوح الواجهة وسهولة الوصول.",
        "centro_text": "مشروع تجاري بهوية عصرية وفرصة تشغيل واضحة للأعمال والخدمات اليومية.",
        "parco_text": "وجهة تجارية تخدم المنطقة المحيطة من خلال موقع واضح وتجربة حركة منظمة.",
        "featured_label": "مشاريع مختارة",
        "featured_title": "كل طريق نختاره يجب أن يصنع قيمة أوضح.",
        "view_all": "كل المشاريع",
        "filters": ["الكل", "سكني", "تجاري", "أحدث الإطلاقات"],
        "team_label": "فريق القيادة",
        "team_title": "قيادة مكرسة لما هو أفضل.",
        "team_text": "قيادة تجمع بين الرؤية، النمو، والتنفيذ؛ وتبني قرارات HIG على الثقة واختيار الموقع الصحيح وجودة التنفيذ.",
        "chairman": "رئيس مجلس الإدارة",
        "vice": "الرئيس التنفيذي",
        "member": "عضو مجلس الإدارة",
        "insights_label": "من مقالاتنا",
        "insights_title": "أخبار ورؤى من HIG.",
        "insights": [
            "اختيار الموقع الصحيح هو بداية القرار العقاري الناجح",
            "BARAH Residence ورؤية HIG لغرب القاهرة",
            "لماذا تتحول حدائق أكتوبر إلى منطقة واعدة للاستثمار التجاري؟",
        ],
        "contact_label": "تواصل مع HIG",
        "contact_title": "ابدأ طريقك بمحادثة واضحة.",
        "contact_text": "اترك بياناتك وسيقوم فريق HIG بالتواصل معك بأحدث تفاصيل المشاريع والمساحات المتاحة.",
        "name": "الاسم",
        "phone": "رقم الهاتف",
        "email": "البريد الإلكتروني",
        "message": "رسالتك",
        "submit": "Request a Call",
        "current_site": "الموقع الحالي",
    },
    "en": {
        "dir": "ltr",
        "other_lang": "AR",
        "other_url": "/ar/",
        "title": "HIG Development | WE KNOW THE ROUTE",
        "description": "A premium HIG Development website concept presenting the company and its residential and commercial projects.",
        "nav": ["Who We Are", "Projects", "Board", "Insights", "Contact"],
        "menu": "Menu",
        "close": "Close",
        "hotline": "Hotline: 01144815252",
        "hero_title": "WE KNOW\nTHE ROUTE.",
        "hero_text": "We develop residential and commercial destinations with clear identity, strong locations, and long-term value.",
        "explore": "Explore Projects",
        "request": "Request a Call",
        "scroll": "Scroll",
        "who_label": "WHO WE ARE",
        "who_title": "Setting a clear benchmark for real estate trust.",
        "who_text": "HIG Development is an Egyptian real estate developer combining development experience with strong contracting roots through El Hosary Contracting. The company starts with the right location, clear planning, and execution that respects the client.",
        "learn_more": "Learn More",
        "stats": ["Years of experience", "Projects portfolio", "EGP million contracting work", "Buildings delivered"],
        "values": [
            ("Exceptional Quality", "Quality starts with the idea and planning, then appears in details, materials, and everyday user experience."),
            ("Adherence", "Contracting and delivery experience helps HIG turn promises into clear, trackable phases."),
            ("Reliability", "Trust comes before sales, with clarity in location, data, communication, and long-term project value."),
            ("Agility", "Real market reading and development-corridor insight shape projects for living and investment needs."),
        ],
        "latest": "Latest Launch",
        "barah_tagline": "Space that restores the soul.",
        "barah_text": "A residential destination in Hadayek October near Zewail Street, Wahat Road, and Fayoum Road, built around space, privacy, and family comfort.",
        "commercial": "Commercial",
        "residential": "Residential",
        "caza_text": "A commercial destination in the Zewail and Hadayek October area, built around clear frontage and easy access.",
        "centro_text": "A commercial project with a modern identity and clear operating value for businesses and daily services.",
        "parco_text": "A commercial destination serving the surrounding area through a clear location and organized movement experience.",
        "featured_label": "OTHER FEATURED PROJECTS",
        "featured_title": "Making every route more valuable.",
        "view_all": "View All Projects",
        "filters": ["All", "Residential", "Commercial", "Latest Launches"],
        "team_label": "TEAM OF EXPERTS",
        "team_title": "Devoted to the unrivaled.",
        "team_text": "Leadership shaped by vision, growth, and execution; building HIG decisions around trust, disciplined locations, and delivery quality.",
        "chairman": "Chairman",
        "vice": "Chief Executive Officer",
        "member": "Board Member",
        "insights_label": "BITS FROM OUR BLOG",
        "insights_title": "News & insights from HIG.",
        "insights": [
            "Choosing the right location is the start of a successful real estate decision",
            "BARAH Residence and HIG's West Cairo vision",
            "Why Hadayek October is becoming a promising commercial investment area",
        ],
        "contact_label": "Contact HIG",
        "contact_title": "Start your route with a clear conversation.",
        "contact_text": "Leave your details and the HIG team will contact you with the latest project and availability details.",
        "name": "Name",
        "phone": "Phone",
        "email": "Email",
        "message": "Message",
        "submit": "Request a Call",
        "current_site": "Current Website",
    },
}


def newweb_preview(request, lang="ar"):
    if lang not in NEWWEB_COPY:
        return redirect("/ar/")
    content = NewWebContent.objects.first()
    return render(request, "newweb/index.html", build_newweb_context(lang, content, request))


def build_newweb_context(lang, content=None, request=None):
    copy = NEWWEB_COPY[lang].copy()
    if content:
        apply_newweb_content(copy, content, lang)
    return {"lang_code": lang, "t": copy, "site_controls": content, "request": request}


def apply_newweb_content(copy, content, lang):
    suffix = f"_{lang}"
    simple_fields = {
        "hero_title": "hero_title",
        "hero_text": "hero_text",
        "who_title": "who_title",
        "who_text": "who_text",
        "barah_tagline": "barah_tagline",
        "barah_text": "barah_text",
        "caza_text": "caza_text",
        "centro_text": "centro_text",
        "parco_text": "parco_text",
        "featured_title": "featured_title",
        "team_title": "team_title",
        "team_text": "team_text",
        "insights_title": "insights_title",
        "contact_title": "contact_title",
        "contact_text": "contact_text",
        "footer_text": "footer_text",
    }
    for key, field in simple_fields.items():
        value = getattr(content, field + suffix, "")
        if value:
            copy[key] = value

    values = []
    for index in range(1, 5):
        title = getattr(content, f"value_{index}_title{suffix}", "")
        text = getattr(content, f"value_{index}_text{suffix}", "")
        if title or text:
            fallback_title, fallback_text = copy["values"][index - 1]
            values.append((title or fallback_title, text or fallback_text))
        else:
            values.append(copy["values"][index - 1])
    copy["values"] = values

    insights = []
    for index in range(1, 4):
        value = getattr(content, f"insight_{index}{suffix}", "")
        insights.append(value or copy["insights"][index - 1])
    copy["insights"] = insights
