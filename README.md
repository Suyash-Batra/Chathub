# ChatHub 💬

**ChatHub** is a streamlined, responsive web application designed for organized group discussions. Built with **Django**, it allows users to discover, create, and participate in chat rooms categorized by specific interests and topics.

## ✨ Core Features

* **Dynamic Room Discovery:** Browse rooms by topic or use the global search to find discussions by name or description.
* **Flexible Topic Management:** Select from a curated list of existing topics or instantly create a new one while setting up a room.
* **Intuitive Messaging UI:** A clean, bubble-based chat interface that distinguishes between your messages and others for a natural conversation flow.
* **User Profiles:** Dedicated pages for every user showing their hosted rooms and recent activity feed.
* **Participation Tracking:** See a live list of active participants within any chat room.
* **Recent Activity:** A global sidebar that keeps you updated on the latest messages across the entire platform.
* **Responsive Design:** A mobile-first approach ensuring the chat experience is seamless on phones, tablets, and desktops.

## 🛠️ Technical Stack

* **Backend:** Python / Django
* **Frontend:** HTML5, CSS3 (Flexbox & Grid), JavaScript
* **Database:** SQLite (Default) / Compatible with PostgreSQL & MySQL
* **Authentication:** Django's robust User Authentication system (Login, Logout, Register).

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/ChatHub.git
    cd ChatHub
    ```

2.  **Set up a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django
    ```

4.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Start the Server**
    ```bash
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

* `models.py`: Contains the `Room`, `Topic`, and `Message` models with relational logic.
* `views.py`: Handles the logic for room CRUD (Create, Read, Update, Delete) and user authentication.
* `templates/`: Modular HTML templates including a base layout and reusable components like feeds and sidebars.
* `static/`: Custom CSS focusing on a clean, modern, and high-contrast user interface.

---
