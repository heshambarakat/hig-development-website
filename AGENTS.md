# HIG Development Website - Codex Instructions

## Main Goal
Build a premium bilingual corporate website for HIG Development on hig-dev.net.

The website must be secure, fast, SEO/AEO optimized, dynamic, animated, easy to edit, and simple to maintain.

## Stack
Use:
- Python
- Django
- Wagtail CMS
- PostgreSQL
- HTML
- CSS
- JavaScript
- Tailwind CSS
- Nginx
- Gunicorn
- Ubuntu VPS

Do not use Docker unless explicitly requested later.
Do not use WordPress.
Do not use React SPA for the main website.
Do not use heavy animation libraries unless absolutely necessary.

## Domain
Production domain:
hig-dev.net

Admin URL:
hig-dev.net/higadmin

The admin URL must not appear in the public website navigation.

## Website Languages
The website must support:
- Arabic
- English

Arabic is the primary language.

Use URL structure:
- /ar/
- /en/

## Admin Panel
Create the Wagtail admin under:
/higadmin

The admin panel must allow editing:
- Pages
- Sections
- Buttons
- Images
- Videos
- Project logos
- Project colors
- Project content
- FAQ
- SEO fields
- Landing pages
- Project map settings
- Leads
- Visitor journey tracking

## Editable Website
Use Wagtail StreamField blocks.

Create reusable editable blocks:
- HeroBlock
- TextImageBlock
- GalleryBlock
- VideoBlock
- CTAButtonBlock
- StatsBlock
- LocationBlock
- DynamicMapBlock
- NearbyPlacesBlock
- FacilitiesBlock
- UnitTypesBlock
- PaymentPlansBlock
- FAQBlock
- LeadFormBlock
- ProjectBrandBlock
- SpacerBlock

Each section should support:
- Show/hide
- Layout variant
- Background color
- Image/video
- Button text
- Button link
- Button visibility
- Arabic and English content

## Dynamic Project Map
Each project must support a dynamic interactive map.

Use Leaflet with OpenStreetMap tiles by default.

Each project map should support:
- Latitude
- Longitude
- Zoom level
- Marker title
- Marker description
- Project address
- Nearby landmarks
- Direction button URL
- Show/hide map option
- Map section title
- Arabic and English content

The map must show OpenStreetMap attribution clearly.

Do not use Google Maps API unless requested later.

## UI/UX
The website must feel:
- Premium
- Real estate focused
- Corporate
- Elegant
- Trustworthy
- Fast
- Mobile-first

Add lightweight motion:
- Scroll reveal animations
- Fade-up sections
- Staggered cards
- Subtle image zoom
- Animated stats
- Smooth CTA hover states
- Lightweight preloader

Avoid:
- Heavy animations
- Cheap templates
- Generic SaaS look
- Crowded sections
- Slow loading pages

## Preloader
Create a short brand preloader:
- Black screen
- HIG logo centered
- Logo appears and scales slightly toward the viewer
- Smooth fade into the website
- Duration around 1.2 seconds
- Do not hurt SEO or performance

## Projects
Initial projects:
- BARAH Residence
- Caza Mall
- IL Centro Mall
- IL Parco Mall

Each project must support:
- Logo
- Brand colors
- Hero image/video
- Gallery
- Location
- Dynamic map
- Nearby landmarks
- Facilities
- Unit types
- Payment plans
- FAQs
- Lead form
- Arabic content
- English content
- SEO fields

## Assets
Use the local assets folders:
- /docs/brand-guidelines
- /assets/logos
- /assets/project-images
- /assets/videos
- /assets/maps

Read each project's brand guideline PDF and use it to infer:
- Colors
- Typography direction
- Logo usage
- Visual style
- Project identity

Do not hardcode final content if it should be editable in the admin.

## Leads
Do not build a CRM.

When a user submits a form:
- Validate name and phone
- Capture project name
- Capture page URL
- Capture UTM parameters
- Capture fbp and fbc cookies when available
- Generate event_id
- Save a backup copy in PostgreSQL
- Send the lead to Google Sheets
- Send email notification to admin
- Fire Meta Pixel Lead event
- Send Meta Conversions API Lead event using the same event_id
- Redirect to a thank-you page

## Google Sheet Columns
- Date
- Time
- Name
- Phone
- Email
- Project
- Unit Type
- Budget
- Message
- Language
- Page URL
- UTM Source
- UTM Medium
- UTM Campaign
- UTM Content
- UTM Term
- fbp
- fbc
- event_id
- Status
- Notes

## Admin Lead Screen
Create a lead screen inside /higadmin showing:
- Lead name
- Phone
- Project
- Source page
- UTM campaign
- Date/time
- Google Sheet sync status
- Tracking journey summary

When opening a lead, show:
- First landing page
- Pages visited before submitting
- Project pages visited
- Time spent per page
- Scroll depth
- CTA clicks
- Lead submission time
- UTM data
- Device/browser

## Visitor Tracking
Track useful visitor journey events:
- session_started
- page_view
- project_view
- map_interaction
- scroll_depth
- cta_click
- lead_form_start
- lead_submit

Keep tracking lightweight.
Do not collect unnecessary sensitive personal data.

## Marketing Tracking
Add placeholders/settings for:
- Google Tag Manager
- GA4
- Meta Pixel
- Meta Conversions API

Use the same event_id for browser Pixel Lead and server CAPI Lead.

## SEO/AEO
Every public page must support:
- Meta title
- Meta description
- Canonical URL
- Open Graph title
- Open Graph description
- Open Graph image
- JSON-LD schema
- FAQ schema when FAQs exist
- Breadcrumb schema
- Clean headings
- Alt text
- Sitemap.xml
- Robots.txt

## Security
- Never commit .env
- Never commit secrets
- Use environment variables
- Use CSRF protection
- Use HTTPS in production
- Use secure cookies in production
- Add rate limiting to lead forms
- Validate phone numbers
- Run Django deployment checks before production

## Deployment
Production server:
- Hostinger VPS
- Ubuntu
- Nginx
- Gunicorn
- PostgreSQL
- SSL via Let's Encrypt

Do not require Docker.

## Documentation
Create README.md in Arabic explaining:
- How to run locally
- How folders are organized
- How to add project assets
- How to create admin user
- How to connect Google Sheets
- How to connect tracking pixels
- How to deploy to VPS
- How to update the site later
