# config/prompts.py

SUMMARY_PROMPT_TEMPLATE = "Summarize the following text in {max_words} words:\n\n{text}\n"

QA_PROMPT_TEMPLATE = "Use the following context to answer the question.\nContext: {context}\nQuestion: {question}\n"

QUESTION_GENERATION_TEMPLATES = {
    "factual": "Create a factual question based on this context:\n{context}\n",
    "analytical": "Create an analytical question based on this context:\n{context}\n",
    "inferential": "Create an inferential question based on this context:\n{context}\n",
    "evaluative": "Create an evaluative question based on this context:\n{context}\n"
}  # ADD THIS CLOSING BRACE

EVALUATION_PROMPT_TEMPLATE = (
    "Given the question: {question}\n"
    "User's answer: {user_answer}\n"
    "Reference context: {context}\n"
    "Evaluate the answer for accuracy, completeness, and clarity. "
    "Provide a score out of 10, strengths, and areas for improvement."
)
