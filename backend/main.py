from pathlib import Path
import uvicorn
from core.registrar import register_app

app = register_app()


if __name__ == "__main__":
    try:
        config = uvicorn.Config(app=f"{Path(__file__).stem}:app")
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
