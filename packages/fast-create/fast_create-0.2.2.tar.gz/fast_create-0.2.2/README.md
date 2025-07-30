# Fast Create - A CLI Tool for FastAPI Projects

![FastAPI](https://img.shields.io/badge/FastAPI-CLI%20Tool-blue?style=for-the-badge&logo=fastapi)

**Fast Create** is a command-line tool that allows you to quickly generate FastAPI project structures with best practices. It automates project setup, dependencies, and server startup, making FastAPI development seamless.

## 🚀 Features
- 📂 **Auto-generates FastAPI project structure**
- 🔧 **Pre-configured settings for FastAPI, Uvicorn, and Pydantic**
- 🚀 **Automatically starts the Uvicorn server after project creation**
- 🛠️ **Includes `.env` support for configurations**
- ✅ **Lightweight and easy to use**

---

## 📌 Installation
You can install `fast-create` from [PyPI](https://pypi.org/):

```sh
pip install fast-create
```

---

## 🛠️ Usage
### **Create a New FastAPI Project**
To generate a new FastAPI project, run:

```sh
fast-create new myapp
```

Replace `myapp` with your desired project name.

### **Folder Structure Generated**
After running the command, the following project structure will be created:

```
myapp/
│── app/
│   ├── main.py  # Entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│── .env  # Environment variables
│── requirements.txt
│── README.md
│── Dockerfile
│── .gitignore
```

---

## ⚡ Running the Server
After creating the project, the Uvicorn server starts automatically. However, you can manually start the server anytime:

```sh
cd myapp
uvicorn app.main:app --reload
```

---

## 🔧 Configuration
### **Environment Variables**
Your `.env` file should contain:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./database.db
MAIL_PASSWORD=your-mail-password
```

Ensure you update this file with your actual credentials.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Contributing
We welcome contributions! Feel free to fork this repo, create a new branch, and submit a pull request.

---

## 📩 Contact
For issues or suggestions, open an [issue](https://github.com/joechristophers/fast-create/issues) or reach out at **joechristophersc@email.com**.

Happy coding! 🎉

