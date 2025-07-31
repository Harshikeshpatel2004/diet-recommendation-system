import numpy as np
import re
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# Configure logging
logger = logging.getLogger(__name__)

def scaling(dataframe):
    try:
        logger.info("Starting data scaling process")
        scaler = StandardScaler()
        prep_data = scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
        logger.info(f"Data scaled successfully. Shape: {prep_data.shape}")
        return prep_data, scaler
    except Exception as e:
        logger.error(f"Error in scaling function: {e}")
        raise

def nn_predictor(prep_data):
    try:
        logger.info("Initializing Nearest Neighbors model")
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)
        logger.info("Nearest Neighbors model fitted successfully")
        return neigh
    except Exception as e:
        logger.error(f"Error in nn_predictor function: {e}")
        raise

def build_pipeline(neigh, scaler, params):
    try:
        logger.info("Building ML pipeline")
        transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
        pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
        logger.info("Pipeline built successfully")
        return pipeline
    except Exception as e:
        logger.error(f"Error in build_pipeline function: {e}")
        raise

def extract_data(dataframe, ingredients):
    try:
        logger.info(f"Extracting data with {len(ingredients)} ingredients")
        extracted_data = dataframe.copy()
        extracted_data = extract_ingredient_filtered_data(extracted_data, ingredients)
        logger.info(f"Data extraction completed. Remaining rows: {len(extracted_data)}")
        return extracted_data
    except Exception as e:
        logger.error(f"Error in extract_data function: {e}")
        raise
    
def extract_ingredient_filtered_data(dataframe, ingredients):
    try:
        extracted_data = dataframe.copy()
        if not ingredients:
            logger.info("No ingredients specified, returning all data")
            return extracted_data
        
        regex_string = ''.join(map(lambda x: f'(?=.*{x})', ingredients))
        logger.info(f"Filtering with regex pattern: {regex_string}")
        
        # Handle potential regex errors
        try:
            filtered_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string, regex=True, flags=re.IGNORECASE)]
            logger.info(f"Filtered data shape: {filtered_data.shape}")
            return filtered_data
        except Exception as regex_error:
            logger.warning(f"Regex filtering failed, returning unfiltered data: {regex_error}")
            return extracted_data
    except Exception as e:
        logger.error(f"Error in extract_ingredient_filtered_data function: {e}")
        raise

def apply_pipeline(pipeline, _input, extracted_data):
    try:
        logger.info("Applying ML pipeline to input data")
        _input = np.array(_input).reshape(1, -1)
        result = extracted_data.iloc[pipeline.transform(_input)[0]]
        logger.info(f"Pipeline applied successfully. Result shape: {result.shape}")
        return result
    except Exception as e:
        logger.error(f"Error in apply_pipeline function: {e}")
        raise

def recommend(dataframe, _input, ingredients=[], params={'n_neighbors': 5, 'return_distance': False}):
    try:
        logger.info("Starting recommendation process")
        logger.info(f"Input shape: {len(_input)}, Ingredients: {ingredients}, Params: {params}")
        
        extracted_data = extract_data(dataframe, ingredients)
        
        if extracted_data.shape[0] >= params['n_neighbors']:
            logger.info(f"Sufficient data available ({extracted_data.shape[0]} rows >= {params['n_neighbors']} neighbors)")
            prep_data, scaler = scaling(extracted_data)
            neigh = nn_predictor(prep_data)
            pipeline = build_pipeline(neigh, scaler, params)
            result = apply_pipeline(pipeline, _input, extracted_data)
            logger.info("Recommendation process completed successfully")
            return result
        else:
            logger.warning(f"Insufficient data: {extracted_data.shape[0]} rows < {params['n_neighbors']} neighbors required")
            return None
    except Exception as e:
        logger.error(f"Error in recommend function: {e}")
        raise

def extract_quoted_strings(s):
    try:
        # Find all the strings inside double quotes
        strings = re.findall(r'"([^"]*)"', s)
        # Join the strings with 'and'
        return strings
    except Exception as e:
        logger.warning(f"Error extracting quoted strings: {e}")
        return []

def output_recommended_recipes(dataframe):
    try:
        if dataframe is not None:
            logger.info("Processing recommended recipes output")
            output = dataframe.copy()
            output = output.to_dict("records")
            
            for recipe in output:
                try:
                    recipe['RecipeIngredientParts'] = extract_quoted_strings(recipe['RecipeIngredientParts'])
                    recipe['RecipeInstructions'] = extract_quoted_strings(recipe['RecipeInstructions'])
                except Exception as e:
                    logger.warning(f"Error processing recipe {recipe.get('Name', 'Unknown')}: {e}")
                    # Set default values if processing fails
                    recipe['RecipeIngredientParts'] = []
                    recipe['RecipeInstructions'] = []
            
            logger.info(f"Successfully processed {len(output)} recipes")
            return output
        else:
            logger.warning("No dataframe provided to output_recommended_recipes")
            return None
    except Exception as e:
        logger.error(f"Error in output_recommended_recipes function: {e}")
        return None

