import models


# Вспомогательные функции для CRUD операций
def get_objects_query(objects):
    result = []
    for object_ in objects:
        tmp = {'id': object_.id, 'title': object_.title, 'description': object_.description}
        result.append(tmp)
    return result


def add_menu_object(object_):
    models.db.add(object_)
    models.db.commit()
    return {'id': str(object_.id), 'title': object_.title, 'description': object_.description}


# Получение экземпляра меню и словаря для ответа API
def get_menu(target_menu_id):
    menu = models.db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()

    if menu is not None:
        result = {
            'id': str(menu.id),
            'title': menu.title,
            'description': menu.description,
        }
        return result, menu
    else:
        return None, None


# Получение экземпляра подменю и словаря для ответа API
def get_submenu(target_menu_id, target_submenu_id):
    submenu = models.db.query(models.Submenu).filter(
        models.Submenu.menu_id == target_menu_id and
        models.Submenu.id == target_submenu_id).first()

    if submenu is not None:
        result = {
            'id': str(submenu.id),
            'title': submenu.title,
            'description': submenu.description,
        }
        return result, submenu
    else:
        return None, None


# Получение экземпляра блюда и словаря для ответа API
def get_dish(target_submenu_id, target_dish_id):
    dish = models.db.query(models.Dish).filter(
        models.Dish.submenu_id == target_submenu_id and
        models.Dish.id == target_dish_id).first()

    if dish is not None:
        result = {
            'id': str(dish.id),
            'title': dish.title,
            'description': dish.description,
            # 'price': str(dish.price)
            'price': f"{dish.price:.{2}f}"
        }
        return result, dish
    else:
        return None, None
