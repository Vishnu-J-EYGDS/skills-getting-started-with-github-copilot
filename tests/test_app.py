import pytest

# imports after conftest has adjusted sys.path
from app import app, activities


def test_root_redirect(client):
    """GET / should redirect to the static index page."""
    # don't automatically follow the redirect so we can inspect headers
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers.get("location") == "/static/index.html"


def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    # basic sanity of returned structure
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    email = "new@mergington.edu"
    r = client.post("/activities/Chess Club/signup", params={"email": email})
    assert r.status_code == 200
    assert r.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client):
    r = client.post("/activities/Foobar/signup", params={"email": "a@b.com"})
    assert r.status_code == 404


def test_signup_duplicate(client):
    email = "michael@mergington.edu"
    r = client.post("/activities/Chess Club/signup", params={"email": email})
    assert r.status_code == 400


def test_remove_participant_success(client):
    email = "daniel@mergington.edu"
    r = client.delete("/activities/Chess Club/participants", params={"email": email})
    assert r.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_activity(client):
    r = client.delete("/activities/Nope/participants", params={"email": "a@b.com"})
    assert r.status_code == 404


def test_remove_nonexistent_participant(client):
    r = client.delete("/activities/Chess Club/participants", params={"email": "nobody@here.com"})
    assert r.status_code == 404
