import os
from dotenv import load_dotenv
import requests

from lib.klaviyo import KlaviyoClient
from lib.menus import MenuSelector

load_dotenv()

client = KlaviyoClient(os.environ.get("KLAVIYO_API_KEY"))

all_lists = client.get_lists()

selected_list = MenuSelector.select_list(all_lists)

saved_list = selected_list

random_profile = MenuSelector.select_random_profile(
    client.get_profiles_from_list(saved_list)
)

print(client.get_all_products())

# Get all products API call is returning no data, even if the interface is providing data.

# print(client.create_coupon("123", "Test Coupon"))

campaign = client.create_campaign(
    name="My new campaign",
    send_datetime="2024-11-08T00:00:00+00:00",
    subject="Buy our product!",
    preview_text="My preview text",
    from_email="store@my-company.com",
    from_label="My Company",
    reply_to_email="reply-to@my-company.com",
    cc_email="cc@my-company.com",
    bcc_email="bcc@my-company.com",
    included_audiences=["V6Xw5s"],
    excluded_audiences=["SFwzWk"]
)
print(campaign)

try:
    template = client.create_template(
        name="Monthly Newsletter Template",
        html_content="""
        <html>
            <body>
                hello world
            </body>
        </html>
        """,
        text_content="hello world"
    )
    print(template)
except requests.HTTPError as e:
    print(f"Error creating template: {e}")

# Traceback (most recent call last):
#   File "C:\Users\micha\klaviyo-dynamic-email-generator\run.py", line 28, in <module>
#     campaign = client.create_campaign(
#                ^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\micha\klaviyo-dynamic-email-generator\lib\klaviyo.py", line 116, in create_campaign
#     return self._make_request("campaigns/", method="POST", data=payload)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\micha\klaviyo-dynamic-email-generator\lib\klaviyo.py", line 26, in _make_request
#     raise e
#   File "C:\Users\micha\klaviyo-dynamic-email-generator\lib\klaviyo.py", line 23, in _make_request
#     response.raise_for_status()
#   File "C:\Users\micha\klaviyo-dynamic-email-generator\venv\Lib\site-packages\requests\models.py", line 1024, in raise_for_status
#     raise HTTPError(http_error_msg, response=self)
# requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://a.klaviyo.com/api/campaigns/
