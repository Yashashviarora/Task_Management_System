"""
Unit tests for Task API endpoints.
Tests all CRUD operations, business rules, and edge cases.
"""
import pytest
from fastapi import status


class TestTaskCreation:
    """Test task creation endpoint."""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation."""
        response = client.post("/api/v1/tasks/", json=sample_task_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["priority"] == sample_task_data["priority"]
        assert data["status"] == "Pending"
        assert "id" in data
    
    def test_create_task_empty_title(self, client):
        """Test that empty title is rejected."""
        response = client.post("/api/v1/tasks/", json={
            "title": "",
            "priority": "Low"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_invalid_priority(self, client):
        """Test that invalid priority is rejected."""
        response = client.post("/api/v1/tasks/", json={
            "title": "Test",
            "priority": "Invalid"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTaskRetrieval:
    """Test task retrieval endpoints."""
    
    def test_get_task_by_id(self, client, sample_task_data):
        """Test retrieving a task by ID."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == task_id
    
    def test_get_nonexistent_task(self, client):
        """Test retrieving a non-existent task."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/tasks/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_list_tasks(self, client, sample_task_data):
        """Test listing all tasks."""
        client.post("/api/v1/tasks/", json=sample_task_data)
        
        response = client.get("/api/v1/tasks/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tasks" in data
        assert data["total"] >= 1


class TestTaskFiltering:
    """Test task filtering and sorting."""
    
    def test_filter_by_status(self, client):
        """Test filtering tasks by status."""
        client.post("/api/v1/tasks/", json={"title": "Task 1", "priority": "Low"})
        
        response = client.get("/api/v1/tasks/?status=Pending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(task["status"] == "Pending" for task in data["tasks"])
    
    def test_filter_by_priority(self, client):
        """Test filtering tasks by priority."""
        client.post("/api/v1/tasks/", json={"title": "High Priority", "priority": "High"})
        
        response = client.get("/api/v1/tasks/?priority=High")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(task["priority"] == "High" for task in data["tasks"])
    
    def test_pagination(self, client):
        """Test pagination."""
        for i in range(5):
            client.post("/api/v1/tasks/", json={"title": f"Task {i}", "priority": "Low"})
        
        response = client.get("/api/v1/tasks/?page=1&page_size=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["page"] == 1


class TestTaskUpdate:
    """Test task update endpoint."""
    
    def test_update_task_success(self, client, sample_task_data):
        """Test successful task update."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Title"}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated Title"
    
    def test_update_completed_task_fails(self, client, sample_task_data):
        """Test that completed tasks cannot be updated."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Mark as completed
        client.patch(f"/api/v1/tasks/{task_id}/complete")
        
        # Try to update
        response = client.put(f"/api/v1/tasks/{task_id}", json={"title": "New Title"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestTaskCompletion:
    """Test task completion endpoint."""
    
    def test_mark_task_completed(self, client, sample_task_data):
        """Test marking a task as completed."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        response = client.patch(f"/api/v1/tasks/{task_id}/complete")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "Completed"


class TestTaskDeletion:
    """Test task deletion (soft delete)."""
    
    def test_delete_task_success(self, client, sample_task_data):
        """Test successful task deletion."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True
    
    def test_deleted_task_not_retrievable(self, client, sample_task_data):
        """Test that deleted tasks cannot be retrieved."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        client.delete(f"/api/v1/tasks/{task_id}")
        
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_deleted_task_not_in_list(self, client, sample_task_data):
        """Test that deleted tasks don't appear in listings."""
        create_response = client.post("/api/v1/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        client.delete(f"/api/v1/tasks/{task_id}")
        
        response = client.get("/api/v1/tasks/")
        task_ids = [task["id"] for task in response.json()["tasks"]]
        assert task_id not in task_ids
