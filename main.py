import streamlit as st
from langchain import PromptTemplate
from langchain_community.llms import OpenAI
import os

# Defineerime PromptTemplate vastavalt luksusautode müügiäpi vajadustele
template = """
You are a luxury car sales copywriter with 20 years of experience. You are analyzing a customer's preferences to write a personalized car description that only this customer will receive;
CAR MODEL input text: {content};
CUSTOMER preferred features: {features};
CUSTOMER budget: {budget};
TASK: Write a car description that is tailored to this customer's preferred features and budget. Use language that appeals to the luxury car buyer;
FORMAT: Present the result in the following order: (CAR DESCRIPTION), (BENEFITS), (IDEAL USE CASE);
CAR DESCRIPTION: describe the car model in 5 sentences;
BENEFITS: describe in 3 sentences why this car model is perfect considering the customer's preferred features and budget;
IDEAL USE CASE: write a story in 5 sentences, about how this car fits into the customer's lifestyle, considering their budget and preferred features;
"""

prompt_template = PromptTemplate(
    input_variables=["features", "budget", "content"],
    template=template,
)

def get_api_key():
    """Küsib OpenAI API võtit, kui see pole keskkonnamuutujana määratud."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:  # Kui keskkonnamuutujas võtit pole, küsi kasutajalt
        openai_api_key = st.text_input("OpenAI API Key", "", type="password", help="Enter your OpenAI API key here if not set as an environment variable.")
    return openai_api_key

def load_llm(openai_api_key):
    return OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)

st.set_page_config(page_title="Luxury Car Tailored Content", page_icon=":car:")
st.header("Personalized Car Description Converter")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    **Purpose:** Personalize car descriptions for each customer; output text is customized based on the customer's a) preferred features and b) budget; the input text is a neutral car model description.
    
    **Instructions:** 
    1) Prepare the car model description (input text).
    2) Determine customer preferences based on combinations of preferred features and budget.
    3) Enter the info in the app's UI, then send it.
    4) Copy the app's output text for the car model description page.
    """)

with col2:
    st.image("luxurycarlogo.jpg.webp", caption='Exquisite Vehicles for Discerning Buyers')

openai_api_key = get_api_key()

if openai_api_key:
    features_input = st.multiselect("Preferred Features", ['Speed', 'Design', 'Comfort', 'Latest Technology', 'Eco-friendly'], key="features_input")
    budget_input = st.selectbox("Budget", ('< 100k €', '100k-200k €', '> 200k €'), key="budget_input")
    car_description_input = st.text_area("Car Model Description", "", key="car_description_input", help="Enter the car model description here.")

    if st.button("Generate Description"):
        if len(car_description_input.split(" ")) > 700:
            st.warning("Please enter content with fewer than 700 words.")
        else:
            llm = load_llm(openai_api_key)
            prompt_with_content = prompt_template.format(features=",".join(features_input), budget=budget_input, content=car_description_input)
            formatted_content = llm(prompt_with_content, max_tokens=1024) 
            st.write(formatted_content)
else:
    st.warning('Please enter an OpenAI API Key to proceed.')


