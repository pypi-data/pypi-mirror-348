# PDF Shelver

**PDF Shelver** helps you turn a pile of scanned PDFs into a searchable, browsable categorized digital archive - automatically!

`pdfshelver` is a command-line tool that helps you organize scanned PDF documents using OCR (Optical Character Recognition) and LLM (Large Language Model), via models running locally with [Ollama](https://ollama.com/). It extracts key metadata (sender, subject, document type, and category) from your PDFs, stores the original PDF files and metadata, and creates a "knowledge base" of softlinks is a separate directory for easy human retrieval.

Important:
- at the moment macOS 14+ (Sonoma and later) only, as it uses the new Apple LiveText OCR framework
- LLMs can be memory intensive. 16 GiB memory are recommended when using the default model "qwen3:8b", the fallback model "gemma3:12b" will probably need 24 GiB
- "good enough" for personal use, but not hardened to catch each and every potentially failure case as would be needed when using in commercial production environments

## Background (and alternatives)

`pdfshelver` was written as a small exercise and showcase for the question "What does one need to keep in mind when being asked *Can we do something like this with AI and state-of-the-art frameworks*?" which one encounters frequently nowadays in any company, bigger or smaller.

I chose a simple problem in my quest for making my personal life easier: automating archiving (and making findable) of paper mail I receive. I do have a scanner which is able to scan stacks of paper both sides and store them as PDFs on a NAS (network attached storage), but those PDFs are neither searchable (no OCR having been performed by the scanner) nor easily findable by topic, or sender, or ... by me once they are somewhere on the filesystem. This is where `pdfshelver` comes in.

Turns out that while a quick proof-of-concept can be thrown together in an hour or two, basic hardening for 'most important' failure cases will still need quite a bit more programming time even when using AI supported coding. Besides typical error possibilities like, e.g., file handling, a whole new category of error checking needs to be reserved for the LLM operation, ranging from "runaway" LLMs - where the LLM simply does not stop generating output - to failures of the LLM to generate the output you asked for - no matter how intricate or detailed you formulate your prompts.

I am well aware of other tools like [OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/) or even complete systems like [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) (which in turn relies on OCRmyPDF).

Both tools are fantastic, and I encourage you to check them out in case you want to build anything more or less "enterprise-ready." However, preliminary tests I did on a couple of scans showed me that the macOS OCR framework gave me quite a bit better OCRed text than OCRmyPDF. Not several orders of magnitude better, but better enough for me to choose to not rely on OCRmyPDF for this small finger exercise. Besides, most of the work needed to make paper-mail archiving (error checking, LLM failure checking, etc.) would be exactly the same with or without OCRmyPDF.

## Key Features
 
- **Organized Storage:** Stores the original PDF and extracted metadata in a designated directory.
- **OCR Processing:** Extracts text from scanned PDFs using OCR.
- **Metadata Extraction:** Uses an LLM to identify sender, subject, document type, and category from the document content.
- **Knowledge Base:** Creates human-readable softlinks in a "sortedby" directory, making it easy to browse and find documents by sender, category, etc. within the filesystem.
- **Customizable:** Supports multiple Ollama models, custom system/user prompts, and flexible directory setup.
- **Rebuild Capability:** Can rebuild the knowledge base from existing stored PDFs and metadata without re-running OCR or LLM.


## Extracted metadata

`pdfshelver` in its default configuration will extract the following data from a PDF:

- Sender (as free text): who is the sender / author of a Document.
- Subject (as free text): a short summary one-liner regarding what the PDF is about
- Document type (choices): is this PDF an "invoice", a "contract", some "info" (information), or "other"?
- Category (choices): does this concern "social", "health", "job", "finance", "pension", "insurance", "taxes", "living", or "other"?

CAVEAT: LLMs are sometimes hit and miss when it comes to the things they will give back as answer. I put in-place basic error checking to make sure that what is extracted is correct regarding syntax, e.g., under category you will get exactly one of the choices the LLM has. However, there is no way to check the LLM actually made the right choice.


## Requirements and installation

### Requirements
- Running at least on macOS Sonoma (macOS 14 and later) with at least 16 GiB RAM.
- [Ollama](https://ollama.com/) running locally or accessible via network. See below for installation.
- `poppler` tools, this should be handled by `brew`, see below for installation.
- Python 3.13+. This should be handled by `uv`, see below for installation.
- Required Python packages: `ollama`, `pdf2image`, `ocrmac`, etc. ... and their dependencies. Also handled by `uv`.
 
### Installation

#### Step 1: Ollama and Ollama models
I assume you already have Ollama installed locally on your machine, or that it is available to you via network. If not, head over to [Ollama](https://ollama.com/) to install it. Then install the default models used by `pdfshelver` like so: `ollama pull qwen3:8b` and `ollama pull gemma3:12b`.

#### Step 2: poppler
`pdfshelver` needs utilities from the `poppler` library. The easiest way to install these is via [Homebrew](https://brew.sh/). If not installed, do it now. Then a simple `brew install poppler` will do the trick.

#### Step 3: PDF Shelver itself
To install `pdfshelver` itself, I recommend [uv](https://docs.astral.sh/uv/) as this Python package and project manager basically makes all headaches of Python package management go away in an instant. If not installed, do this now. Then simply type `uv tool install pdfshelver` and your are good to go!

 
## Quick Start
 
### 1. Set Up Directories
 
You need two directories:
 
- **Store Directory:** Where original PDFs and metadata will be saved.
- **Sortedby Directory:** Where categorized softlinks are created for easy browsing.
 
You can specify these via command-line options or environment variables. Using environment variables, put them into your shell startup script (e.g. `.bashrc` if using bash) or do this:
 
```sh
export PDFSHELVER_DIR_STORE=~/pdfshelver/store
export PDFSHELVER_DIR_SORTEDBY=~/pdfshelver/sortedby
```
 
Or use `--dir_store` and `--dir_sortedby` options on the `pdfshelver` command line call.
 
### 2. Process a PDF
 
```sh
pdfshelver myscan.pdf
```
 
This will:
- copy `myscan.pdf` to the store directory.
- run OCR and extract text.
- use Ollama to extract metadata.
- save metadata and OCR text.
- create categorized softlinks in the sortedby directory.

### 3. Browse Your Knowledge Base
 
Navigate the sortedby directory to find your documents organized by sender, category, etc. In the default organisation, you will find your PDF in all of the the following 'sortedby' directories:
- 'from'. That is, organised just by sender/author
- 'fromcat'. That is, first organised by sender/author, then by the category (e.g. "health") the content belongs to.
- 'catfrom', i.e., first organised by by category ("e.g. "health"), then by sender
 
 
## Command-Line Options
 
- `PDFfile` (positional): The PDF to process.
- `--dir_store DIR`: Directory to store PDFs and metadata.
- `--dir_sortedby DIR`: Directory for the knowledge base (softlinks).
- `--replstr STR`: String in filenames to replace with metadata (default: `autoscan`).
- `--sysin FILE`: Custom SYSTEM prompt for Ollama.
- `--usrin FILE`: Custom USER prompt template for Ollama.
- `--model NAME`: Ollama model(s) to use (comma-separated). Default atm is `qwen3:8b,gemma3:12b`
- `--opts OPTS`: Ollama options (e.g., `temperature=0.0;num_ctx=32768`).
- `--host HOST`: Ollama server host (default: `localhost:11434`).
- `--rebuildkb`: Rebuild the knowledge base from existing store (no OCR/LLM).
- `--opthelp`: Show available Ollama options.
- `--optdesc`: Show Ollama options with descriptions.
- `--msgs`: Show default SYSTEM and USER messages used by `pdfshelver` for the LLM models.
 

## Example
 
```sh
pdfshelver --dir_store ~/pdfshelver/store --dir_sortedby ~/pdfshelver/sortedby 20250510_autoscan_181036.pdf
```
 
As the filename contains the string `autoscan` as in the example above, it will be replaced in the sortedby directory with a string like:
 
```
20250510_John Doe LLC -- invoice -- living -- Delivery cupboard_181036.pdf
```


## Rebuilding the Knowledge Base
 
If you reorganize or lose your sortedby directory, you can rebuild it from the store:
 
```sh
pdfshelver --rebuildkb
```


## Limitations

- Due to simplistic OCR interpretation, is restricted to documents where the writing is left-to-right, top-to-bottom 
- Only the first two pages of each PDF are used for LLM metadata extraction as the metadata to be extracted is often found there. Using more pages often confuses small LLMs and leads to worse performance regarding the quality of their answer.
- All metadata and OCR text are stored alongside the original PDF for future reference, but not stored within the PDF. I.e., no PDF/A is created.
- LLMs sometimes take ... astonishing decisions when processing a document. Expect the results to be "mostly right", but not always 100% correct.
- Especially the "sender" information extracted could use a 2nd step polishing as it may vary wildly. E.g., in one document
the LLM might extract "Big Company LLC" as sender, while in a document with same headers but different textual content it
might be extracted as "Big Company", or "BigCo", or "BigCo Shipping", or, or, or ...

 
## Troubleshooting
 
- Make sure the store and sortedby directories exist and are writable.
- Ensure Ollama is running and accessible.
- For help on Ollama options, use `--opthelp` or `--optdesc`.
 
 
## License
 
MIT License
 
 