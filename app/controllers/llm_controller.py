# app/controllers/llm_controller.py

from app.controllers.base_controller import BaseController
from app.models.schemas import PromptRequest
from app.services.rag_engine import generate_rag_response

class LLMController(BaseController):
    def __init__(self):
        super().__init__()

        @self.router.post("/generate")
        async def generate(req: PromptRequest):
            return {"response": generate_rag_response(req.prompt)}

controller = LLMController()
router = controller.router
