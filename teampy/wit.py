"""Work item tracking API"""
import requests
import json


def _field_update(op, path, value):
    """Return a dictionary for a field operation

    :param op: *add*, *replace* or *test*
    :param path: Path of field
    :param value: Field value
    :return: dict
    """
    return {
        "op": op,
        "path": "/fields/{}".format(path) if "/fields/" not in path else path,
        "value": value
    }


class FieldClient:
    """

    """
    def __init__(self, api_client):
        self.api_client = api_client

    def all(self):
        url = self.api_client._url('wit', 'fields')
        r = self.api_client._get(url)
        return r


class WITClient:
    """Work item tracking client/queries

    For details on fields:
    https://www.visualstudio.com/en-us/docs/integrate/api/wit/work-items

    """
    def __init__(self, api_client):
        self.api_client = api_client

    def _url(self):
        """Return base URL for work items"""
        return self.api_client._url('wit', 'workitems')

    def by_id(self, ids, fields=None, as_of_date=None, expand=None):
        """Get work item(s) by ID

        https://www.visualstudio.com/en-us/docs/integrate/api/wit/work-items#get-a-work-item

        :param ids: Work item ID, or a list of them
        :param fields: List of fields to include with work items
        :type fields: dict
        :param as_of_date:
        :param expand: `all`, `relations` or `none`
        :return:
        """
        if isinstance(ids, list):
            ids = ",".join([str(id_) for id_ in ids])
        params = {"ids": ids}
        if fields:
            params["fields"] = ",".join(fields)
        if as_of_date:
            params["asOf"] = as_of_date
        if expand:
            params["$expand"] = expand
        url = self._url()
        r = self.api_client._get(url, params=params)
        response = []
        for val in r['value']:
            response.append(WorkItem(**val))
        return response

    def create(self, project, work_item_type, fields):
        """Create a work item

        :param project: Project name
        :param work_item_type: Work item type name (such as *Task*)
        :param fields: Dictionary like ``{field_name: field_value}``
        :type fields: dict
        :return:
        """
        url = ("{instance}/tfs/DefaultCollection/{project}/_apis/wit/"
               "workitems/${work_item_type}")
        url = url.format(
            instance=self.api_client.instance,
            project=project,
            work_item_type=work_item_type
        )
        data = []
        for path, value in fields.items():
            data.append(_field_update('add', path, value))
        return self._patch(url, data)

    def _patch(self, url, data):
        """

        :param url:
        :param data:
        :return:
        """
        r = requests.patch(
            url,
            auth=(self.api_client.username, self.api_client.access_token),
            params=self.api_client.request_params,
            headers={
                "content-type": "application/json-patch+json",
                "accept": "application/json"
            },
            data=json.dumps(data)
        )
        return r.json()

    def update(self, id, fields):
        """Update a work item

        :param id: Work item ID
        :param fields: Dictionary like ``{field_name: field_value}``
        :type fields: dict
        :return:
        """
        url = "{instance}/tfs/DefaultCollection/_apis/wit/workitems/{id}"
        url = url.format(
            instance=self.api_client.instance,
            id=id
        )
        data = []
        for path, value in fields.items():
            data.append(_field_update('replace', path, value))
        return self._patch(url, data)

    def add_tag(self, id, value):
        """Add a tag to a work item

        :param id: Work item ID
        :param value: Tag value
        :return:
        """
        url = "{instance}/tfs/DefaultCollection/_apis/wit/workitems/{id}"
        url = url.format(
            instance=self.api_client.instance,
            id=id
        )
        data = [_field_update('add', 'System.Tags', value)]
        return self._patch(url, data)

    def move(self, id, team_project, area_path, iteration_path):
        """Move a work item

        :param id: Work item ID
        :param team_project:
        :param area_path:
        :param iteration_path:
        :return:
        """
        url = ("{instance}/tfs/DefaultCollection/_apis/wit/"
               "workitems/{id}")
        url = url.format(
            instance=self.api_client.instance,
            id=id
        )
        data = [
            _field_update('add', 'System.TeamProject', team_project),
            _field_update('add', 'System.AreaPath', area_path),
            _field_update('add', 'System.IterationPath', iteration_path)
        ]
        return self._patch(url, data)


class Response:
    def __init__(self, count=None, value=None):
        self.count = count
        self.value = value

    def __str__(self):
        return str(self.count)


class WorkItem:
    def __init__(self, fields=None, id=None, relations=None, rev=None,
                 url=None, _links=None):
        self.fields = fields
        self.id = id
        if not relations:
            relations = []
        self.relations = [WorkItemRelation(**r) for r in relations]
        self.rev = rev
        self.url = url
        self._links = _links

    def __str__(self):
        return str(self.id)


class WorkItemFieldOperation:
    def __init__(self, path, value):
        self.path = path
        self.value = value


class Link:
    """
    https://www.visualstudio.com/en-us/docs/integrate/extensions/reference/client/api/tfs/workitemtracking/contracts/link
    """
    def __init__(self, attributes=None, rel=None, url=None, **kwargs):
        self.attributes = attributes
        self.rel = rel
        self.url = url
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return str(self.rel)


class WorkItemRelation(Link):
    """
    https://www.visualstudio.com/en-us/docs/integrate/extensions/reference/client/api/tfs/workitemtracking/contracts/workitemrelation
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


