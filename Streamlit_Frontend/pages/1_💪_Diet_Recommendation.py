import streamlit as st
import pandas as pd
from random import uniform as rnd
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪", layout="wide")

# Nutrition values
nutritions_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

# Initialize session state
if 'person' not in st.session_state:
    st.session_state.person = None
    st.session_state.generated = False
    st.session_state.recommendations = None
    st.session_state.weight_loss_option = None


# Person class
class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self):
        return round(self.weight / ((self.height / 100) ** 2), 2)

    def display_result(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return f"{bmi} kg/m²", "Underweight", "Red"
        elif 18.5 <= bmi < 25:
            return f"{bmi} kg/m²", "Normal", "Green"
        elif 25 <= bmi < 30:
            return f"{bmi} kg/m²", "Overweight", "Yellow"
        else:
            return f"{bmi} kg/m²", "Obesity", "Red"

    def calculate_bmr(self):
        return (10 * self.weight + 6.25 * self.height - 5 * self.age + (5 if self.gender == 'Male' else -161))

    def calories_calculator(self):
        activity_multiplier = {
            'Little/no exercise': 1.2,
            'Light exercise': 1.375,
            'Moderate exercise (3-5 days/wk)': 1.55,
            'Very active (6-7 days/wk)': 1.725,
            'Extra active (very active & physical job)': 1.9
        }
        return self.calculate_bmr() * activity_multiplier[self.activity]

    def generate_recommendations(self):
        total_calories = self.weight_loss * self.calories_calculator()
        recommendations = []
        for meal, percentage in self.meals_calories_perc.items():
            meal_calories = percentage * total_calories
            generator = Generator([meal_calories, rnd(10, 30), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)])
            recommended_recipes = generator.generate().json()['output']
            for recipe in recommended_recipes:
                recipe['image_link'] = find_image(recipe['Name'])
            recommendations.append(recommended_recipes)
        return recommendations


# Display class
class Display:
    def __init__(self):
        self.plans = ["Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"]
        self.weights = [1, 0.9, 0.8, 0.6]
        self.losses = ['-0 kg/week', '-0.25 kg/week', '-0.5 kg/week', '-1 kg/week']

    def display_bmi(self, person):
        if person is None:
            st.error("No person data available. Please input your details.")
            return
        st.header('BMI CALCULATOR')
        bmi_string, category, color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        st.markdown(f'<p style="color:{color}; font-size:20px;">{category}</p>', unsafe_allow_html=True)

    def display_calories(self, person):
        if person is None:
            st.error("No person data available. Please input your details.")
            return
        st.header('CALORIES CALCULATOR')
        maintain_calories = person.calories_calculator()
        for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(4)):
            with col:
                st.metric(label=plan, value=f"{round(maintain_calories * weight)} Calories/day", delta=loss)

    def display_comparison_chart(self, person, recommendations):
        if not recommendations:
            st.error("No recommendations to display.")
            return

        # Total calories chosen by the user
        total_nutrition_values = {nutrition: 0 for nutrition in nutritions_values}
        for meal_recommendation in recommendations:
            for recipe in meal_recommendation:
                for nutrition in nutritions_values:
                    total_nutrition_values[nutrition] += recipe[nutrition]

        # Total calories vs weight loss plan
        total_calories = total_nutrition_values['Calories']
        weight_loss_calories = person.weight_loss * person.calories_calculator()

        options = {
            "xAxis": {"type": "category", "data": ["Chosen Recipes", "Target Calories"]},
            "yAxis": {"type": "value"},
            "series": [
                {
                    "data": [
                        {"value": total_calories, "itemStyle": {"color": "#FF6666" if total_calories > weight_loss_calories else "#66FF66"}},
                        {"value": weight_loss_calories, "itemStyle": {"color": "#3399FF"}},
                    ],
                    "type": "bar",
                }
            ],
        }
        st_echarts(options=options, height="400px")

        # Nutritional Bar Chart with Plotly
        st.subheader("Nutritional Values Comparison:")
        fig = px.bar(
            x=nutritions_values,
            y=[total_nutrition_values[n] for n in nutritions_values],
            title="Total Nutrition Breakdown",
            labels={'x': 'Nutritional Components', 'y': 'Amount'},
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_recommendation(self, person, recommendations):
        if not recommendations:
            st.error("No recommendations available. Please generate recommendations first.")
            return
        st.header('DIET RECOMMENDATIONS')
        for meal, recommendation, col in zip(person.meals_calories_perc.keys(), recommendations, st.columns(len(recommendations))):
            with col:
                st.subheader(meal.capitalize())
                for recipe in recommendation:
                    with st.expander(recipe['Name']):
                        st.markdown(f"![{recipe['Name']}]({recipe['image_link']})")
                        st.markdown(f"**Ingredients:** {', '.join(recipe['RecipeIngredientParts'])}")
                        st.markdown(f"**Instructions:** {', '.join(recipe['RecipeInstructions'])}")


# Form for user input
def user_form():
    st.header("User Details")
    with st.form(key="user_form"):
        age = st.number_input("Age", 1, 120, 25)
        height = st.number_input("Height (cm)", 100, 250, 170)
        weight = st.number_input("Weight (kg)", 20, 200, 70)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", ["Little/no exercise", "Light exercise", "Moderate exercise (3-5 days/wk)", "Very active (6-7 days/wk)", "Extra active (very active & physical job)"])
        weight_loss_option = st.selectbox("Weight Loss Plan", ["Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"])
        meals_calories_perc = {'breakfast': 0.3, 'lunch': 0.4, 'dinner': 0.3}

        submit = st.form_submit_button("Submit")
        if submit:
            weight_loss_multiplier = {"Maintain weight": 1, "Mild weight loss": 0.9, "Weight loss": 0.8, "Extreme weight loss": 0.6}
            st.session_state.person = Person(age, height, weight, gender, activity, meals_calories_perc, weight_loss_multiplier[weight_loss_option])
            st.success("Details submitted successfully!")


# Main app
display = Display()
user_form()

if st.session_state.person:
    display.display_bmi(st.session_state.person)
    display.display_calories(st.session_state.person)

    if st.button("Generate Recommendations"):
        st.session_state.recommendations = st.session_state.person.generate_recommendations()
        st.success("Recommendations generated!")

    if st.session_state.recommendations:
        display.display_comparison_chart(st.session_state.person, st.session_state.recommendations)
        display.display_recommendation(st.session_state.person, st.session_state.recommendations)
