from fastapi import FastAPI
from modules import main_router


app = FastAPI(title='Staginator Core', description='Universal project staging service')

app.include_router(main_router)
