dev:
	watchfiles --filter python --ignore-path .venv,__pycache__ "/Users/vladimirromanenko/programs/game_bot/.venv/bin/python main.py"
fastapi:
	uvicorn server.fastapi_init:app --reload
cf:
	cloudflared tunnel --url http://localhost:8000