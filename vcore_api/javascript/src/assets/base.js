class BaseAsset {
    constructor(api) {
        this.api = api;
        this.requests = this.api.requests;
    }
}

exports.BaseAsset = BaseAsset;