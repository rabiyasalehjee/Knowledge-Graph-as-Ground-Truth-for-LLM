import subprocess
import logging

# Configure logging
logging.basicConfig(filename='llama_kg.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def generate_response(prompt):
    try:
        # Save the prompt to a temporary file
        with open('prompt.txt', 'w') as file:
            file.write(prompt)
        logging.info("Prompt saved to prompt.txt successfully.")
        
        # Prepare the command to load the model and input the prompt
        command = f"""
        /usr/local/bin/ollama run llama3.1:8b << EOF
        {prompt}
        EOF
        """
        logging.info("Running Ollama with the specified command.")
        
        # Execute the command
        response = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Process the output as plain text
        generated_text = response.stdout.strip()
        logging.info("Ollama response received successfully.")
        
        return generated_text

    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running Ollama: {e}")
        logging.error(f"Output: {e.output}")
        raise

# Example knowledge graph triples converted to natural language statements
knowledge_graph = [
    ("1/1/2015", "FLIGHT_DATE", "Qantas Airways"),
    ("Qantas Airways", "OPERATES_FROM", "Brisbane"),
    ("Qantas Airways", "OPERATES_TO", "Auckland"),
    ("Qantas Airways", "ALL_OPERATED_FLIGHTS", "12"),
    ("1/1/2015", "HAS_RELATION", "12"),
    ("1/1/2015", "HAS_RELATION", "Brisbane"),
    ("1/1/2015", "HAS_RELATION", "Auckland")
]

# Convert triples to natural language statements
kg_statements = [f"{head} {relation.replace('_', ' ').lower()} {tail}." for head, relation, tail in knowledge_graph]

# Few-shot examples to guide the model, including their own KGs
few_shot_examples = """
The following are facts from a knowledge graph:
1. Paris is the capital of France.
2. The Eiffel Tower is located in Paris.

Input statement 1: Paris is the capital of France.
Input statement 2: The Eiffel Tower is located in Paris.
Are the values in both input statements related to each other based on the knowledge graph context? Answer only 'yes' or 'no'.
Answer: yes

The following are facts from a knowledge graph:
1. Albert Einstein discovered the theory of relativity.
2. The Great Wall of China is a historic fortification in China.

Input statement 1: Albert Einstein discovered the theory of relativity.
Input statement 2: The Great Wall of China is a historic fortification in China.
Are the values in both input statements related to each other based on the knowledge graph context? Answer only 'yes' or 'no'.
Answer: no
"""

# Inputs to be checked
input_statement1 = "Given the Date '1/1/2015' and the related Airline 'Qantas Airways'."
input_statement2 = "Given the Date '1/1/2015' and the related AllFlights '12'."

# Function to retrieve top-k relevant statements from the knowledge graph
def retrieve_top_k_statements(input_statements, knowledge_graph, k=4):
    relevant_statements = []
    for input_statement in input_statements:
        for head, relation, tail in knowledge_graph:
            if head in input_statement or tail in input_statement:
                statement = (head, relation, tail)
                if statement not in relevant_statements:
                    relevant_statements.append(statement)
                    if len(relevant_statements) == k:
                        break
        if len(relevant_statements) == k:
            break
    return relevant_statements

# Retrieve top-k relevant statements for both input statements
top_k_statements = retrieve_top_k_statements([input_statement1, input_statement2], knowledge_graph)

# Convert top-k statements to natural language
top_k_statements_text = "\n".join([f"{head} {relation.replace('_', ' ').lower()} {tail}." for head, relation, tail in top_k_statements])

# Combine the few-shot examples, top-k prompt, and the input statements for the LLM
final_prompt = f"""
You are a capable language model. Your task is to determine if two input statements are related to each other based on a given knowledge graph.

A knowledge graph is a collection of interconnected entities and their relationships, represented in the form of triples (head, relation, tail). Each triple indicates a relationship between two entities.

Here are some examples to guide you:

{few_shot_examples}

Now, consider the following top-k relevant statements from the knowledge graph:
{top_k_statements_text}

Input statement 1: {input_statement1}
Input statement 2: {input_statement2}

Are the values in both input statements related to each other based on the knowledge graph context? Answer only 'yes' or 'no'.
Answer: 
"""

# Generate the response
response = generate_response(final_prompt)

# Print the complete prompt and the final response
print(f"""
Complete Prompt:
{final_prompt}

Final Response:
{response}
""")
