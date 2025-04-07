from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama

app = Flask(__name__)

# Load your model from here https://huggingface.co/ggml-org/Meta-Llama-3.1-8B-Instruct-Q4_0-GGUF/tree/main
llm = Llama(model_path="models/meta-llama-3.1-8b-instruct-q4_0.gguf")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('prompt', '')
    # Run the model with your prompt
    output = llm(prompt, max_tokens=100)
    response = output["choices"][0]["text"].strip()
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
