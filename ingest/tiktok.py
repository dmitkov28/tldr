import httpx


def get_tiktok_comments(video_id):
    params = {
        "WebIdLastTime": "1724161749",
        "aid": "1988",
        "app_language": "ja-JP",
        "app_name": "tiktok_web",
        "aweme_id": video_id,  # video id
        "browser_language": "en-US",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "MacIntel",
        "browser_version": "5.0 (Macintosh)",
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        "count": "20",
        "current_region": "JP",
        # "cursor": "80",
        "data_collection_enabled": "true",
        "device_id": "7405218256002483744",
        "device_platform": "web_pc",
        "enter_from": "tiktok_web",
        "focus_state": "false",
        "fromWeb": "1",
        "from_page": "video",
        "history_len": "9",
        "is_fullscreen": "false",
        "is_non_personalized": "false",
        "is_page_visible": "true",
        "odinId": "7405218292077626400",
        "os": "mac",
        "priority_region": "",
        "referer": "https://www.google.com/",
        "region": "BG",
        "root_referer": "https://www.google.com/",
        "screen_height": "982",
        "screen_width": "1512",
        "tz_name": "Europe/Sofia",
        "user_is_login": "false",
        "verifyFp": "verify_m02j6622_lz0HLtuM_RzdJ_4l0U_8sVU_MzRJyPDdLVb2",
        "webcast_language": "en",
        "msToken": "bbyOBzffDcwSWzoLri80yCe6CLI4D4KJenxOObh8C_PPbdWynGI_QkH5nEp7UZj1V9naBkT1h3n6PbAAcSXJaI8emAICguU0VHuvzYZx6qtKMqpiNO5E_2wMrk7ilCKXd30NKPd8wL89PxlFo8qRLA==",
        "X-Bogus": "DFSzsIVOvFXAN9fbt1kyNPjIVUXA",
        "_signature": "_02B4Z6wo00001Si3uzQAAIDArp-ekKX8bxEotb-AACzs00",
    }

    data = httpx.get("https://www.tiktok.com/api/comment/list/", params=params)
    processed_data = [
        item.get("share_info", {}).get("desc") for item in data.json().get("comments")
    ]
    return processed_data
