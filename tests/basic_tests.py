import requests

url = 'http://127.0.0.1:2010'

# Шаг 1: Создание задачи
def test_create_task():
    url_create = f"{url}/tasks/"
    task_data = {
        "title": "New Task",
        "description": "This is a test task.",
        "status": "pending"
    }

    response_create = requests.post(url_create, json=task_data)

    assert response_create.status_code == 200, f"Expected 200, but got {response_create.status_code}"
    created_task = response_create.json()
    task_id = created_task["id"]
    assert task_id, "Task ID should be present"
    return task_id

# Шаг 2: Получение задачи по ID
def test_get_task():
    task_id = test_create_task()  # Вызов функции создания задачи, чтобы получить task_id
    url_get = f"{url}/tasks/{task_id}"

    response_get = requests.get(url_get)

    assert response_get.status_code == 200, f"Expected 200, but got {response_get.status_code}"
    task_data = response_get.json()
    assert task_data["id"] == task_id, f"Expected task ID {task_id}, but got {task_data['id']}"

# Шаг 3: Обновление задачи
def test_update_task():
    task_id = test_create_task()  # Вызов функции создания задачи
    url_update = f"{url}/tasks/{task_id}"
    updated_task_data = {
        "title": "Updated Task",
        "description": "This task has been updated.",
        "status": "in_progress"
    }

    response_update = requests.put(url_update, json=updated_task_data)

    assert response_update.status_code == 200, f"Expected 200, but got {response_update.status_code}"
    updated_task = response_update.json()
    assert updated_task["status"] == "in_progress", f"Expected status 'in_progress', but got {updated_task['status']}"

# Шаг 4: Удаление задачи
def test_delete_task():
    task_id = test_create_task()  # Вызов функции создания задачи
    url_delete = f"{url}/tasks/{task_id}"

    response_delete = requests.delete(url_delete)

    assert response_delete.status_code == 204, f"Expected 204, but got {response_delete.status_code}"
    # Проверим, что задача действительно удалена
    response_get_after_delete = requests.get(f"http://127.0.0.1:2009/tasks/{task_id}")
    assert response_get_after_delete.status_code == 404, "Expected 404 after deleting task"

# Шаг 5: Проверка создания задачи с отсутствующими обязательными полями
def test_create_task_missing_fields():
    url_create = f"{url}/tasks/"
    incomplete_task_data = {
        "title": "Incomplete Task"
        # Пропущено обязательное поле "status"
    }

    response_create = requests.post(url_create, json=incomplete_task_data)

    assert response_create.status_code == 422, f"Expected 422, but got {response_create.status_code}"
    error_message = response_create.json().get("detail")
    assert error_message, "Error message should be present"

# Шаг 6: Проверка создания задачи с неверным статусом
def test_create_task_invalid_status():
    url_create = f"{url}/tasks/"
    invalid_task_data = {
        "title": "Invalid Status Task",
        "description": "This task has an invalid status.",
        "status": "invalid_status"  # Неверный статус
    }

    response_create = requests.post(url_create, json=invalid_task_data)

    assert response_create.status_code == 422, f"Expected 400, but got {response_create.status_code}"

# Шаг 7: Проверка получения несуществующей задачи
def test_get_non_existent_task():
    non_existent_task_id = 999999  # Не существующий ID
    url_get = f"{url}/tasks/{non_existent_task_id}"

    response_get = requests.get(url_get)

    assert response_get.status_code == 404, f"Expected 404, but got {response_get.status_code}"
    error_message = response_get.json().get("detail")
    assert "not found" in error_message, f"Expected 'not found' error, but got {error_message}"

# Шаг 8: Проверка обновления задачи с неверными данными
def test_update_task_invalid_data():
    task_id = test_create_task()  # Вызов функции создания задачи
    url_update = f"{url}/tasks/{task_id}"
    invalid_updated_task_data = {
        "title": "Updated Task",
        "description": "This task has an invalid status.",
        "status": "non_existent_status"  # Неверный статус
    }

    response_update = requests.put(url_update, json=invalid_updated_task_data)

    assert response_update.status_code == 422, f"Expected 400, but got {response_update.status_code}"

# Шаг 9: Проверка удаления уже удаленной задачи
def test_delete_already_deleted_task():
    task_id = test_create_task()  # Вызов функции создания задачи
    url_delete = f"{url}/tasks/{task_id}"

    # Сначала удаляем задачу
    response_delete = requests.delete(url_delete)
    assert response_delete.status_code == 204, f"Expected 204, but got {response_delete.status_code}"

    # Попытка удалить ее снова
    response_delete_again = requests.delete(url_delete)
    assert response_delete_again.status_code == 404, f"Expected 404, but got {response_delete_again.status_code}"
    error_message = response_delete_again.json().get("detail")
    assert "not found" in error_message, f"Expected 'not found' error, but got {error_message}"
