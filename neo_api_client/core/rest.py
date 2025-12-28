from __future__ import absolute_import

import json
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from six.moves.urllib.parse import urlencode
from neo_api_client.core.exceptions import ApiException


class RESTClientObject(object):
    """REST API Client

    This class is a client to perform requests to a REST API.

    Attributes:
        configuration (dict): configuration for the API client
    """

    def __init__(self, configuration):
        """
        Initialize the API client with a configuration dictionary and a persistent
        requests.Session to enable connection reuse and pooling which reduces
        per-request latency.
        """
        self.configuration = configuration
        # create a session to enable connection pooling / keep-alive
        self.session = requests.Session()
        # Configure retries for idempotent requests (GET) and to avoid transient failures
        retries = Retry(total=1, backoff_factor=0.1, status_forcelist=[502, 503, 504], allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'PATCH']))
        adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        # Do not override environment proxies unless needed
        # self.session.trust_env = False

    def request(self, method, url, query_params=None, headers=None, body=None, timeout=30):
        """Perform a request to the REST API using a persistent session.

        Using a Session prevents TCP/TLS handshakes on every request which
        significantly reduces per-request latency compared to creating a new
        connection each time.
        """
        method = method.upper()
        assert method in ["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH", "OPTIONS"]

        headers = headers or {}

        # Ensure we have a sensible Content-Type
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        try:
            # Prepare URL with query params
            if query_params:
                # requests can accept params separately, but build full URL for compatibility
                url = url + "?" + urlencode(query_params)

            if method in ["POST", "PUT", "PATCH", "DELETE"]:
                # JSON bodies
                if re.search("json", headers["Content-Type"], re.IGNORECASE):
                    request_kwargs = {"headers": headers, "json": body, "timeout": timeout}
                    response = self.session.request(method=method, url=url, **request_kwargs)
                # form encoded where the API expects jData
                elif re.search("x-www-form-urlencoded", headers["Content-Type"], re.IGNORECASE):
                    request_body = {}
                    if body is not None:
                        request_body["jData"] = json.dumps(body)
                    response = self.session.request(method=method, url=url, headers=headers, data=request_body, timeout=timeout)
                else:
                    msg = """In-Valid Content-Type in the Header Parameters"""
                    raise ApiException(status=0, reason=msg)
            elif method in ["GET"]:
                response = self.session.request(method=method, url=url, headers=headers, timeout=timeout)
            else:
                msg = """Cannot call the API with the provided HTTP Method"""
                raise ApiException(status=0, reason=msg)
        except Exception as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        return response
