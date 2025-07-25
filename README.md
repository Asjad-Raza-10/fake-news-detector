# 🧠 Fake News Detector 📰  
A smart, multi-layered fake news detection system powered by Machine Learning and contextual API validation.

## 🚀 Overview  
This project tackles one of the biggest digital challenges of our era: **detecting fake news**. Traditional machine learning models, no matter how accurate, struggle with context and authenticity — two things vital to validate news in the real world.

That’s why this system goes beyond model predictions by combining them with **six powerful APIs** that cross-verify content validity in real time.

---

## 🎯 Intuition & Problem Statement  
While ML models can be trained to classify news as "real" or "fake" based on language patterns, such predictions often fall short due to:
- Lack of **real-time verification**
- Inability to understand **context** (e.g., satire vs. misinformation)
- Varying **writing styles** and **sources**

To overcome this, I built a **hybrid approach** that:
1. Predicts the nature of news using a trained logistic regression model.
2. **Validates the content through real-world news and fact-check APIs.**

---

## 🧠 Machine Learning Model  

- **Algorithm**: Logistic Regression  
- **Dataset**: [Fake and Real News Dataset (Kaggle)](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset)  
- **Size**: Over 50,000 labeled news articles  
- **Training Platform**: Google Colab  
- **Accuracy**: ~98% on validation set

---

## 🔗 Real-Time API Integration  

Since the model can't fully capture **news context, credibility of the source**, or **timeliness**, I incorporated **6 external APIs** to boost decision-making accuracy:

1. **Google Fact Check API**  
2. **GNews API**  
3. **NewsAPI.org**  
4. **OpenAI GPT API**  
5. **TextRazor API**  
6. **Aylien News API**  

These help:
- Verify if the news exists on reputable platforms
- Fetch similar news from reliable outlets
- Perform real-time fact checking
- Detect language, topics, and sentiment

---

## 💻 Web App  

- **Framework**: [Streamlit](https://streamlit.io)  
- **Frontend Styling**:  
  - Custom CSS via `st.markdown`  
  - Status indicators with colored boxes (red for fake, green for real)  
  - Dynamic intermediate feedback while analyzing  
- **Backend**:
  - Python-based logic combining model + API calls  
  - Shell script (`run_app.sh`) for local deployment

### ✨ UI Highlights:
- Smooth animations for loading and transitions  
- Justification messages based on both model and API findings  
- Input box repositioned for better user experience

---

## 🧪 Testing & Evaluation  
- Ongoing manual testing on **breaking news from various sources**
- Evaluating **API effectiveness + model synergy**
- Planning to publish detailed accuracy benchmarks soon

---

## 📦 Tech Stack

- **Python** (Scikit-learn, Pandas, Requests)
- **Streamlit** (for UI)
- **Google Colab** (model training)
- **Git + GitHub** (version control)
- **APIs** (OpenAI, GNews, etc.)
- **dotenv** (for managing API keys)

---

## 🎯 Future Enhancements

- Add **user login** and **prediction history**
- Support for **multiple languages**
- Integration with **browser extensions** for instant fact-check
- Deploy to **Streamlit Cloud / Hugging Face Spaces**

---

## 🙌 Credits

- Dataset from Kaggle  
- APIs by OpenAI, Google, GNews, TextRazor, and Aylien  
- Logo/icon inspirations from [Flaticon](https://www.flaticon.com/)

---

## 🤝 Let's Connect!

If you’re passionate about AI, ML, or tackling misinformation — feel free to reach out or fork the repo. Let’s build smart, responsible tech together! 🚀

---

**Built with 💡 by Asjad Raza**
