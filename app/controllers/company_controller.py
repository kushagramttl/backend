# app/controllers/company_controller.py

from app.controllers.base_controller import BaseController
from app.data.company_data import COMPANY_DB
from fastapi import HTTPException

class CompanyController(BaseController):
    def __init__(self):
        super().__init__()

        @self.router.get("/company/{symbol}")
        async def get_company_info(symbol: str, field: str = None):
            company = COMPANY_DB.get(symbol.upper())
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")
            return {field: company.get(field, "Field not available")} if field else company

controller = CompanyController()
router = controller.router
