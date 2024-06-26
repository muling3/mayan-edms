from io import BytesIO

import requests


class TestClientAdapter(requests.adapters.BaseAdapter):
    def __init__(self, test_case, response_content=None):
        self.response_content = response_content
        self.test_case = test_case

    def build_response(self, request, django_response):
        """
        Build a requests response from a Django response.
        """
        response = requests.Response()

        response._content = self.response_content

        # Fallback to None if there's no status_code, for whatever reason.
        response.status_code = getattr(
            django_response, 'status_code', None
        )

        # Make headers case-insensitive.
        response.headers = requests.structures.CaseInsensitiveDict(
            getattr(
                django_response, 'headers', {}
            )
        )

        # Set encoding.
        response.encoding = requests.utils.get_encoding_from_headers(
            headers=response.headers
        )
        response.raw = BytesIO(
            initial_bytes=django_response.getvalue()
        )

        response.reason = django_response.reason_phrase

        if isinstance(request.url, bytes):
            response.url = request.url.decode('utf-8')
        else:
            response.url = request.url

        # Add new cookies from the server.
        requests.cookies.extract_cookies_to_jar(
            jar=response.cookies, request=request,
            response=django_response
        )

        # Give the Response some context.
        response.request = django_response
        response.connection = self

        return response

    def close(self):
        """
        No connection needs to be closed, but the method must exists
        or a `NotImplementedError` is raised.
        """

    def send(
        self, request=None, cert=None, proxies=None, stream=False,
        timeout=None, verify=True
    ):
        """
        Craft a Django request based on the attribute of requests'
        request object.
        The `request` needs to go first because upstream
        `requests.sessions` calls this method using positional arguments
        which breaks the interface.
        """
        # Expose the timeout value so that the test case can assert it.
        self.test_case.timeout = timeout

        django_response = self.test_case.generic(
            data=request.body, headers=request.headers, method=request.method,
            viewname=self.test_case._test_view_name
        )

        return self.build_response(
            django_response=django_response, request=request
        )
