from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize the Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# FastAPI app instance
app = FastAPI()

# Pydantic model for incoming request
class TextRequest(BaseModel):
    text: str
    entities: list[str] = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]
    language: str = "en"

@app.post("/analyze/")
async def analyze_text(request: TextRequest):
    """
    Endpoint to detect PII in the provided text.
    """
    try:
        # Use Presidio's AnalyzerEngine to detect PII in the provided text
        results = analyzer.analyze(
            text=request.text, entities=request.entities, language=request.language
        )
        
        # Format the detected PII into a list of dictionaries
        detected_pii = [
            {"entity": result.entity_type, "value": result.text, "confidence": result.score}
            for result in results
        ]
        
        return {"detected_pii": detected_pii}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anonymize/")
async def anonymize_text(request: TextRequest):
    """
    Endpoint to detect and anonymize PII in the provided text.
    """
    try:
        # Use Presidio's AnalyzerEngine to detect PII in the provided text
        results = analyzer.analyze(
            text=request.text, entities=request.entities, language=request.language
        )
        
        # Use Presidio's AnonymizerEngine to anonymize the detected PII
        anonymized_text = anonymizer.anonymize(
            text=request.text, analyzer_results=results
        )
        
        return {"anonymized_text": anonymized_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
