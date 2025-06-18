# 🛍️ Smart Q/A Chatbot for E-Commerce Product Assistance

An intelligent chatbot built with **Python (Flask)** and **Gemini API**, designed to assist users in querying and exploring e-commerce products. Styled using **Tailwind CSS**, this chatbot supports category-based recommendations and product details like specs, pricing, and links.

---

## 💡 Features

- 💬 Smart chatbot using **Gemini API**
- 📦 Detailed product info (name, price, specs, availability)
- 🔗 Clickable product links with placeholders
- 🤖 Intelligent product recommendations
- 🌙 Dark-themed UI built using **Tailwind CSS**
- 🔁 Auto-suggests related products with dynamic linking

---

## 🛠️ Technologies Used

| Frontend         | Backend       | AI API      | Database (Optional) |
|------------------|---------------|-------------|----------------------|
| HTML, Tailwind CSS | Python (Flask) | Gemini (Google AI) | JSON (for product data) |

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ecommerce-chatbot.git
   cd ecommerce-chatbot
2. **Install the required dependencies**
   
   Make sure you have Python installed (preferably Python 3.7+).Install Flask and other required packages using:
   ```bash
   pip install flask requests
3. **Set your Gemini API Key**

   Open the app.py file and replace the placeholder API key with your own:
   ```python
   API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"
4. **Run the Flask application**
   ```bash
   python app.py
5. **Access the chatbot in your browser**
   
   Once the server is running, open:
   ```arduino
   http://localhost:5000/
---

## 📁 Project Structure
```csharp
ecommerce-chatbot/
├── templates/
│   └── index.html        # Frontend UI (chat page with Tailwind)
├── static/               # (Optional) for future CSS/JS
├── app.py                # Flask backend + chatbot logic
├── README.md             # Project documentation

