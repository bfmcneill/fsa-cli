"""
This module combines concepts found on a few different blogs pertaining to how to retry requests.  I stumbled on
the need for this type of logic because the api I am running client against was getting slammed with requests when
running tests causing test results to not be idempotent.

Sources:
1) https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
2) https://www.peterbe.com/plog/best-practice-with-retries-with-requests
3) https://stackoverflow.com/a/47461908

TimeoutHTTPAdapter class code: source 1
request_retry_session(): source 2
idea to replace request.method[get(),post(),patch(),delete()] call in codebase with request_retry_session(): source 2
idea to specify request.Session args as kwargs (data, params,etc) to prevent cryptic type error: source 3
    - if you swap code base logic from using request.get(url,params) to session.get(url,params) an error will get thrown
    - fix error by session.get(url,params=params)

- modifications were made to the code found on blogs to integrate into this codebase.
    - For example HTTPAdapter and Retry can be imported from requests.adapters directly,
        both sources referenced some deeply nested urllib3 import which was causing issues with linter
    - Added POST and PATCH to the allowed methods
    - changed method_whitelist kwarg to allowed_methods kwarg to get rid of deprecation warning
- source 1 references a method_whitelist kwarg in Retry call which has been deprecation
- source 2 does not reference a method_whitelist kwarg, assumes default wich is not
    useful in this case because POST, PATCH are needed in retry logic
"""

import requests
from requests.adapters import HTTPAdapter, Retry

DEFAULT_TIMEOUT = 5  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 503, 504),
    session=None,
):

    http = session or requests.Session()
    retry_strategy = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST", "PATCH", "DELETE"],
    )

    http.mount("http://", TimeoutHTTPAdapter(max_retries=retry_strategy))
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retry_strategy))
    return http
