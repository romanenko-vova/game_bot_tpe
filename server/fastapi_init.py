from fastapi import FastAPI
from fastapi.responses import FileResponse, Response

# 1. сервер, который хостинг, который комп в интернете
# 2. сервер, как fastapi — сервер, который принимает запросы из интернета и отдает ответы
# 3. сервер, как uvicorn — сервер, который запускает fastapi

def init_server():
    app = FastAPI()
    
    @app.get('/')
    def index():
        return FileResponse('templates/index.html')
    
    @app.get('/about')
    def about():
        return FileResponse('templates/about.html')
    
    return app


app = init_server()
