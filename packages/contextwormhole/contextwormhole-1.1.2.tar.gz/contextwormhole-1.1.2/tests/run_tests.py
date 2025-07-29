# run_tests.py - Test Runner Script
# ==================================

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
        else:
            print(f"❌ FAILED: {description} (exit code: {result.returncode})")
            
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ ERROR running {description}: {e}")
        return False

def main():
    """Run all tests and generate reports."""
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🌌 ContextWormhole Test Suite Runner")
    print(f"Working directory: {project_root}")
    
    # Test commands to run
    test_commands = [
        # Basic test run
        ("pytest test_contextwormhole.py -v", "Core functionality tests"),
        
        # All tests with coverage
        ("pytest --cov=contextwormhole --cov-report=html --cov-report=term",
         "All tests with coverage"),
        
        # Performance/benchmark tests (if any)
        ("pytest -k 'performance' -v", "Performance tests"),
        
        # Quick test run (just smoke tests)
        ("pytest -m 'not slow' -v", "Quick test run"),
    ]
    
    # Optional: Run linting/formatting checks
    optional_commands = [
        ("python3 -m black --check ../contextwormhole.py", "Black formatting check"),
        ("python3 -m flake8 ../contextwormhole.py", "Flake8 linting"),
        ("python3 -m mypy ../contextwormhole.py", "MyPy type checking"),
    ]
    
    print(f"\n📋 Will run {len(test_commands)} test suites...")
    
    results = []
    for cmd, description in test_commands:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Run optional commands if tools are available
    print(f"\n🔧 Running optional checks...")
    optional_results = []
    for cmd, description in optional_commands:
        success = run_command(cmd, description)
        optional_results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    print("Core Test Results:")
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {description}")
    
    print("\nOptional Check Results:")
    for description, success in optional_results:
        status = "✅ PASS" if success else "❌ FAIL" 
        print(f"  {status} {description}")
    
    # Overall result
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    print(f"\nOverall: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()