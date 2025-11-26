import streamlit as st
import requests
import time

# Backend configuration
API_BASE = "http://localhost:8000"

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            return True, "✅ Backend connected"
        else:
            return False, f"❌ Backend error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "❌ Backend not running - start it first!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
st.title("🤖 Autonomous QA Agent")
st.markdown("Generate test cases and Selenium scripts from your documentation")

# Check backend status
backend_status, message = check_backend()
st.sidebar.markdown(f"**Backend Status:** {message}")

if not backend_status:
    st.error("Backend server is not running!")
    st.info(
        "**To start the backend:**\n"
        "1. Open a new Command Prompt\n"
        "2. Navigate to your project\n" 
        "3. Run: `python -m uvicorn app.main:app --reload --port 8000`\n"
        "4. Wait for: `Uvicorn running on http://0.0.0.0:8000`"
    )
    st.stop()

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'html_content' not in st.session_state:
    st.session_state.html_content = ""

# Tab interface
tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🧪 Test Generation", "⚙️ Script Generation"])

with tab1:
    st.header("Build Knowledge Base")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Support Documents")
        support_docs = st.file_uploader(
            "Upload product specs, UI guides, etc.",
            type=['md', 'txt', 'json', 'pdf'],
            accept_multiple_files=True,
            key="support_docs"
        )
    
    with col2:
        st.subheader("Upload Checkout HTML")
        html_file = st.file_uploader("Upload checkout.html", type=['html'], key="html_file")
        
        if html_file:
            st.session_state.html_content = html_file.getvalue().decode("utf-8")
            st.success("HTML file loaded successfully!")
            with st.expander("View HTML Content"):
                st.code(st.session_state.html_content[:500] + "..." if len(st.session_state.html_content) > 500 else st.session_state.html_content)
    
    if st.button("🚀 Build Knowledge Base", type="primary"):
        if support_docs:
            with st.spinner("Building knowledge base..."):
                try:
                    # Prepare files for upload
                    files = []
                    for doc in support_docs:
                        files.append(("files", (doc.name, doc.getvalue(), doc.type)))
                    
                    # Send request to backend
                    response = requests.post(f"{API_BASE}/ingest-documents", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Knowledge base built successfully!")
                        st.json(result)
                    else:
                        st.error(f"Backend error {response.status_code}: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Make sure it's running on port 8000.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Request failed: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
        else:
            st.warning("Please upload at least one support document.")

with tab2:
    st.header("Generate Test Cases")
    
    query = st.text_area(
        "Enter your test generation query:",
        value="Generate test cases for discount code validation and form validation",
        height=100
    )
    
    if st.button("🎯 Generate Test Cases"):
        with st.spinner("Generating test cases..."):
            try:
                response = requests.post(f"{API_BASE}/generate-test-cases", params={"query": query})
                if response.status_code == 200:
                    st.session_state.test_cases = response.json()["test_cases"]
                    st.success(f"✅ Generated {len(st.session_state.test_cases)} test cases!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
    
    if st.session_state.test_cases:
        st.subheader("Generated Test Cases")
        for i, tc in enumerate(st.session_state.test_cases):
            with st.expander(f"🧪 {tc['test_id']}: {tc['feature']}"):
                st.write(f"**Scenario:** {tc['test_scenario']}")
                st.write(f"**Expected:** {tc['expected_result']}")
                st.write(f"**Source:** {tc['grounded_in']}")

with tab3:
    st.header("Generate Selenium Script")
    
    if not st.session_state.test_cases:
        st.warning("Please generate test cases first in the 'Test Generation' tab.")
    else:
        test_case_options = {f"{tc['test_id']}: {tc['feature']}": tc for tc in st.session_state.test_cases}
        selected_test = st.selectbox("Select a test case:", options=list(test_case_options.keys()))
        
        if st.button("🛠️ Generate Selenium Script"):
            selected_tc = test_case_options[selected_test]
            
            with st.spinner("Generating Selenium script..."):
                try:
                    # FIXED: Send proper structured data
                    request_data = {
                        "test_case": {
                            "test_id": selected_tc['test_id'],
                            "feature": selected_tc['feature'],
                            "test_scenario": selected_tc['test_scenario'],
                            "expected_result": selected_tc['expected_result'],
                            "grounded_in": selected_tc['grounded_in']
                        },
                        "html_content": st.session_state.html_content
                    }
                    
                    # FIXED: Add proper headers and timeout
                    response = requests.post(
                        f"{API_BASE}/generate-script", 
                        json=request_data,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        script = result.get("script", "")
                        
                        if script:
                            st.success("✅ Script generated successfully!")
                            
                            st.subheader("Generated Selenium Script")
                            st.code(script, language='python')
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Script",
                                data=script,
                                file_name=f"{selected_tc['test_id']}_selenium.py",
                                mime="text/x-python"
                            )
                            
                            # Instructions for running
                            st.info(
                                f"**To run this test:**\n"
                                f"1. Save the script as `{selected_tc['test_id']}_selenium.py`\n"
                                f"2. Make sure `test_page.html` is in the same folder\n"
                                f"3. Run: `python {selected_tc['test_id']}_selenium.py`\n"
                                f"4. Or use: `python run_tests.py` to run all tests"
                            )
                        else:
                            st.error("❌ Script was generated but is empty")
                    else:
                        st.error(f"❌ Backend Error {response.status_code}: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Make sure it's running on port 8000.")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Backend might be busy.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Request failed: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# Display debug information in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Debug Information")
if st.session_state.test_cases:
    st.sidebar.write(f"Test Cases: {len(st.session_state.test_cases)}")
if st.session_state.html_content:
    st.sidebar.write("HTML: ✅ Loaded")
else:
    st.sidebar.write("HTML: ❌ Not loaded")

st.sidebar.markdown("---")
st.sidebar.info(
    "**Usage:**\n"
    "1. Upload documents + HTML in Knowledge Base tab\n"
    "2. Generate test cases in Test Generation tab\n"  
    "3. Select test case and generate script in Script Generation tab\n"
    "4. Run generated Selenium scripts"
)