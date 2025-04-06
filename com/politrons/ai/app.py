from llama_cpp import Llama

# Load the model (make sure the path is correct!)
llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf")

# Example prompt
prompt = "What is the best movie of all times."

# Run the model
output = llm(prompt, max_tokens=100)

# Print the response
print(output["choices"][0]["text"].strip())





