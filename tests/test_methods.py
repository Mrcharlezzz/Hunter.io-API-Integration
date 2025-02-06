import pytest 
import httpx
from fastapi.testclient import TestClient
from api import app , BASE_URL
import logging



LEADS = [
    {
        "email": "alexis@reddit.com",
        "first_name": "Alexis",
        "last_name": "Ohanian",
        "position": "Cofounder",
        "company": "Reddit"
    },
    {
        "email": "steve@airbnb.com",
        "first_name": "Steve",
        "last_name": "Chesky",
        "position": "Cofounder",
        "company": "Airbnb"
    },
    {
        "email": "jack@twitter.com",
        "first_name": "Jack",
        "last_name": "Dorsey",
        "position": "Cofounder",
        "company": "Twitter"
    }
]


@pytest.mark.parametrize(
    "testcase",
    [
        {
            "input": LEADS[0],
            "mock_response": {
                "status_code": 200,
                "json": LEADS[0],
            },
            "expected": {
                "status_code": 200,
                "data": LEADS[0],
            },
            "is_success":True
        },
        {
            "input": LEADS[1],
            "mock_response": {
                "status_code": 403,
                "json": {"details": "Invalid input"}
            },
            "expected": {
                "status_code": 403,
                "data": {"detail": "Invalid input"},
            },
            "is_success":False
        }
    ]
)
def test_create_lead(mocker,testcase):
    
    mock_response=mocker.Mock(spec=httpx.Response)
    mock_response.status_code = testcase["mock_response"]["status_code"]
    mock_response.json.return_value = testcase["mock_response"]["json"]
    mock_response.is_success = testcase["is_success"]

    mocker.patch("api.call_hunter", return_value = mock_response)
    


    client = TestClient(app)

    response = client.post("/leads", json=testcase["input"])

    assert response.status_code == testcase["expected"]["status_code"]
    assert response.json() == testcase["expected"]["data"]








