from mousetools.auth import auth_obj
from mousetools.mixins.couchbase import CouchbaseMixin
from mousetools.mixins.disney import DisneyAPIMixin


def test_couchbase_mixin():
    cb = CouchbaseMixin()
    channel_data = cb.get_channel_data("wdw.facilities.1_0.en_us.attraction.80010177;entityType=Attraction")
    channel_changes = cb.get_channel_changes("wdw.facilities.1_0.en_us")

    assert channel_data

    assert channel_changes
    assert len(channel_changes["results"]) > 0


def test_disney_mixin():
    disney = DisneyAPIMixin()
    data = disney.get_disney_data(
        f"{auth_obj._environments['serviceMenuUrl']}/diningMenuSvc/orchestration/menus/17936197"
    )

    assert data
    assert "menus" in data
