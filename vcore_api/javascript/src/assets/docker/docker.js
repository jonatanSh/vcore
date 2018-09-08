let BaseAsset = require("../base").BaseAsset;
let ImageAsset = require("./images").ImageAsset;

class DockerAssetCollector extends BaseAsset {
    constructor(api) {
        super(api);
        this.images = new ImageAsset(api);
    }
}

exports.DockerAssetCollector = DockerAssetCollector;