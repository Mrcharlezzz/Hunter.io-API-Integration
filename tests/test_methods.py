import pytest 
import httpx
from fastapi.testclient import TestClient
from src.api import app , BASE_URL
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

def create_mock_response(mocker,response):
    mock_response=mocker.Mock(spec=httpx.Response)
    mock_response.status_code = response["status_code"]
    mock_response.json.return_value = response["json"]
    mock_response.is_success = response["is_success"]
    mocker.patch("src.api.call_hunter", return_value = mock_response)


@pytest.mark.parametrize(
    "testcase",
    [
        {
            "input": LEADS[0],
            "mock_response": {
                "status_code": 200,
                "json": LEADS[0],
                "is_success":True,
            },
            "expected": {
                "status_code": 200,
                "data": LEADS[0],
            },
        },
        {
            "input": LEADS[1],
            "mock_response": {
                "status_code": 403,
                "json": {"details": "Invalid input"},
                "is_success":False
            },
            "expected": {
                "status_code": 403,
                "data": {"detail": "Invalid input"},
            },
        }
    ]
)
def test_create_lead(mocker,testcase):
    create_mock_response(mocker,testcase["mock_response"])
    
    client = TestClient(app)
    response = client.post("/leads", json=testcase["input"])

    assert response.status_code == testcase["expected"]["status_code"]
    assert response.json() == testcase["expected"]["data"]


@pytest.mark.parametrize(
    "testcase",
    [
        {
            "input": "2",
            "mock_response": {
                "status_code": 200,
                "json": LEADS[0],
                "is_success":True,
            },
            "expected": {
                "status_code": 200,
                "data": LEADS[0],
            },
        },
        {
            "input": "-1",
            "mock_response": {
                "status_code": None,
                "json": None,
                "is_success": None
            },
            "expected": {
                "status_code": 422,
                "data": {
                    "detail":[
                        {
                            'ctx': {
                                'gt': 0,
                            },
                            'input': '-1',
                            'loc': [
                                'path',
                                'id',
                            ],
                            'msg': 'Input should be greater than 0',
                            'type': 'greater_than',
                        },
                    ],
               },
            },
        }
    ]
)
def test_retrieve_lead(mocker,testcase):

    create_mock_response(mocker,testcase["mock_response"])
    client = TestClient(app)
    response = client.get("/leads/"+testcase["input"])

    assert response.status_code == testcase["expected"]["status_code"]
    assert response.json() == testcase["expected"]["data"]


@pytest.mark.parametrize(
    "testcase",
    [
        {
            "input": LEADS[2],
            "mock_response": {
                "status_code": 200,
                "json": LEADS[2],
                "is_success":True,
            },
            "expected": {
                "status_code": 200,
                "data": LEADS[2],
            },
        },
        {
            "input": LEADS[1],
            "mock_response": {
                "status_code": 403,
                "json": {"details": "Invalid input"},
                "is_success":False
            },
            "expected": {
                "status_code": 403,
                "data": {"detail": "Invalid input"},
            },
        }
    ]
)
def test_update_lead(mocker,testcase):

    create_mock_response(mocker,testcase["mock_response"])
    client = TestClient(app)
    response = client.post("/leads", json=testcase["input"])

    assert response.status_code == testcase["expected"]["status_code"]
    assert response.json() == testcase["expected"]["data"]



@pytest.mark.parametrize(
    "testcase",
    [
        {
            "input": "2",
            "mock_response": {
                "status_code": 200,
                "json": None,
                "is_success":True,
            },
            "expected": {
                "status_code": 200,
                "data": None,
            },
        },
        {
            "input": "-1",
            "mock_response": {
                "status_code": None,
                "json": None,
                "is_success": None,
            },
            "expected": {
                "status_code": 422,
                "data": {
                    "detail":[
                        {
                            'ctx': {
                                'gt': 0,
                            },
                            'input': '-1',
                            'loc': [
                                'path',
                                'id',
                            ],
                            'msg': 'Input should be greater than 0',
                            'type': 'greater_than',
                        },
                    ],
               },
            },
        }
    ]
)
def test_delete_lead(mocker,testcase):

    create_mock_response(mocker,testcase["mock_response"])
    client = TestClient(app)
    response = client.get("/leads/"+testcase["input"])

    assert response.status_code == testcase["expected"]["status_code"]
    assert response.json() == testcase["expected"]["data"]






