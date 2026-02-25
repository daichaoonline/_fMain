import json
import os
import requests
import urllib3
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class GetPages:
    name: str
    uid: str
    photo: str = ""
    category: str = "Page"
    followers: int = 0


@dataclass
class GetAdmins:
    name: str
    uid: str
    photo: str = ""


class GetProfile:
    def __init__(self, token: str):
        self.token = token

    def execute_fetch(self) -> Tuple[List[GetPages], GetAdmins]:
        pages: List[GetPages] = []
        admin_info = GetAdmins()

        try:
            # 1. Fetch Admin Profile
            admin_url = "https://graph.facebook.com/v9.0/me"
            admin_params = {"access_token": self.token, "fields": "name, id, picture.type(large)"}
            admin_resp = requests.get(admin_url, params=admin_params, timeout=10, verify=False)

            if admin_resp.status_code == 200:
                a_data = admin_resp.json()
                admin_info = GetAdmins(
                    name=a_data.get('name', ''),
                    uid=a_data.get('id', ''),
                    photo=a_data.get('picture', {}).get('data', {}).get('url', '')
                )

            # 2. Fetch Managed Pages
            url = "https://graph.facebook.com/v19.0/me/accounts"
            params = {
                "access_token": self.token,
                "fields": "name, id, category, picture.type(large), followers_count",
                "limit": 100
            }
            resp = requests.get(url, params=params, timeout=20, verify=False)
            data = resp.json()

            if 'data' in data:
                for p in data['data']:
                    # Skip if the page ID is the same as the Admin ID
                    if p.get('id') == admin_info.uid:
                        continue

                    pages.append(GetPages(
                        name=p.get('name', ''),
                        uid=p.get('id'),
                        photo=p.get('picture', {}).get('data', {}).get('url', ''),
                        category=p.get('category', 'Page'),
                        followers=p.get('followers_count', 0)
                    ))
        except Exception as e:
            return f"Error: {e}"

        return pages, admin_info


class WriteData:
    def __init__(self, storage_dir: str = "profiles"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save_profile(self, admin: GetAdmins, pages: List[GetPages], token: str):
        if not admin.uid:
            return False

        save_data = {
            admin.name: {
                "admin_uid": admin.uid,
                "token": token,
                "pages": [asdict(p) for p in pages]
            }
        }

        file_path = os.path.join(self.storage_dir, f"{admin.uid}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        return True

    def load_profiles(self) -> List[Dict]:
        profiles = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.storage_dir, filename), "r", encoding="utf-8") as f:
                        profiles.append(json.load(f))
                except Exception as e:
                    continue

        return profiles


# --- Example Usage (Non-UI) ---
# if __name__ == "__main__":
#     # This part replaces your MainWindow logic
#     # You would need to import your AdbFunction and GetUserToken here
#     try:
#         # Example flow:
#         # 1. Get token from ADB (Assuming your existing config imports)
#         # uid, token = some_token_provider.get_user_token_uid()
#
#         test_token = "EAAAAUaZA8jlABQnAk30bkRw53hZBOp0KOJyXETDPzAAPuBZCMZANwm4rZCZCVHHpZAijI4aVDSEFzg97Q7DY124NmklkDA7gZBnKPZAZCf008GI7Nk2IZB8nwBQiDZCQdue1WcOkcHAJT8l5UkFnqkRljbORIDNIMaoei4N3KZBH75OhKc3G9AJ0UApXVUxXu89R0YQZDZD"
#
#         # 2. Fetch Data
#         api_service = FacebookDataService(test_token)
#         page_list, admin_obj = api_service.execute_fetch()
#
#         # 3. Save Data
#         storage = ProfileStorageManager()
#         if storage.save_to_disk(admin_obj, page_list, test_token):
#             print(f"Successfully saved profile for {admin_obj.name}")
#
#     except Exception as e:
#         print(f"Main Process Error: {e}")