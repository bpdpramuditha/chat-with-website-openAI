🤖 Ask AT Digital – Chatbot with OpenAI + LangChain + Streamlit
This project is a chatbot application built with Streamlit, LangChain, HuggingFace embeddings, and OpenAI GPT models. It allows users to ask questions about AT Digital’s website, and the chatbot answers using both:
• The website dataset (website_data.json)
• Its own knowledge (via GPT) if context is missing

---

🚀 Features
✅ Uses LangChain to handle embeddings, retrieval, and conversational memory.
✅ HuggingFace Sentence Transformers (all-MiniLM-L6-v2) for text embeddings.
✅ ChromaDB as the vector store for efficient semantic search.
✅ Custom PromptTemplate ensures the bot always tries to help.
✅ OpenAI GPT model (gpt-4o-mini) for generating responses.
✅ Interactive Streamlit UI with chat history.
✅ Environment variables handled with .env (secure API key storage).

---

📂 Project Structure
├── src/
│ ├── app.py # Main Streamlit app
│ ├── website_data.json # Website dataset (scraped/stored in JSON)
├── .env # Environment variables (OPENAI_API_KEY)
├── .gitIgnore # Files to ignore while pushing to Git

---

🛠️ Installation

1. Clone the repository
   https://github.com/bpdpramuditha/chat-with-website-openAI.git
   cd ask-at-digital

2. Create a virtual environment
   Using conda (recommended):
   • conda create -n ask-at-digital python=3.10 -y conda
   • activate ask-at-digital
   Or using venv:
   • python -m venv venv  
   • venv\Scripts\activate # Windows

3. Install dependencies
   pip install -r requirements.txt
4. Setup environment variables
   • Create a .env file in the project root:
   • OPENAI_API_KEY=your_openai_api_key_here
   ⚠️ Replace your_openai_api_key_here with your actual key from OpenAI.

---

📑 Dataset Format
The app uses a JSON dataset (src/website_data.json) with the following structure:
[{"page": "Home", "url": "https://atdigital.io/", "text": "AT Digital provides web development, AI solutions, and digital marketing services to help businesses grow online."},
{ "page": "About Us", "url": "https://atdigital.io/about", "text": "We are a team of developers, designers, and AI specialists committed to delivering innovative digital solutions."},
{"page": "Services - AI/ML", "url": "https://atdigital.io/services/ai-ml", "text": "Our AI/ML services include custom models for automation, predictive analytics, and chatbot integration."},
{"page": "Services - Web Development", "url": "https://atdigital.io/services/web-development", "text": "We build responsive websites using React, Next.js, and headless CMS solutions like Prismic."},
{ "page": "Services - Digital Marketing", "url": "https://atdigital.io/services/digital-marketing", "text": "Our digital marketing services cover SEO, social media campaigns, content creation, and performance analytics."},
{"page": "Blog - SEO Tips", "url": "https://atdigital.io/blog/seo-tips", "text": "Improving website SEO involves optimizing images, metadata, performance, and content for better ranking."},
{"page": "Contact", "url": "https://atdigital.io/contact", "text": "You can reach us via email at contact@atdigital.io or through our contact form on the website."}]

---

▶️ Running the App
Run Streamlit:
streamlit run src/app.py

---

💡 How It Works 1. Load Data
• Reads website_data.json
• Splits content into chunks (500 chars with 50 overlap)
• Embeds chunks with HuggingFace MiniLM model
• Stores in Chroma vector database 2. Conversational Chain
• Uses ConversationalRetrievalChain with OpenAI GPT (gpt-4o-mini)
• Retrieves relevant chunks from vector DB
• Injects context + chat history into a custom prompt 3. User Interaction
• User inputs a question via st.chat_input()
• Chat history is maintained (HumanMessage, AIMessage)
• Responses are displayed in a clean chat format

---

📜 Example Usage

1. Start the app with streamlit run src/app.py
2. Ask (User):
   What services does AT Digital provide?
   Bot:
   AT Digital provides a range of services including web development, AI solutions, and digital marketing. Our digital marketing services encompass SEO, social media campaigns, content creation, and performance analytics. We have a dedicated team of developers, designers, and AI specialists focused on delivering innovative digital solutions to help businesses grow online. If you have any specific questions about our services, feel free to ask!
3. Continue chatting naturally with context-aware replies.

---

🧰 Requirements
• Python 3.10
• Streamlit
• LangChain
• OpenAI API
• HuggingFace Transformers
• ChromaDB
• python-dotenv

---

🔒 Security Notes
• Do not commit your .env file
• Use .gitignore to exclude secrets
• Always set API keys as environment variables when deploying
