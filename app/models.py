from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentUpload(BaseModel):
    filename: str
    content: str

class TestCase(BaseModel):
    test_id: str
    feature: str
    test_scenario: str
    expected_result: str
    grounded_in: str

class ScriptRequest(BaseModel):
    test_case: TestCase
    html_content: str