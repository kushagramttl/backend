# app/controllers/base_controller.py

from fastapi import APIRouter

class BaseController:
    def __init__(self):
        self.router = APIRouter()
