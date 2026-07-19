from src.models.database import (
    get_all_content,
    get_content_by_id,
    add_content_db,
    update_content_db,
    delete_content_db,
    increment_plays_db,
)


class ContentStore:
    """Capa de acceso a contenido usando MySQL."""

    def get_all(self):
        return get_all_content()

    def get_by_id(self, content_id):
        return get_content_by_id(content_id)

    def add(self, new_item):
        return add_content_db(new_item)

    def update(self, content_id, updated_data):
        return update_content_db(content_id, updated_data)

    def delete(self, content_id):
        delete_content_db(content_id)

    def increment_plays(self, content_id):
        return increment_plays_db(content_id)


content_store = ContentStore()
