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
def hunter_error_response():
    return {
        "errors": [
            {
                "details": "Invalid API key",
                "code": "unauthorized"
            }
        ]
    }


class TestHunterApiIntegration:
    """
    Integration tests for the complete flow from API endpoints to Hunter.io
    """
    
    @pytest.mark.asyncio
    async def test_create_lead_success(self, valid_lead_data, hunter_success_response):
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
    async def test_create_lead_hunter_error(self, valid_lead_data, hunter_error_response):
        """Test error handling when Hunter.io returns an error"""
        
        with patch('httpx.AsyncClient.post') as mock_post:
            # Configure mock error response
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 401
            mock_response.json.return_value = hunter_error_response
            mock_post.return_value = mock_response

            # Make request to our API
            response = client.post("/leads", json=valid_lead_data)

            # Assertions
            assert response.status_code == 401
            assert "Invalid API key" in response.json()["detail"]

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
    async def test_invalid_input_validation(self):
        """Test input validation for invalid data"""
        
        invalid_data = {
            "email": "not-an-email",
            "first_name": "",  # Empty name
            "position": None
        }

        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_lead_id(self):
        """Test validation of invalid lead ID parameter"""
        
        response = client.get("/leads/0")  # ID must be > 0
        assert response.status_code == 422
        
    @pytest.mark.asyncio
    async def test_hunter_timeout(self, valid_lead_data):
        """Test handling of Hunter.io API timeout"""
        
        with patch('httpx.AsyncClient.post') as mock_post:
            # Simulate timeout
            mock_post.side_effect = TimeoutError()

            response = client.post("/leads", json=valid_lead_data)
            assert response.status_code == 503  # Service Unavailable
