# Typhoon OCR

Typhoon OCR is a Python package for extracting structured content from images and PDFs. It provides utilities for document layout analysis and can be used to build OCR applications.

## Features

- Convert images to PDFs for unified processing
- Extract text and layout information from PDFs and images
- Generate OCR-ready messages for API processing
- Built-in prompt templates for different document processing tasks

## Installation

```bash
pip install typhoon-ocr
```

### System Requirements

The package requires the Poppler utilities to be installed on your system:

#### For macOS:
```bash
brew install poppler
```

#### For Linux:
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

The following binaries are required:
- `pdfinfo`
- `pdftoppm`

## Usage

### Core functionality

The package provides three main functions:

```python
from typhoon_ocr import prepare_ocr_messages, get_prompt, image_to_pdf
```

* `prepare_ocr_messages`: Main function to generate complete OCR-ready messages
* `get_prompt`: Access built-in prompt templates for different tasks
* `image_to_pdf`: Convert image files to PDF format

### Basic image/PDF processing

Convert an image to PDF format:

```python
from typhoon_ocr import image_to_pdf

# Convert an image to PDF
pdf_path = image_to_pdf('document.jpg')
```

### Complete OCR workflow

Use the simplified API to prepare messages for OCR processing in a single function call:

```python
from typhoon_ocr import prepare_ocr_messages
from openai import OpenAI

# Prepare messages for OCR processing with just one function call
messages = prepare_ocr_messages(
    pdf_or_image_path="document.pdf",  # Works with PDFs or images
    task_type="default",    # Choose between "default" or "structure"
    page_num=2              # Process page 2 of a PDF (default is 1, always 1 for images)
)

# Or with image
messages = prepare_ocr_messages(
    pdf_or_image_path="scan.jpg",  # Works with PDFs or images
    task_type="default",    # Choose between "default" or "structure"
)

# Use with opentyphoon.ai api or self-host model via vllm
# See model list at https://huggingface.co/collections/scb10x/typhoon-ocr-682713483cb934ab0cf069bd
client = OpenAI(base_url='https://api.opentyphoon.ai/v1')
response = client.chat.completions.create(
    model="typhoon-ocr-preview",
    messages=messages,
    max_tokens=16000,
    extra_body={
        "repetition_penalty": 1.2,
        "temperature": 0.1,
        "top_p": 0.6,
    },

)

# Parse the JSON response
result = response.choices[0].message.content
json_data = json.loads(text_output)['natural_text']
print(json_data)
```

### Available task types
The package comes with built-in prompt templates for different OCR tasks:

- `default`: Extracts markdown representation of the document with tables in markdown format
- `structure`: Provides more structured output with HTML tables and image analysis placeholders

## License

This project is licensed under the Apache 2.0 License. See individual datasets and checkpoints for their respective licenses.

## Acknowledgments

The code is based on work from [OlmoCR](https://github.com/allenai/olmocr) under the Apache 2.0 license. 