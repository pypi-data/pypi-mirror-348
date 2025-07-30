"""Some text related helper functions for pdfshelver"""

import re

# OCRMac unfortunately does not make this type available. Fake an own one.
#  (and hope it does not change in OCRMac)
# May 2025: type ignore because my mypy doesn't know PEP 695 yet (Python 3.12+).
type OCRMacRecognize = list[tuple[str, float, tuple[float, float, float, float]]]  # type: ignore[valid-type]


def reconstruct_lines(annotations: OCRMacRecognize, ywiggle: float = 0.003) -> list[str]:
    """Taking the annotations from ocrmac, reconstruct a text line by line,
    from left to right, top to bottom.

    Input: annotations from ocrmac as list
    Output: list of strings representing lines

    Optional:
    - ywiggle: tolerance the y-position of a recognised text element may have
      wrt to the previous y-element at still be seen to be on the same line.

    Some OCR frameworks apparently love to return single words annotation
    elements (looking at you, 'livetext' from OSX). This simple function
    runs through the annotations and puts words back into full lines."""

    retval: list[str] = []

    if len(annotations) == 0:
        return retval

    # tracking: line element accumulator and y-position of last recognised element
    # take ypos of first annotation found as init to stay on the 1st line when starting
    line: list[str] = []
    lastypos = annotations[0][2][1]

    for ann in annotations:
        txt, _, bbox = ann  # don't care about the recognition certainty
        ypos = bbox[1]
        if abs(ypos - lastypos) >= ywiggle:
            # yup, that's a mew line we're on
            retval.append(" ".join(line))
            line = []
        line.append(txt)
        lastypos = ypos

    # gather remaining elements
    if len(line) > 0:
        retval.append(" ".join(line))

    return retval


def clean_answer_from_think(oanswer: str) -> str:
    """Some LLMs nowadays add a <think> ... </think> as "thinking" process before
    their real answer. Trying to suppress this by using a /nothink in the SYS or USR
    message has two effects (observed with qwen3 and deepthink-r1):
    1) the tags are still added, but empty content and
    2) the answer from the LLM can be notably different / worse

    As we don't want that think-stuff ... do a hail mary and just strip out everything
    between think tags :-)"""
    cleaned = re.sub(r"<think>.*?</think>", "", oanswer, flags=re.DOTALL)
    return cleaned.strip()


def recover_from_markdown(txt: str) -> str:
    """No matter what I try to prevent it in instructions, sometimes the LLMs give an
    answer using markdown like this:
    **Document type:** Correspondance
    ...

    Do. Not. Want!
    This crude regex routine simply strips out all text like "**...:** "
    """
    # Regex: (does not match newlines as no flag re.DOTALL given)
    # - start with "**"
    # - then everything except a newline, colon, or *
    # - then ":** "
    cleaned = re.sub(r"\*\*[^:\*]*:\*\* ", "", txt)
    return cleaned.strip()


def llm_to_metainfodict(
    mtxt: str, infolist: list[str], oneof_choices: dict[str, list[str]]
) -> dict[str, str]:
    """Answer from LLM is (hopefully) semistructured text. Get that into a dict.
    numlines is number of lines expected by the LLM
    If anything is fishy, return an empty dict."""

    mtxt = clean_answer_from_think(mtxt)
    mtxt = recover_from_markdown(mtxt)
    mlines = [s.strip() for s in mtxt.splitlines()]

    # first moment of truth: we need to have exactly the number of lines as
    #  pieces of information we requested
    if len(mlines) != len(infolist):
        print(
            f"You asked to have the following info extracted: {infolist}"
            f"Answer from LLM has {len(mlines)} and not {len(infolist)} lines, which is unexpected."
        )
        return {}

    retval: dict[str, str] = dict(zip(infolist, mlines, strict=True))

    # 2nd moment of truth: for pieces of information where we restricted the answer to
    #  choices, check that we indeed have an answer being part of the choices we wanted.
    for key, allowed in oneof_choices.items():
        retval[key] = retval[key].lower()  # .lower() as LLMs sometimes capitalise :-/
        if retval[key] not in allowed:
            print(f"{key} seen as '{retval[key]}', which is not in allowed {allowed}.")
            return {}

    # "from" and "subject" can basically contain anything, including
    #  characters which might not be printable or may not be used afterwards
    #  in a file- or directory name (which we want)
    # Sanitise these!

    for key in ["from", "subject"]:
        # Take out chars generally not usable as filename (/, :, *, ...)
        news = re.sub(r"[\/:\*\?<>|\\]", "", retval[key])

        # Take only chars which are printable
        news = "".join([x if x.isprintable() else "" for x in news])

        # strip leading blanks/dots (unsure whether regex might be more efficient)
        oldlen = -1
        while oldlen != len(news):
            oldlen = len(news)
            news = news.strip().strip(".")

        retval[key] = news

    return retval
