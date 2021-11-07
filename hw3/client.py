from urllib import parse

import pytest
import requests

from data_objects.campaign import Campaign
from data_objects.segment import Segment
from settings import app_url, login_string, password_string


class APIClient:
    username = None
    password = None
    session = None
    csrf_token = None
    headers = None

    def set_csrf_token(self):
        res = self.session.get("https://target.my.com/wdwd").headers["set-cookie"]
        token = res.split("=")[1]
        token = token.split(";")[0]
        self.csrf_token = token
        return

    @pytest.fixture(autouse=True)
    def api_client(self):
        self.username = login_string
        self.password = password_string
        self.session = requests.Session()
        url_to_request = "https://auth-ac.my.com/auth?lang=ru&nosavelogin=0"
        headers = {
            "Referer": "https://target.my.com/",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "email": self.username,
            "password": self.password,
            "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/",
        }
        self.session.post(url_to_request, headers=headers, data=data)
        self.set_csrf_token()
        self.headers = {"X-CSRFToken": self.csrf_token}
        yield self.session
        self.session.close()

    def load_campaign_picture(self, filename, width, height):
        file = open(filename, "rb")
        data_photo = {"width": width, "height": height}

        download_photo_url = "https://target.my.com/api/v2/content/static.json"
        upload_photo_static = self.session.post(
            download_photo_url,
            headers=self.headers,
            data=data_photo,
            files={"file": file},
        ).json()
        id_photo = upload_photo_static["id"]
        return id_photo

    def load_campaign_url(self, url):
        url_parsed = parse.quote(url, safe="")
        url_id = self.session.get(
            "https://target.my.com/api/v1/urls/?url=" + url_parsed
        ).json()["id"]
        return url_id

    def create_campaign(self):
        id_photo = self.load_campaign_picture("download.jpeg", 1080, 607)
        id_photo_small = self.load_campaign_picture("download1.jpeg", 300, 300)
        url_id = self.load_campaign_url(app_url)

        create_campaign_url = "https://target.my.com/api/v2/campaigns.json"

        campaign_class = Campaign(url_id, id_photo, id_photo_small)

        resp = self.session.post(
            create_campaign_url, headers=self.headers, json=campaign_class.data_json
        )
        campaign_id = resp.json()["id"]
        campaign_class.id = int(campaign_id)
        return campaign_class

    def latest_created_campaign(self):
        check_campaign_id_full_list = self.session.get(
            "https://target.my.com/api/v2/campaigns.json?fields=id&_status__in=active"
        )
        check_campaign_id = self.session.get(
            f"https://target.my.com/api/v2/campaigns.json?fields=id&_status__in=active&offset={check_campaign_id_full_list.json()['count'] - 1}"
        )
        return check_campaign_id.json()["items"][0]["id"]

    def create_segment(self):
        segment_class = Segment()
        url = "https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags"
        res = self.session.post(url, headers=self.headers, json=segment_class.data_json)
        segment_id = res.json()["id"]
        segment_class.id = segment_id
        return segment_class

    def get_list_of_latest_active_segments(self):
        url_to_check = (
            "https://target.my.com/api/v2/remarketing/segments.json?fields=id"
        )
        r_data = self.session.get(url_to_check).json()
        offset = r_data["count"] - 2 if r_data["count"] - 2 > 0 else 0
        url_to_check2 = f"https://target.my.com/api/v2/remarketing/segments.json?fields=id&offset={offset}"  # two last segments
        segment_list = self.session.get(url_to_check2).json()
        segments = segment_list["items"]
        segment_ids = []
        for segment in segments:
            segment_ids.append(segment["id"])
        return segment_ids
