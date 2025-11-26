import subprocess
import sys
import os
import glob

def run_selenium_test(test_file):
    """Run a Selenium test file"""
    try:
        print(f"🚀 Running {test_file}...")
        print("-" * 50)
        
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print(f"❌ {test_file} - FAILED")
            if result.stderr:
                print("Error:", result.stderr)
            if result.stdout:
                print("Output:", result.stdout)
        
        print("-" * 50)
        return result.returncode == 0
        
    except Exception as e:
        print(f"💥 Error running {test_file}: {e}")
        return False

def find_test_files():
    """Find all Selenium test files in the current directory"""
    test_patterns = [
        "TC-*.py",
        "test_*.py", 
        "*_selenium.py"
    ]
    
    test_files = []
    for pattern in test_patterns:
        test_files.extend(glob.glob(pattern))
    
    # Remove duplicates and exclude this file
    test_files = list(set(test_files))
    if "run_tests.py" in test_files:
        test_files.remove("run_tests.py")
    
    return sorted(test_files)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['selenium', 'webdriver-manager']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    """Run all Selenium tests"""
    print("🧪 Starting Selenium Test Suite")
    print("=" * 60)
    
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print(f"\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return
    
    # Check if test page exists
    if not os.path.exists("test_page.html"):
        print("❌ test_page.html not found!")
        print("💡 Make sure test_page.html is in the same directory")
        return
    
    # Find test files
    test_files = find_test_files()
    
    if not test_files:
        print("ℹ️  No test files found.")
        print("💡 Generate test scripts using the Streamlit app first")
        print("   Available patterns: TC-*.py, test_*.py, *_selenium.py")
        return
    
    print(f"📁 Found {len(test_files)} test file(s):")
    for tf in test_files:
        print(f"   - {tf}")
    
    print("\n" + "=" * 60)
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            if run_selenium_test(test_file):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️  {test_file} not found")
    
    print("=" * 60)
    print(f"📊 TEST SUMMARY:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📋 Total:  {len(test_files)}")
    print("=" * 60)
    
    if failed == 0 and passed > 0:
        print("🎉 All tests passed! Excellent work!")
    elif failed > 0:
        print("💡 Some tests failed. Check the output above for details.")
        sys.exit(1)  # Exit with error code if any tests failed

if __name__ == "__main__":
    main()