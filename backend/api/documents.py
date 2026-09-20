from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from ..services.document_parser import process_uploaded_document

router = APIRouter(prefix="/api", tags=["Document Processing"])


@router.post("/upload-document")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None)
):
    """
    Extracts business demand points, cities, quantities, and industry profiles
    from uploaded CSVs, TXT invoices, or freeform dispatch text.
    """
    try:
        if file:
            content_bytes = await file.read()
            content = content_bytes.decode("utf-8", errors="ignore")
            filename = file.filename
        elif text_content:
            content = text_content
            filename = "pasted_report.txt"
        else:
            raise HTTPException(status_code=400, detail="Either a file or text_content must be provided.")

        result = process_uploaded_document(filename=filename, content=content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document parsing failed: {str(e)}")
