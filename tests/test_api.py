import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    # Create in-memory SQLite engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    # Create and yield session
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Override get_session dependency and return TestClient."""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ============== COURT TESTS ==============

def test_create_court(client: TestClient):
    """Test creating a new court."""
    response = client.post(
        "/courts/",
        json={
            "name": "Central Park Court",
            "address": "123 Main St",
            "city": "New York",
            "num_courts": 4,
            "has_lighting": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Central Park Court"
    assert data["city"] == "New York"


def test_get_courts(client: TestClient):
    """Test listing courts."""
    # Create a court first
    client.post(
        "/courts/",
        json={
            "name": "Downtown Court",
            "address": "456 Oak Ave",
            "city": "Boston",
            "num_courts": 2,
            "has_lighting": False,
        },
    )
    
    # Get all courts
    response = client.get("/courts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Downtown Court"


def test_patch_court_partial_update(client: TestClient):
    create_response = client.post(
        "/courts/",
        json={
            "name": "West Court",
            "address": "10 West St",
            "city": "Chicago",
            "num_courts": 3,
            "has_lighting": False,
        },
    )
    court_id = create_response.json()["id"]

    response = client.patch(f"/courts/{court_id}", json={"has_lighting": True})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "West Court"
    assert data["has_lighting"] is True


def test_player_skill_level_validation(client: TestClient):
    response = client.post(
        "/players/",
        json={"name": "Alex", "city": "Boston", "skill_level": "yolo"},
    )
    assert response.status_code == 422


def test_duplicate_player_registration_is_rejected(client: TestClient):
    court_response = client.post(
        "/courts/",
        json={
            "name": "Downtown Court",
            "address": "456 Oak Ave",
            "city": "Boston",
            "num_courts": 2,
            "has_lighting": False,
        },
    )
    court_id = court_response.json()["id"]

    player_response = client.post(
        "/players/",
        json={"name": "Sam", "city": "Boston", "skill_level": "beginner"},
    )
    player_id = player_response.json()["id"]

    game_response = client.post(
        "/games/",
        json={
            "scheduled_time": "2026-04-02T18:00:00",
            "court_id": court_id,
            "skill_level": "beginner",
            "max_players": 10,
            "status": "open",
        },
    )
    game_id = game_response.json()["id"]

    first_registration = client.post(f"/games/{game_id}/players/{player_id}")
    assert first_registration.status_code == 200

    duplicate_registration = client.post(f"/games/{game_id}/players/{player_id}")
    assert duplicate_registration.status_code == 400
    assert duplicate_registration.json()["detail"] == "Player is already registered for this game"


def test_list_games_includes_registered_players(client: TestClient):
    court_response = client.post(
        "/courts/",
        json={
            "name": "Harbor Court",
            "address": "100 Bay St",
            "city": "Miami",
            "num_courts": 1,
            "has_lighting": True,
        },
    )
    court_id = court_response.json()["id"]

    player_response = client.post(
        "/players/",
        json={"name": "Taylor", "city": "Miami", "skill_level": "intermediate"},
    )
    player_id = player_response.json()["id"]

    game_response = client.post(
        "/games/",
        json={
            "scheduled_time": "2026-05-03T19:30:00",
            "court_id": court_id,
            "skill_level": "intermediate",
            "max_players": 10,
            "status": "open",
        },
    )
    game_id = game_response.json()["id"]

    register_response = client.post(f"/games/{game_id}/players/{player_id}")
    assert register_response.status_code == 200

    games_response = client.get("/games/")
    assert games_response.status_code == 200
    games = games_response.json()

    game = next(g for g in games if g["id"] == game_id)
    assert len(game["players"]) == 1
    assert game["players"][0]["id"] == player_id
