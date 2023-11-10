from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from modules import main_router


app = FastAPI(title='Staginator Core', description='Universal project staging service')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
