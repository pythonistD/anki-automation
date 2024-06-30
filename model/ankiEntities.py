from dataclasses import dataclass


@dataclass
class AnkiCard:
    title: str
    body: str
    tags: list[str]

    

    