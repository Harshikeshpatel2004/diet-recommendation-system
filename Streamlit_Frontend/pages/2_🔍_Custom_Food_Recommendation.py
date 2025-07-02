import streamlit as st
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
import pandas as pd
from streamlit_echarts import st_echarts

# Set page configuration
st.set_page_config(
    page_title="Custom Food Recommendation 🌱",
    page_icon="🍲",
    layout="wide"
)

# Nutrition values
nutrition_values = [
    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
    'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent'
]

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None

# Classes for recommendation and display
class Recommendation:
    def __init__(self, nutrition_list, nb_recommendations, ingredient_txt):
        self.nutrition_list = nutrition_list
        self.nb_recommendations = nb_recommendations
        self.ingredient_txt = ingredient_txt

    def generate(self):
        params = {'n_neighbors': self.nb_recommendations, 'return_distance': False}
        ingredients = self.ingredient_txt.split(';')
        generator = Generator(self.nutrition_list, ingredients, params)
        recommendations = generator.generate()
        recommendations = recommendations.json()['output']
        if recommendations is not None:
            for recipe in recommendations:
                recipe['image_link'] = find_image(recipe['Name'])
        return recommendations

class Display:
    def __init__(self):
        self.nutrition_values = nutrition_values

    def display_recommendation(self, recommendations):
        st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Recommended Recipes 🍴</h2>", unsafe_allow_html=True)
        if recommendations is not None:
            rows = len(recommendations) // 5
            for column, row in zip(st.columns(5), range(5)):
                with column:
                    for recipe in recommendations[rows * row:rows * (row + 1)]:
                        recipe_name = recipe['Name']
                        expander = st.expander(recipe_name, expanded=False)
                        recipe_link = recipe['image_link']
                        recipe_img = f'<div style="text-align: center;"><img src="{recipe_link}" alt="{recipe_name}" style="width:100%; border-radius:10px;"></div>'
                        nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutrition_values})
                        expander.markdown(recipe_img, unsafe_allow_html=True)
                        expander.markdown(f"<h5 style='text-align: center;'>Nutritional Values (g):</h5>", unsafe_allow_html=True)
                        expander.dataframe(nutritions_df)
                        expander.markdown("<h5>Ingredients:</h5>")
                        for ingredient in recipe['RecipeIngredientParts']:
                            expander.markdown(f"- {ingredient}")
                        expander.markdown("<h5>Instructions:</h5>")
                        for instruction in recipe['RecipeInstructions']:
                            expander.markdown(f"- {instruction}")
                        expander.markdown("<h5>Cooking Times:</h5>")
                        expander.markdown(f"""
                            - **Cook Time**: {recipe['CookTime']} min  
                            - **Prep Time**: {recipe['PrepTime']} min  
                            - **Total Time**: {recipe['TotalTime']} min  
                        """)
        else:
            st.info("No recipes found matching your ingredients.", icon="🙁")

    def display_overview(self, recommendations):
        if recommendations is not None:
            st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Recipe Overview 📊</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col2:
                selected_recipe_name = st.selectbox("Choose a recipe to analyze:", [recipe['Name'] for recipe in recommendations])
            selected_recipe = next(recipe for recipe in recommendations if recipe['Name'] == selected_recipe_name)
            options = {
                "title": {"text": "Nutrition Breakdown", "subtext": f"{selected_recipe_name}", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left"},
                "series": [
                    {
                        "name": "Nutritional Values",
                        "type": "pie",
                        "radius": "50%",
                        "data": [
                            {"value": selected_recipe[nutrition_value], "name": nutrition_value} for nutrition_value in self.nutrition_values
                        ],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }
            st_echarts(options=options, height="600px")
            st.caption("Tip: Click on a segment to highlight or hide its value.")

# Page title
st.markdown("<h1 style='text-align: center;'>🍽️ Custom Food Recommendation System</h1>", unsafe_allow_html=True)

# Instantiate classes
display = Display()

# Input form for user preferences
with st.form("recommendation_form"):
    st.markdown("<h3>Adjust Nutritional Preferences:</h3>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        Calories = st.slider("Calories", 0, 2000, 500)
        CholesterolContent = st.slider("Cholesterol", 0, 300, 0)
        FiberContent = st.slider("Fiber", 0, 50, 10)
    with col2:
        FatContent = st.slider("Fat", 0, 100, 50)
        SodiumContent = st.slider("Sodium", 0, 2300, 400)
        SugarContent = st.slider("Sugar", 0, 40, 10)
    with col3:
        SaturatedFatContent = st.slider("Saturated Fat", 0, 13, 0)
        CarbohydrateContent = st.slider("Carbohydrates", 0, 325, 100)
        ProteinContent = st.slider("Protein", 0, 40, 10)
    nb_recommendations = st.slider("Number of Recommendations", 5, 20, 5)
    ingredient_txt = st.text_input("Ingredients (separated by ';')", placeholder="e.g., Milk;Eggs;Butter")
    st.caption("Enter multiple ingredients to refine your search.")
    generated = st.form_submit_button("Generate Recommendations")
    if generated:
        with st.spinner("Finding the best recipes for you..."):
            recommender = Recommendation(
                [Calories, FatContent, SaturatedFatContent, CholesterolContent, SodiumContent,
                 CarbohydrateContent, FiberContent, SugarContent, ProteinContent],
                nb_recommendations,
                ingredient_txt
            )
            st.session_state.recommendations = recommender.generate()
            st.session_state.generated = True

# Display results if generated
if st.session_state.generated:
    display.display_recommendation(st.session_state.recommendations)
    display.display_overview(st.session_state.recommendations)
