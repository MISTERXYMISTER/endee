# Resume Analyzer

A smart resume analysis and search application built with Streamlit and Endee vector database. Upload resumes, generate embeddings, and search through them using natural language queries.

## Features

- **PDF Resume Parsing**: Extract and process resume content from PDF files
- **Vector Embeddings**: Transform resume text into semantic embeddings using SentenceTransformer
- **Semantic Search**: Query resumes using natural language and find the most relevant matches
- **Vector Database**: Store and manage embeddings efficiently using Endee
- **Interactive UI**: User-friendly Streamlit interface for easy interaction

## Tech Stack

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[PyPDF2](https://pypi.org/project/PyPDF2/)** - PDF text extraction
- **[Sentence Transformers](https://www.sbert.net/)** - Semantic embeddings (all-MiniLM-L6-v2 model)
- **[Endee](https://github.com/endee-ai/endee)** - Vector database for semantic search
- **[Docker](https://www.docker.com/)** - Containerization (optional)

## Prerequisites

- Python 3.8 or higher
- Endee service running (default: `localhost:8080`)

## Installation

### Local Setup

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Endee is running**:
   ```bash
   docker-compose up -d
   ```
   Or ensure you have an Endee instance accessible at `localhost:8080`

### Docker Setup

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

This will start both the Streamlit app and the Endee vector database.

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Basic Workflow

1. **Upload Resumes**: Use the file uploader to select PDF resume files
2. **Process & Index**: The app automatically extracts text and creates embeddings
3. **Search**: Enter natural language queries to find relevant resumes
4. **View Results**: See the top 5 most relevant matches with similarity scores

## Project Structure

```
Resume_analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose configuration
└── README.md             # This file
```

## Key Configuration

- **Index Name**: `resumes`
- **Embedding Dimension**: 384 (MiniLM model output size)
- **Embedding Model**: `all-MiniLM-L6-v2` (lightweight, efficient)
- **Search Method**: Cosine similarity
- **Top Results**: 5 most relevant resumes per query

## API Integration

The app connects to Endee using the Python client:

```python
from endee import Endee

client = Endee("localhost:8080")
index = client.get_index("resumes")
```

## Troubleshooting

### Connection Error to Endee

- Ensure Endee service is running: `docker-compose up -d`
- Check that `localhost:8080` is accessible
- Verify no port conflicts on port 8080

### Embedding Generation Issues

- Ensure sufficient memory for the SentenceTransformer model
- Model will be downloaded on first use (~100MB)

### PDF Processing Issues

- Ensure PDFs are not password-protected
- Check that PDFs contain extractable text (not scanned images)

## Future Enhancements

- Support for multiple file formats (DOCX, TXT)
- Resume quality scoring
- Skill extraction and matching
- Batch upload and processing
- Full-text indexing alongside embeddings
- Advanced filtering and faceted search

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

See the LICENSE file in the project root for details.

## Support

For issues or questions, please check the project's issue tracker or refer to the [Endee documentation](https://github.com/endee-ai/endee).
