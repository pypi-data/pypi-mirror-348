"""Tests for ollama parameter conversion"""

import pytest

from dm_ollamalib.optionhelper import help_long, help_overview, qa_ollama_desc, to_ollama_options

# Pylint ... ignore missing function docstrings
# pylint: disable = C0116

# Ruff ... PLR2004 ignore magic value comparisons


def test_1param_and_int() -> None:
    tests = "num_ctx=8092"
    res = to_ollama_options(tests)
    assert res["num_ctx"] == 8092  # noqa: PLR2004
    assert isinstance(res["num_ctx"], int)


def test_multiparam_and_float() -> None:
    tests = "top_p=0.9;temperature=0.8"
    res = to_ollama_options(tests)
    assert res["top_p"] == 0.9  # noqa: PLR2004
    assert res["temperature"] == 0.8  # noqa: PLR2004


def test_bool() -> None:
    tests = "low_vram=true;logits_all=FALSE"
    res = to_ollama_options(tests)
    assert res["low_vram"] is True
    assert res["logits_all"] is False
    assert isinstance(res["low_vram"], bool)


def test_lststr() -> None:
    tests = "stop=2;stop=blubb"
    res = to_ollama_options(tests)
    assert res["stop"] == ["2", "blubb"]
    assert isinstance(res["stop"], list)
    tmp: list[str] = res["stop"]
    assert isinstance(tmp[0], str)  # pylint: disable=E1136 # sorry pylint, you're wrong


# no str parameters in Ollama atm
# def test_str():

# test adding parameters to existing one


def test_into_existing() -> None:
    res = to_ollama_options("top_p=0.9")
    res = to_ollama_options("temperature=0.8", res)
    assert res["top_p"] == 0.9  # noqa: PLR2004
    assert res["temperature"] == 0.8  # noqa: PLR2004


# test edge cases


def test_empty() -> None:
    to_ollama_options("")
    to_ollama_options("   ")
    to_ollama_options(";  ;")


# tests for help strings
# As difficult to check 'correctness', just check whether
#  num_ctx is present ... will probably be there forever


def test_help_overview() -> None:
    s = help_overview()
    assert "num_ctx : int" in s


def test_help_long() -> None:
    s = help_long()
    assert "num_ctx : int" in s


def test_qa_help() -> None:
    x = qa_ollama_desc()
    assert x == []


# test expected failures


@pytest.mark.parametrize(
    "parameterstr",
    [
        ("ThisParamDoesNotExist=1024"),  # d'oh
        ("low_vram"),  # no =
        ("low_vram=True=Ooops"),  # too many =
        ("lowvram="),  # no value
        ("=1024"),  # no parameter name
        ("low_vram=rue"),  # bool error
        ("num_ctx=0x8000"),  # int error
        ("num_ctx=1.4"),  # int error
        ("top_p=0.9x"),  # float error
    ],
)
def test_paramvalerror(parameterstr: str) -> None:
    with pytest.raises(ValueError):
        to_ollama_options(parameterstr)


def test_paramtypeerror() -> None:
    tests = 5
    with pytest.raises(TypeError):
        to_ollama_options(tests)  # type: ignore[arg-type]  # yes, mypy, that is intentional
