# from fastapi import FastAPI
# from app.services.rag_engine import generate_rag_response
# from app.services.llama_engine import generate_response
# from app.models.schemas import PromptRequest

# # Create FastAPI app
# app = FastAPI()

# # Define endpoint to generate LLaMA response
# @app.post("/generate")
# def generate(request: PromptRequest):
#     result = generate_response(request.prompt)
#     return { "response": result }

# @app.post("/rag")
# def rag(req: PromptRequest):
#     return {"response": generate_rag_response(req.prompt)}

from fastapi import FastAPI
from app.controllers.llm_controller import router as llm_router
from app.controllers.company_controller import router as company_router

app = FastAPI()

app.include_router(llm_router, prefix="/api")
app.include_router(company_router, prefix="/api")
