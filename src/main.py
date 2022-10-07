import string
import time
import random

from fastapi import FastAPI, Request

from .pages import user

app = FastAPI()

app.include_router(user.router)


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# @app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # logger.info(f"rid={idem} start request path={request.url.path}")
    print(f"rid={idem} start request {request.method} path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    # try:
    #     request_body = await request.json()
    # except:
    #     request_body = {}
    #
    # print(f"rid={idem} Body: {request_body}")
    print(f"rid={idem} Path Params: {request.path_params}")
    print(f"rid={idem} Query Params: {request.query_params}")
    print(f"rid={idem} Cookies: {request.cookies}")

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    # logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    print(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/")
async def root():
    return {"status": "OK"}
