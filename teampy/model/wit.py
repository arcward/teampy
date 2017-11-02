"""Work item tracking API models"""


class WorkItem:
    def __init__(self, fields=None, id=None, relations=None, rev=None):
        self.fields = fields
        self.id = id
        self.relations = relations
        self.rev = rev


class Project:
    def __init__(self, id=None, name=None, description=None, url=None,
                 state=None, revision=None):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.state = state
        self.revision = revision


