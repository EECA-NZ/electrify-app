from fastapi.testclient import TestClient
from app.main import app  # Adjust this import according to your project structure

client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint to ensure it returns the correct response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_startup_event(capsys):
    """
    Test the startup event to ensure the correct print output.
    """
    app.router.on_startup[0]()
    captured = capsys.readouterr()
    assert "Visit http://localhost:8000 or http://127.0.0.1:8000 to access the app." in captured.out
