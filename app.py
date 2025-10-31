from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
import bcrypt
import uuid
from utils import encryption, link_manager, db_manager

# App setup
app = Flask(__name__)
app.config.from_pyfile('config.py')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helpers
def current_user():
    return session.get('user')  # dict with username and id (if logged in)

# Routes
@app.route('/')
def index():
    user = current_user()
    return render_template('index.html', user=user)

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Please provide username and password', 'error')
            return redirect(url_for('signup'))

        if db_manager.get_user_by_username(username):
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))

        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_manager.add_user({"id": str(uuid.uuid4()), "username": username, "password_hash": pw_hash, "guest": False})
        flash('Signup successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Guest signup (creates a guest user and logs in)
@app.route('/guest')
def guest():
    guest_id = str(uuid.uuid4())[:8]
    username = f"guest-{guest_id}"
    pw_hash = bcrypt.hashpw(uuid.uuid4().hex.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_manager.add_user({"id": str(uuid.uuid4()), "username": username, "password_hash": pw_hash, "guest": True})
    session['user'] = {"id": username, "username": username, "guest": True}
    flash(f'Signed in as guest: {username}', 'success')
    return redirect(url_for('dashboard'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = db_manager.get_user_by_username(username)
        if not user:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user'] = {"id": user.get('id'), "username": user.get('username'), "guest": user.get('guest', False)}
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out', 'success')
    return redirect(url_for('index'))

# Dashboard (user home)
@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        flash('Please login or signup to view dashboard', 'error')
        return redirect(url_for('login'))
    # Show links owned by user (owner_id equals username used as id)
    all_links = db_manager.get_all_links()
    my_links = [l for l in all_links if l.get('owner') == user['username']]
    return render_template('dashboard.html', user=user, links=my_links)

# Upload file route
@app.route('/upload', methods=['POST'])
def upload_file():
    user = current_user()
    if not user:
        flash('Please login or signup to upload', 'error')
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    password = request.form.get('file_password', '').strip()
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    if not password:
        flash('Set a password for the file', 'error')
        return redirect(url_for('index'))

    filename = file.filename
    safe_local = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{filename}")
    file.save(safe_local)

    # Encrypt file and get path to encrypted file
    try:
        enc_path = encryption.encrypt_file(safe_local, password)
    except Exception as e:
        flash('Encryption failed: ' + str(e), 'error')
        return redirect(url_for('index'))

    # Create link record (owner is username)
    link_id = link_manager.generate_link(enc_path, password, entry_type='file', owner=user['username'])
    link_url = url_for('access', link_id=link_id, _external=True)
    flash(f'File secured! Shareable link: {link_url}', 'success')
    return redirect(url_for('dashboard'))

# Secure cloud link route
@app.route('/secure_link', methods=['POST'])
def secure_link():
    user = current_user()
    if not user:
        flash('Please login or signup to secure links', 'error')
        return redirect(url_for('login'))

    cloud_link = request.form.get('cloud_link', '').strip()
    password = request.form.get('link_password', '').strip()
    if not cloud_link:
        flash('Enter a cloud link', 'error')
        return redirect(url_for('index'))
    if not password:
        flash('Set a password', 'error')
        return redirect(url_for('index'))

    try:
        enc = encryption.encrypt_text(cloud_link, password)
    except Exception as e:
        flash('Encryption failed: ' + str(e), 'error')
        return redirect(url_for('index'))

    link_id = link_manager.generate_link(enc, password, entry_type='link', owner=user['username'])
    link_url = url_for('access', link_id=link_id, _external=True)
    flash(f'Cloud link secured! Shareable link: {link_url}', 'success')
    return redirect(url_for('dashboard'))

# Access route: show form or serve file/redirect
@app.route('/access/<link_id>', methods=['GET', 'POST'])
def access(link_id):
    record = db_manager.get_link_by_id(link_id)
    if not record:
        flash('Invalid or expired link', 'error')
        return render_template('access.html', record=None)

    if request.method == 'GET':
        return render_template('access.html', record={"id": link_id, "type": record.get('type')})

    password = request.form.get('password', '').strip()
    if not password:
        flash('Enter password', 'error')
        return redirect(url_for('access', link_id=link_id))

    # Verify bcrypt-hashed password
    if not bcrypt.checkpw(password.encode('utf-8'), record.get('password_hash').encode('utf-8')):
        flash('Incorrect password', 'error')
        return redirect(url_for('access', link_id=link_id))

    # Correct password: serve
    if record.get('type') == 'link':
        try:
            original = encryption.decrypt_text(record.get('data'), password)
            return redirect(original)
        except Exception:
            flash('Failed to decrypt link', 'error')
            return redirect(url_for('access', link_id=link_id))
    elif record.get('type') == 'file':
        try:
            enc_path = record.get('data')
            temp_path = encryption.decrypt_file(enc_path, password)
            # send file as attachment
            return send_file(temp_path, as_attachment=True)
        except Exception:
            flash('Failed to decrypt file', 'error')
            return redirect(url_for('access', link_id=link_id))
    else:
        flash('Unknown record type', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
