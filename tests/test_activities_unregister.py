def test_unregister_success_removes_participant(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["removed"] == 1
    assert payload["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "notfound@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_is_case_insensitive_and_trimmed(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "  MICHAEL@MERGINGTON.EDU  "},
    )

    assert response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants
