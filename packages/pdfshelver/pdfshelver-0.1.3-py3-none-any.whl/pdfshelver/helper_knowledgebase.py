"""Helper functions for 'knowledgebase' sortedby directory for pdfshelver"""

import json
import re
from pathlib import Path

from pdfshelver.helper_fs import create_dir


def rebuild_knowledge_base(storedir: Path, sortedbydir: Path, replstr: str) -> None:
    """Bla"""
    for pdffile in storedir.rglob("*.pdf"):
        stemname = pdffile.stem
        dirname = pdffile.parent
        if (Path(dirname) / f"{stemname}.ok").exists():
            jsonfile = Path(dirname) / f"{stemname}.pdfshelver.json"
            with jsonfile.open("r") as fin:
                metainf = json.load(fin)
                print(pdffile, metainf)
                kb_name = create_knowledgebase_stemname(stemname, replstr, metainf)
                link_in_kb_directory(sortedbydir, kb_name, str(pdffile), metainf)
        else:
            print(f"No OK file for {pdffile}")
    return


def __likd_single(
    topname: str, subnames: list[str], metainf: dict[str, str], kbstemname: str, origpath: str
) -> None:
    """Helper function. See call in 'link'_in_kb_directory to understand."""
    tpathelem = [topname]
    tpathelem.extend(metainf[sn] for sn in subnames)

    d = "/".join(tpathelem)
    create_dir(d)
    linkpath = Path(f"{d}/{kbstemname}.pdf")
    linkpath.unlink(missing_ok=True)
    linkpath.symlink_to(Path(origpath))
    return


def link_in_kb_directory(
    kbdir: Path, kbstemname: str, origpath: str, metainf: dict[str, str]
) -> None:
    """Link the OCRed PDF via various paths so that this can be easily found in filesystem
    in the sortedby path."""
    __likd_single(f"{kbdir}/searchby_from", ["from"], metainf, kbstemname, origpath)
    __likd_single(f"{kbdir}/searchby_catfrom", ["category", "from"], metainf, kbstemname, origpath)
    __likd_single(f"{kbdir}/searchby_fromcat", ["from", "category"], metainf, kbstemname, origpath)
    return


def create_knowledgebase_stemname(stemname: str, replstr: str, metainf: dict[str, str]) -> str:
    """Create a filename with basic info on that PDF, will be linked from the sortedby
    directory."""

    repby = " -- ".join(
        # [metainf["from"], metainf["subject"]]
        [metainf["from"], metainf["doctype"], metainf["category"], metainf["subject"]]
    )

    retval: str
    if replstr in stemname:
        retval = re.sub(replstr, repby, stemname, count=1)
    else:
        retval = f"{repby}_{stemname}"

    return retval
