"""PDFShelver main code file"""

import argparse
import importlib.metadata
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

import ollama
from dm_ollamalib.optionhelper import help_long, help_overview, to_ollama_options
from ocrmac import ocrmac  # type: ignore[import-untyped]
from pdf2image import convert_from_path  # pyright: ignore[reportUnknownVariableType]

from pdfshelver.cmdline_parser import parse_cmd_line
from pdfshelver.config import (
    DEFAULT_EXTRACT_INFO,
    DEFAULT_ONEOF_CHOICES,
    DEFAULT_SYSMSG,
    DEFAULT_USERMSG_TEMPLATE,
    create_sysusrmsg,
)
from pdfshelver.helper_fs import copy_file
from pdfshelver.helper_knowledgebase import (
    create_knowledgebase_stemname,
    link_in_kb_directory,
    rebuild_knowledge_base,
)
from pdfshelver.helper_ollama import get_ollama_response
from pdfshelver.helper_text import llm_to_metainfodict, reconstruct_lines

__version__ = importlib.metadata.version("pdfshelver")

# Textual content recovered via OCR from PDF will be stored as this type
# Outer list: pages
# Inner list: single lines of a page
# May 2025: type ignore because my mypy doesn't know PEP 695 yet (Python 3.12+).
type Ocrcontent = list[list[str]]  # type: ignore[valid-type]


def early_exits(opts: argparse.Namespace) -> None:
    """handle early exits: version or help on Ollama options?"""
    if opts.opthelp:
        print(help_overview())
        sys.exit(0)
    if opts.optdesc:
        print(help_long())
        sys.exit(0)
    if opts.version:
        print(__version__)
        sys.exit(0)

    if opts.msgs:
        print(
            f"Ollama SYSTEM message:\n{DEFAULT_SYSMSG}"
            "\n---------------------------------\n\n"
            f"Ollama USER message template:\n{DEFAULT_USERMSG_TEMPLATE}"
            "\n---------------------------------\n\n"
        )
        try:
            _, usrmsg = create_sysusrmsg("", "")
        except ValueError as e:
            print(
                "Error happened while creating the final USER message."
                " This points to a problem with the configuration."
                f" Message was:\n{e}"
                "\nAborting."
            )
            sys.exit(1)
        print(f"Ollama final USER message:\n{usrmsg}")
        sys.exit(0)
    return


def get_ollama_options(oopts: str) -> ollama.Options:
    """quick check of --opt for an early bail out if there's an error there."""
    try:
        oparams: ollama.Options = to_ollama_options(oopts)
    except ValueError as e:
        print(e)
        print("Aborting.", file=sys.stderr)
        sys.exit(1)
    return oparams


def get_pdf_content(fname: str) -> Ocrcontent:
    """Takes PDF, returns ocrcontent"""
    retval = []
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(fname, output_folder=path)

        # I have no idea how to get this right without quietening pyright / pylance
        for img in images_from_path:
            annotations = ocrmac.OCR(  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                img, framework="livetext"
            ).recognize()
            retval.append(  # pyright: ignore[reportUnknownMemberType]
                reconstruct_lines(annotations)  # pyright: ignore[reportUnknownArgumentType]
            )
    return retval  # pyright: ignore[reportUnknownVariableType]


def append_pdfcontent_to_usrmsg(usrmsg: str, pdfc: Ocrcontent) -> str:
    """Create final user-message for Ollama
    == user msg so far + content of first max 2 pages of PDF file)"""

    # take first two pages, making a single string out of it
    # join every element by a newline, and every page by
    # newline+pagefeed+newline

    pdftxt = "\n\f\n".join("\n".join(page) for page in pdfc[:2]).strip()
    if len(pdftxt) == 0:
        raise ValueError("Found no text in PDF? Aborting.")

    return f"{usrmsg}\n\nSCANDOCSTART\n\n{pdftxt}"


def write_ocr_content(pdfc: Ocrcontent, destdir: Path, stemname: str) -> None:
    """As on the tin: write the OCRed content as text file with .ocr.txt filetype."""
    dpath = destdir / f"{stemname}.ocr.txt"

    with dpath.open("w", encoding="UTF-8") as fout:
        for idx, page in enumerate(pdfc):
            if idx > 0:
                print("\n\f\n", file=fout)
            for line in page:
                print(line, file=fout)
    return


def write_metainf(metainf: dict[str, str], destdir: Path, stemname: str) -> None:
    """Write meta information on PDF document as JSON to .autometa.json"""
    dpath = destdir / f"{stemname}.pdfshelver.json"

    with dpath.open("w", encoding="UTF-8") as fout:
        print(json.dumps(metainf, indent=4, ensure_ascii=False), file=fout)
    return


def get_dirs_path(opts: argparse.Namespace) -> tuple[Path, Path]:
    """Provides store and sortedby directories either from commandline opts or environment
    variable"""
    if len(opts.dir_store) == 0:
        store = os.environ.get("PDFSHELVER_DIR_STORE", "")
        if len(store) == 0:
            print(
                "Need a directory to store PDFs to. No value was given on"
                " the command line via --dir_store, and no environment variable"
                " PDFSHELVER_DIR_STORE was found."
            )
            sys.exit(1)
    else:
        store = opts.dir_store

    if len(opts.dir_sortedby) == 0:
        sortedby = os.environ.get("PDFSHELVER_DIR_SORTEDBY", "")
        if len(sortedby) == 0:
            print(
                "Need a directory to sort your PDFs into. No value was given on"
                " the command line via --dir_store, and no environment variable"
                " PDFSHELVER_DIR_SORTED was found."
            )
            sys.exit(1)
    else:
        sortedby = opts.dir_sortedby

    # Careful, some functions of pathlib, shutils, etc. will not expand a ~
    # therefor, do it manually for all paths which might come from the user

    return (Path(store).expanduser(), Path(sortedby).expanduser())


def pdfshelver_mainworkflow(
    pdffn: str,
    storedir: Path,
    sortedbydir: Path,
    ollamaopts: str,
    sysin: str,
    usrin: str,
    models: str,
    host: str,
    replstr: str,
) -> None:
    """The main workflow of pdfshelver:
    1) copy PDF to store directory
    2) run OCR on PDF
    3) evaluate OCRed text with a LLM to extract meta information
    4) create softlinks in knowledgebase 'sortedby' directory for human to find"""

    # get ollama options now, if fails, hard exit
    oparams = get_ollama_options(ollamaopts)

    # Up to this point, nothing happened on disk. This is why on error,
    #  above functions will perform a sys.exit
    # Starting now, we do something on disk and therefore we will work
    #  with try ... except to catch errors and act accordingly

    stemname = Path(pdffn).stem

    ##########################################
    # Set a guard file
    guardfile = Path(storedir) / f"{stemname}.guard"
    endfile = Path(storedir) / f"{stemname}.ok"

    allok = False
    try:
        with guardfile.open("w"):
            pass

        endfile.unlink(missing_ok=True)  # remove old ".ok" if it existed

        ##########################################
        # Copy the PDF to our store
        print("Copying PDF to store (if necessary).")
        storefn = copy_file(pdffn, storedir / f"{stemname}.pdf")

        ##########################################
        # Create Ollama query SYSmsg and USRmsg)
        #  and run Ollama
        sysmsg, usrmsg = create_sysusrmsg(sysin, usrin)
        print("Running OCR to get PDF content.")
        pdfcontent = get_pdf_content(pdffn)
        usrmsg = append_pdfcontent_to_usrmsg(usrmsg, pdfcontent)
        print(sysmsg, usrmsg)

        metainf = {}
        for model in [m.strip() for m in models.split(",")]:
            print(f"Now running Ollama model {model}")
            metaraw = get_ollama_response(
                sysmsg,
                usrmsg,
                model,
                oparams,
                host,
            )

            metainf = llm_to_metainfodict(metaraw, DEFAULT_EXTRACT_INFO, DEFAULT_ONEOF_CHOICES)
            if len(metainf) > 0:
                break

        if len(metainf) == 0:
            raise RuntimeError("No LLM model gave back a good answer")

        write_ocr_content(pdfcontent, storedir, stemname)
        write_metainf(metainf, storedir, stemname)

        kb_name = create_knowledgebase_stemname(stemname, replstr, metainf)
        link_in_kb_directory(sortedbydir, kb_name, storefn, metainf)

        allok = True
    except NotImplementedError as e:
        print(
            f"Ouch, some part of the code was hit that is not implemented yet.\n{e}",
            file=sys.stderr,
        )
        traceback.print_exc(file=sys.stderr)
    except (RuntimeError, ValueError) as e:
        print(f"Encountered an problem, message is: {e}", file=sys.stderr)
    except Exception as e:  # pylint: disable=W0718 # yes pylint, this is broad catch
        print(f"Encountered an unhandled exception, message is: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if not allok:
        endfile = Path(storedir) / f"{stemname}.fail"

    # rename the guard file to a success file or fail file
    guardfile.rename(endfile)

    if not allok:
        sys.exit(1)


def cli_entry() -> int:
    """Entry point to pdfshelver.

    Parse cmd line, get SYSTEM and USR msg, setup the Ollama model, and stream answer back.
    """

    ##########################################
    # Setup from command line and basic sanity checks
    opts = parse_cmd_line()
    early_exits(opts)

    storedir, sortedbydir = get_dirs_path(opts)

    for p in [storedir, sortedbydir]:
        if not p.is_dir():
            print(f"Not a directory: {p}\nAborting.")
            sys.exit(1)

    if opts.rebuildkb:
        rebuild_knowledge_base(storedir, sortedbydir, opts.replstr)
        sys.exit(0)

    pdffn = opts.pdffile
    if len(pdffn) == 0:
        print("Missing mandatory argument PDFfile.", file=sys.stderr)
        sys.exit(1)
    if not Path(pdffn).is_file():
        print(f"{pdffn} does not seem to be a file?\nAborting.", file=sys.stderr)
        sys.exit(1)

    pdfshelver_mainworkflow(
        pdffn,
        storedir,
        sortedbydir,
        opts.opts,
        opts.sysin,
        opts.usrin,
        opts.model,
        opts.host,
        opts.replstr,
    )

    return 0
