""" Src main, to run go to base directory and run python -m src """

import asyncio
from src import app

if __name__ == "__main__":
    asyncio.run(app.run())
