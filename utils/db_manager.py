import json
import os

USERS_PATH = "users.json"
LINKS_PATH = "links.json"

def _ensure(file_path, default):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default, f)

def get_all_users():
    _ensure(USERS_PATH, [])
    with open(USERS_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def add_user(user_dict):
    users = get_all_users()
    users.append(user_dict)
    with open(USERS_PATH, 'w') as f:
        json.dump(users, f, indent=4)

def get_user_by_username(username):
    users = get_all_users()
    for u in users:
        if u.get('username') == username:
            return u
    return None

# Links functions
def get_all_links():
    _ensure(LINKS_PATH, [])
    with open(LINKS_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_all_links(data):
    with open(LINKS_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def add_link(entry):
    links = get_all_links()
    links.append(entry)
    save_all_links(links)

def get_link_by_id(link_id):
    links = get_all_links()
    for l in links:
        if l.get('id') == link_id:
            return l
    return None

def update_link(entry):
    links = get_all_links()
    for i, l in enumerate(links):
        if l.get('id') == entry.get('id'):
            links[i] = entry
            save_all_links(links)
            return True
    return False

