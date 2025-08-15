from transformers import pipeline

def ask(prompt):
    generator = pipeline( model="gpt2")
    result = generator(prompt, max_length=50, num_return_sequences=1)
    print(result[0]["generated_text"])

if __name__ == '__main__':
    ask("what version of model are you?")