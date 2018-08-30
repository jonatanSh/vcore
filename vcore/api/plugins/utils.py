def async_request(request):
    return api_base_wrapper({
        "request": request.id,
        "message": "this request is async, to check if it's done, head to api/request/is_done/<request_id>",
        "is_done_url": "/api/request/is_done/{0}".format(request.id)
    })


def api_error(error):
    return api_base_wrapper({
        "trace": str(error),
        "error": True,
    })


def api_base_wrapper(data):
    if "error" not in data:
        data["error"] = False
    return data
