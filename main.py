from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

import models
import utils

app = FastAPI()


# CRUD for Menu
@app.get("/api/v1/menus")
def view_menu():
    result = utils.get_objects_query(models.db.query(models.Menu).all())
    return JSONResponse(result)


@app.get("/api/v1/menus/{target_menu_id}")
def view_key_menu(target_menu_id):
    result, menu = utils.get_menu(target_menu_id)
    if menu is not None:
        submenus = models.db.query(models.Submenu).filter(models.Submenu.menu_id == target_menu_id)
        dishes_count = 0
        for submenu in submenus:
            dishes_count = dishes_count + models.db.query(models.Dish). \
                filter(models.Dish.submenu_id == submenu.id).count()

        result['submenus_count'] = models.db.query(models.Submenu). \
            filter(models.Submenu.menu_id == target_menu_id).count()
        result['dishes_count'] = dishes_count

        return JSONResponse(result)
    else:
        return JSONResponse({'detail': 'menu not found'}, status_code=404)


@app.post("/api/v1/menus")
def post_menu(data=Body()):
    result = utils.add_menu_object(models.Menu(title=data['title'], description=data['description']))
    return JSONResponse(result, status_code=201)


@app.patch("/api/v1/menus/{target_menu_id}")
def update_menu(target_menu_id, data=Body()):
    result, menu = utils.get_menu(target_menu_id)

    result['title'] = menu.title = data['title']
    result['description'] = menu.description = data['description']
    models.db.commit()
    return JSONResponse(result)


@app.delete("/api/v1/menus/{target_menu_id}")
def delete_menu(target_menu_id):
    result, menu = utils.get_menu(target_menu_id)

    models.db.delete(menu)
    models.db.commit()
    return JSONResponse(result)


# CRUD for Submenu
@app.get("/api/v1/menus/{target_menu_id}/submenus")
def view_submenu(target_menu_id):
    result = utils.get_objects_query(models.db.query(
        models.Submenu).where(models.Submenu.menu_id == target_menu_id))
    return JSONResponse(result)


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def view_key_submenu(target_menu_id, target_submenu_id):
    result, submenu = utils.get_submenu(target_menu_id, target_submenu_id)
    if submenu is not None:
        result['dishes_count'] = models.db.query(models.Dish). \
            filter(models.Dish.submenu_id == target_submenu_id).count()
        return JSONResponse(result)
    else:
        return JSONResponse({'detail': 'submenu not found'}, status_code=404)


@app.post("/api/v1/menus/{target_menu_id}/submenus")
def post_submenu(target_menu_id, data=Body()):
    result = utils.add_menu_object(
        models.Submenu(title=data['title'], description=data['description'], menu_id=target_menu_id)
    )
    return JSONResponse(result, status_code=201)


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def update_submenu(target_menu_id, target_submenu_id, data=Body()):
    result, submenu = utils.get_submenu(target_menu_id, target_submenu_id)

    result['title'] = submenu.title = data['title']
    result['description'] = submenu.description = data['description']
    models.db.commit()
    return JSONResponse(result)


@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def delete_submenu(target_menu_id, target_submenu_id):
    result, submenu = utils.get_submenu(target_menu_id, target_submenu_id)

    models.db.delete(submenu)
    models.db.commit()
    return JSONResponse(result)


# CRUD for Dish
@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
def view_dish(target_submenu_id):
    objects = models.db.query(models.Dish).where(models.Dish.submenu_id == target_submenu_id)
    result = []
    for object_ in objects:
        tmp = {'id': object_.id,
               'title': object_.title,
               'description': object_.description,
               'price': object_.price
               }
        result.append(tmp)

    return JSONResponse(result)


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def view_key_dish(target_submenu_id, target_dish_id):
    result, dish = utils.get_dish(target_submenu_id, target_dish_id)
    if dish is not None:
        return JSONResponse(result)
    else:
        return JSONResponse({'detail': 'dish not found'}, status_code=404)


@app.post("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
def post_dish(target_submenu_id, data=Body()):
    dish = models.Dish(title=data['title'], description=data['description'],
                       price=data['price'], submenu_id=target_submenu_id)
    models.db.add(dish)
    models.db.commit()
    result = {
        'id': str(dish.id),
        'title': dish.title,
        'description': dish.description,
        'price': f"{dish.price:.{2}f}"
    }
    return JSONResponse(result, status_code=201)


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def update_dish(target_submenu_id, target_dish_id, data=Body()):
    result, dish = utils.get_dish(target_submenu_id, target_dish_id)

    result['title'] = dish.title = data['title']
    result['description'] = dish.description = data['description']
    result['price'] = dish.price = data['price']
    models.db.commit()
    return JSONResponse(result)


@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def delete_dish(target_submenu_id, target_dish_id):
    result, dish = utils.get_dish(target_submenu_id, target_dish_id)

    models.db.delete(dish)
    models.db.commit()
    return JSONResponse(result)
