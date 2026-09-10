from datetime import datetime, timezone


def incident_payload():
    return {
        "title": "High CPU usage",
        "description": "API CPU exceeded 90 percent",
        "severity": "high",
        "source": "cloudwatch",
        "service": "nexus-api",
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }


def test_create_incident(client):
    response = client.post(
        "/api/v1/incidents",
        json=incident_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "High CPU usage"
    assert data["severity"] == "high"
    assert data["status"] == "open"
    assert data["source"] == "cloudwatch"
    assert data["service"] == "nexus-api"


def test_list_incidents(client):
    client.post(
        "/api/v1/incidents",
        json=incident_payload(),
    )

    response = client.get("/api/v1/incidents")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "High CPU usage"


def test_get_incident(client):
    create_response = client.post(
        "/api/v1/incidents",
        json=incident_payload(),
    )

    incident_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/incidents/{incident_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == incident_id
    assert data["status"] == "open"


def test_get_nonexistent_incident(client):
    response = client.get("/api/v1/incidents/99999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Incident not found"
    }


def test_invalid_incident_payload(client):
    payload = incident_payload()

    payload["title"] = ""
    payload["source"] = ""
    payload["service"] = ""

    response = client.post(
        "/api/v1/incidents",
        json=payload,
    )

    assert response.status_code == 422


def test_list_incidents_pagination(client):
    for i in range(3):
        payload = incident_payload()
        payload["title"] = f"Incident {i}"
        client.post("/api/v1/incidents", json=payload)

    response = client.get("/api/v1/incidents?limit=2")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2


def test_list_incidents_invalid_limit(client):
    response = client.get("/api/v1/incidents?limit=101")

    assert response.status_code == 422