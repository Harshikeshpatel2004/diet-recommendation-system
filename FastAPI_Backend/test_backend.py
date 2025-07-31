#!/usr/bin/env python3
"""
Test script for the FastAPI backend
Run this to test the backend locally before deployment
"""

import requests
import json
import os
import sys

def test_health_check(base_url="http://localhost:8000"):
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{base_url}/")
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_predict_endpoint(base_url="http://localhost:8000"):
    """Test the predict endpoint with sample data"""
    # Sample nutrition input (calories, fat, saturated_fat, cholesterol, sodium, carbs, fiber, sugar, protein)
    sample_nutrition = [500.0, 20.0, 5.0, 50.0, 300.0, 60.0, 8.0, 15.0, 25.0]
    sample_ingredients = ["chicken", "rice"]
    sample_params = {"n_neighbors": 3, "return_distance": False}
    
    request_data = {
        "nutrition_input": sample_nutrition,
        "ingredients": sample_ingredients,
        "params": sample_params
    }
    
    try:
        print(f"Sending request to {base_url}/predict/")
        print(f"Request data: {json.dumps(request_data, indent=2)}")
        
        response = requests.post(
            f"{base_url}/predict/",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("✅ Successfully parsed JSON response")
                print(f"Response keys: {list(json_response.keys())}")
                
                if json_response.get('error'):
                    print(f"❌ Error in response: {json_response['error']}")
                    print(f"Message: {json_response.get('message', 'No message')}")
                    return False
                
                output = json_response.get('output', [])
                if output:
                    print(f"✅ Found {len(output)} recipes")
                    for i, recipe in enumerate(output[:2]):  # Show first 2 recipes
                        print(f"  Recipe {i+1}: {recipe.get('Name', 'Unknown')}")
                else:
                    print("⚠️ No recipes found in output")
                    print(f"Message: {json_response.get('message', 'No message')}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"Response text (first 500 chars): {response.text[:500]}")
                return False
        else:
            print(f"❌ HTTP error {response.status_code}")
            print(f"Response text: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the server is running")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_dataset_loading():
    """Test if the dataset can be loaded"""
    try:
        import pandas as pd
        import os
        
        # Check if dataset file exists
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(current_dir, 'Data', 'dataset.csv')
        
        print(f"Checking dataset at: {dataset_path}")
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset file not found at: {dataset_path}")
            return False
        
        # Try to load the dataset
        try:
            dataset = pd.read_csv(dataset_path, compression='gzip')
            print(f"✅ Dataset loaded successfully with gzip compression")
        except Exception as e:
            print(f"⚠️ Failed to load with gzip: {e}")
            try:
                dataset = pd.read_csv(dataset_path)
                print(f"✅ Dataset loaded successfully without compression")
            except Exception as e2:
                print(f"❌ Failed to load dataset: {e2}")
                return False
        
        print(f"Dataset shape: {dataset.shape}")
        print(f"Dataset columns: {list(dataset.columns)}")
        
        # Check if required columns exist
        required_columns = ['RecipeIngredientParts', 'RecipeInstructions']
        for col in required_columns:
            if col in dataset.columns:
                print(f"✅ Column '{col}' found")
            else:
                print(f"❌ Required column '{col}' not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dataset loading: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing FastAPI Backend")
    print("=" * 50)
    
    # Test dataset loading
    print("\n1. Testing dataset loading...")
    dataset_ok = test_dataset_loading()
    
    if not dataset_ok:
        print("❌ Dataset loading failed. Please check the dataset file.")
        sys.exit(1)
    
    # Test health check
    print("\n2. Testing health check endpoint...")
    health_ok = test_health_check()
    
    if not health_ok:
        print("❌ Health check failed. Make sure the server is running.")
        print("To start the server, run: uvicorn main:app --reload")
        sys.exit(1)
    
    # Test predict endpoint
    print("\n3. Testing predict endpoint...")
    predict_ok = test_predict_endpoint()
    
    if predict_ok:
        print("\n✅ All tests passed! The backend is working correctly.")
    else:
        print("\n❌ Predict endpoint test failed. Check the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 