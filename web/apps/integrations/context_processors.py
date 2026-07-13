import os


def tracking_settings(request):
    return {
        "GTM_CONTAINER_ID": os.getenv("GTM_CONTAINER_ID", ""),
        "GA4_MEASUREMENT_ID": os.getenv("GA4_MEASUREMENT_ID", ""),
        "META_PIXEL_ID": os.getenv("META_PIXEL_ID", ""),
    }
