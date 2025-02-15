import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import json
from datetime import datetime
from typing import Dict, Any

from src.leads_crud.presentation.endpoints import app
from src.leads_crud.domain.lead import Lead
from src.leads_crud.infraestructure.hunter.hunter import HunterLeadCrud

client = TestClient(app)

# Test Data

@pytest.fixture
def update_lead_data():
    return {
        "company": "Avangenio"
    }


@pytest.fixture
def input_lead_data():
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "position": "Developer",
        "company": "Test Corp"
    }

def expected_lead_data():
    return {
        "id": "1",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "position": "Developer",
        "company": "Test Corp"
    }

@pytest.fixture
def hunter_success_response():
    return {
        "data": {
            "id": "1",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "position": "Developer",
            "company": "Test Corp"
        }
    }

@pytest.fixture
def hunter_error_response_400():
    
    return {
        "errors": [
            {
                "id": "wrong_params",
                "code": 400,
                "details": "You are missing a parameter"
            }
        ]
    }

@pytest.fixture
def hunter_error_response_404():
    return {
        "errors": [
            {
                "id": "not found",
                "code": 404,
                "details": "id not found"
            }
        ]
    }

class TestHunterApiIntegration:
    """
    Integration tests for the complete flow from API endpoints to Hunter.io
    """
    
    @pytest.mark.asyncio
    async def test_create_lead_success(self, input_lead_data, hunter_success_response):
        """Test successful lead creation flow"""
        
        # Mock the external Hunter.io API call
        with patch('httpx.AsyncClient.post') as mock_post:
            # Configure mock response
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.json.return_value = hunter_success_response
            mock_post.return_value = mock_response

            # Make request to our API
            response = client.post("/leads", json=input_lead_data)

            # Assertions
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["email"] == expected_lead_data["email"]
            assert response_data["first_name"] == expected_lead_data["first_name"]
            assert response_data["last_name"] == expected_lead_data["last_name"]
            assert "datetime" in response_data
            assert "id" in response_data

            # Verify Hunter.io API was called correctly
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "https://api.hunter.io/v2/leads" in str(call_args)

    @pytest.mark.asyncio
    async def test_create_lead_hunter_error(self, input_lead_data, hunter_error_response_400):
        """Test error handling when Hunter.io returns an error"""
        
        with patch('httpx.AsyncClient.post') as mock_post:
            # Configure mock error response
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 400
            mock_response.json.return_value = hunter_error_response_400
            mock_post.return_value = mock_response

            # Make request to our API
            response = client.post("/leads", json=input_lead_data)

            # Assertions
            assert response.status_code == 400
            assert "You are missing a parameter" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_retrieve_lead_success(self, hunter_success_response):
        """Test successful lead retrieval flow"""
        
        lead_id = 1

        with patch('httpx.AsyncClient.get') as mock_get:
            # Configure mock response
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.json.return_value = hunter_success_response
            mock_get.return_value = mock_response

            # Make request to our API
            response = client.get(f"/leads/{lead_id}")

            # Assertions
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["email"] == hunter_success_response["data"]["email"]
            assert "datetime" in response_data

            # Verify Hunter.io API was called correctly
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert f"https://api.hunter.io/v2/leads/{lead_id}" in str(call_args)

    @pytest.mark.asyncio
    async def test_retrieve_lead_not_found(self):
        """Test retrieval of non-existent lead"""
        
        lead_id = 999

        with patch('httpx.AsyncClient.put') as mock_put:
            # Configure mock error response
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 404
            mock_response.json.return_value = {"details": "Lead not found"}
            mock_put.return_value = mock_response

            # Make request to our API
            response = client.get(f"/leads/{lead_id}")

            # Assertions
            assert response.status_code == 404
            assert "Lead not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_lead_success(self, update_lead_data):
        """Test successful lead update flow"""
        
        lead_id = 1

        with patch('httpx.AsyncClient.post') as mock_post:
            # Configure mock response
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 204

            # Make request to our API
            response = client.put(f"/leads/{lead_id}", json=update_lead_data)

            # Assertions
            assert response.status_code == 204

            # Verify Hunter.io API was called correctly
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert f"https://api.hunter.io/v2/leads/{lead_id}" in str(call_args)

    @pytest.mark.asyncio
    async def test_update_lead_invalid(self,):
        """Test error handling when updating a lead with invalid data"""
        
        lead_id = 1

        with patch('httpx.AsyncClient.post') as mock_post:
            # Configure mock error response
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 400
            mock_response.json.return_value = hunter_error_response_400()
            mock_post.return_value = mock_response

            # Make request to our API
            response = client.put(f"/leads/{lead_id}", json={})

            # Assertions
            assert response.status_code == 400
            assert "Invalid data" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_delete_lead_success(self):
        """Test successful lead deletion flow"""
        
        lead_id = 1

        with patch('httpx.AsyncClient.put') as mock_put:
            # Configure mock response
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 204
            mock_put.return_value = mock_response

            # Make request to our API
            response = client.delete(f"/leads/{lead_id}")

            # Assertions
            assert response.status_code == 204

            # Verify Hunter.io API was called correctly
            mock_put.assert_called_once()
            call_args = mock_put.call_args
            assert f"https://api.hunter.io/v2/leads/{lead_id}" in str(call_args)

    @pytest.mark.asyncio
    async def test_delete_lead_not_found(self):
        """Test deletion of non-existent lead"""
        
        lead_id = 999

        with patch('httpx.AsyncClient.put') as mock_put:
            # Configure mock error response
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 404
            mock_response.json.return_value = hunter_error_response_404
            mock_put.return_value = mock_response

            # Make request to our API
            response = client.delete(f"/leads/{lead_id}")

            # Assertions
            assert response.status_code == 404
            assert "id not found" in response.json()["detail"]

    