import json
from json import JSONDecodeError

from requests import session

from neo_api_client.urls import PROD_BASE_URL_GW_NAPI


class TotpAPI(object):

    def __init__(self, api_client):
        self.api_client = api_client
        # self.base64_token = api_client.configuration.base64_token
        self.rest_client = api_client.rest_client
        self.totp_session = None

    def totp_login(self, mobile_number=None, ucc=None, totp=None):
        header_params = {'Authorization': "Bearer " + self.api_client.configuration.bearer_token, 'neo-fin-key': self.api_client.configuration.get_neo_fin_key()}
        if self.api_client.configuration.base_url == PROD_BASE_URL_GW_NAPI:
            URL = self.api_client.configuration.get_url_details("totp_login_napi")
        else:
            URL = self.api_client.configuration.get_url_details("totp_login")
        body_params = {
            "mobileNumber": mobile_number,
            "ucc": ucc,
            "totp": totp
        }
        totp_login = self.rest_client.request(
            url=URL, method='POST',
            headers=header_params,
            body=body_params
        )
        try:
            totp_login_data = totp_login.json()
        except JSONDecodeError:
            print("Received non-JSON response:", totp_login.text)
            return {
                "Error": "Unexpected response format. Expected JSON but received something else."
            }
        # totp_login_data = totp_login.json()
        if 200 <= totp_login.status_code <= 299:
            self.api_client.configuration.view_token = totp_login_data.get("data").get("token")
            self.api_client.configuration.sid = totp_login_data.get("data").get("sid")
        return totp_login_data

    def totp_validate(self, mpin=None):
        header_params = {'Authorization': "Bearer " + self.api_client.configuration.bearer_token,
                         "sid": self.api_client.configuration.sid,
                         "Auth": self.api_client.configuration.view_token,
                         'neo-fin-key': self.api_client.configuration.get_neo_fin_key()
                         }
        if self.api_client.configuration.base_url == PROD_BASE_URL_GW_NAPI:
            URL = self.api_client.configuration.get_url_details("totp_validate_napi")
        else:
            URL = self.api_client.configuration.get_url_details("totp_validate")
        body_params = {
            "mpin": mpin
        }
        totp_validate = self.rest_client.request(
            url=URL, method='POST',
            headers=header_params,
            body=body_params
        )
        try:
            totp_validate_data = totp_validate.json()
        except JSONDecodeError:
            print("Received non-JSON response:", totp_validate.text)
            return {
                "Error": "Unexpected response format. Expected JSON but received something else."
            }
        # totp_validate_data = totp_validate.json()
        if 200 <= totp_validate.status_code <= 299:
            self.api_client.configuration.edit_token = totp_validate_data.get("data").get("token")
            self.api_client.configuration.edit_sid = totp_validate_data.get("data").get("sid")
            self.api_client.configuration.edit_rid = totp_validate_data.get("data").get("rid")
            self.api_client.configuration.serverId = totp_validate_data.get("data").get("hsServerId")
            self.api_client.configuration.data_center = totp_validate_data.get("data").get("dataCenter")
        return totp_validate_data
