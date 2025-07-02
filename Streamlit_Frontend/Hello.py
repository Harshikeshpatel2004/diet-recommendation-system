import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🥗 Welcome to the Diet Recommendation System!")
st.write(
    """
    ### Your personal assistant for healthier and smarter food choices! 🌟
    
    - 👩‍⚕️ **Understand your BMI and calorie needs.**
    - 🥘 **Get personalized diet recommendations based on your preferences.**
    - 📊 **Track nutritional values for better health management.**

    Start by selecting one of the tools from the sidebar to explore your options!
    """
)

# Add an image or banner (optional)
st.image(
    "Dietimage.png",
    caption="Healthy food for a healthy life!",
    width=500,
    
)

# Sidebar content
st.sidebar.title("Diet Recommendation System")
st.sidebar.success("Select a recommendation tool to get started!")
