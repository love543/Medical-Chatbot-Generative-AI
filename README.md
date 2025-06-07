# 🩺 Medical-Chatbot-Generative-AI
A conversational RAG-based AI chatbot for answering medical queries using LangChain, Pinecone, Flask, and OpenRouter (OpenAI-compatible API).  
It retrieves relevant information from documents and generates contextual answers using GPT.

---

# 🚀 How to run?
## STEPS:

### ✅ Step 01: Clone the repository

```bash
git clone https://github.com/love543/Medical-Chatbot-Generative-AI.git
cd Medical-Chatbot-Generative-AI
```

### ✅ STEP 02- Create a conda environment after opening the repository

```bash 
conda create -n AskMedi python=3.10 -y
```

```bash
conda activate AskMedi
```

### ✅ STEP 03- install the requirements
```bash
pip install -r requirements.txt
``` 


### ✅ STEP 04- Add API Keys
Create a `.env` file in the root directory and add your Pincone & OpenAI credentials as follows:


```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
FLASK_SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### ✅ STEP 05- Store Embeddings to Pinecone
```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

### ✅ STEP 06- Run the Application

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:8080 
```

### 📹 Demo Video
https://drive.google.com/file/d/1Or4onJnVKWhnFrJx9GrXLrKaddn156k8/view?usp=sharing


### 🖼️ Screenshots
![Screenshot 2025-06-07 183207](https://github.com/user-attachments/assets/5901acf7-de4d-4aea-b264-44a0af6ef65b)


### Techstack Used:

- 🐍 Python 3.10
- 🧠 LangChain
- 🌐 Flask
- 🧬 HuggingFace Transformers
- 🔥 OpenRouter (GPT Compatible)
- 🌲 Pinecone Vector DB


### 💡 Features
- Contextual answering with RAG (Retrieval-Augmented Generation)

- Session-based memory using Flask

- Semantic document search using Pinecone

- Clean UI and chat history support

- Easily extendable for medical documents or other domains


### 🛠️ Requirements
- Python 3.10+
- Conda or venv
- Pinecone account & index
- OpenRouter API key

### 📬 Contributing
Contributions are welcome!
Feel free to fork the repo, create a branch, and submit a pull request.


### 🛡️ License
This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for more details.
