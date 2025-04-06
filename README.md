# Chat Room using Websockets

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
      "username": "user1",
      "email": "user1@gmail.com",
      "password": "1234"
      ```
    * Example request body for the second user:
      ```bash 
      "username": "user2",
      "email": "user2@gmail.com",
      "password": "1234"
      ```
2. Get JWT tokens
   * Use the auth/login endpoint for each user to obtain access tokens
   * Save both tokens for WebSocket connections

## 💬 Connecting to Chat
1. WebSocket Setup
   * Open [Hoppscotch WebSocket Client](https://hoppscotch.io/realtime/websocket)
   * Configure connection with both users:
      ```bash 
      ws://localhost:8000/chat/ws?token=YOUR_TOKEN_HERE
      ```
    * Press connect and start chatting :)
  
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
      
