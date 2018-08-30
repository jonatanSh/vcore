from ..base_asset import Asset


class Image(Asset):

    def build(self):
        return self.requests.get("docker/build")

    def __str__(self):
        return "ImageAsset(methods: [build])"
