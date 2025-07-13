from langchain_community.llms import LlamaCpp
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict
import logging
from langchain_community.llms import LlamaCpp
from config.prompts import (
    SUMMARY_PROMPT_TEMPLATE, QA_PROMPT_TEMPLATE,
    QUESTION_GENERATION_TEMPLATES, EVALUATION_PROMPT_TEMPLATE
)
from config.settings import AUTO_SUMMARY_MAX_WORDS, QUESTION_TYPES
from config.settings import MODEL_PATH, MODEL_CONTEXT_LENGTH, MODEL_TEMPERATURE, MODEL_MAX_TOKENS, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP





class LangChainHelper:
    """Advanced LangChain integration helper for local LLaMA operations."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.llm = None
        self.embeddings = None
        self.text_splitter = None
        self._initialize_components()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def _initialize_components(self):
        """Initialize LangChain components."""
        try:
            # Initialize LLaMA model
            self.llm = LlamaCpp(
                model_path=MODEL_PATH,
                n_ctx=MODEL_CONTEXT_LENGTH,
                n_batch=512,
                n_threads=8,
                f16_kv=True,
                verbose=False,
                temperature=MODEL_TEMPERATURE,
                max_tokens=MODEL_MAX_TOKENS,
                top_p=0.95,
                repeat_penalty=1.1
            )

            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )

            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )

            self.logger.info("LangChain components initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize LangChain components: {e}")
            raise

    def generate_summary(self, text: str) -> str:
        """Generate document summary using LLaMA."""
        prompt = PromptTemplate(
            template=SUMMARY_PROMPT_TEMPLATE,
            input_variables=["text", "max_words"]
        )

        formatted_prompt = prompt.format(
            text=text[:3000],  # Limit input for efficiency
            max_words=AUTO_SUMMARY_MAX_WORDS
        )

        try:
            summary = self.llm(formatted_prompt)
            return summary.strip()
        except Exception as e:
            self.logger.error(f"Summary generation failed: {e}")
            return "Summary generation unavailable."

    def create_qa_chain(self, vectorstore) -> RetrievalQA:
        """Create Question-Answering chain with retrieval."""
        qa_prompt = PromptTemplate(
            template=QA_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            chain_type_kwargs={
                "prompt": qa_prompt,
                "verbose": True
            },
            return_source_documents=True
        )

    def generate_questions(self, context: str, question_type: str = "mixed") -> List[Dict]:
        """Generate questions from context using advanced NLP techniques."""
        if question_type == "mixed":
            questions = []
            for q_type in QUESTION_TYPES:
                prompt = PromptTemplate(
                    template=QUESTION_GENERATION_TEMPLATES[q_type],
                    input_variables=["context"]
                )

                formatted_prompt = prompt.format(context=context[:2000])

                try:
                    response = self.llm(formatted_prompt)
                    questions.append({
                        "type": q_type,
                        "question": response.strip(),
                        "difficulty": self._assess_difficulty(response),
                        "source_context": context[:500]
                    })
                except Exception as e:
                    self.logger.error(f"Question generation failed for {q_type}: {e}")

            return questions
        else:
            # Single question type generation
            prompt = PromptTemplate(
                template=QUESTION_GENERATION_TEMPLATES[question_type],
                input_variables=["context"]
            )

            formatted_prompt = prompt.format(context=context[:2000])
            response = self.llm(formatted_prompt)

            return [{
                "type": question_type,
                "question": response.strip(),
                "difficulty": self._assess_difficulty(response),
                "source_context": context[:500]
            }]

    def evaluate_answer(self, question: str, user_answer: str, context: str) -> Dict:
        """Evaluate user's answer using multiple criteria."""
        prompt = PromptTemplate(
            template=EVALUATION_PROMPT_TEMPLATE,
            input_variables=["question", "user_answer", "context"]
        )

        formatted_prompt = prompt.format(
            question=question,
            user_answer=user_answer,
            context=context
        )

        try:
            evaluation = self.llm(formatted_prompt)
            return self._parse_evaluation(evaluation)
        except Exception as e:
            self.logger.error(f"Answer evaluation failed: {e}")
            return {
                "score": 0,
                "feedback": "Evaluation temporarily unavailable.",
                "strengths": [],
                "improvements": []
            }

    def _assess_difficulty(self, question: str) -> str:
        """Assess question difficulty level."""
        # Simple heuristic based on question complexity
        word_count = len(question.split())
        if word_count < 10:
            return "Easy"
        elif word_count < 20:
            return "Medium"
        else:
            return "Hard"

    def _parse_evaluation(self, evaluation_text: str) -> Dict:
        """Parse LLM evaluation response into structured format."""
        # Advanced parsing logic for evaluation response
        lines = evaluation_text.strip().split('\n')
        result = {
            "score": 7,  # Default score
            "feedback": evaluation_text[:200],
            "strengths": [],
            "improvements": []
        }

        # Extract score if mentioned
        for line in lines:
            if "score" in line.lower() or "rating" in line.lower():
                try:
                    import re
                    score_match = re.search(r'(\d+)', line)
                    if score_match:
                        result["score"] = min(int(score_match.group(1)), 10)
                except:
                    pass

        return result
