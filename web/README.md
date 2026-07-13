# موقع HIG Development

موقع HIG Development مبني باستخدام Django + Wagtail CMS، عربي أولاً، ويدعم الإنجليزية عبر `/ar/` و`/en/`.

## التشغيل المحلي

```bash
cd "C:\Users\M&H\Desktop\HIG WEB\web"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_hig_content
python manage.py createsuperuser
python manage.py runserver
```

افتح الموقع:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/ar/`
- `http://127.0.0.1:8000/en/`
- `http://127.0.0.1:8000/higadmin/`

## بيانات الأدمن المحلية الحالية

تم إنشاء مستخدم محلي للمراجعة:

- Username: `admin`
- Password: `HigAdmin@2026`

غيّر كلمة المرور قبل أي نشر حقيقي.

## تنظيم الملفات

- `apps/pages`: صفحات Wagtail العامة و StreamField blocks.
- `apps/projects`: صفحات المشاريع وخرائطها.
- `apps/leads`: الليدز وشاشة Lead Inbox.
- `apps/tracking`: تتبع رحلة الزائر.
- `apps/integrations`: Google Sheets و Meta CAPI.
- `apps/seo`: robots وSEO helpers.
- `templates`: قوالب الموقع.
- `static`: CSS وJS ونسخ public من اللوجوهات.
- `media`: الصور التي يتم استيرادها داخل Wagtail.

الأصول الأصلية تبقى خارج التطبيق في:

- `../assets/logos`
- `../assets/project-images`
- `../assets/videos`
- `../assets/maps`
- `../docs/brand-guidelines`

## زرع المحتوى الأولي

الأمر:

```bash
python manage.py seed_hig_content
```

ينشئ الصفحات الأساسية ويستورد اللوجوهات والصور الحقيقية المتاحة داخل فولدرات المشروع.

لن يكتب فوق محتوى تم تعديله من الأدمن. لإعادة الزرع بالقوة:

```bash
python manage.py seed_hig_content --force
```

## لوحة التحكم

لوحة التحكم:

```text
/higadmin
```

من خلالها يمكن تعديل:

- الصفحات
- السكاشن
- الصور
- لوجوهات المشاريع
- ألوان المشاريع
- خرائط المشاريع
- الأسئلة الشائعة
- SEO
- الليدز
- رحلة الزائر

## Google Sheets

ضع القيم في `.env`:

```env
GOOGLE_SHEETS_ENABLED=True
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_CREDENTIALS_JSON=
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
```

إعادة محاولة الليدز التي فشل إرسالها:

```bash
python manage.py retry_failed_sheet_sync
```

## Meta Pixel وCAPI

ضع القيم في `.env`:

```env
META_PIXEL_ID=
META_CAPI_ACCESS_TOKEN=
META_CAPI_TEST_EVENT_CODE=
```

يتم استخدام نفس `event_id` للـ browser Pixel والـ server CAPI عند إرسال Lead.

## PostgreSQL

محلياً يمكن التشغيل بدون `DATABASE_URL` باستخدام SQLite للمراجعة السريعة.

للإنتاج أو VPS استخدم:

```env
DATABASE_URL=postgres://user:password@localhost:5432/hig_dev
```

## النشر على Hostinger VPS

البيئة المقترحة:

- Ubuntu
- PostgreSQL
- Gunicorn
- Nginx
- SSL عبر Let's Encrypt

قبل النشر:

```bash
python manage.py check --deploy
python manage.py collectstatic
```

## تحديث الموقع لاحقاً

كل المحتوى المهم يجب تحديثه من Wagtail وليس من الكود:

- نصوص عربي/إنجليزي
- صور وفيديوهات
- خرائط
- لوجوهات
- ألوان المشاريع
- SEO
- نماذج التواصل
