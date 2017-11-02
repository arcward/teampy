import requests
from teampy.wit import WITClient, FieldClient


class APIClient:
    def __init__(self, instance, username, access_token,
                 collection="DefaultCollection"):
        """

        :param instance: Instance address (ex: *http://localhost:8080*)
        :param username: Remote username
        :param access_token: Access token (to generate one, see
            https://docs.microsoft.com/en-us/vsts/accounts/use-personal-access-tokens-to-authenticate)
        :param collection: Base collection to use
        """
        self.instance = instance
        self.username = username
        self.access_token = access_token
        self.collection = collection
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json"
        }
        self.request_params = {
            "api-version": "2.0"
        }
        self.work_items = WITClient(self)
        self.fields = FieldClient(self)

    def _url(self, area, resource):
        tmpl = ("{instance}/tfs/{collection}/_apis/{area}/{resource}")
        return tmpl.format(
            instance=self.instance,
            collection=self.collection,
            area=area,
            resource=resource
        )

    def _get(self, url, params=None):
        if not params:
            params = {}
        params.update(self.request_params)
        r = requests.get(
            url,
            auth=(self.username, self.access_token),
            params=params
        )
        return r.json()
