<div align="center">

# memify

A simple to use flashcard command-line program.

</div>

### Why?

- I was spending more time setting up Quizlet than studying so I wanted a simpler solution.
- Why publish?
  - My sister saw me using it and wanted access. :p

## Installation

**Clone the repo**

```bash
git clone git@github.com:clamsfeel2/memify.git
cd memify
```

With [pipx](https://pipx.pypa.io/) -- *what I use*:

```bash
pipx install .
```

You can now run `memify -h` from **anywhere**.

With [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv venv       # Create virtual environment
uv sync       # Install dependencies
uv run memify # Run memify
```

With [Poetry](https://python-poetry.org/)

```bash
poetry install
poetry run memify # Run from poetry shell
ln -s "$(poetry env info --path)/bin/memify" /somewhere/in/your/path/gb # Symlink to somewhere in your path instead
```

> [!NOTE]
> `memify` will **not** be available globally unless you use `poetry run`.
>
> If you want the command globally without `poetry run`, use `pipx` or `uv` instead.

## Setup

In order for `memify` to work you must have a parent directory that holds each class and sets. For example, the structure should look something like this

```
Flashcards
├── Math
│   └── notes.md
├── CS
│   └── bash_test_cmd.md
└── English
    └── reading_cards.md
```

>[!IMPORTANT]
> You **must** set `FLASHCARD_SETS_PATH` environment variable to the full path to your sets.
> So for above `FLASHCARD_SETS_PATH` would be set as the full path to `Flashcards`.

## Formatting Your Flashcards

```
Anything following '#' will be considered a `Question`

Anything following '##' will be considered an `Answer`

EXAMPLE:

# What is the capital of France?
## Paris

OR

# What is the capital of France

some other text

more random text

## Paris
```

***Just remember that a Question (a single `#`) must be followed by an Answer (a double `##`). So, this will result in an error***

```
# What is the capital of France?
# Paris

OR

## What is the capital of France?

other text

## Paris
```

Anything else within your `.md` set files will be ignored, so theoretically you could fill these sets with notes and have your questions and answers scattered throughout the notes, so you may study and then test yourself on key concepts all from the same file!

***You may have linebreaks and you may omit whitespace***

### Specify A Card To Always Be Shown First

`memify` will always randomize the cards within your sets. If you want a set to **always** start with a certain card for instructions or whatever reason begin the question with `FIRST_CARD` for example

```
# FIRST_CARD What is the capital of France?
## Paris
```

## Styling Output

>[!WARNING]
> As a general rule: **do not** apply any of these to your answers or else you will have a bad time in `memify --quiz`

`memify` supports the following markdown syntax with a few of my own modifications...

```
# *This will be italics*
## **This will be bold**

# ~~This will be crossed out~~
## __This text will be underlined__
```

If you want to insert a newline in your output you may use `\n`. For example this

```
# What is the capital of France?\na) Paris.\nb)Denver.\nc)Copenhagen.
## a
```

Will be output as

```
What is the capital of France?
a) Paris.
b) Denver.
c) Copenhagen.
```

## Usage

```
usage: main.py [-h] [-s [f/flipped]] [-q] [-r] [-p PATH]

options:
  -h, --help            show this help message and exit
  -s [f/flipped], --study [f/flipped]
                        choose a flashcard set to study. Supply 'f or flipped' argument to start the cards with the back 'up'.
  -q, --quiz            choose a flashcard set to quiz yourself on.
  -r, --remove-incorrect
                        remove all incorrect sets.
  -p PATH, --path PATH  specify full path to file which holds a set.
```

## Roadmap

- [x] Add option to display back of cards first.
- [ ] Ability to choose which incorrect sets to remove rather than every single one.
- [ ] Add `to_practice` category, where all the questions missed by 3 nums or 1 letter go.
- [ ] Use a config file to default certain options so you don't need to rely on cli args.
- [ ] Implement spaced repetition algorithm.
