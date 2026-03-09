def test_get_activities(client):
    """Test GET /activities endpoint returns all activities."""
    # Arrange: No specific setup needed as activities are reset by fixture

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response data
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_root_redirect(client):
    """Test GET / endpoint redirects to static frontend."""
    # Arrange: No specific setup needed

    # Act: Make GET request to /
    response = client.get("/", follow_redirects=False)

    # Assert: Check redirect response
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"


def test_signup_valid(client):
    """Test successful signup for an activity."""
    # Arrange: Choose an activity and email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = client.get("/activities").json()[activity_name]["participants"].copy()

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response and participant was added
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]

    # Verify participant was added to the activity
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == len(initial_participants) + 1


def test_signup_duplicate(client):
    """Test signup fails when student is already signed up."""
    # Arrange: Choose an activity and email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity."""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_valid(client):
    """Test successful unregister from an activity."""
    # Arrange: Choose an activity and email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    initial_participants = client.get("/activities").json()[activity_name]["participants"].copy()

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response and participant was removed
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Successfully unregistered {email} from {activity_name}" in data["message"]

    # Verify participant was removed from the activity
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == len(initial_participants) - 1


def test_unregister_not_signed_up(client):
    """Test unregister fails when student is not signed up."""
    # Arrange: Choose an activity and email not signed up
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity."""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]