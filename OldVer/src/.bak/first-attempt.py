#!/usr/bin/env python

import re
import sys

class Flashcard:
    incorrect_answers = []

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    @classmethod
    def flashcard_quiz(cls):
        num_correct = 0
        num_wrong = 0

        print("Welcome to the Flashcard Quiz!\n")
        for card in cls.parse_markdown(sys.argv[1]):
            print("Question:", card.question)
            user_answer = input("Your answer: ").strip().lower()
            if user_answer == card.answer.lower():
                print("Correct!")
                num_correct += 1
            else:
                print("Incorrect. The correct answer is:", card.answer)
                cls.incorrect_answers.append(card.answer)
                num_wrong += 1
            print() 

        print("Quiz completed!")
        print("Number of correct answers:", num_correct)
        print("Number of incorrect answers:", num_wrong)

    @classmethod
    def parse_markdown(cls, filename):
        flashcards = []
        with open(filename, 'r') as file:
            markdown_text = file.read()

        current_question = None
        current_answer = None
        for line in markdown_text.split('\n'):
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                if level == 1:
                    current_question = title
                elif level == 2:
                    current_answer = title
            if current_answer and current_question:
                flashcards.append(Flashcard(current_question, current_answer))
                current_answer = None

        return flashcards
def print_rounded_box(content):
    lines = content.split('\n')
    max_length = max(len(line) for line in lines)
    
    print('╭' + '─' * (max_length + 2) + '╮')
    for line in lines:
        print('│ ' + line.ljust(max_length) + ' │')
    print('╰' + '─' * (max_length + 2) + '╯')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py markdown_file.md")
        sys.exit(1)
    Flashcard.flashcard_quiz()
