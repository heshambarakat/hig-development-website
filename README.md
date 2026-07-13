# HIG Development Website

Premium Arabic-first bilingual corporate website for HIG Development, built with Django and Wagtail CMS.

## Application

The deployable application is in [`web/`](web/). It includes the public Arabic and English website, Wagtail administration, lead capture, visitor journey tracking, SEO foundations, and production-ready Django settings.

Local setup and deployment instructions are documented in Arabic in [`web/README.md`](web/README.md).

## Important

- Never commit `.env` or production credentials.
- Local databases, uploaded media, virtual environments, and raw design archives are intentionally excluded.
- Public website assets are maintained under `web/static/`.
