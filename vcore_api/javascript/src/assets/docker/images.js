let BaseAsset = require("../base").BaseAsset;

class ImageAsset extends BaseAsset {
    list(handler) {
        this.requests.async_get("docker/query/images/list", handler)
    }
}

exports.ImageAsset = ImageAsset;