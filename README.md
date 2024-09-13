# Knowledge Graph as Ground Truth for LLM

## Purpose
- This script uses a knowledge graph as ground truth to help a language model (LLM) determine if two input sentences are related.
- The knowledge graph consists of triples (head, relation, tail), representing facts, and is used to ground the LLM's responses in factual data.

## How It Works
- **Knowledge Graph:** A set of hardcoded triples (e.g., ("Qantas Airways", "OPERATES_FROM", "Brisbane")) provides the factual relationships between entities.
- **Few-shot Prompting:** The LLM is guided with examples to understand how to analyze and relate sentences using the knowledge graph. These few-shot examples give the model context and show it how to evaluate relationships between input sentences based on provided facts.
- **Relationship Detection:** The LLM checks if the input sentences refer to related entities based on the knowledge graph, providing a simple "yes" or "no" response with reasoning. The model uses relevant triples from the knowledge graph to support its decision.

## Example Output

- Input statement 1: Given the Date '1/1/2015' and the related Airline 'Qantas Airways'. 
- Input statement 2: Given the Date '1/1/2015' and the related AllFlights '12'.

**Answer: yes**

## Explanation: 
- Both statements share the entity '1/1/2015,' linking them to 'Qantas Airways.'

## Usage of Few-shot Learning and Prompting to Control Hallucinations

The script effectively leverages **few-shot learning** and well-structured prompts to guide the language model (LLM) and minimize hallucinations. Here’s how:

### Few-shot Learning:
- **Few-shot examples** are provided to the LLM to establish context and guide its understanding. These examples show how the LLM should analyze input sentences based on the knowledge graph.
- By giving the model both **positive** (related statements) and **negative** (unrelated statements) examples, we define the expected behavior, helping the LLM to:
  - Correctly identify when two input sentences are related or unrelated.
  - Understand how to draw relationships from the knowledge graph triples.

This approach ensures the LLM provides answers that are fact-based and grounded in the data, reducing the risk of generating unrelated or incorrect information.

### Why It Works:
1. **Few-shot examples** define the task clearly and provide the model with necessary guidance.
2. **Grounding the model in knowledge graph facts** prevents hallucination by ensuring the model relies on factual data.
3. **Structured prompts** with clear, simple outputs help limit model responses to what's required, reducing the chances of irrelevant output.

This method ensures that the LLM’s responses are both accurate and consistent with the provided knowledge graph.
