from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_router import api_router
app = FastAPI()
#app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api/v1')

if __name__ == '__main__':
    import uvicorn
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    uvicorn.run(app, host='127.0.0.1', port=8000)