def async_request(request):
    return {
        "request": request.id,
        "message": "this request is async, to check if it's done, head to api/request/is_done/<request_id>",
        "is_done_url": "api/request/is_done/{0}".format(request.id)
    }
