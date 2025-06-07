from flask import Flask, render_template, request, jsonify, session
from src.helper import download_huggingface_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt  
from src.chat_history import save_message
from src.openrouter_llm import OpenRouterLLM
import json
import os


app = Flask(__name__)
load_dotenv()

# Load API keys from environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Ensure required keys are set
if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in environment.")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in environment.")
if not app.secret_key:
    raise ValueError("Missing FLASK_SECRET_KEY in environment.")


# Load embeddings and vector index
embeddings = download_huggingface_embeddings()
index_name = "askmedi"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize LLM and chain
llm = OpenRouterLLM()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/history')
def history():
    try:
        with open("chat_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    return jsonify(history)


@app.route('/get', methods=["GET", "POST"])
def chat():
    msg = request.form.get('msg', '').strip()
    if not msg:
        return "Please enter a question.", 400

    # Initialize session history
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Save user message
    session['chat_history'].append({"role": "user", "content": msg})

    # Optional: limit session memory to last 10 messages
    MAX_HISTORY = 10
    if len(session['chat_history']) > MAX_HISTORY:
        session['chat_history'] = session['chat_history'][-MAX_HISTORY:]

    # Build context from history
    conversation = ""
    for entry in session['chat_history']:
        prefix = "User: " if entry["role"] == "user" else "Bot: "
        conversation += prefix + entry["content"] + "\n"

    try:
        # Get response from RAG chain
        response = rag_chain.invoke({"input": conversation})
        answer = response.get("answer", "Sorry, no answer was returned.")

        # Save bot response
        session['chat_history'].append({"role": "assistant", "content": answer})

        save_message("user", msg, is_bot=False)
        save_message("bot", answer, is_bot=True)

        return str(answer)
    except Exception as e:
        print("Error:", str(e))
        return "Sorry, something went wrong.", 500


@app.route('/clear_history', methods=["POST"])
def clear_history():
    with open("chat_history.json", "w") as f:
        json.dump([], f)
    session.pop('chat_history', None)
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
