"""Default text analysis configuration for pdfshelver"""

import re
from pathlib import Path

# Default system message for priming the LLM
# May 2025. Note that with Ollama, it is best to have a fixed SYSMSG and do
#  specialisation in the USRMSG as every time a system message is changed,
#  Ollama takes waaaaaaay longer to startup as it seems to re-initialise (part of?)
#  the model.
DEFAULT_SYSMSG = """You are the world best expert in extracting information from text
which was created via OCR from scanned documents.

You will be given some basic facts and instructions, followed by a marker
"SCANDOCSTART" which will denote the start of the text for you to analyse.
Be careful, due to unorthodox formating of the printed document, OCR may have placed
any information requested anywhere within the linear extracted text and not
where one would initially expect it.

Important instructions, my life depends on you adhering strictly to these:
- Resolve conflicts quickly.
- Do NEVER add any explanation to your response.
- DO NOT use markdown in your answer.
- NEVER EVER AT ALL explain your response.

For classification and storage of incoming documents, you need to extract just the
pieces of information described further down. Each piece of information is to be given on a
single line and nothing else.

"""

# Template for the user message describing for the LLM what to extract
# Note there will be text replacements performed using ONEOF_choices (or later,
#  something easier to be user defined) before handing this to the LLM.
# The text replacement will be done on strings like "//ONEOF_xxx//", where 'xxx'
#  is the key of the ONEOF_CHOICES dict. The replacement text will be generated
#  by the associated values and prepended by some text making sure it's a choice
#  the LLM has to make.
# E.g., the text
#   Second line: What's the type of the document? //ONEOF_doctype//
# would be replaced by
#   Second line: What's the type of the document? Choose best fit to one of 'invoice',
#      'contract', 'info', 'other'.
DEFAULT_USERMSG_TEMPLATE = """
First line: who is the sender respectively author? If from a non-person entity (e.g. company, agency, etc.), just use the entity name.
Second line: what is the type of the document? //ONEOF_doctype//
Third line: concise, but as precise as possible, what is the subject? Give this response in the language of the document!
Fourth line: categorise the document content. //ONEOF_category//

Example for an answer in the next four lines:
Doe's Furniture LLC
info
Delivery date cupboard
living

"""  # noqa: E501 # ruff, yes it is too long, but some LLMs interpret this differently if split up


# As we ask the LLM to extract the following info from the textual content,
#  each info on a single line, we need to formalise this metainfo for the JSON results.
# Defaults are:
# - from: from whom is the document?
# - doctype: is it an invoice, a contract, ...?
# - subject: a short subject line regarding content
# - category: to which category of life does that fit?
DEFAULT_EXTRACT_INFO = ["from", "doctype", "subject", "category"]

# Some information we ask the LLM should not be free text, but a choice.
# The following dict tells our pdfshelver for which metainformation
# which choices are valid.
# This will be used for two things:
#  1. The USR message will be adapted so that the LLM knows about valid choices.
#  2. The answer of the LLM will be checked for these expected values
#     and if not present, the whole LLM answer will be categorised as 'invalid answer'.

DEFAULT_ONEOF_CHOICES = {
    "doctype": ["invoice", "contract", "info", "other"],
    "category": [
        "social",
        "health",
        "job",
        "finance",
        "pension",
        "insurance",
        "taxes",
        "living",
        "other",
    ],
}


def create_sysusrmsg(sysfn: str, usrfn: str) -> tuple[str, str]:
    """Prepare Ollama SYS and USR messages to be used."""
    sysmsg = ""
    usrmsg = ""
    if len(sysfn) > 0:
        with Path(sysfn).open(encoding="utf-8") as fin:
            sysmsg = fin.read()
    else:
        sysmsg = DEFAULT_SYSMSG
    if len(usrfn) > 0:
        with Path(usrfn).open(encoding="utf-8") as fin:
            usrmsg = fin.read()
    else:
        usrmsg = DEFAULT_USERMSG_TEMPLATE
    usrmsg = __expand_usr_msg(usrmsg, DEFAULT_ONEOF_CHOICES)
    return (sysmsg, usrmsg)


def __expand_usr_msg(mtemplate: str, txtrepl: dict[str, list[str]]) -> str:
    retval = mtemplate
    for key, choices in txtrepl.items():
        if len(choices) < 2:  # noqa: PLR2004 # ruff, that is not really a magic value!
            raise ValueError(
                f"The choices given for '{key}' are {choices}, but I need at least two choices."
            )
        replvals = [f"'{x}'" for x in choices]
        replstr = f"Choose best fit to one of {', '.join(replvals)}."
        retval = re.sub(f"//ONEOF_{key}//", replstr, retval, flags=re.DOTALL)

    return retval
