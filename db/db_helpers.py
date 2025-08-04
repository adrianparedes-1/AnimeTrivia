from db.session_manager import get_db
from typing import Callable, Iterable, Type, Mapping
from sqlalchemy import Column


def construct_orm_model_from_list(
    dto_list: Iterable,
    model: Type,
    unique_attr: Column,
    dto_value_getter: Callable
) -> list:
    """
    Construct ORM models with unique values from a DTO list.
    Returns a list with unique objs not in db.

    :param dto_list: The incoming DTO list
    :param model: The ORM model class
    :param unique_attr: The model column to check for uniqueness
    :param dto_value_getter: Function to extract the field from a DTO item
    """
    dto_set = {dto_value_getter(item) for item in (dto_list or [])}

    if not dto_set:
        return []
    
    with next(get_db()) as db:
        existing_objs = (
            db.query(model)
                   .filter(unique_attr.in_(dto_set))
                   .all()
        )
        existing_set = {getattr(o, unique_attr.key) for o in existing_objs}
        new_objs = [
            model(**{unique_attr.key: n}) # unique_attr=n / table_field = n
            for n in (dto_set - existing_set) 
        ]
        if new_objs:
            try:
                db.add_all(new_objs)
                db.commit()
            except:
                db.rollback()
                raise 
        return new_objs + existing_objs


def construct_parent_with_children(
    parent_model: Type,                  
    scalar_fields: Mapping[str, list],                 
    children_map: Mapping[str, Iterable],      
):
    """
    Creates a parent ORM object with given scalar fields
    and attaches lists of ORM children.

    :param parent_model: ORM class for the parent table
    :param scalar_fields: dict of scalar field names and values for the parent
    :param children_map: dict mapping relationship names to lists of ORM instances
    """
    parent_instance = parent_model(**scalar_fields)
    for rel_name, children in children_map.items():
        setattr(parent_instance, rel_name, children)
        # basically this: parent_instance.rel_name = children

    with next(get_db()) as db:
        if parent_instance:
            db.add(parent_instance)
            try:
                db.commit()
            except Exception:
                db.rollback()
                raise 
            