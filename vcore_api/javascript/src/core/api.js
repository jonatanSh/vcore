let RequestFactory = require("./api_requests.js").RequestFactory;
let DockerAssetCollector = require("../assets/docker/docker").DockerAssetCollector;

class Api {
    constructor(base_url = "http://localhost", port = 5002) {
        let url = base_url + ":" + port;
        this.requests = new RequestFactory(url);
        this.docker = new DockerAssetCollector(this);
    }
}

exports.Api = Api;