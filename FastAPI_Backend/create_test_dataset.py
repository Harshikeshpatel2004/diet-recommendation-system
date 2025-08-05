#!/usr/bin/env python3
"""
Create a small test dataset for deployment testing
"""

import pandas as pd
import numpy as np
import os

def create_test_dataset():
    """Create a small test dataset with sample recipes"""
    
    # Sample recipes for testing
    test_recipes = [
        {
            'Name': 'Chicken Salad',
            'CookTime': '15 min',
            'PrepTime': '10 min',
            'TotalTime': '25 min',
            'RecipeIngredientParts': '["chicken breast", "lettuce", "tomatoes", "olive oil"]',
            'RecipeInstructions': '["Cook chicken", "Chop vegetables", "Mix ingredients"]',
            'Calories': 350.0,
            'FatContent': 12.0,
            'SaturatedFatContent': 2.0,
            'CholesterolContent': 85.0,
            'SodiumContent': 450.0,
            'CarbohydrateContent': 8.0,
            'FiberContent': 3.0,
            'SugarContent': 4.0,
            'ProteinContent': 45.0
        },
        {
            'Name': 'Vegetarian Pasta',
            'CookTime': '20 min',
            'PrepTime': '15 min',
            'TotalTime': '35 min',
            'RecipeIngredientParts': '["pasta", "tomatoes", "basil", "olive oil"]',
            'RecipeInstructions': '["Boil pasta", "Prepare sauce", "Combine ingredients"]',
            'Calories': 420.0,
            'FatContent': 8.0,
            'SaturatedFatContent': 1.0,
            'CholesterolContent': 0.0,
            'SodiumContent': 380.0,
            'CarbohydrateContent': 75.0,
            'FiberContent': 6.0,
            'SugarContent': 8.0,
            'ProteinContent': 12.0
        },
        {
            'Name': 'Salmon with Rice',
            'CookTime': '25 min',
            'PrepTime': '10 min',
            'TotalTime': '35 min',
            'RecipeIngredientParts': '["salmon", "rice", "vegetables", "lemon"]',
            'RecipeInstructions': '["Cook salmon", "Prepare rice", "Add vegetables"]',
            'Calories': 480.0,
            'FatContent': 18.0,
            'SaturatedFatContent': 3.0,
            'CholesterolContent': 95.0,
            'SodiumContent': 520.0,
            'CarbohydrateContent': 45.0,
            'FiberContent': 4.0,
            'SugarContent': 2.0,
            'ProteinContent': 38.0
        },
        {
            'Name': 'Greek Salad',
            'CookTime': '0 min',
            'PrepTime': '15 min',
            'TotalTime': '15 min',
            'RecipeIngredientParts': '["cucumber", "tomatoes", "olives", "feta cheese"]',
            'RecipeInstructions': '["Chop vegetables", "Mix ingredients", "Add dressing"]',
            'Calories': 180.0,
            'FatContent': 14.0,
            'SaturatedFatContent': 6.0,
            'CholesterolContent': 25.0,
            'SodiumContent': 680.0,
            'CarbohydrateContent': 8.0,
            'FiberContent': 3.0,
            'SugarContent': 5.0,
            'ProteinContent': 6.0
        },
        {
            'Name': 'Beef Stir Fry',
            'CookTime': '15 min',
            'PrepTime': '20 min',
            'TotalTime': '35 min',
            'RecipeIngredientParts': '["beef", "vegetables", "soy sauce", "ginger"]',
            'RecipeInstructions': '["Slice beef", "Stir fry vegetables", "Add sauce"]',
            'Calories': 380.0,
            'FatContent': 16.0,
            'SaturatedFatContent': 5.0,
            'CholesterolContent': 75.0,
            'SodiumContent': 720.0,
            'CarbohydrateContent': 22.0,
            'FiberContent': 5.0,
            'SugarContent': 6.0,
            'ProteinContent': 32.0
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(test_recipes)
    
    # Save to Data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'Data')
    
    # Create Data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    test_dataset_path = os.path.join(data_dir, 'dataset_test.csv')
    df.to_csv(test_dataset_path, index=False)
    
    print(f"✅ Test dataset created with {len(df)} recipes")
    print(f"📁 Saved to: {test_dataset_path}")
    print(f"📊 Dataset size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    return True

if __name__ == "__main__":
    create_test_dataset() 