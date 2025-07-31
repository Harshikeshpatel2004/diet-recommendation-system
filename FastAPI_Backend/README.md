# FastAPI Backend - Diet Recommendation System

This is the backend API for the Diet Recommendation System, built with FastAPI and deployed on Render.

## Features

- **Safe File Paths**: Uses `os.path.join` for portable file paths
- **Comprehensive Error Handling**: All functions have try-catch blocks with detailed logging
- **JSON Response Guarantee**: Always returns valid JSON responses, even on errors
- **Detailed Logging**: Extensive logging for debugging deployment issues
- **Graceful Degradation**: Handles missing data and edge cases gracefully

## File Structure

```
FastAPI_Backend/
├── main.py              # FastAPI application with endpoints
├── model.py             # ML model functions with error handling
├── Data/
│   └── dataset.csv      # Recipe dataset (91MB)
├── test_backend.py      # Test script for debugging
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the Backend

```bash
python test_backend.py
```

This will test:
- Dataset loading
- Health check endpoint
- Predict endpoint with sample data

## API Endpoints

### Health Check
- **GET** `/`
- Returns: `{"health_check": "OK", "message": "Diet Recommendation API is running"}`

### Predict Recipes
- **POST** `/predict/`
- **Request Body:**
```json
{
  "nutrition_input": [500.0, 20.0, 5.0, 50.0, 300.0, 60.0, 8.0, 15.0, 25.0],
  "ingredients": ["chicken", "rice"],
  "params": {
    "n_neighbors": 5,
    "return_distance": false
  }
}
```

- **Response Format:**
```json
{
  "output": [
    {
      "Name": "Recipe Name",
      "CookTime": "30 min",
      "PrepTime": "15 min",
      "TotalTime": "45 min",
      "RecipeIngredientParts": ["ingredient1", "ingredient2"],
      "Calories": 450.0,
      "FatContent": 15.0,
      "SaturatedFatContent": 3.0,
      "CholesterolContent": 45.0,
      "SodiumContent": 250.0,
      "CarbohydrateContent": 55.0,
      "FiberContent": 6.0,
      "SugarContent": 12.0,
      "ProteinContent": 28.0,
      "RecipeInstructions": ["step1", "step2"]
    }
  ],
  "error": null,
  "message": "Successfully generated 3 recipe recommendations"
}
```

## Error Handling

The API always returns valid JSON responses with the following structure:

### Success Response
```json
{
  "output": [...],
  "error": null,
  "message": "Success message"
}
```

### Error Response
```json
{
  "output": null,
  "error": "Error description",
  "message": "User-friendly message"
}
```

## Deployment on Render

### 1. Environment Setup
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2. Environment Variables
- `PORT`: Automatically set by Render
- No additional environment variables required

### 3. File Paths
The backend uses absolute paths to ensure the dataset is found correctly:
```python
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, 'Data', 'dataset.csv')
```

## Debugging Common Issues

### 1. Dataset Loading Issues
- **Problem:** "Dataset file not found" error
- **Solution:** Ensure `Data/dataset.csv` is in the correct location
- **Check:** Run `python test_backend.py` to verify dataset loading

### 2. JSON Decode Errors
- **Problem:** Frontend gets `JSONDecodeError`
- **Solution:** Backend now always returns valid JSON with error handling
- **Check:** Look at backend logs for detailed error messages

### 3. No Recommendations Found
- **Problem:** Empty recommendations returned
- **Solution:** Check if nutrition values are reasonable and ingredients exist in dataset
- **Debug:** Use the test script with different parameters

### 4. Memory Issues
- **Problem:** Server crashes due to memory limits
- **Solution:** Dataset is loaded per request, not globally
- **Optimization:** Consider reducing dataset size or using database

## Logging

The backend includes comprehensive logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Log levels:
- **INFO**: Normal operations (dataset loading, API calls)
- **WARNING**: Non-critical issues (regex failures, missing images)
- **ERROR**: Critical issues (file not found, ML errors)

## Frontend Integration

The Streamlit frontend has been updated to handle the new response format:

1. **Error Handling**: Checks for `error` field in response
2. **Graceful Degradation**: Shows warnings for missing recipes
3. **Timeout Handling**: 30-second timeout for API calls
4. **Fallback Images**: Uses placeholder images if recipe images fail to load

## Testing

### Manual Testing
```bash
# Test health check
curl http://localhost:8000/

# Test predict endpoint
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{"nutrition_input":[500,20,5,50,300,60,8,15,25],"ingredients":["chicken"],"params":{"n_neighbors":3}}'
```

### Automated Testing
```bash
python test_backend.py
```

## Troubleshooting

### Check Render Logs
1. Go to your Render dashboard
2. Select your FastAPI service
3. Click on "Logs" tab
4. Look for error messages and warnings

### Common Error Messages
- `"Dataset file not found"`: Check if dataset.csv is in Data/ folder
- `"Failed to load dataset"`: Check file format and compression
- `"Insufficient data"`: Try different nutrition values or ingredients
- `"Error generating recommendations"`: Check ML model parameters

### Performance Optimization
- Dataset is ~91MB, consider compression or database storage
- ML model uses Nearest Neighbors with cosine similarity
- Consider caching for frequently requested recipes 