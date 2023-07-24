from httpx import AsyncClient


async def test_add_category(ac: AsyncClient):
    response = await ac.post("/menu/category", json={
        "name": "category1",
        "is_publish": True
    })
    assert response.status_code == 200


async def test_add_topping(ac: AsyncClient):
    response = await ac.post("/menu/topping", json={
        "name": "topping1"
    })
    assert response.status_code == 200


async def test_add_food1(ac: AsyncClient):
    response = await ac.post("/menu/food", json={
        "description": "description food1",
        "price": 234,
        "name": "food1",
        "is_special": True,
        "is_vegan": True,
        "is_publish": True,
        "category_id": 1,
        "toppings_id": [
            1
        ]
    })
    assert response.status_code == 200


async def test_add_food2(ac: AsyncClient):
    response = await ac.post("/menu/food", json={
        "description": "description food2",
        "price": 534,
        "name": "food2",
        "is_special": True,
        "is_vegan": False,
        "is_publish": False,
        "category_id": 1,
        "toppings_id": []
    })
    assert response.status_code == 200


async def test_get_specific_foods(ac: AsyncClient):
    response = await ac.get("/menu/public_food_by_filter", params={
        "filter_vegan": "true",
        "filter_special": "true",
        "filter_topping": "topping1",
    })
    print('ddddddddddddddddddddddddddd', response.json()[0])
    assert response.status_code == 200
    assert len(response.json()[0].get('foods')) == 1
    assert response.json()[0].get('foods')[0].get('name') == 'food1'
