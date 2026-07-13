import json
import os
from datetime import timezone

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _credentials_from_env():
    raw_credentials = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "").strip()
    if not raw_credentials:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS_JSON is empty.")
    credentials_info = json.loads(raw_credentials)
    return Credentials.from_service_account_info(credentials_info, scopes=SCOPES)


def _lead_row(lead):
    created = lead.created_at.astimezone(timezone.utc)
    return [
        created.strftime("%Y-%m-%d"),
        created.strftime("%H:%M:%S"),
        lead.name,
        lead.phone,
        lead.email,
        lead.project,
        lead.unit_type,
        lead.budget,
        lead.message,
        lead.language,
        lead.page_url,
        lead.utm_source,
        lead.utm_medium,
        lead.utm_campaign,
        lead.utm_content,
        lead.utm_term,
        lead.fbp,
        lead.fbc,
        str(lead.event_id),
        lead.status,
        lead.notes,
    ]


def sync_lead_to_google_sheet(lead):
    if os.getenv("GOOGLE_SHEETS_ENABLED", "False").lower() != "true":
        lead.google_sheet_status = "disabled"
        lead.google_sheet_synced = False
        lead.save(update_fields=["google_sheet_status", "google_sheet_synced"])
        return False

    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip()
    worksheet_name = os.getenv("GOOGLE_SHEETS_WORKSHEET_NAME", "Leads").strip() or "Leads"
    if not spreadsheet_id:
        lead.google_sheet_status = "sync_failed"
        lead.google_sheet_error = "GOOGLE_SHEETS_SPREADSHEET_ID is empty."
        lead.google_sheet_synced = False
        lead.save(update_fields=["google_sheet_status", "google_sheet_error", "google_sheet_synced"])
        return False

    try:
        service = build("sheets", "v4", credentials=_credentials_from_env(), cache_discovery=False)
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{worksheet_name}!A:U",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [_lead_row(lead)]},
        ).execute()
    except Exception as exc:
        lead.google_sheet_status = "sync_failed"
        lead.google_sheet_error = str(exc)
        lead.google_sheet_synced = False
        lead.save(update_fields=["google_sheet_status", "google_sheet_error", "google_sheet_synced"])
        return False

    lead.google_sheet_status = "synced"
    lead.google_sheet_error = ""
    lead.google_sheet_synced = True
    lead.save(update_fields=["google_sheet_status", "google_sheet_error", "google_sheet_synced"])
    return True
