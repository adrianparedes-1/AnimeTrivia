Here’s your **updated README in proper Markdown** format:

````markdown
# AnimeTrivia 🎮✨

AnimeTrivia is a multiplayer anime and manga-themed trivia game built with Python. Players compete by guessing songs, shows, or characters, with game state managed in Redis for fast, ephemeral gameplay.

## Features

- Multiplayer support
- Real-time game state stored in Redis (using JSON module)
- Lightweight backend designed for quick gameplay
- Randomized trivia questions per game session
- Easy to extend with new question sets

## Requirements

- Python 3.11+
- Docker (for Redis)
- Redis with JSON module (`ReJSON`)

## Setup

### 1. Run Redis with JSON support

Make sure Docker is installed and running. Then start a Redis container with the JSON module:

```bash
docker run -p 6379:6379 --name redis-redisjson redislabs/rejson:latest
````

This will start Redis on port `6379` with JSON capabilities enabled.

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file and add any required environment variables, e.g.:

```env
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
```

### 4. Start the Application

```bash
python main.py
```

## Usage

* Create or join a trivia room
* Start a game session
* Guess songs, shows, or characters
* Track scores in real-time

## Project Structure

* `main.py` — entry point for the application
* `game/` — game logic and room management
* `redis_utils.py` — Redis interactions using JSON
* `schemas.py` — Pydantic models for request/response validation
* `requirements.txt` — Python dependencies

## Notes

* Redis must be running with the JSON module enabled for proper game state management.
* Game rooms are ephemeral and stored in Redis as JSON objects.

## Contributing

1. Fork the repository
2. Create a new feature branch
3. Submit a pull request

```

I can also **add a “Development & Testing” section** showing how to simulate multiplayer locally and explain the Redis JSON structure for game rooms. This helps anyone running or contributing to the project understand it fully. Do you want me to add that?
```
