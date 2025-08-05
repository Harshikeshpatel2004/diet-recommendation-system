import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, conlist
from typing import List, Optional
import pandas as pd
from model import recommend, output_recommended_recipes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class PredictionIn(BaseModel):
    nutrition_input: conlist(float, min_items=9, max_items=9)
    ingredients: list[str] = []
    params: Optional[params] = None

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: list[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None
    error: Optional[str] = None
    message: Optional[str] = None

def load_dataset():
    """Safely load the dataset with proper error handling"""
    try:
        # Use os.path.join for portable file paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try optimized dataset first, then fallback to original
        optimized_path = os.path.join(current_dir, 'Data', 'dataset_optimized.csv')
        original_path = os.path.join(current_dir, 'Data', 'dataset.csv')
        
        # Try to load optimized dataset first, then test dataset, then original
        if os.path.exists(optimized_path):
            logger.info(f"Attempting to load optimized dataset from: {optimized_path}")
            try:
                dataset = pd.read_csv(optimized_path, compression='gzip')
                logger.info("Optimized dataset loaded successfully with gzip compression")
            except Exception as e:
                logger.warning(f"Failed to load optimized dataset with gzip: {e}")
                try:
                    dataset = pd.read_csv(optimized_path)
                    logger.info("Optimized dataset loaded successfully without compression")
                except Exception as e2:
                    logger.error(f"Failed to load optimized dataset: {e2}")
                    dataset = None
        else:
            logger.info("Optimized dataset not found, trying test dataset")
            dataset = None
        
        # If optimized dataset failed, try test dataset
        if dataset is None:
            test_path = os.path.join(current_dir, 'Data', 'dataset_test.csv')
            if os.path.exists(test_path):
                logger.info(f"Attempting to load test dataset from: {test_path}")
                try:
                    dataset = pd.read_csv(test_path)
                    logger.info("Test dataset loaded successfully")
                except Exception as e:
                    logger.error(f"Failed to load test dataset: {e}")
                    dataset = None
            else:
                logger.info("Test dataset not found, trying original dataset")
                dataset = None
        
        # If optimized dataset failed or doesn't exist, try original
        if dataset is None and os.path.exists(original_path):
            logger.info(f"Attempting to load original dataset from: {original_path}")
            try:
                dataset = pd.read_csv(original_path, compression='gzip')
                logger.info("Original dataset loaded successfully with gzip compression")
            except Exception as e:
                logger.warning(f"Failed to load original dataset with gzip: {e}")
                try:
                    dataset = pd.read_csv(original_path)
                    logger.info("Original dataset loaded successfully without compression")
                except Exception as e2:
                    logger.error(f"Failed to load original dataset: {e2}")
                    return None, f"Failed to load dataset: {str(e2)}"
        
        if dataset is None:
            logger.error("No dataset file found")
            return None, "No dataset file found. Please ensure dataset.csv or dataset_optimized.csv exists in the Data folder."
        
        if dataset.empty:
            logger.error("Dataset is empty")
            return None, "Dataset is empty"
        
        logger.info(f"Dataset loaded successfully with {len(dataset)} rows")
        return dataset, None
        
    except Exception as e:
        logger.error(f"Unexpected error loading dataset: {e}")
        return None, f"Unexpected error loading dataset: {str(e)}"

@app.get("/")
def home():
    return {"health_check": "OK", "message": "Diet Recommendation API is running"}

@app.post("/predict/", response_model=PredictionOut)
async def predict_recipes(prediction_input: PredictionIn):
    """
    Generate recipe recommendations based on nutrition input and ingredients
    """
    try:
        logger.info("Received prediction request")
        logger.info(f"Nutrition input: {prediction_input.nutrition_input}")
        logger.info(f"Ingredients: {prediction_input.ingredients}")
        
        # Load dataset with error handling
        dataset, error = load_dataset()
        if error:
            logger.error(f"Dataset loading failed: {error}")
            return JSONResponse(
                status_code=500,
                content={
                    "output": None,
                    "error": error,
                    "message": "Failed to load dataset"
                }
            )
        
        # Set default params if not provided
        if prediction_input.params is None:
            prediction_input.params = params()
        
        logger.info("Generating recommendations...")
        
        # Generate recommendations
        try:
            recommendation_dataframe = recommend(
                dataset, 
                prediction_input.nutrition_input, 
                prediction_input.ingredients, 
                prediction_input.params.dict()
            )
            
            if recommendation_dataframe is None:
                logger.warning("No recommendations found for given criteria")
                return {
                    "output": None,
                    "error": None,
                    "message": "No recipes found matching your criteria. Try adjusting your nutrition requirements or ingredients."
                }
            
            # Process recommendations
            output = output_recommended_recipes(recommendation_dataframe)
            
            if output is None or len(output) == 0:
                logger.warning("No recipes returned after processing")
                return {
                    "output": None,
                    "error": None,
                    "message": "No recipes found after processing. Try different nutrition values or ingredients."
                }
            
            logger.info(f"Successfully generated {len(output)} recommendations")
            return {
                "output": output,
                "error": None,
                "message": f"Successfully generated {len(output)} recipe recommendations"
            }
            
        except Exception as e:
            logger.error(f"Error in recommendation generation: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "output": None,
                    "error": f"Error generating recommendations: {str(e)}",
                    "message": "Failed to generate recommendations"
                }
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "output": None,
                "error": f"Unexpected error: {str(e)}",
                "message": "Internal server error"
            }
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler to ensure JSON responses"""
    logger.error(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "output": None,
            "error": f"Internal server error: {str(exc)}",
            "message": "An unexpected error occurred"
        }
    )

