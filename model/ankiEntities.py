from dataclasses import dataclass

import genanki

import random


@dataclass
class AnkiCard:
    title: str
    body: str
    tags: list[str]


class Anki:
    def __init__(self) -> None:
        self.anki_model = self.create_model()
        self.anki_deck = self.create_deck()
        self.anki_package = genanki.Package(self.anki_deck)

    def create_model(self):
        model_id = random.randrange(1 << 30, 1 << 31)
        my_model = genanki.Model(
            model_id,
            'Default Model',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Front}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
                },
            ]
        )
        return my_model
    
    def create_deck(self):
        deck_id = random.randrange(1 << 30, 1 << 31)
        my_deck = genanki.Deck(
            deck_id,
            'My Test Deck'
        )
        return my_deck
    
    def add_media_image(self, abs_path_to_image:str):
        self.anki_package.media_files.append(abs_path_to_image)

    def add_bunch_of_media_image(self, abs_path_to_image_list: list[str]):
        if abs_path_to_image_list is not None:
            self.anki_package.media_files.extend(abs_path_to_image_list)

    def generate_anki_package_of_cards(self, name_of_anki_package:str):
        self.anki_package.write_to_file(name_of_anki_package + ".apkg")
        print(f'Колода сохранена как {name_of_anki_package}.apkg')

    def create_anki_card(self, anki_card: AnkiCard):
        card = genanki.Note(model=self.anki_model, fields=[anki_card.title, anki_card.body])
        self.anki_deck.add_note(card)

    def create_bunch_of_cards(self, anki_cards_list: list[AnkiCard]):
        for c in anki_cards_list:
            self.create_anki_card(c)
    