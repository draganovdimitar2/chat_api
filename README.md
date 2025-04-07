# Chat Room API

## 📘 Project Overview
This project was created as a way to introduce myself to WebSockets using **FastAPI**. It's a backend chat application that demonstrates real-time communication and includes integration with **PostgreSQL** using an ORM approach via **SQLModel**, along with **Alembic** for handling database migrations.

The system features secure user authentication using **JWT tokens**, **Argon2** for password hashing, and **OAuth2** for authorization flow.  
> 🚧 This project is still in active development, with more features and improvements on the way.
## ⚙️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/draganovdimitar2/chat_api.git
    ```
2. Navigate to the project directory:
    ```bash
    cd chat_api
    ```
3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    ```
    * for powershell
    ```bash
    env\Scripts\activate
    ```
    * for linux/os
    ```bash
    source env/bin/activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt "fastapi[standard]"
    ```
5. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```
    
## ▶️ Running the Application
1. Start the server:
  ```bash
  fastapi dev app/
  ```
  * The application will be available at http://127.0.0.1:8000

2. Access API documentation
  * Open http://127.0.0.1:8000/docs in your browser to interact with the Swagger UI

## 🔑 Authentication Setup
1. Register users
   * Use the auth/register endpoint in Swagger UI to create 2 test users
   * Example request body for the first user:
      ```bash 
      "username": "test1",
      "email": "test1@gmail.com",
      "password": "1234"
      ```
    * Example request body for the second user:
      ```bash 
      "username": "test2",
      "email": "test2@gmail.com",
      "password": "1234"
      ```
2. Get JWT tokens
   * Use the auth/login endpoint for each user to obtain access tokens
   * Save both tokens for WebSocket connections

## 💬 Connecting to Chat
Because this project currently lacks a frontend interface, you can connect to the chat using a WebSocket client.
1. WebSocket Setup
   * Open [Hoppscotch WebSocket Client](https://hoppscotch.io/realtime/websocket)
   * Connect using each user's token:
      ```bash 
      ws://localhost:8000/chat/ws?token=YOUR_TOKEN_HERE
      ```
    * Press Connect and start chatting :)
  
## 🔮 Future Improvements
1. Frontend Development 👥
    * I hope to collaborate with a frontend developer to create a dedicated chat interface with modern UI/UX
2. Enhanced Features
    - User presence indicators (online/offline status)
    - Message history persistence
    - Read receipts and typing indicators
    - File/Image sharing capabilities
    - Multiple chat rooms/channels
3. Advanced Functionality
    - Message search functionality
    - User profile management
      
