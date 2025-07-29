import requests


class Location:
    """
    A class representing a location attachment for GroupMe.
    """

    def __init__(self, lat: float, lng: float, name: str = None):
        """
        Initializes the Location with latitude and longitude.

        :param lat: Latitude of the location.
        :param lng: Longitude of the location.
        """
        self.lat = lat
        self.lng = lng
        self.name = name

    def dict(self):
        """
        Returns a dictionary representation of the Location.

        :return: Dictionary representation of the Location.
        """
        return {
            "type": "location",
            "lat": str(self.lat),
            "lng": str(self.lng),
            "name": self.name,
        }


class GroupMeImage:
    """
    A class representing an image uploaded to GroupMe's image service.
    """

    def __init__(self, url: str):
        """
        Initializes the GroupMeImage from a GroupMe image URL. Use from_url to
        upload an image.

        :param url: The URL of the image.
        """

        self.url = url
        self.large = url + ".large"
        self.preview = url + ".preview"
        self.avatar = url + ".avatar"

    @classmethod
    def from_url(cls, url: str, access_token: str):
        img_res = requests.get(url, stream=True)

        res = requests.post(
            "https://image.groupme.com/pictures",
            headers={
                "X-Access-Token": access_token,
            },
            data=img_res.content
        )
        if res.status_code >= 300:
            raise Exception(f"Failed to upload image: {res.status_code} {res.text}")
        print(res.json())
        return cls(res.json()["payload"]["url"])

    def dict(self):
        """
        Returns a dictionary representation of the GroupMeImage.

        :return: Dictionary representation of the GroupMeImage.
        """
        return {"type": "image", "url": self.large}
