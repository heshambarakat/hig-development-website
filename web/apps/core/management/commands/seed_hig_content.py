from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from wagtail.models import Page, Site

from apps.core.models import NewWebContent
from apps.pages.models import AboutPage, ContactPage, HomePage, NewsArticlePage, NewsIndexPage, ThankYouPage
from apps.projects.models import ProjectDetailPage, ProjectsIndexPage


ROOT = Path(__file__).resolve().parents[5]
ASSETS = ROOT / "assets"
HIG_HERO_VIDEO = "/static/videos/hig/hig-hero-web.mp4"
BARAH_HERO_VIDEO = "/static/videos/barah/barah-hero.mp4"


PROJECTS = {
    "barah-residence": {
        "title": "BARAH Residence",
        "logo": ASSETS / "logos" / "barah" / "barah logo.png",
        "hero": ASSETS / "project-images" / "barah" / "Scene-02_m1-gigapixel-hq-width-5000px.jpg",
        "hero_video": BARAH_HERO_VIDEO,
        "gallery": [
            ASSETS / "project-images" / "barah" / "gate01-2.jpeg",
            ASSETS / "project-images" / "barah" / "Scene-01_m1 copy-gigapixel-hq-width-5000px.jpg",
            ASSETS / "project-images" / "barah" / "Scene-01_m1 copy-gigapixel-hq-width-5000px.jpg",
            ASSETS / "project-images" / "barah" / "Scene-03_m1 copy-gigapixel-hq-width-5000px.jpg",
            ASSETS / "project-images" / "barah" / "Scene-04_m1 copy-gigapixel-hq-width-5000px.jpg",
            ASSETS / "project-images" / "barah" / "Scene-08_hq-width-5000px.jpg",
            ASSETS / "project-images" / "barah" / "shot 01.jpg",
            ASSETS / "project-images" / "barah" / "shot02.png",
        ],
        "colors": ("#B9945B", "#080A0F"),
        "lat": "29.9739000",
        "lng": "30.9144000",
        "address_ar": "حدائق أكتوبر، غرب القاهرة، بالقرب من شارع زويل ومحاور الفيوم والواحات.",
        "address_en": "Hadayek October, West Cairo, near Zewail Street and the Fayoum and Wahat corridors.",
        "intro_ar": "براح ريزيدنس ليس مجرد مشروع سكني؛ هو مفهوم مبني على المساحة والراحة والخصوصية وإحساس العائلة. المشروع يقع في حدائق أكتوبر على Club Street بجوار Sun Capital، بتصميم New Classic ومساحات خضراء واسعة.",
        "intro_en": "BARAH Residence is more than a residential project; it is a concept built around space, comfort, privacy, and family life. It is located in Hadayek October on Club Street next to Sun Capital, with New Classic architecture and generous open areas.",
        "nearby": [
            ("شارع زويل", "Zewail Street", "قريب"),
            ("طريق الواحات", "Wahat Road", "3 دقائق"),
            ("طريق الفيوم", "Fayoum Road", "3 دقائق"),
            ("الأهرامات والمتحف المصري الكبير", "Pyramids and Grand Egyptian Museum", "6 دقائق"),
            ("Mall of Egypt", "Mall of Egypt", "9 دقائق"),
            ("Sphinx International Airport", "Sphinx International Airport", "20 دقيقة"),
        ],
        "facilities": [
            ("75% مساحات مفتوحة", "75% open spaces", "مباني على 25% فقط من مساحة المشروع، والباقي مساحات خضراء ولاندسكيب ومسطحات مائية."),
            ("منطقة تجارية وموتيل", "Commercial mall and hotel component", "خدمات يومية ومكون فندقي داعم لقيمة المشروع وتجربة السكان."),
            ("ممرات حركة", "Jogging and cycling paths", "مسارات مناسبة للحركة اليومية والمشي والرياضة الخفيفة."),
            ("مناطق عائلية", "Family areas", "مساحات للأطفال والتجمعات العائلية ضمن بيئة آمنة ومنظمة."),
        ],
        "unit_types": [
            ("وحدات سكنية", "Residential units", "مساحات سكنية من 70 متر إلى 170 متر حسب بيانات الإطلاق، بتخطيطات تراعي الخصوصية والتهوية والإطلالات المفتوحة."),
            ("وحدات فندقية", "Hotel units", "وحدات فندقية من 35 متر إلى 45 متر حسب بيانات الإطلاق، مع تحديث التفاصيل النهائية من الإدارة."),
            ("مساحات تجارية", "Retail spaces", "مول تجاري لخدمة سكان المشروع والمنطقة المحيطة."),
        ],
        "plans": [
            ("أنظمة سداد مرنة", "Flexible payment systems", "أنظمة سداد مصممة لتناسب السكن والاستثمار، مع توضيح أحدث مقدم وتقسيط عند التواصل مع فريق المبيعات."),
            ("تواصل مع المبيعات", "Talk to sales", "اترك بياناتك وسيقوم فريق HIG بتوضيح أحدث الأسعار والمساحات المتاحة."),
        ],
        "faqs": [
            ("أين يقع BARAH Residence؟", "Where is BARAH Residence located?", "يقع في حدائق أكتوبر على Club Street بجوار Sun Capital، بالقرب من شارع زويل ومحاور الواحات والفيوم.", "It is located in Hadayek October on Club Street next to Sun Capital, near Zewail Street, Wahat Road, and Fayoum Road."),
            ("ما فكرة براح؟", "What is the BARAH concept?", "براح مبني على ثلاث مساحات: مساحة في المكان، مساحة في الوقت، ومساحة نفسية تخلي الحياة أهدأ وترد الروح.", "BARAH is built around spatial comfort, time that feels slower, and psychological ease for a calmer way of living."),
            ("هل المشروع سكني أم تجاري؟", "Is it residential or commercial?", "براح مشروع سكني مع مول تجاري ومكون فندقي وخدمات داعمة لتجربة السكان.", "BARAH is residential, supported by a commercial mall, hotel component, and lifestyle services."),
            ("كيف أعرف الأسعار والمساحات؟", "How can I get prices and sizes?", "املأ نموذج التواصل وسيقوم فريق المبيعات بإرسال أحدث التفاصيل المتاحة.", "Submit the lead form and the sales team will share the latest available details."),
        ],
    },
    "caza-mall": {
        "title": "Caza Mall",
        "logo": ASSETS / "logos" / "caza" / "CAZA LOGO1.png",
        "hero": ASSETS / "project-images" / "caza" / "Caza cover.jpg",
        "hero_video": "",
        "gallery": [
            ASSETS / "project-images" / "caza" / "Mall.png",
            ASSETS / "project-images" / "caza" / "S1.jpg",
            ASSETS / "project-images" / "caza" / "S10-N.png",
            ASSETS / "project-images" / "caza" / "S2.jpg",
            ASSETS / "project-images" / "caza" / "S3.jpg",
            ASSETS / "project-images" / "caza" / "S4.jpg",
            ASSETS / "project-images" / "caza" / "S5-N.png",
            ASSETS / "project-images" / "caza" / "S9-N.png",
        ],
        "colors": ("#2C5C4A", "#D8B56D"),
        "lat": "29.9698000",
        "lng": "30.9294000",
        "address_ar": "منطقة زويل وحدائق أكتوبر، بالقرب من ميدان البترول والحي الإيطالي.",
        "address_en": "Zewail area and Hadayek October, near Petrol Square and the Italian District.",
        "intro_ar": "Caza Mall وجهة تجارية من HIG Development مصممة لتجمع بين الواجهة الواضحة، سهولة الوصول، وتجربة تشغيل مناسبة للأنشطة التجارية.",
        "intro_en": "Caza Mall is a commercial destination by HIG Development, designed around visibility, access, and an efficient operating experience for businesses.",
        "nearby": [
            ("ميدان البترول", "Petrol Square", "قريب"),
            ("الحي الإيطالي", "Italian District", "قريب"),
            ("شارع زويل", "Zewail Street", "مباشر"),
        ],
        "facilities": [
            ("واجهات تجارية", "Retail frontages", "مساحات واضحة تساعد على الظهور واستقبال العملاء."),
            ("حركة زوار", "Visitor flow", "توزيع مناسب للحركة بين المداخل والوحدات."),
            ("خدمات تشغيل", "Operational services", "تأسيس مناسب للتشغيل التجاري اليومي."),
        ],
        "unit_types": [
            ("محلات تجارية", "Retail units", "وحدات للأنشطة التجارية والخدمات."),
            ("مساحات إدارية وطبية", "Administrative and medical spaces", "مساحات مناسبة للأنشطة الإدارية والطبية والخدمية حسب طبيعة المشروع والمنطقة."),
        ],
        "plans": [
            ("أنظمة تعاقد مرنة", "Flexible contract systems", "خطط تعاقد وسداد مناسبة للأنشطة التجارية والإدارية، ويتم توضيح المتاح حسب نوع الوحدة والمساحة."),
        ],
        "faqs": [
            ("أين يقع Caza Mall؟", "Where is Caza Mall located?", "يقع في نطاق زويل وحدائق أكتوبر بالقرب من ميدان البترول والحي الإيطالي.", "It is in the Zewail and Hadayek October area near Petrol Square and the Italian District."),
            ("ما نوع الوحدات؟", "What unit types are available?", "CAZA يقدم وحدات تجارية وإدارية وطبية تخدم احتياجات المستثمرين والأنشطة اليومية في المنطقة.", "CAZA offers commercial, administrative, and medical units for investors and daily service activities."),
        ],
    },
    "il-centro-mall": {
        "title": "IL Centro Mall",
        "logo": ASSETS / "logos" / "il-centro" / "IL CENTRO LOGO.png",
        "hero": ASSETS / "project-images" / "il-centro" / "il centro day 3.png",
        "hero_video": "",
        "gallery": [
            ASSETS / "project-images" / "il-centro" / "il centro day 3.png",
            ASSETS / "project-images" / "il-centro" / "il centro n.png",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-1.jpg",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-2.jpg",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-3.jpg",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-4.jpg",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-5.jpg",
            ASSETS / "project-images" / "il-centro" / "extracted-from-brochure" / "il-centro-brochure-page-6.jpg",
        ],
        "colors": ("#1D2F45", "#B9945B"),
        "lat": "",
        "lng": "",
        "address_ar": "وجهة تجارية من HIG Development في نطاق حدائق أكتوبر، مصممة لتكون فرصة إيجار وتشغيل واضحة.",
        "address_en": "A commercial destination by HIG Development in the Hadayek October area, designed around clear leasing and operating value.",
        "intro_ar": "IL Centro Mall مشروع تجاري يقدم واجهة عصرية وهوية بصرية هادئة مناسبة للأنشطة التجارية والخدمية.",
        "intro_en": "IL Centro Mall is a commercial project with a modern facade and a calm brand presence for retail and service activities.",
        "nearby": [("مناطق سكنية قريبة", "Nearby residential communities", "قريب"), ("محاور حركة", "Main access routes", "سهل الوصول")],
        "facilities": [
            ("تصميم تجاري", "Commercial design", "واجهة ومساحات مناسبة للظهور التجاري."),
            ("فرصة إيجار واضحة", "Clear leasing opportunity", "مشروع تجاري مناسب للأنشطة التي تحتاج ظهورا وسهولة وصول وتشغيل يومي."),
        ],
        "unit_types": [("محلات ووحدات خدمات", "Retail and service units", "وحدات تجارية وخدمية مناسبة للأنشطة اليومية والعلامات التي تبحث عن موقع واضح.")],
        "plans": [("أنظمة سداد تجارية", "Commercial payment systems", "أنظمة سداد وتعاقد يتم شرحها حسب الوحدة والنشاط، مع تركيز على وضوح التكلفة والعائد المتوقع.")],
        "faqs": [
            ("ما الذي يميز IL Centro Mall؟", "What makes IL Centro Mall different?", "IL Centro يركز على الوضوح التجاري: واجهة مباشرة، سهولة وصول، وفرصة مناسبة للأنشطة التي تحتاج ظهورا وتشغيلا مستمرا.", "IL Centro focuses on commercial clarity: direct frontage, easy access, and an opportunity for businesses that need visibility and daily operation."),
            ("هل IL Centro مناسب للإيجار التجاري؟", "Is IL Centro suitable for commercial leasing?", "نعم، اتجاه المشروع مناسب للأنشطة التجارية والخدمية التي تبحث عن موقع منظم وسهل التسويق.", "Yes, the project direction suits retail and service activities looking for an organized and marketable location."),
        ],
    },
    "il-parco-mall": {
        "title": "IL Parco Mall",
        "logo": ASSETS / "logos" / "il-parco" / "IL PARCO LOGO.png",
        "hero": ASSETS / "project-images" / "il-parco" / "IMG_8685.JPG",
        "hero_video": "",
        "gallery": [
            ASSETS / "project-images" / "il-parco" / "IMG_8687.JPG",
            ASSETS / "project-images" / "il-parco" / "IMG_8688.JPG",
            ASSETS / "project-images" / "il-parco" / "IMG_8689.JPG",
            ASSETS / "project-images" / "il-parco" / "IMG_8690.JPG",
            ASSETS / "project-images" / "il-parco" / "IMG_8691.JPG",
        ],
        "colors": ("#163B35", "#B9945B"),
        "lat": "29.9722000",
        "lng": "30.9225000",
        "address_ar": "منطقة زويل وحدائق أكتوبر، وجهة تجارية تركز على الظهور والتنفيذ والثقة.",
        "address_en": "Zewail and Hadayek October area, a commercial destination focused on visibility, execution, and trust.",
        "intro_ar": "IL Parco Mall وجهة تجارية بهوية راقية تركز على الواجهة، سهولة الحركة، وتجربة زوار منظمة.",
        "intro_en": "IL Parco Mall is a refined commercial destination focused on frontage, circulation, and an organized visitor experience.",
        "nearby": [("شارع زويل", "Zewail Street", "قريب"), ("مناطق سكنية", "Residential communities", "قريب"), ("خدمات يومية", "Daily services", "محيطة")],
        "facilities": [
            ("هوية راقية", "Premium identity", "تصميم بصري مناسب لمشروع تجاري منظم."),
            ("واجهات واضحة", "Clear frontages", "تجربة مناسبة للعلامات التجارية والأنشطة الخدمية."),
            ("سهولة الوصول", "Easy access", "موقع يدعم حركة الزوار اليومية."),
        ],
        "unit_types": [("وحدات تجارية", "Retail units", "محلات ومساحات تجارية مناسبة للأنشطة الخدمية والبيع المباشر.")],
        "plans": [("خطط سداد مرنة", "Flexible payment plans", "خطط سداد مناسبة للاستثمار التجاري، مع توضيح التفاصيل حسب المساحة والنشاط عند التواصل مع فريق المبيعات.")],
        "faqs": [
            ("ما طبيعة IL Parco Mall؟", "What is IL Parco Mall?", "وجهة تجارية من HIG Development تخدم أنشطة البيع والخدمات.", "A commercial destination by HIG Development for retail and service activities."),
        ],
    },
}


NEWS = [
    {
        "slug": "barah-residence-west-cairo",
        "title": "BARAH Residence in West Cairo",
        "title_ar": "براح ريزيدنس: مساحة ترد الروح في غرب القاهرة",
        "title_en": "BARAH Residence: Space that restores calm in West Cairo",
        "intro": "BARAH Residence presents HIG's West Cairo vision through space, privacy, family comfort, and investment logic.",
        "intro_ar": "براح ريزيدنس يقدم رؤية HIG لغرب القاهرة من خلال المساحة، الخصوصية، راحة العائلة، والمنطق الاستثماري.",
        "intro_en": "BARAH Residence presents HIG's West Cairo vision through space, privacy, family comfort, and investment logic.",
        "body_ar": "<p>براح ليس عنوانا سكنيا فقط. الفكرة مبنية على مساحة في المكان، مساحة في الوقت، ومساحة نفسية تجعل الحياة أهدأ. المشروع في حدائق أكتوبر على Club Street بجوار Sun Capital، مع 25% مبان و75% مساحات مفتوحة وخضراء.</p>",
        "body_en": "<p>BARAH is not only a residential address. It is built around spatial openness, time that feels slower, and psychological comfort. The project is in Hadayek October on Club Street next to Sun Capital, with 25% built-up area and 75% open and green spaces.</p>",
    },
    {
        "slug": "commercial-destinations",
        "title": "Commercial destinations by HIG",
        "title_ar": "الوجهات التجارية في HIG: وضوح الموقع وقوة التشغيل",
        "title_en": "HIG Commercial Destinations: Location clarity and operating value",
        "intro": "Caza Mall, IL Centro Mall, and IL Parco Mall reflect HIG's commercial and administrative expansion.",
        "intro_ar": "CAZA وIL Centro وIL Parco يعكسون توسع HIG في المشروعات التجارية والإدارية بمنطق مختلف لكل وجهة.",
        "intro_en": "CAZA, IL Centro, and IL Parco reflect HIG's commercial and administrative expansion with a distinct logic for each destination.",
        "body_ar": "<p>تقدم HIG Development مشروعات تجارية وإدارية وطبية بمنطق مختلف لكل وجهة. IL Centro يعتمد على وضوح فرصة الإيجار التجاري، CAZA يركز على الموقع والأرقام والمنطق الاستثماري، وIL Parco يحتاج لإبراز التنفيذ والتقدم والثقة.</p>",
        "body_en": "<p>HIG Development presents commercial, administrative, and medical opportunities with a distinct logic for each destination. IL Centro focuses on clear commercial leasing, CAZA on location and investment logic, and IL Parco on execution progress and credibility.</p>",
    },
    {
        "slug": "why-location-matters",
        "title": "Why location matters in real estate",
        "title_ar": "لماذا يبدأ الاستثمار العقاري من الموقع؟",
        "title_en": "Why location matters in real estate investment",
        "intro": "HIG studies urban growth, new roads, future lifestyle, and long-term demand before choosing locations.",
        "intro_ar": "اختيار الموقع عند HIG مرتبط بمحاور النمو، الطرق الجديدة، ومستقبل الطلب وليس مجرد نقطة على الخريطة.",
        "intro_en": "HIG studies urban growth, new roads, future lifestyle, and long-term demand before choosing locations.",
        "body_ar": "<p>اختيار الموقع عند HIG ليس عشوائيا. القرار مرتبط بمحاور الحركة الجديدة، خطط الدولة للتوسع العمراني، مستقبل الحياة اليومية، وقابلية المنطقة للنمو. لذلك يوضح الموقع الخريطة، المناطق القريبة، وقصة كل موقع بطريقة سهلة.</p>",
        "body_en": "<p>Location selection at HIG is not random. It is tied to new roads, state development plans, future lifestyle, and area growth potential. That is why the website presents maps, nearby landmarks, and each location story clearly.</p>",
    },
    {
        "slug": "how-to-read-developer-credibility",
        "title": "How to read developer credibility",
        "title_ar": "إزاي تقرأ مصداقية المطور العقاري؟",
        "title_en": "How to read developer credibility",
        "intro": "Execution history, contracting roots, and visible progress are stronger trust signals than promises alone.",
        "intro_ar": "تاريخ التنفيذ، جذور المقاولات، والتقدم الحقيقي على الأرض أهم من الوعود وحدها.",
        "intro_en": "Execution history, contracting roots, and visible progress are stronger trust signals than promises alone.",
        "body_ar": "<p>المطور القوي لا يعتمد على الإعلان فقط. ابحث عن خبرة التنفيذ، حجم الأعمال السابقة، وضوح التخطيط، وقدرة الشركة على تحويل المشروع من وعد إلى واقع. لذلك تعتمد HIG على خبرتها المتراكمة وجذورها في المقاولات كجزء أساسي من الثقة.</p>",
        "body_en": "<p>A strong developer is not built on advertising alone. Look for execution history, previous work scale, planning clarity, and the ability to turn a promise into reality. HIG uses its accumulated experience and contracting roots as core trust signals.</p>",
    },
    {
        "slug": "barah-family-comfort",
        "title": "BARAH and family comfort",
        "title_ar": "براح والراحة العائلية: السكن كإحساس مش متر فقط",
        "title_en": "BARAH and family comfort: Home as a feeling, not only square meters",
        "intro": "BARAH connects space, childhood, privacy, and daily calm into a residential concept.",
        "intro_ar": "براح يربط بين المساحة، الطفولة، الخصوصية، والهدوء اليومي في مفهوم سكني واحد.",
        "intro_en": "BARAH connects space, childhood, privacy, and daily calm into a residential concept.",
        "body_ar": "<p>قيمة براح ليست في المساحة فقط، بل في معنى المساحة. مكان يسمح للأطفال بالحركة، للعائلة بالراحة، وللحياة اليومية أن تكون أهدأ. هذا هو الفرق بين مشروع سكني عادي ومكان يرد الروح.</p>",
        "body_en": "<p>The value of BARAH is not only in space, but in what space creates. A place for children to move, families to feel calm, and daily life to slow down. That is the difference between a normal residential project and a place that restores comfort.</p>",
    },
]


class Command(BaseCommand):
    help = "Seed HIG Development pages with real local assets. Non-destructive unless --force is used."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite editable seeded content.")

    def handle(self, *args, **options):
        force = options["force"]
        root = Page.objects.get(depth=1)

        home = HomePage.objects.first()
        if not home:
            home = HomePage(title="HIG Development", slug="home")
            root.add_child(instance=home)

        hig_primary = self.import_image(ASSETS / "logos" / "hig" / "hig-logo-primary-blueeee.png", "HIG logo primary")
        hero = self.import_image(PROJECTS["barah-residence"]["hero"], "HIG homepage hero fallback")
        barah_secondary = self.import_image(ASSETS / "project-images" / "barah" / "Scene-08_hq-width-5000px.jpg", "HIG homepage Barah secondary")
        board_images = [
            self.import_image(ASSETS / "project-images" / "hig" / "board-members" / "eng-ahmed-ashour.png", "Board portrait Eng Ahmed Ashour"),
            self.import_image(ASSETS / "project-images" / "hig" / "board-members" / "eng-alaa-el-hosary.png", "Board portrait Eng Alaa El Hosary"),
            self.import_image(ASSETS / "project-images" / "hig" / "board-members" / "eng-islam-senousi.png", "Board portrait Eng Islam Senousi"),
        ]

        if force or not home.body:
            home.meta_title = "HIG Development | WE KNOW THE ROUTE"
            home.meta_description = "HIG Development builds premium residential and commercial real estate destinations in Egypt."
            home.og_image = hero
            home.body = self.home_body(hero, barah_secondary, board_images)
            home.save_revision().publish()

        Site.objects.update_or_create(
            is_default_site=True,
            defaults={"hostname": "127.0.0.1", "port": 8000, "root_page": home, "site_name": "HIG Development"},
        )

        self.seed_basic_page(home, AboutPage, "About HIG", "about", self.about_body(hero, board_images), force)
        self.seed_basic_page(home, ContactPage, "Contact", "contact", self.contact_body(), force)
        news_index = self.seed_basic_page(home, NewsIndexPage, "News", "news", self.news_index_body(), force)
        self.seed_news(news_index, force)
        self.seed_basic_page(home, ThankYouPage, "Thank You", "thank-you", self.thank_you_body(), force)

        projects_index = self.seed_projects_index(home, force)
        Page.fix_tree()
        projects_index.refresh_from_db()
        for slug, data in PROJECTS.items():
            self.seed_project(projects_index, slug, data, force)
        self.seed_newweb_content(force)

        self.stdout.write(self.style.SUCCESS("HIG content seeded with real local assets."))

    def import_image(self, path, title):
        if not path.exists():
            return None
        Image = get_image_model()
        existing = Image.objects.filter(title=title).first()
        if existing:
            return existing
        with path.open("rb") as image_file:
            image = Image(title=title)
            image.file.save(path.name, File(image_file), save=True)
        return image

    def seed_basic_page(self, home, model, title, slug, body, force):
        page = model.objects.child_of(home).filter(slug=slug).first()
        if not page:
            page = model(title=title, slug=slug)
            home.add_child(instance=page)
        if force or not getattr(page, "body", None):
            page.body = body
            page.meta_title = f"{title} | HIG Development"
            page.meta_description = f"{title} page for HIG Development."
            page.save_revision().publish()
        return page

    def seed_newweb_content(self, force):
        content = NewWebContent.objects.first()
        if not content:
            content = NewWebContent(title="HIG New Website Content")
        if force or not content.hero_text_ar:
            content.hero_text_ar = "نطور وجهات سكنية وتجارية واضحة الهوية، قوية الموقع، ومصممة لقيمة طويلة المدى."
            content.hero_text_en = "We develop residential and commercial destinations with clear identity, strong locations, and long-term value."
            content.who_title_ar = "نضع معيارًا واضحًا للثقة في التطوير العقاري."
            content.who_title_en = "Setting a clear benchmark for real estate trust."
            content.who_text_ar = "HIG Development شركة تطوير عقاري مصرية تجمع بين خبرة التطوير وجذور مقاولات قوية من El Hosary Contracting. فلسفة الشركة تبدأ من اختيار الموقع الصحيح، تخطيط واضح، وتنفيذ يحترم العميل."
            content.who_text_en = "HIG Development is an Egyptian real estate developer combining development experience with strong contracting roots through El Hosary Contracting. The company starts with the right location, clear planning, and execution that respects the client."
            content.value_1_title_ar = "جودة استثنائية"
            content.value_1_title_en = "Exceptional Quality"
            content.value_1_text_ar = "جودة تبدأ من الفكرة والتخطيط، وتظهر في التفاصيل، المواد، وتجربة الاستخدام اليومية."
            content.value_1_text_en = "Quality starts with the idea and planning, then appears in details, materials, and everyday user experience."
            content.value_2_title_ar = "التزام"
            content.value_2_title_en = "Adherence"
            content.value_2_text_ar = "خبرة مقاولات وتنفيذ تساعد HIG على تحويل الوعود إلى مراحل واضحة قابلة للمتابعة."
            content.value_2_text_en = "Contracting and delivery experience helps HIG turn promises into clear, trackable phases."
            content.value_3_title_ar = "موثوقية"
            content.value_3_title_en = "Reliability"
            content.value_3_text_ar = "الثقة قبل البيع؛ وضوح في الموقع، البيانات، التواصل، وقيمة المشروع طويلة المدى."
            content.value_3_text_en = "Trust comes before sales, with clarity in location, data, communication, and long-term project value."
            content.value_4_title_ar = "مرونة"
            content.value_4_title_en = "Agility"
            content.value_4_text_ar = "قراءة واقعية للسوق ومحاور التنمية، مع تطوير مشاريع تلائم احتياجات السكن والاستثمار."
            content.value_4_text_en = "Real market reading and development-corridor insight shape projects for living and investment needs."
            content.barah_tagline_ar = "مساحة ترد الروح."
            content.barah_tagline_en = "Space that restores the soul."
            content.barah_text_ar = "وجهة سكنية في حدائق أكتوبر بالقرب من شارع زويل ومحاور الواحات والفيوم، بمفهوم قائم على المساحة، الخصوصية، والراحة العائلية."
            content.barah_text_en = "A residential destination in Hadayek October near Zewail Street, Wahat Road, and Fayoum Road, built around space, privacy, and family comfort."
            content.caza_text_ar = "وجهة تجارية في نطاق زويل وحدائق أكتوبر، مبنية على وضوح الواجهة وسهولة الوصول."
            content.caza_text_en = "A commercial destination in the Zewail and Hadayek October area, built around clear frontage and easy access."
            content.centro_text_ar = "مشروع تجاري بهوية عصرية وفرصة تشغيل واضحة للأعمال والخدمات اليومية."
            content.centro_text_en = "A commercial project with a modern identity and clear operating value for businesses and daily services."
            content.parco_text_ar = "وجهة تجارية تخدم المنطقة المحيطة من خلال موقع واضح وتجربة حركة منظمة."
            content.parco_text_en = "A commercial destination serving the surrounding area through a clear location and organized movement experience."
            content.featured_title_ar = "كل طريق نختاره يجب أن يصنع قيمة أوضح."
            content.featured_title_en = "Making every route more valuable."
            content.team_title_ar = "قيادة مكرسة لما هو أفضل."
            content.team_title_en = "Devoted to the unrivaled."
            content.team_text_ar = "قيادة تجمع بين الرؤية، النمو، والتنفيذ؛ وتبني قرارات HIG على الثقة واختيار الموقع الصحيح وجودة التنفيذ."
            content.team_text_en = "Leadership shaped by vision, growth, and execution; building HIG decisions around trust, disciplined locations, and delivery quality."
            content.insights_title_ar = "أخبار ورؤى من HIG."
            content.insights_title_en = "News & insights from HIG."
            content.insight_1_ar = "اختيار الموقع الصحيح هو بداية القرار العقاري الناجح"
            content.insight_1_en = "Choosing the right location is the start of a successful real estate decision"
            content.insight_2_ar = "BARAH Residence ورؤية HIG لغرب القاهرة"
            content.insight_2_en = "BARAH Residence and HIG's West Cairo vision"
            content.insight_3_ar = "لماذا تتحول حدائق أكتوبر إلى منطقة واعدة للاستثمار التجاري؟"
            content.insight_3_en = "Why Hadayek October is becoming a promising commercial investment area"
            content.contact_title_ar = "ابدأ طريقك بمحادثة واضحة."
            content.contact_title_en = "Start your route with a clear conversation."
            content.contact_text_ar = "اترك بياناتك وسيقوم فريق HIG بالتواصل معك بأحدث تفاصيل المشاريع والمساحات المتاحة."
            content.contact_text_en = "Leave your details and the HIG team will contact you with the latest project and availability details."
        content.save()

    def seed_projects_index(self, home, force):
        page = ProjectsIndexPage.objects.child_of(home).filter(slug="projects").first()
        if not page:
            page = ProjectsIndexPage(title="Projects", slug="projects")
            home.add_child(instance=page)
        if force or not page.intro_ar:
            page.intro_ar = "استكشف مشروعات HIG Development السكنية والتجارية، من براح ريزيدنس إلى الوجهات التجارية Caza وIL Centro وIL Parco."
            page.intro_en = "Explore HIG Development residential and commercial projects, from BARAH Residence to Caza, IL Centro, and IL Parco."
            page.meta_title = "Projects | HIG Development"
            page.meta_description = "Explore HIG Development projects, locations, galleries, facilities, and lead forms."
            page.save_revision().publish()
        return page

    def seed_project(self, projects_index, slug, data, force):
        page = ProjectDetailPage.objects.child_of(projects_index).filter(slug=slug).first()
        logo = self.import_image(data["logo"], f"{data['title']} logo")
        hero = self.import_image(data["hero"], f"{data['title']} hero")
        gallery = [img for img in [self.import_image(path, f"{data['title']} gallery {index + 1}") for index, path in enumerate(data["gallery"])] if img]
        if not page:
            page = ProjectDetailPage(title=data["title"], slug=slug)
            projects_index.add_child(instance=page)

        if force or not page.hero_image:
            page.project_name_ar = data["title"]
            page.project_name_en = data["title"]
            page.brand_primary_color = data["colors"][0]
            page.brand_secondary_color = data["colors"][1]
            page.logo = logo
            page.hero_image = hero
            page.hero_video_url = data.get("hero_video", "")
            page.latitude = data["lat"] or None
            page.longitude = data["lng"] or None
            page.map_zoom = 14
            page.map_marker_title = data["title"]
            page.map_marker_description = data["address_ar"]
            page.project_address = data["address_ar"]
            page.directions_url = self.directions_url(data)
            page.nearby_landmarks = [{"name": ar, "distance": distance} for ar, _, distance in data["nearby"]]
            page.meta_title = f"{data['title']} | HIG Development"
            page.meta_description = f"Explore {data['title']} by HIG Development: location, facilities, gallery, FAQs, and contact form."
            page.og_image = hero
            page.body = self.project_body(data, logo, hero, gallery)
            page.save_revision().publish()

    def seed_news(self, news_index, force):
        for item in NEWS:
            article = NewsArticlePage.objects.child_of(news_index).filter(slug=item["slug"]).first()
            if not article:
                article = NewsArticlePage(title=item["title"], slug=item["slug"])
                news_index.add_child(instance=article)
            if force or not article.body:
                article.intro = item["intro"]
                article.title_ar = item["title_ar"]
                article.title_en = item["title_en"]
                article.intro_ar = item["intro_ar"]
                article.intro_en = item["intro_en"]
                article.date = date.today()
                article.meta_title = f"{item['title']} | HIG Development"
                article.meta_description = item["intro"]
                article.body = [
                    ("text_image", {
                        "show_section": True,
                        "layout_variant": "centered",
                        "title_ar": item["title_ar"],
                        "title_en": item["title_en"],
                        "text_ar": item["body_ar"],
                        "text_en": item["body_en"],
                        "show_button": True,
                        "button_text_ar": "استكشف المشاريع",
                        "button_text_en": "Explore Projects",
                        "button_link": "/ar/projects/",
                    })
                ]
                article.save_revision().publish()

    def directions_url(self, data):
        if data["lat"] and data["lng"]:
            return f"https://www.openstreetmap.org/directions?to={data['lat']}%2C{data['lng']}"
        return ""

    def board_members_block(self, images=None):
        images = images or []
        return ("board_members", {
            "show_section": True,
            "section_anchor_id": "board-members",
            "title_ar": "مجلس الإدارة",
            "title_en": "Board Members",
            "subtitle_ar": "قيادة تجمع بين الرؤية، النمو، والتنفيذ؛ وتبني قرارات HIG على الثقة واختيار الموقع الصحيح وجودة التنفيذ.",
            "subtitle_en": "Leadership shaped by vision, growth, and execution; building HIG decisions around trust, disciplined locations, and delivery quality.",
            "members": [
                {
                    "name_ar": "م. أحمد عاشور",
                    "name_en": "Eng. Ahmed Ashour",
                    "title_ar": "الرئيس التنفيذي",
                    "title_en": "Chief Executive Officer",
                    "bio_ar": "يقود مسار النمو والتوسع، ويربط قرارات الاستثمار بفهم السوق ومحاور التنمية واحتياجات العملاء.",
                    "bio_en": "Drives growth and expansion, connecting investment decisions with market insight, development corridors, and customer needs.",
                    "image": images[0] if len(images) > 0 else None,
                },
                {
                    "name_ar": "م. علاء الحصري",
                    "name_en": "Eng. Alaa El Hosary",
                    "title_ar": "رئيس مجلس الإدارة",
                    "title_en": "Chairman",
                    "bio_ar": "يقود رؤية HIG القائمة على الثقة، اختيار الموقع الصحيح، والتخطيط طويل المدى لمشروعات سكنية وتجارية واضحة القيمة.",
                    "bio_en": "Leads HIG's vision around trust, disciplined location selection, and long-term value across residential and commercial destinations.",
                    "image": images[1] if len(images) > 1 else None,
                },
                {
                    "name_ar": "م. إسلام سنوسي",
                    "name_en": "Eng. Islam Senousi",
                    "title_ar": "عضو مجلس الإدارة",
                    "title_en": "Board Member",
                    "bio_ar": "يركز على التنفيذ والجودة والتفاصيل الهندسية التي تحول وعد المشروع إلى تجربة موثوقة على أرض الواقع.",
                    "bio_en": "Focuses on execution, quality, and engineering detail that turns a project promise into a reliable real-world experience.",
                    "image": images[2] if len(images) > 2 else None,
                },
            ],
        })

    def home_body(self, hero, secondary_image=None, board_images=None):
        return [
            ("hero", {
                "show_section": True,
                "eyebrow_ar": "HIG Development",
                "eyebrow_en": "HIG Development",
                "title_ar": "WE KNOW THE ROUTE.",
                "title_en": "WE KNOW THE ROUTE.",
                "subtitle_ar": "نطوّر وجهات سكنية وتجارية واضحة الهوية، قوية الموقع، ومصممة لقيمة طويلة المدى.",
                "subtitle_en": "We develop residential and commercial destinations with clear identity, strong locations, and long-term value.",
                "image": hero,
                "video_url": HIG_HERO_VIDEO,
                "button_text_ar": "استكشف المشاريع",
                "button_text_en": "Explore Projects",
                "button_link": "/ar/projects/",
                "show_button": True,
            }),
            ("text_image", {
                "show_section": True,
                "layout_variant": "split",
                "title_ar": "HIG Development",
                "title_en": "HIG Development",
                "text_ar": "<p>HIG Development شركة تطوير عقاري مصرية تجمع بين خبرة التطوير وجذور مقاولات قوية من El Hosary Contracting. الشركة تتحرك بمنطق واضح: اختيار موقع صحيح، تخطيط مدروس، تنفيذ موثوق، وقيمة طويلة المدى.</p>",
                "text_en": "<p>HIG Development is an Egyptian real estate developer combining development experience with strong contracting roots through El Hosary Contracting. The route is clear: the right location, studied planning, credible execution, and long-term value.</p>",
                "image": hero,
                "secondary_image": secondary_image,
                "button_text_ar": "اعرف المزيد",
                "button_text_en": "Learn More",
                "button_link": "/ar/about/",
                "show_button": True,
            }),
            ("stats", {
                "show_section": True,
                "title_ar": "أرقام تعكس الثقة",
                "title_en": "Built on trust",
                "stats": [
                    {"value": "10+", "label_ar": "سنوات خبرة متراكمة", "label_en": "Years of accumulated experience"},
                    {"value": "50+", "label_ar": "مشروعا في محفظة الخبرات", "label_en": "Projects across the experience portfolio"},
                    {"value": "950M+", "label_ar": "جنيه أعمال مقاولات", "label_en": "EGP contracting work"},
                    {"value": "79+", "label_ar": "مبنى ضمن خبرات الإسكان", "label_en": "Buildings through housing work"},
                ],
            }),
            self.board_members_block(board_images),
            ("cta_button", {
                "show_section": True,
                "title_ar": "ابدأ رحلتك العقارية مع HIG",
                "title_en": "Start your real estate journey with HIG",
                "text_ar": "اترك بياناتك وسيقوم فريق HIG بالتواصل معك بأحدث التفاصيل.",
                "text_en": "Leave your details and the HIG team will contact you with the latest details.",
                "button_text_ar": "تواصل معنا",
                "button_text_en": "Contact Us",
                "button_link": "/ar/contact/",
                "show_button": True,
            }),
            ("lead_form", {
                "show_section": True,
                "section_anchor_id": "home-lead",
                "title_ar": "سجل اهتمامك بمشروعات HIG",
                "title_en": "Register your interest in HIG projects",
                "project_name": "HIG Development",
                "button_text_ar": "إرسال الطلب",
                "button_text_en": "Submit Request",
            }),
        ]

    def about_body(self, image, board_images=None):
        return [
            ("text_image", {
                "show_section": True,
                "layout_variant": "split",
                "title_ar": "We Know The Route",
                "title_en": "We Know The Route",
                "text_ar": "<p>HIG Development لا تبدأ من الصفر؛ خلفها أكثر من 10 سنوات خبرة متراكمة، جذور مقاولات قوية، ومحفظة خبرات تتجاوز 50 مشروعا بين السكني والتجاري والإداري. فلسفة الشركة أن الثقة تسبق البيع، وأن المشروع الناجح يبدأ من موقع صحيح وتخطيط واضح وتنفيذ يحترم العميل.</p>",
                "text_en": "<p>HIG Development is not starting from zero. It brings more than 10 years of accumulated experience, strong contracting roots, and a portfolio of more than 50 projects across residential, commercial, and administrative categories. The company's philosophy is that trust comes before sales, and successful projects start with location, planning, and execution quality.</p>",
                "image": image,
                "button_text_ar": "شاهد المشاريع",
                "button_text_en": "View Projects",
                "button_link": "/ar/projects/",
                "show_button": True,
            }),
            self.board_members_block(board_images),
        ]

    def news_index_body(self):
        return [
            ("cta_button", {
                "show_section": True,
                "layout_variant": "centered",
                "title_ar": "أخبار ورؤى HIG",
                "title_en": "HIG News and Insights",
                "text_ar": "مقالات قصيرة عن المشروعات، المواقع، والقرارات العقارية.",
                "text_en": "Short articles about projects, locations, and real estate decision-making.",
                "show_button": False,
            })
        ]

    def contact_body(self):
        return [
            ("lead_form", {
                "show_section": True,
                "title_ar": "تواصل مع فريق HIG",
                "title_en": "Contact HIG team",
                "project_name": "General",
                "button_text_ar": "إرسال",
                "button_text_en": "Submit",
            })
        ]

    def thank_you_body(self):
        return [
            ("cta_button", {
                "show_section": True,
                "layout_variant": "centered",
                "title_ar": "تم استلام طلبك",
                "title_en": "Your request has been received",
                "text_ar": "سيتواصل معك فريق HIG في أقرب وقت.",
                "text_en": "The HIG team will contact you shortly.",
                "button_text_ar": "العودة للرئيسية",
                "button_text_en": "Back Home",
                "button_link": "/ar/",
                "show_button": True,
            })
        ]

    def project_body(self, data, logo, hero, gallery):
        nearby_places = [{"name_ar": ar, "name_en": en, "distance_ar": distance, "distance_en": distance} for ar, en, distance in data["nearby"]]
        return [
            ("project_brand", {
                "show_section": True,
                "project_name_ar": data["title"],
                "project_name_en": data["title"],
                "logo": logo,
                "primary_color": data["colors"][0],
                "secondary_color": data["colors"][1],
                "description_ar": data["intro_ar"],
                "description_en": data["intro_en"],
            }),
            ("text_image", {
                "show_section": True,
                "layout_variant": "split",
                "title_ar": "نظرة عامة على المشروع",
                "title_en": "Project overview",
                "text_ar": f"<p>{data['intro_ar']}</p>",
                "text_en": f"<p>{data['intro_en']}</p>",
                "image": hero,
                "button_text_ar": "اطلب التفاصيل",
                "button_text_en": "Request Details",
                "button_link": "#lead",
                "show_button": True,
            }),
            ("dynamic_map", {
                "show_section": True,
                "title_ar": "الموقع والخريطة",
                "title_en": "Location and map",
                "latitude": data["lat"] or None,
                "longitude": data["lng"] or None,
                "zoom_level": 14,
                "marker_title_ar": data["title"],
                "marker_title_en": data["title"],
                "marker_description_ar": data["address_ar"],
                "marker_description_en": data["address_en"],
                "directions_url": self.directions_url(data),
                "nearby_places": nearby_places,
            }),
            ("gallery", {"show_section": True, "title_ar": "معرض المشروع", "title_en": "Project gallery", "images": gallery}),
            ("facilities", {"show_section": True, "title_ar": "المميزات", "title_en": "Facilities", "facilities": self.simple_items(data["facilities"])}),
            ("unit_types", {"show_section": True, "title_ar": "أنواع الوحدات", "title_en": "Unit types", "unit_types": self.simple_items(data["unit_types"])}),
            ("payment_plans", {"show_section": True, "title_ar": "خطط الدفع", "title_en": "Payment plans", "plans": self.simple_items(data["plans"])}),
            ("faq", {
                "show_section": True,
                "title_ar": "أسئلة شائعة",
                "title_en": "FAQ",
                "faqs": [
                    {"question_ar": qar, "question_en": qen, "answer_ar": f"<p>{aar}</p>", "answer_en": f"<p>{aen}</p>"}
                    for qar, qen, aar, aen in data["faqs"]
                ],
            }),
            ("lead_form", {
                "show_section": True,
                "section_anchor_id": "lead",
                "title_ar": f"اطلب تفاصيل {data['title']}",
                "title_en": f"Request {data['title']} details",
                "project_name": data["title"],
                "button_text_ar": "إرسال",
                "button_text_en": "Submit",
            }),
        ]

    def simple_items(self, rows):
        return [
            {"title_ar": ar, "title_en": en, "description_ar": desc, "description_en": desc}
            for ar, en, desc in rows
        ]
