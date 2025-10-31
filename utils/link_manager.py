import uuid
import bcrypt
from . import db_manager

def generate_link(data, password, entry_type='link', owner="anonymous"):
    link_id = str(uuid.uuid4())[:8]
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    record = {
        "id": link_id,
        "type": entry_type,     # 'file' or 'link'
        "data": data,
        "password_hash": pw_hash,
        "owner": owner,
        "used": False
    }
    db_manager.add_link(record)
    return link_id
