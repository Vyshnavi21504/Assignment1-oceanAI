from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import aiofiles
import json
from typing import List

app = FastAPI(title="Autonomous QA Agent")

# CORS middleware - IMPORTANT for Streamlit connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Autonomous QA Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

@app.post("/ingest-documents")
async def ingest_documents(files: List[UploadFile] = File(...)):
    try:
        documents_processed = 0
        processed_files = []
        
        for file in files:
            # Create safe filename
            safe_filename = file.filename.replace(" ", "_")
            file_path = f"data/{safe_filename}"
            
            # Save file to data directory
            async with aiofiles.open(file_path, "wb") as f:
                content = await file.read()
                await f.write(content)
            
            documents_processed += 1
            processed_files.append(safe_filename)
            
            # Log the file processing
            print(f"Processed file: {safe_filename}")
        
        return {
            "status": "Knowledge Base Built", 
            "documents_processed": documents_processed,
            "processed_files": processed_files,
            "message": f"Successfully processed {documents_processed} files"
        }
    
    except Exception as e:
        print(f"Error in ingest-documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

@app.post("/generate-test-cases")
async def generate_test_cases(query: str):
    try:
        # Mock response for now - you'll add AI later
        test_cases = [
            {
                "test_id": "TC-001",
                "feature": "Discount Code",
                "test_scenario": "Apply valid discount code SAVE15",
                "expected_result": "15% discount applied to total price",
                "grounded_in": "product_specs.md"
            },
            {
                "test_id": "TC-002", 
                "feature": "Form Validation",
                "test_scenario": "Submit form with invalid email",
                "expected_result": "Error message shown in red text",
                "grounded_in": "ui_ux_guide.txt"
            },
            {
                "test_id": "TC-003",
                "feature": "Payment Method",
                "test_scenario": "Select PayPal payment option",
                "expected_result": "PayPal option is selected successfully",
                "grounded_in": "product_specs.md"
            }
        ]
        return {"test_cases": test_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test cases: {str(e)}")

@app.post("/generate-script")
async def generate_script(request_data: dict):
    try:
        # Extract test_case from the request data
        test_case = request_data.get("test_case", {})
        html_content = request_data.get("html_content", "")
        
        # Validate that we have the required test_case data
        if not test_case or "test_id" not in test_case:
            raise HTTPException(
                status_code=400, 
                detail="Missing required test_case data with test_id"
            )
        
        # Get test case details with safe defaults
        test_id = test_case.get('test_id', 'TC-000')
        feature = test_case.get('feature', 'General')
        test_scenario = test_case.get('test_scenario', 'Test scenario')
        
        # Create class name and method name
        class_name = test_id.replace('-', '')
        method_name = test_id.lower().replace('-', '_')
        
        # FIXED: Enhanced Selenium script with proper f-string formatting
        script = f'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os

class Test{class_name}:
    """Test Case: {test_id} - {feature}"""
    
    def setup_method(self, method):
        """Setup before each test"""
        # Setup Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Get the absolute path to test_page.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(current_dir, "test_page.html")
        self.driver.get("file://" + html_file)
    
    def teardown_method(self, method):
        """Cleanup after each test"""
        self.driver.quit()
    
    def test_{method_name}(self):
        """{test_scenario}"""
        
        # Test steps will vary based on the test case
        feature_lower = "{feature}".lower()
        if "discount" in feature_lower:
            self._test_discount_code()
        elif "form" in feature_lower or "validation" in feature_lower:
            self._test_form_validation()
        elif "payment" in feature_lower:
            self._test_payment_method()
        else:
            self._test_general()
    
    def _test_discount_code(self):
        """Test discount code functionality"""
        print("🧪 Testing discount code functionality...")
        
        try:
            # Find discount code input and apply button
            discount_input = self.driver.find_element(By.ID, "discountCode")
            apply_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Apply Discount')]")
            
            # Enter valid discount code
            discount_input.clear()
            discount_input.send_keys("SAVE15")
            apply_button.click()
            
            # Wait for and verify success message
            success_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "discountMessage"))
            )
            
            assert "15% discount applied" in success_message.text, "Discount success message not found"
            assert "success" in success_message.get_attribute("class"), "Success CSS class not applied"
            
            # Verify total price is updated
            total_element = self.driver.find_element(By.ID, "total")
            expected_total = "16.99"  # 15% off 19.99
            assert total_element.text == expected_total, f"Expected total {{expected_total}}, got {{total_element.text}}"
            
            print("✅ Discount code test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Discount code test failed: {{e}}")
            return False
    
    def _test_form_validation(self):
        """Test form validation"""
        print("🧪 Testing form validation...")
        
        try:
            # Try to submit form with empty fields
            pay_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Pay Now')]")
            pay_button.click()
            
            # Check for error messages
            name_error = self.driver.find_element(By.ID, "nameError")
            email_error = self.driver.find_element(By.ID, "emailError")
            
            assert "required" in name_error.text, "Name required error not shown"
            assert "required" in email_error.text, "Email required error not shown"
            
            # Test invalid email
            email_input = self.driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys("invalid-email")
            pay_button.click()
            
            email_error = self.driver.find_element(By.ID, "emailError")
            assert "Invalid email format" in email_error.text, "Invalid email error not shown"
            
            print("✅ Form validation test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Form validation test failed: {{e}}")
            return False
    
    def _test_payment_method(self):
        """Test payment method selection"""
        print("🧪 Testing payment method selection...")
        
        try:
            # Select PayPal option
            paypal_radio = self.driver.find_element(By.ID, "paypal")
            paypal_radio.click()
            
            # Verify PayPal is selected
            assert paypal_radio.is_selected(), "PayPal radio button not selected"
            
            # Verify Credit Card is not selected
            credit_card_radio = self.driver.find_element(By.ID, "creditcard")
            assert not credit_card_radio.is_selected(), "Credit card should not be selected"
            
            print("✅ Payment method test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Payment method test failed: {{e}}")
            return False
    
    def _test_general(self):
        """General test implementation"""
        print("🧪 Executing general test...")
        
        try:
            # Basic test - just verify page loads
            title = self.driver.find_element(By.TAG_NAME, "h1")
            assert "Test Checkout Page" in title.text
            print("✅ Page loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ General test failed: {{e}}")
            return False

def run_test():
    """Run the test"""
    test = Test{class_name}()
    try:
        test.setup_method(None)
        success = test.test_{method_name}()
        if success:
            print("🎉 All tests passed!")
        else:
            print("💥 Some tests failed!")
        return success
    except Exception as e:
        print(f"❌ Test execution error: {{e}}")
        return False
    finally:
        test.teardown_method(None)

if __name__ == "__main__":
    success = run_test()
    exit(0 if success else 1)
'''
        return {"script": script}
    
    except Exception as e:
        print(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")