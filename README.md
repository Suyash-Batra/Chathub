# ChatHub 💬

**ChatHub** is a modern, high-performance real-time chat platform built for dynamic conversations, private communities, and media-rich collaboration. Originally started as a Django prototype, it has evolved into a production-ready application with secure messaging, cloud-native deployment, and advanced room management features.

## ✨ Key Features

* **Real-Time Messaging:** Instant message delivery and live room updates powered by WebSockets.
* **Media Support:** Share photos, files, and voice chats directly inside conversations.
* **Cloud Media Storage:** Integrated with **Cloudinary** for scalable image and file storage.
* **Secure Rooms:** Private rooms require a key to join, with room access protected and encrypted.
* **Encrypted Data:** Private room keys and sensitive message data are securely encrypted.
* **Public & Private Rooms:** Create open public spaces or restricted private rooms for controlled discussions.
* **Ephemeral Rooms:** Temporary rooms that automatically delete messages after 24 hours.
* **Global Search:** Search rooms, users, and content quickly using a global search bar.
* **Smart Room Intelligence:**

  * Auto-detect room sentiment with mood-tracking signals
  * Auto-detect room language based on the room description
* **Built-in Commands:**

  * `/generate` — generate an image prompt
  * `/advice` — get helpful advice
  * `/joke` — generate a light, lame joke
* **Custom Avatars:** Users can upload custom avatars, and rooms can have their own profile pictures.
* **Admin Management:** Full Django admin panel support for managing users, rooms, messages, and platform data.
* **Editable Content Tools:** Admins and authorized users can edit users, rooms, and delete messages when needed.
* **Badge System:** Users can earn badges by completing tasks and achievements, which are displayed on their profiles.
* **API Support:** Built-in GET APIs for rooms, users, badges, and related platform data.
* **Production Deployment:** Hosted on **Render** for reliable cloud deployment.
* **Database Power:** Uses **TiDB** as the database for scalable, MySQL-compatible storage.
* **Redis Support:** Uses **Upstash Redis** for caching, real-time communication, and background task support.
* **Docker Support:** Includes a `Dockerfile` and `docker-compose.yml` for containerized development and deployment.

## 🛠️ Technical Stack

* **Backend:** Python 3.14 / Django 5.2
* **Real-Time Engine:** Django Channels + Daphne
* **Database:** TiDB Cloud (MySQL-compatible)
* **Cache / Message Broker:** Upstash Redis
* **Media Storage:** Cloudinary
* **Deployment:** Render
* **Containerization:** Docker & Docker Compose
* **Frontend:** HTML5, CSS3, JavaScript
* **Task Processing:** Celery (optional / background tasks)
* **Static File Handling:** WhiteNoise

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* TiDB database access
* Upstash Redis account
* Cloudinary account for media storage
* Docker (optional, for containerized setup)

### Installation (Local Setup)

1. **Clone the repository**

   ```bash
   git clone https://github.com/YourUsername/ChatHub.git
   cd ChatHub
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True

   DATABASE_URL=your_tidb_connection_string
   REDIS_URL=your_upstash_redis_url

   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Run migrations and start the server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Open the app**

   ```
   http://127.0.0.1:8000/
   ```

---

## 🐳 Docker Setup

ChatHub supports containerized deployment using Docker.

1. **Build and start containers**

   ```bash
   docker-compose up --build
   ```

2. **Or use the provided startup script (Windows)**

   ```bash
   start.bat
   ```

This will automatically spin up the application along with required services.

---

## 📂 Project Architecture

* **`studybud/asgi.py`** — ASGI entry point for HTTP and WebSocket traffic
* **`base/consumers.py`** — WebSocket logic for real-time chat messages
* **`base/models.py`** — Data models for users, rooms, topics, messages, badges, and encrypted room access
* **`settings.py`** — Production configuration for TiDB, Redis, Cloudinary, and deployment settings
* **`base/views.py`** — Room, profile, search, and API-related views

## 🌐 Deployment Notes

**Live Demo:** https://chathub-72tx.onrender.com

### Media Storage

ChatHub uses **Cloudinary** for cloud-based media handling, making uploads reliable in production environments.

### Security

ChatHub is designed with security in mind, including encrypted private room keys, secure environment variables, and controlled access to rooms and messages.

## 🏅 Badges & Achievements

Users can earn badges by completing platform tasks and milestones. These badges are displayed on their profiles as a record of activity and achievement.

## 📡 API Features

ChatHub provides GET endpoints for:

* Rooms
* Users
* Badges

These APIs make it easy to extend or integrate with other services.

---

**ChatHub** combines real-time messaging, cloud-native deployment, secure collaboration, and smart room features into one powerful platform.
