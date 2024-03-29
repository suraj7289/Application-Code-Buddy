# Application Code Buddy: Your AI-powered Code Assistant

Application Code Buddy is a software application designed to assist developers with various tasks related to understanding and maintaining their codebase. It leverages the power of artificial intelligence (AI) and natural language processing (NLP) to provide functionalities such as:

- Detailed code summaries: Get a concise overview of the application's functionality.
- Code refactoring and cleanup suggestions: Identify potential improvements to enhance code quality and maintainability.
- Code reusability recommendations: Discover opportunities to reuse existing code within the application.
- Test case generation: Generate automated test cases based on the code's logic.
- Answering questions about the code: Ask questions about the code and receive informative answers derived from code analysis and documentation.
Features:

Agent-based architecture: Utilizes a central agent that coordinates various custom tools for efficient processing.
Chunking and embedding: Splits code into smaller chunks and generates vector representations for similarity search.
Similarity search engine: Locates relevant documentation based on code similarity.
Large Language Model (LLM): I have used Google Gemini Model (you can have your own LLM and related keys) in .env file for response generation.
Streamlit UI: User-friendly interface for uploading code zip files and interacting with the application.
Getting Started:

# Prerequisites:

Python 3.x
Required libraries (listed in requirements.txt)
Installation:

Clone this repository:

Bash
git clone https://github.com/suraj7289/Application-Code-Buddy.git

Navigate to the project directory:

Bash
cd application-code-buddy

# Install dependencies:

pip install -r requirements.txt

# Run the application:

streamlit run app.py

Upload your application code as a ZIP file and start chatting with the Code Buddy.

The application will analyze your code and respond with relevant information.

# Custom Prompts:

Separate prompt files are provided for each custom tool and the agent. These files can be customized to tailor the behavior of the application to your specific needs.

# Disclaimer:

This application is still under development and may not be suitable for production use. We encourage you to use it for educational and experimental purposes only.
