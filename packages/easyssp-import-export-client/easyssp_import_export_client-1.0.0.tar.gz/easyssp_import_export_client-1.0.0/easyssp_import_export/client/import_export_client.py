from typing import Annotated, Any

from easyssp_utils.client import ApiClient, ApiResponse
from easyssp_utils.client.api_client import RequestSerialized
from pydantic import Field, StrictBytes, StrictFloat, StrictInt, StrictStr, validate_call

from easyssp_import_export import models
from easyssp_import_export.models import UploadResponse


class ImportExportClient:
    """
    This class contains methods for importing and exporting SSP files using the EasySSP Import-Export API.
    """

    def __init__(self, username: str, password: str, api_client=None, user_agent=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default(username=username, password=password, client_id="import-export-api",
                                               user_agent=user_agent)
        self.api_client = api_client

    @validate_call
    def export_ssp(
            self,
            ssp_id: Annotated[StrictStr, Field(description="ID of the SSP-model to download")],
            _request_timeout: (
                    None |
                    Annotated[StrictFloat, Field(gt=0)] |
                    tuple[
                        Annotated[StrictFloat, Field(gt=0)],
                        Annotated[StrictFloat, Field(gt=0)]
                    ]
            ) = None,
            _request_auth: dict[StrictStr, Any] | None = None,
            _content_type: StrictStr | None = None,
            _headers: dict[StrictStr, Any] | None = None,
            _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[bytearray]:
        """Exports an SSP-file

        Downloads the SSP-model corresponding to the SSP-model id as an .ssp-file.

        :param ssp_id: ID of the SSP-model to download (required)
        :type ssp_id: str
        :param _request_timeout: timeout setting for this request. If one
                                  number is provided, it will be a total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._export_ssp_serialize(
            ssp_id=ssp_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: dict[str, str | None] = {
            "200": "bytearray",
            "400": "LocalizedErrorMessage",
            "404": "LocalizedErrorMessage",
            "401": "ErrorMessage",
            "403": "ErrorMessage",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
            custom_models=models
        )

    def _export_ssp_serialize(
            self,
            ssp_id,
            _request_auth,
            _content_type,
            _headers,
            _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: dict[str, str] = {
        }

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[
            str, str | bytes | list[str] | list[bytes] | list[tuple[str, bytes]]
        ] = {}
        _body_params: bytes | None = None

        # process the path parameters
        if ssp_id is not None:
            _path_params["sspId"] = ssp_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(
                [
                    "application/x-ssp-package",
                    # 'application/json'
                ]
            )

        # authentication setting
        _auth_settings: list[str] = [
        ]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/integration/api/v1/ssp/{sspId}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )

    @validate_call
    def import_ssd(
            self,
            filename: Annotated[StrictStr | None, Field(
                description="The name of the SSD-file. Will use this as template for the SSP-file name when downloading the SSP-model.")] = None,
            body: StrictBytes | StrictStr | tuple[StrictStr, StrictBytes] | None = None,
            _request_timeout: (
                    None |
                    Annotated[StrictFloat, Field(gt=0)] |
                    tuple[
                        Annotated[StrictFloat, Field(gt=0)],
                        Annotated[StrictFloat, Field(gt=0)]
                    ]
            ) = None,
            _request_auth: dict[StrictStr, Any] | None = None,
            _content_type: StrictStr | None = None,
            _headers: dict[StrictStr, Any] | None = None,
            _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UploadResponse]:
        """Imports an SSD-file

        Loads a .ssd-file and adds it to a new SSP-model. When successful, the API returns the ID of the created SSP-model as well as a URL that can be used to open the SSP-Model in the easySSP WebApp.

        :param filename: The name of the SSD file. Will use this as a template for the SSP-file name when downloading the SSP-model.
        :type filename: str
        :param body:
        :type body: bytearray
        :param _request_timeout: timeout setting for this request. If one
                                  number is provided, it will be a total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._import_ssd_serialize(
            filename=filename,
            body=body,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: dict[str, str | None] = {
            "200": "UploadResponse",
            "400": "LocalizedErrorMessage",
            "500": "ErrorMessage",
            "401": "ErrorMessage",
            "403": "ErrorMessage",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
            custom_models=models
        )

    def _import_ssd_serialize(
            self,
            filename,
            body,
            _request_auth,
            _content_type,
            _headers,
            _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: dict[str, str] = {
        }

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[
            str, str | bytes | list[str] | list[bytes] | list[tuple[str, bytes]]
        ] = {}
        _body_params: bytes | None = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if filename is not None:
            _header_params["Filename"] = filename
        # process the form parameters
        # process the body parameter
        if body is not None:
            # convert to a byte array if the input is a file name (str)
            if isinstance(body, str):
                with open(body, "rb") as _fp:
                    _body_params = _fp.read()
            elif isinstance(body, tuple):
                # drop the filename from the tuple
                _body_params = body[1]
            else:
                _body_params = body

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(
                [
                    "application/json"
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params["Content-Type"] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        "application/x-ssp-definition"
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params["Content-Type"] = _default_content_type

        # authentication setting
        _auth_settings: list[str] = [
        ]

        return self.api_client.param_serialize(
            method="POST",
            resource_path="/integration/api/v1/ssd",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )

    @validate_call
    def import_ssp(
            self,
            filename: Annotated[StrictStr | None, Field(
                description="The name of the SSP-file. Will use this as a file name when downloading the SSP-model.")] = None,
            body: StrictBytes | StrictStr | tuple[StrictStr, StrictBytes] | None = None,
            _request_timeout: (
                    None |
                    Annotated[StrictFloat, Field(gt=0)] |
                    tuple[
                        Annotated[StrictFloat, Field(gt=0)],
                        Annotated[StrictFloat, Field(gt=0)]
                    ]
            ) = None,
            _request_auth: dict[StrictStr, Any] | None = None,
            _content_type: StrictStr | None = None,
            _headers: dict[StrictStr, Any] | None = None,
            _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UploadResponse]:
        """Imports an SSP-file

        Loads a .ssp-file. When successful, the API returns the ID of the created SSP-model as well as a URL that can be used to open the SSP-Model in the easySSP WebApp.

        :param filename: The name of the SSP-file. Will use this as a file name when downloading the SSP-model.
        :type filename: str
        :param body:
        :type body: bytearray
        :param _request_timeout: timeout setting for this request. If one
                                  number is provided, it will be a total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._import_ssp_serialize(
            filename=filename,
            body=body,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: dict[str, str | None] = {
            "200": "UploadResponse",
            "400": "LocalizedErrorMessage",
            "500": "ErrorMessage",
            "401": "ErrorMessage",
            "403": "ErrorMessage",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
            custom_models=models
        )

    def _import_ssp_serialize(
            self,
            filename,
            body,
            _request_auth,
            _content_type,
            _headers,
            _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: dict[str, str] = {
        }

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[
            str, str | bytes | list[str] | list[bytes] | list[tuple[str, bytes]]
        ] = {}
        _body_params: bytes | None = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if filename is not None:
            _header_params["Filename"] = filename
        # process the form parameters
        # process the body parameter
        if body is not None:
            # convert to a byte array if the input is a file name (str)
            if isinstance(body, str):
                with open(body, "rb") as _fp:
                    _body_params = _fp.read()
            elif isinstance(body, tuple):
                # drop the filename from the tuple
                _body_params = body[1]
            else:
                _body_params = body

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(
                [
                    "application/json"
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params["Content-Type"] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        "application/x-ssp-package"
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params["Content-Type"] = _default_content_type

        # authentication setting
        _auth_settings: list[str] = [
        ]

        return self.api_client.param_serialize(
            method="POST",
            resource_path="/integration/api/v1/ssp",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )
