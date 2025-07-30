"""Helper functions interface to Ollama for pdfshelver"""

import sys
from collections.abc import Callable, Iterable
from typing import Any

import httpx
import ollama
from dm_streamvalve.streamvalve import StopCriterion, StreamValve


def setup_ollama(
    sysmsg: str, usrmsg: str, model: str, params: ollama.Options, host: str | None = None
) -> Iterable[ollama.ChatResponse]:
    """Starts an Ollama model and returns a stream to it
    Parameters:
    - sysmsg: string with SYSTEM message for Ollama
    - usrmsg: string with USER message for Ollama
    - model: model to run with ollama
    - params: ollama parameter structure
    """

    try:
        client = ollama.Client(host=host)
        ostream: Iterable[ollama.ChatResponse] = client.chat(  # pyright: ignore[reportUnknownMemberType]
            model=model,
            messages=[
                {"role": "system", "content": sysmsg},
                {"role": "user", "content": f"{usrmsg}\n"},
            ],
            options=params,
            stream=True,
        )
    except Exception as err:
        raise RuntimeError("Could not connect to ollama?") from err

    # we get an ostream object back regardless whether there's a working
    #  Ollama server present ... ouch.

    return ostream


def monitor_accepted_chat_response_stdout(s: str) -> None:
    """Callback for streamvalve to monitor chat response"""
    print(s, end="", flush=True)
    return


def monitor_accepted_chat_response_stderr(s: str) -> None:
    """Callback for streamvalve to monitor chat response"""
    print(s, file=sys.stderr, end="", flush=True)
    return


def run_ostream_via_streamvalve(
    ostream: Iterable[ollama.ChatResponse],
    max_linerepeats: int = 0,
    max_lines: int = 0,
    max_linetokens: int = 0,
    max_paragraphs: int = 0,
    monitor_callback: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Setup a StreamValve and run the Ollama stream through it. Try to handle known errors
    gracefully with a message

    Return:
    - the return value from streamvalve

    Parameters:
    - ostream: an Iterable[ChatResponse]. Basically the return value of ollama.chat()
    - max_linerepeats: if >0, stop after this number of non-empty lines that are repeated.
      Lines do not need to be following each other to be spotted as repeats.
    - max_lines: if > 0, max number of complete lines read from Ollama
    - max_paragraphs: if > 0, max number of complete lines read from Ollama
    - monitor_callback: a callback to pass to streamvalve for monitoring the stream

    Returns
    - Tuple. First elem is all text collected from ollama,
      second is stop criterion as text if not None
    """

    def extract_chat_response(cr: ollama.ChatResponse) -> str:
        """Callback for streamvalve to extract chat response as str"""
        return cr["message"]["content"]  # type: ignore[no-any-return]

    sv = StreamValve(
        ostream,
        callback_extract=extract_chat_response,
        callback_token=monitor_callback,
        max_linerepeats=max_linerepeats,
        max_lines=max_lines,
        max_linetokens=max_linetokens,
        max_paragraphs=max_paragraphs,
    )
    ret = sv.process()

    # streams sometimes end without a newline at the end. In this case, and if the stream
    #  was monitored, simply emit a newline on the stream to make it look nice when returning
    #  to the command line
    #
    # pylint cannot infer ret["text"] being a str
    if monitor_callback and len(ret["text"]) > 0 and ret["text"][-1] != "\n":  # pylint: disable = E1136
        monitor_callback("\n")

    if ret["stopcrit"] != StopCriterion.END_OF_STREAM:
        print(
            "\nReading from Ollama model stopped early."
            f"\nCriterion: {ret['stopcrit']}\nMessage: {ret['stopmsg']}"
            f"\nStopped at token/line: {ret['stopat']!r}\n",
            file=sys.stderr,
        )

    return ret


def get_ollama_response(
    sysmsg: str, usermsg: str, model: str, params: ollama.Options, host: str
) -> str:
    """Send request to Ollama and returns its response as text.
    Hard exits if something fails."""

    monitor = monitor_accepted_chat_response_stdout
    # Setup the Ollama stream and stream
    ostream = setup_ollama(sysmsg, usermsg, model, params, host)

    try:
        result = run_ostream_via_streamvalve(
            ostream,
            max_linerepeats=3,
            max_lines=200,
            max_linetokens=1000,
            max_paragraphs=20,
            monitor_callback=monitor,
        )
    except ollama.ResponseError as e:
        raise RuntimeError(
            f"Ollama response error: {e}\n\nNo further information available, sorry.",
        ) from e
    except httpx.ConnectError as e:
        machine = "on your computer?" if len(host) == 0 else f"at {host} ?"
        raise RuntimeError(
            f"Connection error: {e}\n\nIs Ollama running {machine}",
        ) from e

    return result["text"]  # type: ignore[no-any-return]
