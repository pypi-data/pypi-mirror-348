# ContextExtract

A Python package for extracting contextual key-value pairs from URLs, PDFs, or text inputs using the Groq API.

## Example Output

When you run the package on a URL like Wikipedia's Artificial Intelligence page, you'll get structured JSON output similar to:

```json
{
  "Topic": "Artificial intelligence",
  "Redirect": "AI",
  "AI": "disambiguation and Artificial intelligence (disambiguation)",
  "Series": "Artificial intelligence (AI)",
  "Major Goals": [
    "Artificial general intelligence",
    "Intelligent agent",
    "Recursive self-improvement",
    "Planning",
    "Computer vision",
    "General game playing",
    "Knowledge representation",
    "Natural language processing",
    "Robotics",
    "AI safety"
  ],
  "Approaches": [
    "Machine learning",
    "Symbolic",
    "Deep learning",
    "Bayesian networks",
    "Evolutionary algorithms",
    "Hybrid intelligent systems",
    "Systems integration"
  ],
  "Applications": [
    "Bioinformatics",
    "Deepfake",
    "Earth sciences",
    "Finance",
    "Generative AI",
    "Art",
    "Audio",
    "Music",
    "Government",
    "Healthcare",
    "Mental health",
    "Industry",
    "Translation",
    "Military",
    "Physics"
  ],
  "Projects": [
    "Philosophy",
    "Artificial consciousness",
    "Chinese room",
    "Friendly AI",
    "Control problem/Takeover",
    "Ethics",
    "Existential risk",
    "Turing test",
    "Uncanny valley"
  ],
  "History": [
    "Timeline",
    "Progress",
    "AI winter",
    "AI boom"
  ],
  "_metadata": {
    "source": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "source_type": "url",
    "extraction_params": {}
  }
}

```

## Quick Start

### Installation

```bash
pip install contextextract
```

### Usage

```python
from contextextract import ContextExtractor

# Initialize with your Groq API key
extractor = ContextExtractor(api_key="gsk_Jv2a5u...")

# Extract from URL
url_data = extractor.extract_from_url("https://en.wikipedia.org/wiki/Artificial_intelligence")

# Extract from PDF
pdf_data = extractor.extract_from_pdf("path/to/document.pdf")

# Extract from text
text_data = extractor.extract_from_text("Your text content here...")

# Save to JSON file
extractor.save_to_json(url_data, "output.json")
```

### Command Line Usage

```bash
# Set your API key as an environment variable
export GROQ_API_KEY="gsk_Jv2a5u..."

# Extract from URL
contextextract url https://en.wikipedia.org/wiki/Artificial_intelligence -o ai_data.json

# Extract from PDF
contextextract pdf document.pdf -o pdf_data.json

# Extract from text file
contextextract text input.txt --is-file -o text_data.json

# Extract from direct text input
contextextract text "This is sample text to extract key information from."
```

## Features

- **URL Processing**: Extract key-value pairs from web content
- **PDF Processing**: Extract structured data from PDF documents
- **Text Processing**: Extract information from raw text input
- **Customization**: Configure extraction parameters
- **JSON Output**: Save results in structured JSON format
- **Command Line Interface**: Use from terminal without writing code

## Requirements

- Python 3.8+
- Groq API key (starts with "gsk_")

## Advanced Usage

### Customizing Extraction

```python
# Custom extraction parameters
params = {
    "model": "llama3-70b-8192",  # Choose Groq model
    "system_message": "Extract technical terms and their definitions as key-value pairs."
}

# Use custom parameters
result = extractor.extract_from_url("https://en.wikipedia.org/wiki/Machine_learning", params)
```

### Error Handling

```python
try:
    result = extractor.extract_from_url("https://example.com/page")
    if "error" in result:
        print(f"API Error: {result['error']}")
    else:
        print("Extraction successful!")
except Exception as e:
    print(f"Exception occurred: {e}")
```

## Development

### Local Development Setup

## 1. Set Up Your Project Environment

### Create Directory Structure

Open your terminal/command prompt and run:

```bash
# Create main project directory
mkdir -p contextextract/src/contextextract/processors contextextract/src/contextextract/utils contextextract/tests
cd contextextract
```

## 2. Create Package Files

Copy all the code files provided into their respective directories:

### Core Files
- `LICENSE` → Place in root directory
- `README.md` → Place in root directory
- `pyproject.toml` → Place in root directory
- `setup.py` → Place in root directory

### Package Files
- `src/contextextract/__init__.py`
- `src/contextextract/extractor.py`
- `src/contextextract/cli.py`
- `src/contextextract/processors/__init__.py`
- `src/contextextract/processors/url_processor.py`
- `src/contextextract/processors/pdf_processor.py`
- `src/contextextract/processors/text_processor.py`
- `src/contextextract/utils/__init__.py`
- `src/contextextract/utils/helpers.py`

### Test Files
- `tests/__init__.py`
- `tests/test_extractor.py`

## 3. Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## 4. Install Required Dependencies

```bash
pip install requests beautifulsoup4 PyPDF2 tqdm groq
```

## 5. Install the Package in Development Mode

```bash
pip install -e .
```

## 6. Set Your Groq API Key

```bash
# On Windows:
set GROQ_API_KEY=gsk_Jv2a5u...

# On macOS/Linux:
export GROQ_API_KEY=gsk_Jv2a5u...
```

Replace `gsk_Jv2a5u...` with your actual Groq API key.

## 7. Run the Example Script

Create a file called `example_run.py` in the root directory with the following content:

```python
from contextextract import ContextExtractor
import os

# Get API key from environment variable
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("Please set your GROQ_API_KEY environment variable")
    exit(1)

# Initialize the extractor
extractor = ContextExtractor(api_key=api_key)

# URL to extract information from
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
print(f"Extracting information from {url}...")

# Perform extraction
result = extractor.extract_from_url(url)

# Save to JSON file
output_file = "ai_data.json"
extractor.save_to_json(result, output_file)

print(f"Extraction complete! Data saved to {output_file}")
```

Run the example:

```bash
python example_run.py
```

## 8. Try the Command Line Interface

Once installed in development mode, you can also use the command line interface:

```bash
# Extract from URL
contextextract url https://en.wikipedia.org/wiki/Artificial_intelligence

# Extract from a text input
contextextract text "Artificial intelligence is the simulation of human intelligence by machines."
```

## Troubleshooting

1. **ImportError**: Make sure you've installed the package in development mode with `pip install -e .`

2. **API Key Issues**: Verify your Groq API key is correctly set and starts with "gsk_"

3. **Dependency Errors**: Ensure all required packages are installed:
   ```bash
   pip install requests beautifulsoup4 PyPDF2 tqdm groq
   ```
4. **Permission Issues**: Make sure you have appropriate permissions for creating files in the output directory
