import genanki

# Модель карточки, поддерживающая изображения
my_model = genanki.Model(
    1607392320,
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

# Создание колоды
my_deck = genanki.Deck(
    2059400111,
    'My Test Deck'
)

# Добавление карточек с изображениями
note1 = genanki.Note(
    model=my_model,
    fields=[
        'What is this?',
        'This is a cat.<br><img src="cat.jpg">'
    ]
)
my_deck.add_note(note1)

note2 = genanki.Note(
    model=my_model,
    fields=[
        'What is this?',
        'This is a dog.<br><img src="dog.jpg">'
    ]
)
my_deck.add_note(note2)

# Создание пакета и добавление изображений
my_package = genanki.Package(my_deck)
my_package.media_files = [
    'images/cat.jpg',
    'images/dog.jpg',
]

# Сохранение пакета в файл .apkg
my_package.write_to_file('my_image_deck.apkg')

print('Колода с изображениями сохранена как my_image_deck.apkg')
