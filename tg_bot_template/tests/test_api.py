import pytest
from tg_bot_template.domain.entities import User
from sqlalchemy import text

@pytest.mark.asyncio
async def test_create_user(client, session):
    user_data = {"user_id": 123, "name": "Test User", "info": "Test Info"}
    response = await client.post("/set_info", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]

@pytest.mark.asyncio
async def test_get_user(client, session):
    user = User(id=123, name="Test User", info="Test Info")
    session.add(user)
    await session.commit()

    response = await client.get(f"/user/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user.id
    assert data["info"] == user.info


@pytest.mark.asyncio
async def test_push_button(client, session):
    """Тест нажатия кнопки и проверка инкремента счетчика taps"""
    # Создаем пользователя
    user = User(id=123, name="Test User", info="Test Info", taps=0)
    session.add(user)
    await session.commit()

    # Нажимаем кнопку
    response = await client.post("/push_the_button", json={"user_id": user.id})
    assert response.status_code == 200
    data = response.json()
    assert data["taps"] == 1

    # Получаем обновленного пользователя
    result = await session.execute(text("SELECT taps FROM users WHERE id = :user_id"), {"user_id": user.id})
    updated_taps = result.scalar()
    assert updated_taps == 1

@pytest.mark.asyncio
async def test_get_rating(client, session):
    users = [
        User(id=1, name="User 1", info="Info 1", taps=5),
        User(id=2, name="User 2", info="Info 2", taps=3),
        User(id=3, name="User 3", info="Info 3", taps=7)
    ]
    for user in users:
        session.add(user)
    await session.commit()

    response = await client.get("/rating/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_taps"] == 5
    assert data["total_taps"] == 15

@pytest.mark.asyncio
async def test_user_not_found(client):
    response = await client.get("/profile/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_invalid_user_id(client):
    response = await client.get("/profile/invalid")
    assert response.status_code == 422
