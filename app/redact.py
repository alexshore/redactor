from typing import Any
from json import load, dump
from bs4 import BeautifulSoup
import spacy

NLP = spacy.load("en_core_web_sm")
NLP.add_pipe("merge_entities")


def redact_html(data: str) -> str:
    soup = BeautifulSoup(data, "html.parser")
    for text in soup.findAll(string=True):
        text.replaceWith(redact_str(str(text)))
    return str(soup)


def redact_str(data: str):
    doc = NLP(data)
    # probably shouldn't be done with a 1-liner
    redacted = ["REDACTED" if token.ent_type_ == "PERSON" else token.text for token in doc]
    return " ".join(redacted)


def redact_json(data: Any) -> any:
    match data:
        case dict():
            return {key: redact_json(val) for key, val in data.items()}
        case list():
            return [redact_json(elem) for elem in data]
        case str() if BeautifulSoup(data, "html.parser").find():
            return redact_html(data)
        case str():
            return redact_str(data)
        case _:
            return data


def main():
    with open("example.json", "r") as file:
        data = load(file)

    redacted = redact_json(data)

    with open("redacted.json", "w") as file:
        dump(redacted, file)


if __name__ == "__main__":
    main()
