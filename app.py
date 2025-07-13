import streamlit as st
from datetime import datetime
from typing import Dict

# Import custom modules
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from helpers.langchain_helper import LangChainHelper
from helpers.ui_helper import UIHelper
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT, SIDEBAR_STATE, SUPPORTED_FORMATS, MODEL_CONTEXT_LENGTH


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)


class AIResearchAssistant:

    def __init__(self):
        self.ui_helper = UIHelper()
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStoreManager()
        self.langchain_helper = LangChainHelper()
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        if 'current_document' not in st.session_state:
            st.session_state.current_document = None
        if 'qa_history' not in st.session_state:
            st.session_state.qa_history = []
        if 'generated_questions' not in st.session_state:
            st.session_state.generated_questions = []
        if 'challenge_mode' not in st.session_state:
            st.session_state.challenge_mode = False

    def render_header(self):
        """Render application header with modern design."""
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #1f77b4; font-size: 3rem; margin-bottom: 0;'>
                🔬 AI Research Assistant by Suryansh
            </h1>
            <p style='color: #666; font-size: 1.2rem; margin-top: 0.5rem;'>
                Intelligent Document Analysis with Local LLaMA Integration
            </p>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render sidebar with document management."""
        with st.sidebar:
            st.markdown("### 📁 Document Management")

            # File upload section
            uploaded_files = st.file_uploader(
                "Upload Documents",
                type=SUPPORTED_FORMATS,
                accept_multiple_files=True,
                help=f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            )

            if uploaded_files:
                if st.button("📊 Process Documents", type="primary"):
                    self.process_uploaded_files(uploaded_files)

            # Document list
            if st.session_state.documents:
                st.markdown("### 📚 Processed Documents")
                for idx, doc in enumerate(st.session_state.documents):
                    with st.expander(f"📄 {doc['metadata']['filename']}"):
                        st.write(f"**Size:** {doc['metadata']['file_size']:,} bytes")
                        st.write(f"**Type:** {doc['metadata']['file_type'].upper()}")
                        st.write(f"**Chunks:** {doc['metadata']['total_chunks']}")
                        st.write(f"**Words:** {doc['metadata']['word_count']:,}")

                        if st.button(f"Select", key=f"select_{idx}"):
                            st.session_state.current_document = doc
                            st.rerun()

            # Model information
            st.markdown("### 🤖 Model Information")
            st.info(f"""
            **Model:** LLaMA-2-7B-Chat
            **Format:** GGUF (Quantized)
            **Context:** {MODEL_CONTEXT_LENGTH:,} tokens
            **Status:** Ready
            """)

    def process_uploaded_files(self, uploaded_files):
        """Process uploaded files and update session state."""
        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, uploaded_file in enumerate(uploaded_files):
            progress = (idx + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing {uploaded_file.name}...")

            # Process document
            result = self.document_processor.process_document(uploaded_file)

            if result["success"]:
                # Store in vector database
                chunks = result["content"]["chunks"]
                metadata = result["content"]["metadata"]

                # Create embeddings and store
                doc_id = self.vector_store.add_document(chunks, metadata)

                # Add to session state
                document_data = {
                    "id": doc_id,
                    "metadata": metadata,
                    "summary": result["content"]["summary"],
                    "raw_text": result["content"]["raw_text"]
                }

                st.session_state.documents.append(document_data)
                st.success(f"✅ {uploaded_file.name} processed successfully!")
            else:
                st.error(f"❌ Failed to process {uploaded_file.name}: {result['message']}")

        progress_bar.empty()
        status_text.empty()

    def render_main_content(self):
        """Render main content area."""
        if not st.session_state.current_document:
            self.render_welcome_screen()
        else:
            self.render_document_interface()

    def render_welcome_screen(self):
        """Render welcome screen when no document is selected."""
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 3rem 0;'>
                <h2 style='color: #333;'>Welcome to AI Research Assistant devloped by Suryansh Gupta</h2>
                <p style='font-size: 1.1rem; color: #666; margin: 2rem 0;'>
                    Upload documents to begin intelligent analysis with your local LLaMA model.
                </p>

                <div style='background: #f8f9fa; padding: 2rem; border-radius: 10px; margin: 2rem 0;'>
                    <h3 style='color: #1f77b4; margin-bottom: 1rem;'>Features</h3>
                    <div style='text-align: left;'>
                        <p>🔍 <strong>Ask Anything:</strong> Intelligent Q&A with document citations</p>
                        <p>🎯 <strong>Challenge Me:</strong> AI-generated questions for self-assessment</p>
                        <p>📊 <strong>Auto Summary:</strong> Instant document summarization</p>
                        <p>🔒 <strong>Privacy First:</strong> Everything runs locally on your machine</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def render_document_interface(self):
        """Render document analysis interface."""
        doc = st.session_state.current_document

        # Document header
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #1f77b4, #17a2b8); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h2 style='color: white; margin: 0;'>📄 {doc['metadata']['filename']}</h2>
            <p style='color: #e3f2fd; margin: 0.5rem 0 0 0;'>
                {doc['metadata']['word_count']:,} words • {doc['metadata']['total_chunks']} chunks
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Document summary
        with st.expander("📋 Document Summary", expanded=True):
            st.write(doc['summary'])

        # Mode selection
        mode = st.selectbox(
            "🎛️ Select Mode",
            ["Ask Anything", "Challenge Me"],
            help="Choose how you want to interact with the document"
        )

        if mode == "Ask Anything":
            self.render_qa_mode()
        else:
            self.render_challenge_mode()

    def render_qa_mode(self):
        """Render Q&A mode interface."""
        st.markdown("### 💬 Ask Questions About Your Document")

        # Question input
        question = st.text_input(
            "Your Question:",
            placeholder="What is the main topic of this document?",
            help="Ask any question about the uploaded document"
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🔍 Get Answer", type="primary")

        if ask_button and question:
            with st.spinner("Analyzing document and generating response..."):
                # Query vector store
                retriever = self.vector_store.get_retriever()
                qa_chain = self.langchain_helper.create_qa_chain(
                    self.vector_store.get_vectorstore()
                )

                try:
                    result = qa_chain({"query": question})
                    answer = result["result"]
                    source_docs = result["source_documents"]

                    # Display answer
                    st.markdown("#### 📝 Answer")
                    st.write(answer)

                    # Display sources
                    with st.expander("📚 Source References"):
                        for idx, doc in enumerate(source_docs):
                            st.markdown(f"**Source {idx + 1}:**")
                            st.write(f"*{doc.page_content[:300]}...*")
                            st.markdown("---")

                    # Add to history
                    st.session_state.qa_history.append({
                        "question": question,
                        "answer": answer,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "sources": len(source_docs)
                    })

                except Exception as e:
                    st.error(f"Error generating response: {e}")

        # Q&A History
        if st.session_state.qa_history:
            with st.expander("📚 Q&A History"):
                for idx, qa in enumerate(reversed(st.session_state.qa_history[-5:])):
                    st.markdown(f"**Q{len(st.session_state.qa_history) - idx}:** {qa['question']}")
                    st.write(f"**A:** {qa['answer'][:200]}...")
                    st.caption(f"🕒 {qa['timestamp']} • 📄 {qa['sources']} sources")
                    st.markdown("---")

    def render_challenge_mode(self):
        """Render Challenge Me mode interface."""
        st.markdown("### 🎯 Challenge Me Mode")
        st.info("Test your understanding with AI-generated questions!")

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🎲 Generate Questions", type="primary"):
                self.generate_challenge_questions()

        with col2:
            difficulty = st.selectbox(
                "Difficulty Level:",
                ["Mixed", "Easy", "Medium", "Hard"]
            )

        # Display generated questions
        if st.session_state.generated_questions:
            for idx, q_data in enumerate(st.session_state.generated_questions):
                with st.container():
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                                border-left: 4px solid #1f77b4;'>
                        <h4 style='color: #1f77b4; margin-bottom: 1rem;'>
                            Question {idx + 1} ({q_data['type'].title()})
                        </h4>
                        <p style='font-size: 1.1rem; margin-bottom: 1rem;'>{q_data['question']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Answer input
                    user_answer = st.text_area(
                        f"Your Answer for Question {idx + 1}:",
                        key=f"answer_{idx}",
                        height=100
                    )

                    if st.button(f"📊 Evaluate Answer {idx + 1}", key=f"eval_{idx}"):
                        if user_answer.strip():
                            self.evaluate_user_answer(q_data, user_answer, idx)
                        else:
                            st.warning("Please provide an answer before evaluation.")

    def generate_challenge_questions(self):
        """Generate challenge questions from current document."""
        doc = st.session_state.current_document

        with st.spinner("Generating challenging questions..."):
            # Use sample text from document
            sample_text = doc['raw_text'][:3000]  # Limit for efficiency

            try:
                questions = self.langchain_helper.generate_questions(
                    context=sample_text,
                    question_type="mixed"
                )

                st.session_state.generated_questions = questions
                st.success(f"✅ Generated {len(questions)} questions!")

            except Exception as e:
                st.error(f"Failed to generate questions: {e}")

    def evaluate_user_answer(self, question_data: Dict, user_answer: str, question_idx: int):
        """Evaluate user's answer and provide feedback."""
        doc = st.session_state.current_document

        with st.spinner("Evaluating your answer..."):
            try:
                evaluation = self.langchain_helper.evaluate_answer(
                    question=question_data['question'],
                    user_answer=user_answer,
                    context=question_data['source_context']
                )

                # Display evaluation results
                col1, col2 = st.columns([1, 2])

                with col1:
                    score = evaluation['score']
                    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 4 else "#dc3545"

                    st.markdown(f"""
                    <div style='text-align: center; padding: 1rem; background: {score_color}; 
                                color: white; border-radius: 10px;'>
                        <h2 style='margin: 0;'>{score}/10</h2>
                        <p style='margin: 0; opacity: 0.9;'>Score</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown("**📝 Feedback:**")
                    st.write(evaluation['feedback'])

                    if evaluation.get('strengths'):
                        st.markdown("**✅ Strengths:**")
                        for strength in evaluation['strengths']:
                            st.write(f"• {strength}")

                    if evaluation.get('improvements'):
                        st.markdown("**🎯 Areas for Improvement:**")
                        for improvement in evaluation['improvements']:
                            st.write(f"• {improvement}")

            except Exception as e:
                st.error(f"Evaluation failed: {e}")

    def run(self):
        """Main application entry point."""
        # Load custom CSS
        self.ui_helper.load_custom_css()

        # Render UI components
        self.render_header()
        self.render_sidebar()
        self.render_main_content()

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>🔬 AI Research Assistant | Powered by Local LLaMA-2 | Built with Streamlit</p>
        </div>
        """, unsafe_allow_html=True)


# Application entry point
def main():
    app = AIResearchAssistant()
    app.run()


if __name__ == "__main__":
    main()
