# GitHub Repository Explainer

A lightweight Streamlit web application that analyzes a GitHub repository and generates a structured explanation of its codebase using an LLM hosted through Groq.

The application accepts a public GitHub repository URL, clones the repository temporarily, collects relevant source files, and sends the extracted code to an AI model. The generated response is organized into a project overview, main technologies, and an explanation of how the project works.

## Features

- Enter a GitHub repository URL through a simple Streamlit interface.
- Clone and inspect a repository automatically.
- Read common source and configuration files including:
  - `.py`
  - `.js`
  - `.jsx`
  - `.html`
  - `.css`
  - `.md`
  - `.json`
- Ignore the repository's `.git` directory during analysis.
- Combine readable source files into a single code context for the AI model.
- Generate a structured explanation with:
  1. **Project Overview**
  2. **Main Technologies**
  3. **How it works**
- Uses Groq for fast LLM inference.
- Includes a Dev Container configuration for development in GitHub Codespaces or compatible VS Code environments.

## How It Works

The application follows a simple pipeline:

```text
GitHub Repository URL
        ↓
Clone Repository
        ↓
Find Supported Source Files
        ↓
Read and Combine File Contents
        ↓
Send Code Context to Groq
        ↓
Generate Structured Explanation
        ↓
Display Result in Streamlit
```

The application temporarily clones the repository using GitPython. It then searches through the cloned directory for supported file types and combines their contents into a single code context.

To prevent excessively large prompts, the collected context is limited to approximately 15,000 characters before being sent to the model.

## Tech Stack

- **Python** — Core application language
- **Streamlit** — Web interface
- **GitPython** — Cloning and accessing GitHub repositories
- **Groq** — LLM API and inference
- **OpenAI GPT-OSS 20B** — Model used for repository analysis
- **GitHub** — Source repositories analyzed by the application

## Project Structure

```text
GithubRepoReader/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── app.py
├── requirements.txt
├── README.md
└── __pycache__/
```

### `app.py`

Contains the complete Streamlit application, including:

- GitHub repository cloning
- File discovery and extraction
- Code context preparation
- Groq API integration
- AI prompt construction
- Streamlit UI and result display

### `requirements.txt`

Contains the Python dependencies required by the application:

```text
streamlit
gitpython
groq
```

### `.devcontainer/devcontainer.json`

Provides a Python 3.11 development environment and configures Streamlit to run automatically on port `8501`.

## Getting Started

### Prerequisites

Make sure you have:

- Python 3.9 or later
- Git
- A Groq API key
- Internet access

### 1. Clone the Repository

```bash
git clone https://github.com/sohamsen-exe/GithubRepoReader.git
cd GithubRepoReader
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

The application expects the API key to be provided through Streamlit Secrets.

Create the following file:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Replace `your_groq_api_key_here` with your actual Groq API key.

> Do not commit your `secrets.toml` file or expose your API key publicly.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will start on the default Streamlit port:

```text
http://localhost:8501
```

## Using the Application

Once the application is running:

1. Open the Streamlit application in your browser.
2. Enter the URL of a GitHub repository.
3. Click **Explain Repository**.
4. The application clones the repository and analyzes supported source files.
5. The AI-generated explanation is displayed directly in the application.

Example input:

```text
https://github.com/username/repository
```

## Supported Files

The current implementation analyzes files with the following extensions:

| Extension | Typical Usage |
|---|---|
| `.py` | Python source code |
| `.js` | JavaScript |
| `.jsx` | React components |
| `.html` | HTML |
| `.css` | CSS |
| `.md` | Markdown documentation |
| `.json` | Configuration/data files |

Other file types are currently ignored.

## Development with GitHub Codespaces

The repository includes a Dev Container configuration based on Python 3.11.

The configured environment:

- Uses the Microsoft Python 3.11 Bookworm Dev Container image.
- Installs dependencies from `requirements.txt`.
- Installs Streamlit.
- Starts the Streamlit application automatically.
- Forwards port `8501`.
- Opens the application preview when the port is forwarded.

This makes the project suitable for development through GitHub Codespaces or VS Code Dev Containers.

## Configuration

The main application configuration is handled in `app.py`.

The Groq client is initialized using:

```python
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
```

The application currently uses the following model:

```text
openai/gpt-oss-20b
```

## Limitations

The current implementation has a few practical limitations:

- The application is designed primarily for repositories containing supported text-based source files.
- Only a selected set of file extensions are analyzed.
- The combined repository context is limited to approximately 15,000 characters.
- Very large repositories may therefore have only part of their code analyzed.
- Binary files are not processed.
- The current workflow is designed around repositories that can be cloned successfully through Git.
- The application does not currently provide detailed file-by-file analysis or repository visualizations.

## Possible Improvements

Future versions could include:

- File-by-file AI analysis
- Support for additional programming languages
- Repository architecture diagrams
- Automatic dependency detection
- GitHub repository metadata analysis
- Code complexity and quality analysis
- Downloadable AI-generated reports
- Support for private repositories through GitHub authentication
- Streaming AI responses
- Adjustable context size
- Repository summaries with project recommendations and improvement suggestions

## Security Notes

The application uses a Groq API key through Streamlit Secrets. API keys should never be hard-coded into the source code or committed to GitHub.

Temporary repository data is stored in a temporary directory while the application is processing it and is removed after analysis.

## Author

**Soham Sen**

GitHub: [@sohamsen-exe](https://github.com/sohamsen-exe)

## License

This project is available for personal and educational use. Add a specific open-source license such as MIT if you intend to formally permit redistribution and modification.
