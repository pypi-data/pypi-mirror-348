"""Command line options for pdfshelver"""

import argparse


def parse_cmd_line() -> argparse.Namespace:
    """Setup of commandline parser"""

    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] pdffile || %(prog)s [options] --rebuildkb",
        description=(
            "Performs OCR on a PDF, uses Ollama to find sender, subject, document"
            " type and category of the document. Will store the PDF in its original form"
            " under its original name together"
            " with metadata in its store. Furthermore, softlinks to the OCRed document"
            " will be created in the searchby directory - eventually renamed so that"
            " the name contains human readable information - so that it is easily retrievable."
        ),
    )

    parser.add_argument(
        "pdffile",
        nargs="?",
        default="",
        metavar="PDFfile",
        help="PDF to run through OCR and ollame category/sender ident",
    )

    parser.add_argument(
        "-v",
        "--version",
        default=False,
        action="store_true",
        help=("print version of %(prog)s and exit."),
    )
    parser.add_argument(
        "--opthelp",
        default=False,
        action="store_true",
        help=("show a list of Ollama options that can be set via --opts and exit."),
    )
    parser.add_argument(
        "--optdesc",
        default=False,
        action="store_true",
        help=(
            "show a list of Ollama options and descriptions (if available) that can be"
            " set via --opts and exit."
        ),
    )
    parser.add_argument(
        "--msgs",
        default=False,
        action="store_true",
        help=(
            "Shows the default SYSTEM and USER messages for the LLM pdfshelver is"
            "  working with and exit."
            " Note that two USER messages will be shown: once the template message,"
            " and once the final message which pdfshelver creates while taking into"
            " account things like restricted choices the LLM needs to make."
        ),
    )

    group = parser.add_argument_group("Directory options")
    group.add_argument(
        "--dir_store",
        default="",
        type=str,
        metavar="DIRNAME",
        help=(
            "Path to directory where the raw PDFs and additional metadata"
            " will be stored. If not given, the environment variable"
            " PDFSHELVER_DIR_STORE needs to exist and contain a valid path."
        ),
    )
    group.add_argument(
        "--dir_sortedby",
        default="",
        type=str,
        metavar="DIRNAME",
        help=(
            "Path to directory where pdfshelver will create a knowledge base of your"
            " PDFs, where PDFs will be categorised to be easily findable."
            " If not given, the environment variable"
            " PDFSHELVER_DIR_SORTEDBY needs to exist and contain a valid path."
        ),
    )

    group = parser.add_argument_group("File naming options")
    group.add_argument(
        "--replstr",
        default="autoscan",
        type=str,
        metavar="REPLACEMENT",
        help=(
            "Default: '%(default)s'."
            " If the original name of the PDF contains the string given here, the names"
            " in the 'searchby' knowledgebase directory will have that string replaced with basic"
            " information retrieved by Ollama to give as much information as possible."
            "\n"
            "E.g.: 20250506_autoscan_163535.pdf might become"
            " 20250506_Doe's LLC -- invoice -- living -- Delivery cupboard_163535.pdf"
        ),
    )

    group = parser.add_argument_group("Ollama setup options")
    group.add_argument(
        "--sysin",
        default="",
        type=str,
        metavar="FILENAME",
        help=(
            "Name of a text file with an Ollama SYSTEM msg to prime the model. Overrides"
            " internal default if given."
        ),
    )
    group.add_argument(
        "--usrin",
        default="",
        type=str,
        metavar="FILENAME",
        help=(
            "Name of a text file with an USER msg template to prime the model. Overrides"
            " internal default if given."
        ),
    )
    group.add_argument(
        "--model",
        # default="dolphin3",  # has additional newlines in answer! Can go off rails (AU)!
        # default="mistral-nemo",  # does not care about language asks, answers in english
        # default="deepseek-r1:8b",  # difficult to steer, response often has more than asked for
        # default="qwen3:14b",  # definitely needs 24 Gib RAM on Mac
        # default="qwen3:8b",  # mostly good answers
        # default="qwen3:4b",  # not as good as 8b
        # default="gemma3:4b",  # fails on more documents than it should
        # default="gemma3:12b",  # mostly good answers
        default="qwen3:8b,gemma3:12b",
        metavar="NAME",
        type=str,
        help="Use Ollama model <NAME>. Default: %(default)s",
    )
    group.add_argument(
        "--opts",
        default="temperature=0.0;num_ctx=16384",
        metavar="OPTS",
        type=str,
        help=(
            "Semicolon separated list of options for Ollama."
            ' E.g.: --options="num_ctx=16384;temperature=0.0"'
            ' Default: "%(default)s"'
        ),
    )
    group.add_argument(
        "--host",
        default="",
        type=str,
        help=(
            "The default empty string will connect to 'localhost:11434' where Ollama"
            " is usually installed. Set this to connect to any other Ollama server you have"
            " access to."
            ' Default: "%(default)s"'
        ),
    )

    group = parser.add_argument_group("Special commands")
    group.add_argument(
        "--rebuildkb",
        default=False,
        action="store_true",
        help=(
            "Using all existing PDF files in the 'store' directory (and associated)"
            " metadata, rebuild the 'sortedby' knowledgebase directory."
            " This does *not* redo OCR or go via Ollama LLM models."
            " The following command line options will be evaluated:"
            " --storedir, --sortedbydir, --replstr"
        ),
    )

    opts = parser.parse_args()

    return opts
