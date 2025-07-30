import requests

from ..log import footprint

from .jsonable_encoder import jsonable_encoder
from .exception import RequestException, exception_to_dict


__all__ = (
    'request',
)


def request(
        method: str,
        path: str,
        host: str | None = None,
        auth_key: str | None = None,
        auth_value: str | None = None,
        auth_type: str | None = None,
        disable_caching: bool = True,
        full_return: bool = False,
        json_return: bool = True,
        internal_service: bool = True,
        push_logs: bool = True,
        **kwargs,
):
    if host is None:
        return None

    if headers := kwargs.get('headers'):
        kwargs['headers'] = jsonable_encoder(headers)

    error_details = {
        'subject': 'Error on sending request',
        'controller': 'dtpyfw.core.request',
        'payload': {
            'host': host,
            'auth_key': auth_key,
            'auth_type': auth_type,
            'method': method,
            'path': path,
            'disable_caching': disable_caching,
            'json_return': json_return,
            'internal_service': internal_service,
        }
    }

    url = f'{host}/{path}'

    if auth_key is not None and auth_value is not None and auth_type is not None:
        if auth_type == 'params':
            if 'params' not in kwargs:
                kwargs['params'] = {}

            kwargs['params'][auth_key] = auth_value
        elif auth_type == 'headers':
            if 'headers' not in kwargs:
                kwargs['headers'] = {}

            kwargs['headers'][auth_key] = auth_value

    if disable_caching:
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'].update({
            'Cache-Control': 'private, no-cache, no-store, must-revalidate, max-age=0, s-maxage=0',
            'Pragma': 'no-cache',
            'Expires': '0',
        })

    try:
        response = requests.request(method=method, url=url, **kwargs)
        status_code = response.status_code
    except Exception as exc:
        if push_logs:
            error_details['payload']['error'] = exception_to_dict(exc)
            footprint.leave(
                **error_details,
                log_type='error',
                message="We faced an error while we wanted to send an internal request.",
            )
        raise RequestException(
            status_code=500,
            message='Request Sending Error',
            controller='dtpyfw.core.request',
        )

    if full_return:
        return response

    elif json_return:
        try:
            response_json = response.json()
        except Exception as exc:
            if push_logs:
                error_details['payload']['error'] = exception_to_dict(exc)
                error_details['payload']['headers'] = response.headers
                error_details['payload']['text'] = response.text
                footprint.leave(
                    **error_details,
                    log_type='error',
                    message="We faced a non JSON response from the request.",
                )
            raise RequestException(
                status_code=500,
                message='Request Parsing Error',
                controller='dtpyfw.core.request',
            )
    else:
        return response.text

    if internal_service:
        is_success = response_json.get('success', False) if isinstance(response_json, dict) else False
        if is_success:
            return response_json.get('data')
        else:
            if push_logs:
                error_details['payload']['headers'] = response.headers
                error_details['payload']['response'] = response_json
                footprint.leave(
                    **error_details,
                    log_type='error',
                    message="We received an error after getting response from the source.",
                )
            raise RequestException(
                status_code=status_code,
                message=response_json.get('message'),
                controller='dtpyfw.core.request',
            )
    else:
        return response_json
