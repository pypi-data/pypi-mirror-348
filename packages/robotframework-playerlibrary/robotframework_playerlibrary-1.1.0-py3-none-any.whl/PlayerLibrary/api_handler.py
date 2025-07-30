import json
from json import JSONDecodeError
from typing import Optional

from playwright.sync_api import APIResponse, expect
from .base_context import BaseContext
from .utils import pretty_logging
from robotlibcore import keyword


class APIHandler(BaseContext):

    def __init__(self, ctx):
        super().__init__(ctx)

    @keyword("start api session")
    def start_api_session(self):
        """
        Start a session to interact with RESTful API
        """
        self.setup_assertion_timeout()
        self.api = self.player.request.new_context()

    @keyword("rest post")
    def rest_post(self, url: str, headers: str, body: str, code: int = 200):
        """
        Call the POST request to the selected endpoint
        
        *url*: the endpoint of the request

        *headers*: header of the request
        
        *body*: body of the request
        
        *code*: expected response code of the request
        """
        response = self.api.post(
            url,
            headers=json.loads(headers),
            data=body,
        )
        try:
            resp_body = response.json()
        except (JSONDecodeError, TypeError):
            resp_body = str(response.body())
        self.http_request_should_be_finished(response, code)
        pretty_logging(url)
        pretty_logging(headers)
        pretty_logging(body)
        pretty_logging(response.status)
        pretty_logging(resp_body)
        return resp_body

    @keyword("rest patch")
    def rest_patch(self, url: str, headers: str, body: str, code: int = 200):
        """
        Call the PATCH request to the selected endpoint
        
        *url*: the endpoint of the request

        *headers*: header of the request
        
        *body*: body of the request
        
        *code*: expected response code of the request
        """
        response = self.api.patch(
            url,
            headers=json.loads(headers),
            data=body,
        )
        try:
            resp_body = response.json()
        except (JSONDecodeError, TypeError):
            resp_body = str(response.body())
        self.http_request_should_be_finished(response, code)
        pretty_logging(url)
        pretty_logging(headers)
        pretty_logging(body)
        pretty_logging(response.status)
        pretty_logging(resp_body)
        return resp_body

    @keyword("rest put")
    def rest_put(self, url: str, headers: str, body: str, code: int = 200):
        """
        Call the PUT request to the selected endpoint
        
        *url*: the endpoint of the request

        *headers*: header of the request
        
        *body*: body of the request
        
        *code*: expected response code of the request
        """
        response = self.api.put(
            url,
            headers=json.loads(headers),
            data=body,
        )
        try:
            resp_body = response.json()
        except (JSONDecodeError, TypeError):
            resp_body = str(response.body())
        self.http_request_should_be_finished(response, code)
        pretty_logging(url)
        pretty_logging(headers)
        pretty_logging(body)
        pretty_logging(response.status)
        pretty_logging(resp_body)
        return resp_body

    @keyword("rest delete")
    def rest_delete(self, url: str, headers: str, code: int = 200):
        """
        Call the DELETE request to the selected endpoint
        
        *url*: the endpoint of the request

        *headers*: header of the request
        
        *code*: expected response code of the request
        """
        response = self.api.delete(
            url,
            headers=json.loads(headers),
        )
        try:
            resp_body = response.json()
        except (JSONDecodeError, TypeError):
            resp_body = str(response.body())
        self.http_request_should_be_finished(response, code)
        pretty_logging(url)
        pretty_logging(headers)
        pretty_logging(response.status)
        pretty_logging(resp_body)
        return resp_body

    @keyword("rest get")
    def rest_get(self, url: str, headers: str, code: int = 200):
        """
        Call the GET request to the selected endpoint
        
        *url*: the endpoint of the request

        *headers*: header of the request
        
        *code*: expected response code of the request
        """
        response = self.api.get(
            url,
            headers=json.loads(headers)
        )
        try:
            resp_body = response.json()
        except (JSONDecodeError, TypeError):
            resp_body = str(response.body())
        self.http_request_should_be_finished(response, code)
        pretty_logging(url)
        pretty_logging(headers)
        pretty_logging(response.status)
        pretty_logging(resp_body)
        return resp_body

    @keyword("rest dispose")
    def rest_dispose(self):
        """
        Close the API session
        """
        self.api.dispose()

    @keyword("http request should be finished")
    def http_request_should_be_finished(self, response: APIResponse, code: int):
        """
        Ensure that the request is successfully sent and processed
        
        *response*: the response of the API
   
        *code*: the response code of the request
        """
        if str(code).startswith("2"):
            expect(response).to_be_ok()
        else:
            expect(response).not_to_be_ok()

    @keyword("create header")
    def create_header(self, token: Optional[str] = None, content_type: str ="application/json", **kwargs):
        """
        Create a header for a request

        *content-types*: ``application/json`` ``application/x-www-form-urlencoded`` ``multipart/form-data`` ``undefined``

        *token*: the optional token for authentication

        *kwargs*: Other key-value pairs required for the header
        """
        header = kwargs
        if token:
            header["Authorization"] = f"Bearer {token}"
        if content_type:
            header["content-type"] = content_type
        return json.dumps(header)
