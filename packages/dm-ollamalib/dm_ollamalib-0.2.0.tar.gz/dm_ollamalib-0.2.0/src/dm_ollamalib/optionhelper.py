"""Module with helper functions to easily parse ollama options from a string
as well as dump available options and/or their description to a string."""

import re

# Jan 2025. Weird pylint bug, see https://github.com/pylint-dev/pylint/issues/10112
from textwrap import fill as twfill
from typing import get_type_hints

from ollama import Options as oOptions

# get names of options + types directly from Ollama
OLLAMA_OPTION_TYPES = get_type_hints(oOptions)

# paranoia check ... should never happen except if Ollama library changes drastically
#
if len(OLLAMA_OPTION_TYPES) == 0:
    raise RuntimeError(
        "Something seems to have drastically changed in the Ollama Python library:"
        " typehints of Ollama options has length 0. Sorry, need to abort."
    )  # pragma: nocover


# Descriptions for Ollama options. Would be nice if one could get that interactively
#  from the server, but ... well, that's second best possibility.
#
# taken from https://pypi.org/project/ollama-python/
# ... which had more complete description
# than https://github.com/ollama/ollama/blob/main/docs/modelfile.md :-(((
# Also
#  https://llama-cpp-python.readthedocs.io/en/latest/api-reference/
# and
#  https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html#_chat_properties
# and
#  https://docs.redpanda.com/redpanda-connect/components/processors/ollama_chat/
OLLAMA_OPTION_DESC = {
    "embedding_only": (
        "This option has been removed from Ollama API. See"
        " https://github.com/spring-projects/spring-ai/issues/503"
    ),
    "frequency_penalty": (
        "Positive values penalize new tokens based on the frequency of their appearance in the"
        " text so far. This decreases the model's likelihood to repeat the same line verbatim."
        " Default: 0.0"
        " (Source: Spring AI docs)."
    ),
    "logits_all": (
        "Return logits for all tokens, not just the last token. Must be True for completion to"
        " return logprobs."
        " (Source: llama.cpp API reference)"
    ),
    "main_gpu": (
        "When using multiple GPUs this option controls which GPU is used for small tensors"
        " for which the overhead of splitting the computation across all GPUs is not worthwhile."
        " The GPU in question will use slightly more VRAM to store a scratch buffer for"
        " temporary results."
        " (Source: Spring AI docs)."
        " Might ve currently buggy, see https://github.com/ollama/ollama/issues/6493"
    ),
    "mirostat": (
        "Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled,"
        " 1 = Mirostat, 2 = Mirostat 2.0)"
    ),
    "mirostat_eta": (
        "Influences how quickly the algorithm responds to feedback from the generated text."
        " A lower learning rate will result in slower adjustments, while a higher learning"
        " rate will make the algorithm more responsive. (Default: 0.1)"
    ),
    "mirostat_tau": (
        "Controls the balance between coherence and diversity of the output. A lower value"
        " will result in more focused and coherent text. (Default: 5.0)"
    ),
    "num_ctx": (
        "Sets the size of the context window used to generate the next token. (Default: 2048)"
    ),
    "numa": ("numa policy. (Source: llama.cpp API reference)"),
    "num_batch": ("Prompt processing maximum batch size. Default: 512. (Source: Spring AI docs)"),
    "num_gpu": (
        "The number of layers to send to the GPU(s). On macOS it defaults to 1 to enable metal"
        " support, 0 to disable, -1 to be set dynamically."
        " Default: -1"
    ),
    # Seems to not exist, or has disappeared from Ollama Python?
    #  "num_gqa": (
    #     "The number of GQA groups in the transformer layer. Required for some models, for example"
    #     "it is 8 for llama2:70b"
    # ),
    "num_keep": (
        "Specify the number of tokens from the initial prompt to retain when the model resets"
        " its internal context. Default: 4. Use -1 to retain all tokens from the initial prompt."
        " (Source: Spring AI docs)"
    ),
    "num_predict": (
        "Maximum number of tokens to predict when generating text. (Default: 128,"
        " -1 = infinite generation, -2 = fill context)"
    ),
    "num_thread": (
        "Sets the number of threads to use during computation. By default, Ollama will detect"
        " this for optimal performance. It is recommended to set this value to the number of"
        " physical CPU cores your system has (as opposed to the logical number of cores)."
        " 0 lets the runtime decide."
        " Default: 0"
    ),
    "presence_penalty": (
        "Positive values penalize new tokens if they have appeared in the text so far."
        " This increases the model's likelihood to talk about new topics."
        " Default: 0.0"
        " Source: Redpanda docs"
    ),
    "repeat_last_n": (
        "Sets how far back for the model to look back to prevent repetition. Default: 64,"
        " 0 = disabled, -1 = num_ctx"
    ),
    "repeat_penalty": (
        "Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will"
        " penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more"
        " lenient. Default: 1.1"
    ),
    "seed": (
        "Sets the random number seed to use for generation. Setting this to a specific number will"
        " make the model generate the same text for the same prompt. Default: -1"
    ),
    "stop": (
        "Sets the stop sequences to use. When this pattern is encountered the LLM will stop"
        " generating text and return. Multiple stop patterns may be set by specifying multiple"
        " separate stop options in a modelfile. Default is no entry/empty."
    ),
    "temperature": (
        "The temperature of the model. Increasing the temperature will make the model answer"
        " more creatively. Default: 0.8"
    ),
    "tfs_z": (
        "Option was removed from llama.cpp/ollama, see https://github.com/ollama/ollama/pull/8515"
    ),
    "top_k": (
        "Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more"
        " diverse answers, while a lower value (e.g. 10) will be more conservative. Default: 40"
    ),
    "top_p": (
        "Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text,"
        " while a lower value (e.g., 0.5) will generate more focused and conservative text."
        " Default: 0.9"
    ),
    "typical_p": (
        "The typical-p value to use for sampling. Locally Typical Sampling implementation"
        " described in the paper https://arxiv.org/abs/2202.00666."
        " Default: 0.9."
        " (Source: llama.cpp API reference)"
    ),
    "use_mmap": (
        "By default, models are mapped into memory, which allows the system to load only the"
        " necessary parts of the model as needed. However, if the model is larger than your"
        " total amount of RAM or if your system is low on available memory, using mmap might"
        " increase the risk of pageouts, negatively impacting performance. Disabling mmap"
        " results in slower load times but may reduce pageouts if you're not using mlock. Note"
        " that if the model is larger than the total amount of RAM, turning off mmap would"
        " prevent the model from loading at all."
        " Default: False"
        " (Source: Spring AI docs)"
    ),
    "use_mlock": (
        "Lock the model in memory, preventing it from being swapped out when memory-mapped."
        " This can improve performance but trades away some of the advantages of memory-mapping"
        " by requiring more RAM to run and potentially slowing down load times as the model"
        " loads into RAM."
        " (Source: Spring AI docs)"
    ),
    "vocab_only": ("Only load the vocabulary, not the weights. (Source: llama.cpp API reference)"),
}


def qa_ollama_desc() -> list[str]:
    """QA function, only for running tests. Checks whether all keys of
    OLLAMA_OPTION_DESC also exist in the current Ollama options
    Returns empty list if all ok, else list contains keys of OLLAMA_OPTION_DESC
    which should not exist."""
    retval: list[str] = [x for x in OLLAMA_OPTION_DESC if x not in OLLAMA_OPTION_TYPES]
    return retval


def help_overview() -> str:
    """Convenience. Create a string showing name and type of supported Ollama options."""

    collection = _collect_ollama_options()
    max_namelen = len(max(collection, key=lambda x: len(x[0]))[0]) + 3

    mtext = "(multiple)"
    tlist: list[str] = []
    for pname, ptype, multiple in collection:
        ms = "" if not multiple else mtext
        tlist.append(f"{pname:>{max_namelen}} : {ptype:<6} {ms}")
    return "\n".join(tlist)


def help_long() -> str:
    """Convenience. Create a string showing name, type and description of supported Ollama
    options.
    Note: The description text for options is not present in the Ollama Python module,
    some options even have no good description online at all.
    """
    collection = _collect_ollama_options()
    tlist: list[str] = []
    tlist.append("""This documentation was scraped together from the following sources:
- https://pypi.org/project/ollama-python/
- https://github.com/ollama/ollama/blob/main/docs/modelfile.md
- https://llama-cpp-python.readthedocs.io/en/latest/api-reference/
- https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html#_chat_properties
- https://docs.redpanda.com/redpanda-connect/components/processors/ollama_chat/
""")
    mtext = "(multiple)"
    for pname, ptype, multiple in collection:
        ms = "" if not multiple else mtext
        tlist.append(f"{pname} : {ptype} {ms}")
        if pname in OLLAMA_OPTION_DESC:
            tlist.append(twfill(OLLAMA_OPTION_DESC[pname]))
        else:
            tlist.append("This parameter seems to be new, or not described in docs as of May 2025.")
        tlist.append("")
    return "\n".join(tlist)


def _collect_ollama_options() -> list[tuple[str, str, bool]]:
    collection: list[tuple[str, str, bool]] = []
    pnames = sorted(OLLAMA_OPTION_TYPES.keys())
    for pname in pnames:
        ptype = OLLAMA_OPTION_TYPES[pname]
        match = re.search(r"\[(.*?)\]$", str(ptype))
        multiple = False
        if match:
            ptype = match.group(1)
            match = re.search(r"\[(.*?)\]$", ptype)
            if match:
                ptype = match.group(1)
                multiple = True
        collection.append((pname, ptype, multiple))
    return collection


# ruff complains about too many branches and too many statements
# ... that's life when checking validity of user input
def to_ollama_options(params: str, oopt: oOptions | None = None) -> oOptions:  # noqa: PLR0912, PLR0915
    """Transform a string with semicolon separated Ollama options to dict.

    The Python Ollama library wants the Ollama options as correct Python types in a dict,
    i.e., one cannot use strings. This functions transforms any string with
    Ollama options into a dict with correct types.
    Ollama uses a TypedDict, the dict[str, Any] returned by this function is compatible.

    Arguments:
    - options: Either str or Iterable[str]. E.g. "num_ctx=8092;temperature=0.8"

    Exceptions raised:
    - ValueError for
        - unrecognised Ollama options
        - conversion errors of a string to required type (int, float, bool)
        - incomplete options (e.g. "num_ctx=" or "=8092")
        - unknown Ollama options
    - RuntimeError if Ollama Python library has unexpected parameter types not handled
      by this function (should not happen, except if Ollama devs implemented something new)
    """

    def _check_pname_pval(pn: str, pv: str) -> None:
        """Factored out as inner function to circumvent pylint R0912 (too many branches)"""
        if len(pn) == 0:
            raise ValueError("Ollama parameter (left of equal sign) is empty")
        if len(pv) == 0:
            raise ValueError(f"Ollama parameter '{pn}' is empty (nothing right of equal sign)")
        if pn not in OLLAMA_OPTION_TYPES:
            known = ", ".join(sorted(OLLAMA_OPTION_TYPES.keys()))
            raise ValueError(f"Unknown ollama parameter '{pn}'. Known options:\n{known}")

    # yes, pylance, params SHOULD always be a string. But what if the user didn't care?
    # Allow to_ollama_options to oint in the right direction
    if not isinstance(params, str):  # pyright: ignore
        raise TypeError(f"params should be a str, but is a {type(params)}")

    if oopt is None:
        oopt = oOptions()

    for semsplit in params.split(";"):
        plist = [x.strip() for x in semsplit.split("=")]

        # Check syntactic validity of this parameter:
        # there must be an equal sign and a left and a right side.

        if len(plist) == 1 and len(plist[0]) == 0:
            continue  # no = sign but empty string ... let that pass
        if len(plist) < 2:  # noqa: PLR2004
            raise ValueError(f"Missing an equal sign ('=') in '{semsplit}'")
        if len(plist) > 2:  # noqa: PLR2004
            raise ValueError(f"Found more than one equal sign ('=') in '{semsplit}'")

        pname, pval = plist
        _check_pname_pval(pname, pval)

        # Argh! match cannot directly match types.
        # Going via the string representation is ... ugly

        ptype = str(OLLAMA_OPTION_TYPES[pname])
        match ptype:
            case "typing.Optional[int]":
                try:
                    oopt[pname] = int(pval)
                except ValueError as e:
                    raise ValueError(
                        f"Ollama parameter '{pname}' expected an int, got '{{pval}}'\n{{e}}"
                    ) from e
            case "typing.Optional[float]":
                try:
                    oopt[pname] = float(pval)
                except ValueError as e:
                    raise ValueError(
                        f"Ollama parameter '{pname}' expected a float, got '{pval}'"
                    ) from e
            case "typing.Optional[bool]":
                pval = pval.lower()
                if pval == "false":
                    oopt[pname] = False
                elif pval == "true":
                    oopt[pname] = True
                else:
                    raise ValueError(
                        f"Ollama parameter '{pname}' expected 'true' or 'false', got '{pval}'"
                    )
            case "typing.Optional[typing.Sequence[str]]":
                if pname in oopt:
                    oopt[pname].append(str(pval))
                else:
                    oopt[pname] = [str(pval)]
            case "typing.Optional[str]":  # pragma: nocover
                # currently not used by the Ollama Python module, but easy to be prepared
                oopt[pname] = str(pval)
            case _:  # pragma: nocover
                raise RuntimeError(
                    "Type Ollama uses not yet handled!"
                    f" Parameter type '{OLLAMA_OPTION_TYPES[pname]}' for '{pname}'."
                )
    return oopt
