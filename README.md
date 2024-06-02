<div align="center">

# memify

A simple to use flashcard command-line program.

</div>

### Why?

- I started to get frustrated with how long it would take me to setup a Quizlet set, or kept losing my handwritten flashcards.
  - really just wanted a **super simple** flashcard program that allowed me to create sets and study the sets with minimal effort. After all, shouldn't that effort be used for the actual studying?!
- I didn't know a thing about Python and wanted to learn. The codebase is very messy because of this...
- Why publish?
  - My sister saw me using it and wanted access. :p

In order for `memify` to work you must have a parent directory that holds each class and sets. For example, the structure should look something like this

```bash
Flashcards
├── Math
│   └── notes.md
├── CS
│   └── bash_test_cmd.md
└── English
    └── zara_class.md
```

>[!IMPORTANT]
> You **must** set `FLASHCARD_SETS_PATH` environment variable to the full path to your sets.
> So for above `FLASHCARD_SETS_PATH` would be set as the full path to `Flashcards`.

Any file ending with `.md` will be considered a set, and `memify` will prompt you to choose a set to use. 

**If a file does not end in `.md` it will be ignored.**

Anything else within your set files will be ignored, so theoretically you could fill your sets with notes and have your questions and answers scattered throughout the notes, so you may study and then test yourself on key concepts all from the same file!

The format in which to create flashcards is

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

```bash
# What is the capital of France?
# Paris

OR

## What is the capital of France?

other text

## Paris
```

`memify` will always randomize the cards within your sets. If you want a set to **always** start with a certain card for instructions or whatever reason begin the question with `FIRST_CARD` for example

```bash
# FIRST_CARD What is the capital of France?
## Paris
```

If you want to insert a newline in your output you may use `\n`. `memify` is not yet regex compliant, but it understands `\n`.

## Usage

```bash
USAGE: memify [flag]
-h, --help            show this help message and exit
-s, --study           choose a flashcard set to study.
-q, --quiz            choose a flashcard set to quiz yourself on.
-f FILEPATH, --filepath FILEPATH
                      specify full path to file which holds a set.
```

## Roadmap

- [ ] Add `to_practice` category, where all the questions missed by 3 nums or 1 letter go.
