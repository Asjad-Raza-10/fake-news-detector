import streamlit as st
import pickle
import sklearn

# Load the model
with open("../model/fake_news_model.pkl", "rb") as file:
    model = pickle.load(file)

# Streamlit UI
st.title("📰 Fake News Detector")
st.markdown("_Trained on US news data. Results may vary for other regions._")

# Input from user
news_input = st.text_area("Enter a news headline or article text:", height=200)

if st.button("Check if it's Real or Fake"):
    if news_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        prediction = model.predict([news_input])
        label = "✅ Real News" if prediction[0] == 1 else "❌ Fake News"
        st.subheader(f"Prediction: {label}")
