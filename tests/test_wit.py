import pytest
import json
from teampy import wit


def test__field_update():
    val = wit._field_update("add", "System.Title", "Example Title")
    expected = {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Example Title"
    }
    assert val == expected


def test__field_update_full():
    val = wit._field_update("add", "/fields/System.Title", "Example Title")
    expected = {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Example Title"
    }
    assert val == expected


@pytest.fixture()
def work_item():
    wi = None
    with open('work_item.json') as json_file:
        wi = json.load(json_file)
    return wi


@pytest.fixture()
def work_item_full():
    wi = None
    with open('work_item_full.json') as json_file:
        wi = json.load(json_file)
    return wi


def test_work_item(work_item):
    wi = wit.WorkItem(**work_item)
    assert wi.id == 309


def test_work_item_full(work_item_full):
    wi = wit.WorkItem(**work_item_full)
    assert wi.id == 309
    assert len(wi.relations) > 0