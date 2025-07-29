from typing import Union, Sequence, List, Any, TypedDict

try:
    from gruut import sentences as gruut_sentences  # type: ignore

    _has_gruut = True
except ModuleNotFoundError:
    _has_gruut = False


class Word(TypedDict):
    """Processed word from a Sentence"""

    idx: int
    """Zero-based index of sentence"""

    text: str = ""
    """Text with normalized whitespace"""

    text_with_ws: str = ""
    """Text with original whitespace"""
    
    phonemes: str = ""
    """phonemes as string"""

    phonemes_list: List[str] = []
    """List of phonemes"""


def run(
    entry: Union[str, Sequence[str]],
    lang: str = "en_US",
    ssml: bool = False,
    major_breaks: bool = True,
    minor_breaks: bool = True,
    punctuations: bool = True,
    explicit_lang: bool = True,
    break_phonemes: bool = True,
    pos: bool = True,
    **process_kwargs: Any,
) -> List[Word]:
    """Phonemizes the given texts using gruut if available.
    example usage:
    ```python
    from gr1336_toolbox import phonemizer

    phonemized_text = phonemizer.run("Hello, how are you?")[0]["phonemes"] 
    print(phonemized_text) # hɛlˈoʊ|hˈaʊˈɑɹjˈu‖
    """
    assert (
        _has_gruut
    ), "You must have gruut installed to used this feature! (pip install gruut)"
    assert isinstance(entry, (str, list, tuple)), f"Invalid entry type: {type(entry)}"
    if not entry:
        return []
    if isinstance(entry, str):
        entry = [entry]
    results: List[Word] = []
    gruut_kwargs = {
        "lang": lang,
        "ssml": ssml,
        "major_breaks": major_breaks,
        "minor_breaks": minor_breaks,
        "punctuations": punctuations,
        "explicit_lang": explicit_lang,
        "phonemes": True,
        "break_phonemes": break_phonemes,
        "pos": pos,
        **process_kwargs,
    }
    gruut_kwargs.pop("text", None)
    for text in entry:
        if not text.strip():
            continue
        cur_sent = Word(
            idx=len(results),
            phonemes="",
            phonemes_list=[],
            text="",
            text_with_ws="",
        )

        for sent in gruut_sentences(text, **gruut_kwargs):
            for word in sent:
                if word.phonemes:
                    results_pho = "".join(word.phonemes)
                    cur_sent["phonemes"] += results_pho
                    cur_sent["phonemes_list"].append(results_pho)
                    cur_sent["text"] += word.text
                    cur_sent["text_with_ws"] += word.text_with_ws
        results.append(cur_sent)
    return results
