import json

from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .db import products_collection, redis_client


CACHE_KEY = "products"


@csrf_exempt
def products(request):

    # GET — получить список товаров
    if request.method == "GET":

        # Проверяем Redis
        cached_products = redis_client.get(CACHE_KEY)

        if cached_products:
            print(">>> Данные получены из Redis")

            return JsonResponse(
                json.loads(cached_products),
                safe=False
            )

        # Если в Redis ничего нет — идём в MongoDB
        print(">>> Данные получены из MongoDB")

        products_list = []

        for product in products_collection.find():
            products_list.append({
                "id": str(product["_id"]),
                "name": product["name"],
                "description": product["description"],
                "price": product["price"]
            })

        # Сохраняем список в Redis
        redis_client.set(
            CACHE_KEY,
            json.dumps(products_list),
            ex=300
        )

        return JsonResponse(
            products_list,
            safe=False
        )

    # POST — добавить товар
    if request.method == "POST":

        data = json.loads(request.body)

        product = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"]
        }

        result = products_collection.insert_one(product)

        # После добавления список изменился
        redis_client.delete(CACHE_KEY)

        return JsonResponse({
            "message": "Товар добавлен",
            "id": str(result.inserted_id)
        }, status=201)

    return JsonResponse({
        "error": "Метод не поддерживается"
    }, status=405)


@csrf_exempt
def product_detail(request, product_id):

    try:
        object_id = ObjectId(product_id)
    except Exception:
        return JsonResponse({
            "error": "Неверный ID товара"
        }, status=400)

    # PUT — изменить товар
    if request.method == "PUT":

        data = json.loads(request.body)

        result = products_collection.update_one(
            {"_id": object_id},
            {
                "$set": {
                    "name": data["name"],
                    "description": data["description"],
                    "price": data["price"]
                }
            }
        )

        if result.matched_count == 0:
            return JsonResponse({
                "error": "Товар не найден"
            }, status=404)

        # Очищаем старый кэш
        redis_client.delete(CACHE_KEY)

        return JsonResponse({
            "message": "Товар изменён"
        })

    # DELETE — удалить товар
    if request.method == "DELETE":

        result = products_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return JsonResponse({
                "error": "Товар не найден"
            }, status=404)

        # Очищаем старый кэш
        redis_client.delete(CACHE_KEY)

        return JsonResponse({
            "message": "Товар удалён"
        })

    return JsonResponse({
        "error": "Метод не поддерживается"
    }, status=405)