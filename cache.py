# cache.py

import time
from config import sheet

# Variabel cache untuk menyimpan data agar tidak perlu mengakses ulang Google Sheets
cached_inout_data = None
cached_stok_data = None
cached_main_data = None
cached_list_data = None

# Waktu kedaluwarsa cache dalam detik (24 jam)
CACHE_EXPIRY = 45989
cache_timestamps = {
    "inout": 0,
    "stok": 0,
    "main": 0,
    "list": 0
}

def get_google_sheet_data(spreadsheet_id, range_name):
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

def reset_cache(data_type=None):
    global cached_inout_data, cached_stok_data, cached_main_data, cached_list_data
    if data_type is None:
        cached_inout_data = None
        cache_timestamps["inout"] = 0
        cached_stok_data = None
        cache_timestamps["stok"] = 0
        cached_main_data = None
        cache_timestamps["main"] = 0
        cached_list_data = None
        cache_timestamps["list"] = 0
    elif data_type == "inout":
        cached_inout_data = None
        cache_timestamps["inout"] = 0
    elif data_type == "stok":
        cached_stok_data = None
        cache_timestamps["stok"] = 0
    elif data_type == "main":
        cached_main_data = None
        cache_timestamps["main"] = 0
    elif data_type == "list":
        cached_list_data = None
        cache_timestamps["list"] = 0
    else:
        raise ValueError("Invalid data type")