"""
Test the complete document verification and storage pipeline
"""

from verify_and_store import process_document
import os

def test_pipeline():
    """Test the complete pipeline with sample documents"""
    
    # Create test_docs directory if it doesn't exist
    os.makedirs("test_docs", exist_ok=True)
    
    # Test with the sample document we created
    test_images = [
        "test_docs/sample_document.jpg"  # Our created sample image
    ]
    
    print("Testing document verification and storage pipeline...")
    print("=" * 50)
    
    for image_path in test_images:
        print(f"\nProcessing: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"  ⚠️  File not found: {image_path}")
            print("  Please provide a valid test image for this test.")
            continue
            
        # Process the document
        response = process_document(image_path)
        
        print(f"  Status: {response.get('status', 'UNKNOWN')}")
        
        if response.get('status') == 'VERIFIED':
            print(f"  ✅ Document verified as REAL")
            print(f"  🔗 URL: {response.get('image_url', 'N/A')}")
            print(f"  🆔 Public ID: {response.get('public_id', 'N/A')}")
        elif response.get('status') == 'REJECTED':
            print(f"  ❌ Document rejected as FAKE")
            print(f"  💬 Reason: {response.get('message', 'No reason provided')}")
        else:
            print(f"  ⚠️  Error occurred")
            print(f"  💬 Message: {response.get('message', 'No message provided')}")
    
    print("\n" + "=" * 50)
    print("Pipeline testing completed")

# Run the test
if __name__ == "__main__":
    test_pipeline()