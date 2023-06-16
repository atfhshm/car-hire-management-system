from fastapi import FastAPI
from fastapi import applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from dataclasses import dataclass

from .routes import auth


app = FastAPI()

app.include_router(auth.router)


# app.mount("/static", StaticFiles(directory="./static"), name="static")


# def swagger_monkey_patch(*args, **kwargs):
#     return get_swagger_ui_html(
#         *args,
#         **kwargs,
#         swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui/swagger-ui.css",
#     )


# applications.get_swagger_ui_html = swagger_monkey_patch


@dataclass
class Message:
    project: str = "car-hire-management-system"
    location: str = "root"
    version: str = "0.0.1"


@app.get("/", tags=["root"], response_model=Message)
def root():
    return Message()
