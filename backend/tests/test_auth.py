"""Test authentication"""

import pytest
from tests.conftest import client
from app.schemas.user import UserCreate


def test_register_user():
    """Test user registration"""
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == user_data["email"]


def test_login_user():
    """Test user login"""
    # First register
    user_data = {
        "email": "logintest@example.com",
        "full_name": "Login Test",
        "password": "testpassword123"
    }
    
    client.post("/api/v1/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "email": "logintest@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
