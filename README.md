<div align="center">

# memify

A simple to use flashcard command-line program.

</div>

## Sections

- [Why](#why)
- [Setup](#setup)
- [Formatting Your Flashcards](#formatting-your-flashcards)
    - [Using `.md` Sets](#instructions-for-sets-using-md)
    - [Using `.csv` Sets](#instructions-for-sets-using-csv)
    - [Specify First Card](#specify-a-card-to-always-be-shown-first)
- [Styling Output](#styling-output)

### Why?

- I started to get frustrated with how long it would take me to setup a Quizlet set, or kept losing my handwritten flashcards.
  - really just wanted a **super simple** flashcard program that allowed me to create sets and study the sets with minimal effort. After all, shouldn't that effort be used for the actual studying?!
- I didn't know a thing about Python and wanted to learn. The codebase is very messy because of this...
- Why publish?
  - My sister saw me using it and wanted access. :p


## Setup

In order for `memify` to work you must have a parent directory that holds each class and sets. For example, the structure should look something like this

```
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

## Formatting Your Flashcards

`memify` currently accepts two types of files: `.md` and `.csv`.

### Instructions For Sets Using `.md`

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

### Instructions For Sets Using `.csv`

The format in `.csv` files must be

```
Question, Answer, Question, Answer,...

For example,

What is the capital of France?, Paris, Memify will help me learn **everything**?, true
```

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

***ALL OF THESE EXAMPLES ARE SHOWN IN `.md`, BUT CAN BE USED THE EXACT SAME WAY IN YOUR `.csv` SETS***

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
