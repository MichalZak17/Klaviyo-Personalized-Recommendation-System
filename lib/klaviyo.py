import requests

class KlaviyoClient:
    BASE_URL = "https://a.klaviyo.com/api/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "revision": "2024-06-15",
            "Authorization": f"Klaviyo-API-Key {self.api_key}"
        }

    def _make_request(self, endpoint: str, method: str = "GET", params: dict = None, data: dict = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.headers.copy()
        if method == "POST":
            headers["content-type"] = "application/json"
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"Request to {url} failed with status code {response.status_code}: {response.text}")
            raise e
        return response.json()

    def get_lists(self) -> dict:
        return self._make_request("lists/")

    def get_profiles_from_list(self, list_id: str, page_size: int = 20) -> dict:
        params = {"page[size]": page_size}
        return self._make_request(f"lists/{list_id}/profiles/", params=params)

    def get_all_products(self, page_size: int = 20) -> dict:
        params = {"page[size]": page_size}
        return self._make_request("images/", params=params)

    def create_coupon(self, external_id: str, description: str) -> dict:
        payload = {
            "data": {
                "type": "coupon",
                "attributes": {
                    "external_id": external_id,
                    "description": description
                }
            }
        }
        return self._make_request("coupons/", method="POST", data=payload)

    def create_campaign(self, name: str, send_datetime: str, subject: str, preview_text: str, from_email: str,
                        from_label: str, reply_to_email: str, cc_email: str = None, bcc_email: str = None,
                        included_audiences: list = None, excluded_audiences: list = None) -> dict:
        payload = {
            "data": {
                "type": "campaign",
                "attributes": {
                    "name": name,
                    "audiences": {
                        "included": included_audiences or [],
                        "excluded": excluded_audiences or []
                    },
                    "send_strategy": {
                        "method": "static",
                        "options_static": {
                            "datetime": send_datetime,
                            "is_local": True,
                            "send_past_recipients_immediately": True
                        },
                        "options_throttled": {
                            "datetime": "2024-06-25T20:21:11.514Z",
                            "throttle_percentage": 0
                        },
                        "options_sto": { "date": "2024-06-25" }
                    },
                    "send_options": { "use_smart_sending": True },
                    "tracking_options": {
                        "is_add_utm": True,
                        "utm_params": [
                            {
                                "name": "utm_medium",
                                "value": "campaign"
                            }
                        ],
                        "is_tracking_clicks": True,
                        "is_tracking_opens": True
                    },
                    "campaign-messages": { "data": [
                        {
                            "type": "campaign-message",
                            "attributes": {
                                "channel": "email",
                                "label": "My message name",
                                "content": {
                                    "subject": subject,
                                    "preview_text": preview_text,
                                    "from_email": from_email,
                                    "from_label": from_label,
                                    "reply_to_email": reply_to_email,
                                    "cc_email": cc_email,
                                    "bcc_email": bcc_email
                                },
                                "render_options": {
                                    "shorten_links": True,
                                    "add_org_prefix": True,
                                    "add_info_link": True,
                                    "add_opt_out_language": False
                                }
                            }
                        }
                    ]}
                }
            }
        }
        return self._make_request("campaigns/", method="POST", data=payload)

    def create_template(self, name: str, html_content: str, text_content: str) -> dict:
        payload = {
            "data": {
                "type": "template",
                "attributes": {
                    "name": name,
                    "html": html_content,
                    "text": text_content
                }
            }
        }
        return self._make_request("templates/", method="POST", data=payload)