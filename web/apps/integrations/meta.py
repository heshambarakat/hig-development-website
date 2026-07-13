import os
import hashlib
import time

import requests


def send_meta_lead_event(lead, request):
    pixel_id = os.getenv("META_PIXEL_ID", "")
    access_token = os.getenv("META_CAPI_ACCESS_TOKEN", "")
    if not pixel_id or not access_token:
        return False

    user_data = {
        "ph": [_hash(lead.phone)],
        "client_user_agent": request.META.get("HTTP_USER_AGENT", ""),
        "client_ip_address": request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        or request.META.get("REMOTE_ADDR", ""),
    }
    if lead.email:
        user_data["em"] = [_hash(lead.email)]
    if lead.fbp:
        user_data["fbp"] = lead.fbp
    if lead.fbc:
        user_data["fbc"] = lead.fbc
    payload = {
        "data": [{
            "event_name": "Lead",
            "event_time": int(time.time()),
            "event_id": str(lead.event_id),
            "event_source_url": lead.page_url,
            "action_source": "website",
            "user_data": user_data,
            "custom_data": {"content_name": lead.project or "HIG Development"},
        }]
    }
    test_code = os.getenv("META_CAPI_TEST_EVENT_CODE", "")
    if test_code:
        payload["test_event_code"] = test_code
    try:
        response = requests.post(
            f"https://graph.facebook.com/v21.0/{pixel_id}/events",
            params={"access_token": access_token},
            json=payload,
            timeout=8,
        )
        return response.ok
    except requests.RequestException:
        return False


def _hash(value):
    normalized = "".join(str(value).strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
