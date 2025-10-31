# 🔐 CloudLock — Secure Cloud Access Gateway  

*A privacy-first platform to share cloud files securely with encryption and access control.*

---

## 👥 Team Details  

**Team Name:** Hack SC — Team 68  

**Members:**  
- Charan Dindi  
- Shashank Dasari  
- Dakshitha Kak  
- Ajitha Alamkonda  

---

## 💡 Problem Statement  

Cloud storage platforms like Google Drive or Dropbox let anyone access a shared file if they have the link — no real protection once the link is public.  
This creates major privacy and security risks when sharing sensitive data.

**CloudLock** solves this by introducing a secure sharing layer with password protection, link expiry, and encryption, ensuring only the intended recipient can access the file.

---

## 🚀 Solution Overview  

1. Users upload their files to CloudLock.  
2. The files are encrypted before being stored.  
3. CloudLock generates a unique secure link with optional password and expiry time.  
4. Recipients can safely access the shared files only through CloudLock’s verification process.  

This ensures complete privacy, control, and peace of mind while sharing data online.

---

## ⚙️ Tech Stack  

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** SQLite / JSON  
- **Encryption:** bcrypt, Custom Encryption Utilities  
- **Version Control:** Git & GitHub  

---

## 📁 Folder Structure  
CloudLock/
├─ app.py
├─ config.py
├─ templates/
│ ├─ base.html
│ ├─ index.html
│ ├─ login.html
│ ├─ register.html
│ ├─ signup.html
│ ├─ dashboard.html
│ └─ access.html
├─ static/
│ ├─ css/
│ ├─ js/
│ └─ images/
├─ utils/
│ ├─ db_manager.py
│ ├─ encryption.py
│ ├─ link_manager.py
│ └─ init.py
├─ uploads/
├─ instance/
├─ links.json
├─ users.json
└─ README.md

---

## 🧠 Key Features  

✅ Secure file uploads with encryption  
✅ Password-protected and time-limited access  
✅ User registration and login with bcrypt  
✅ Simple Flask architecture (easy to extend)  
✅ Modern UI built using HTML, CSS, and JS  
✅ Lightweight — no external database setup required  

---

## 🧩 Installation & Setup  

To run the project locally, follow these steps:  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/shashankdasari-lab/Cloudlock-hackx-team68.git

# 2️⃣ Navigate into the project folder
cd Cloudlock-hackx-team68

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the Flask app
python app.py





Challenges Faced

Implementing end-to-end encryption with file upload

Handling secure password hashing and authentication

Structuring the Flask app for modularity

Debugging routes and JSON-based database handling

Completing under hackathon deadlines ⏰

🌟 Future Enhancements

🚀 Google Drive / Dropbox integration
🔐 Two-Factor Authentication (2FA)
📊 File analytics (views, downloads, location tracking)
💬 Real-time notifications & activity logs
☁️ Cloud deployment on AWS / Render

📜 License

This project is licensed under the MIT License — feel free to use, modify, and improve it.

❤️ Acknowledgments

Made with ❤️ by Team Hack SC (Team 68)

“Security isn’t an option — it’s a necessity.”

📞 Contact 

🔗 GitHub Repo: CloudLock – Hack SC Team 68

👨‍💻 Developer: Shashank Dasari
