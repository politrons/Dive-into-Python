from llama_cpp import Llama

# Load the model (make sure the path is correct!)
llm = Llama(model_path="models/meta-llama-3.1-8b-instruct-q4_0.gguf")

# Example prompt
prompt = "what is the meaning of life?"

# Run the model
output = llm(prompt, max_tokens=100)

# Print the response
response = output["choices"][0]["text"].strip()
print(response)

output = llm(response, max_tokens=100)

response = output["choices"][0]["text"].strip()

print(response)







