import pandas as pd
from app.services.rag_engine import rag_engine
from app.core.config import settings
import os
import uuid

class ExtractionService:
    def __init__(self):
        pass

    async def extract_structured_data(self, client_id: str, extraction_prompt: str):
        """
        Uses the RAG engine to extract specific data and formats it as a structured table.
        Example: "Extract all monthly expenses for 2023"
        """
        # 1. Trigger a specific extraction prompt for the LLM
        full_prompt = (
            f"You are a data extraction specialist. Based on the client's documents, "
            f"extract the following information and return ONLY a CSV-formatted list. "
            f"CSV Format: columns separated by commas, no markdown blocks, no conversational text.\n\n"
            f"Extraction Request: {extraction_prompt}"
        )

        # We reuse the RAG logic to get context, but change the prompt to force CSV
        # For simplicity in this MVP, we'll call the rag_engine logic
        response = await rag_engine.answer_question(client_id, full_prompt)
        csv_content = response['answer']

        # 2. Convert the response to a Pandas DataFrame to validate
        from io import StringIO
        try:
            df = pd.read_csv(StringIO(csv_content))

            # 3. Save as Excel file in the client's folder
            client_dir = os.path.join(settings.UPLOAD_DIR, client_id, "reports")
            os.makedirs(client_dir, exist_ok=True)

            filename = f"extraction_{uuid.uuid4().hex[:8]}.xlsx"
            file_path = os.path.join(client_dir, filename)
            df.to_excel(file_path, index=False)

            return {
                "status": "success",
                "filename": filename,
                "data": df.to_dict(orient="records"),
                "file_path": file_path
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to parse structured data: {str(e)}",
                "raw_response": csv_content
            }

extraction_service = ExtractionService()
