# ChatHub 💬

**ChatHub** is a high-performance, real-time web application designed for organized group discussions. Originally built as a Django prototype, it has been scaled into a production-ready platform featuring live messaging and cloud-native architecture.

## ✨ New & Advanced Features

* **Real-Time Messaging (WebSockets):** Instant message delivery and room updates without page refreshes, powered by Django Channels.
* **Production Deployment:** Fully hosted on **Render** with automated CI/CD pipelines.
* **Cloud Database Integration:** Migrated from SQLite to **TiDB (MySQL-compatible)** for scalable, distributed data storage with SSL encryption.
* **Global Activity Feed:** A live sidebar that keeps you updated on the latest messages across the entire platform.
* **Voice & Media Ready:** Infrastructure support for voice messaging and file uploads (via Cloudinary integration).
* **Secure Authentication:** Enhanced security with CSRF protection, secure environment variables, and encrypted model fields.
* **Dynamic Room Discovery:** Browse rooms by topic or use the global search to find discussions by name or description.

## 🛠️ Technical Stack

* **Backend:** Python 3.14 / Django 5.2
* **Asynchronous Engine:** **Daphne** (ASGI) & **Django Channels**
* **Real-Time Layer:** **Redis** (via Upstash) for WebSocket layering and task queuing.
* **Database:** **TiDB Cloud** (MySQL) with server-side SSL certificates.
* **Static/Media Hosting:** **WhiteNoise** for optimized static delivery; Cloudinary-ready for media.
* **Task Queue:** **Celery** integration for background processing (Optional/Development).
* **Frontend:** HTML5, CSS3 (Custom Flexbox/Grid), JavaScript (WebSockets).

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Redis Server (or Upstash account)
* TiDB / MySQL Database

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/ChatHub.git
    cd ChatHub
    ```

2.  **Set up a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows: venv\Scripts\activate
    # Mac/Linux: source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL=your_tidb_connection_string
    REDIS_URL=your_redis_url
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    ```

5.  **Run Migrations & Start**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000/`.

---

## 📂 Project Architecture

* **`studybud/asgi.py`**: The entry point for the ASGI server (Daphne), handling both HTTP and WebSocket protocols.
* **`base/consumers.py`**: Contains the WebSocket logic for real-time chat broadcasting.
* **`base/models.py`**: Relational logic for `User`, `Room`, `Topic`, and `Message` with support for encrypted fields.
* **`settings.py`**: Production-ready configuration including `WhiteNoise`, `dj-database-url`, and `CSRF_TRUSTED_ORIGINS`.

---

🌐 Live Demo & Deployment Notes
Live Link: https://chathub-72tx.onrender.com

⚠️ Important Note on Media Files (Images/Uploads)
While the application supports full image and file transitions locally, the live demo has specific limitations due to the Render Free Tier infrastructure:

Local Environment: Files and images work perfectly as they are stored on your local persistent disk.

Live Production: Render uses an ephemeral file system. This means any file uploaded to the chat-files/ directory is wiped immediately whenever the instance restarts or a new deployment occurs.

No 24-Hour Persistence: Unlike some "temporary" hosting, the Free Tier does not guarantee even short-term persistence (like 24 hours) for local media storage.

Database Persistence: All text-based data (Rooms, Messages, Users, and Topics) is 100% persistent as it is hosted on a separate TiDB Cloud cluster.
