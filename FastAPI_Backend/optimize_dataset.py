#!/usr/bin/env python3
"""
Dataset optimization script for Diet Recommendation System
Reduces dataset size and improves loading performance
"""

import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def optimize_dataset():
    """Optimize the dataset for deployment"""
    try:
        # Load the original dataset
        current_dir = os.path.dirname(os.path.abspath(__file__))
        original_path = os.path.join(current_dir, 'Data', 'dataset.csv')
        optimized_path = os.path.join(current_dir, 'Data', 'dataset_optimized.csv')
        
        logger.info(f"Loading original dataset from: {original_path}")
        
        # Try to load with compression first
        try:
            df = pd.read_csv(original_path, compression='gzip')
            logger.info("Loaded with gzip compression")
        except:
            df = pd.read_csv(original_path)
            logger.info("Loaded without compression")
        
        logger.info(f"Original dataset shape: {df.shape}")
        logger.info(f"Original dataset size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # Remove rows with missing critical data
        initial_rows = len(df)
        df = df.dropna(subset=['Name', 'RecipeIngredientParts', 'RecipeInstructions'])
        logger.info(f"Removed {initial_rows - len(df)} rows with missing data")
        
        # Keep only essential columns
        essential_columns = [
            'Name', 'CookTime', 'PrepTime', 'TotalTime',
            'RecipeIngredientParts', 'RecipeInstructions',
            'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
            'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent'
        ]
        
        # Check which columns exist
        existing_columns = [col for col in essential_columns if col in df.columns]
        df = df[existing_columns]
        
        # Sample the dataset to reduce size (keep 5000 recipes)
        if len(df) > 5000:
            df = df.sample(n=5000, random_state=42)
            logger.info(f"Sampled to {len(df)} recipes")
        
        # Optimize data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Convert to string and limit length
                df[col] = df[col].astype(str).str[:500]  # Limit string length
            elif df[col].dtype == 'float64':
                df[col] = df[col].astype('float32')  # Reduce precision
            elif df[col].dtype == 'int64':
                df[col] = df[col].astype('int32')  # Reduce precision
        
        # Save optimized dataset
        df.to_csv(optimized_path, index=False, compression='gzip')
        
        logger.info(f"Optimized dataset shape: {df.shape}")
        logger.info(f"Optimized dataset size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        logger.info(f"Saved optimized dataset to: {optimized_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error optimizing dataset: {e}")
        return False

if __name__ == "__main__":
    success = optimize_dataset()
    if success:
        print("✅ Dataset optimization completed successfully!")
    else:
        print("❌ Dataset optimization failed!") 