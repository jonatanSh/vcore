var requestify = require('requestify');

class RequestFactory {
    constructor(base_url) {
        this.url = base_url;
    }

    async_post(uri, handler, parameters = {}) {
        let url = RequestFactory.join(this.url, uri);
        requestify.post(url, parameters).then(function (response) {
            handler(response)
        });
    }

    async_get(uri, handler, parameters = {}) {
        parameters = RequestFactory.build_url_for_get(parameters);
        if (parameters === "?") {
            parameters = "";
        }
        let url = RequestFactory.join(this.url, uri + parameters);
        console.log(url, handler);
        requestify.get(url).then(function (response) {
            handler(response)
        });
    }

    static build_url_for_get(dict) {
        let url = "";
        for (let key in dict) {
            url += "&" + key + "=" + dict[key];
        }
        return "?" + url.substring(1)
    }

    static join() {
        let base = "";
        for (let arg of arguments) {
            if (base.substring(base.length - 1) === "/") {
                base += arg;
            }
            else {
                base += "/" + arg;
            }
        }
        if (base.substring(1, 0) === "/") {
            base = base.substring(1);
        }
        return base;
    }
}

exports.RequestFactory = RequestFactory;
