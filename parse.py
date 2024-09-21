from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Follow these instructions carefully please: \n\n"
    "1. **Extract Information:** Only extract relevant information that matches the parse description: {parse_description}."
    "2. **No Extra Information:** Do not include any additional explainations, comments or any unrelated text to your response."
    "3. **Empty Message:** If no information matches the description, return an empty string ('')."
    "4. **Requested Information:** Your output must only include explicitly requested data, with no other additional text."
)

model = OllamaLLM(model="llama3")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start = 1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description" : parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)