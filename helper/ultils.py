import hashlib
import os

def to_dict(obj):
    if not hasattr(obj, '__table__'):
        raise ValueError("The provided object is not a valid SQLAlchemy model instance.")
    
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def generate_name(name):
    name = name + 'xuanloc'
    name_bytes = name.encode('utf-8')
    hash_object = hashlib.sha256(name_bytes)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def save_image(file_obj, filename):
        storage_path = 'storage/images'
        storage_public_path = 'frontend/src/assets/storage/images'

        local_path = os.path.join(storage_path, f'{filename}.jpg')
        public_path = os.path.join(storage_public_path, f'{filename}.jpg')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        file_obj.seek(0)
        file_obj.save(local_path)
        file_obj.seek(0)
        file_obj.save(public_path)
        return {'local': local_path, 'public': public_path}