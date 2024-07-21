"""
Skills: Functions, loops, error handling.
Description: Build a quiz game that asks users multiple-choice questions.
Provide feedback on correct/incorrect answers and keep score.
"""
import requests
import random
import time
import threading

class QuizGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.load_questions()
        self.time_up = False

    def fetch_results(self, amount=5, difficulty=None, category=None):
        url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
        if difficulty:
            url += f"&difficulty={difficulty}"
        if category:
            url += f"&category={category}"
        response = requests.get(url)
        data = response.json()
        return data['results']

    def get_difficulty_and_category(self):
        difficulty = input("Choose difficulty level (easy, medium, hard): ").strip().lower()
        category = input("Enter category ID (leave blank for any category): ").strip()
        return difficulty, category

    def load_questions(self):
        difficulty, category = self.get_difficulty_and_category()
        questions = self.fetch_results(difficulty=difficulty, category=category)
        for q in questions:
            options = [
                q['correct_answer'],
                q['incorrect_answers'][0],
                q['incorrect_answers'][1],
                q['incorrect_answers'][2]
            ]
            
            random.shuffle(options)  # Shuffle the options
            
            formatted_question = {
                "question": q['question'],
                "options": [
                    f"A. {options[0]}",
                    f"B. {options[1]}",
                    f"C. {options[2]}",
                    f"D. {options[3]}"
                ],
                "answer": chr(options.index(q['correct_answer']) + 65)  # Find the correct answer's new position
            }
            self.questions.append(formatted_question)

    def ask_question(self, question):
        def countdown():
            nonlocal timer
            for i in range(timer, 0, -1):
                print(f"Time left: {i} seconds", end='\r')
                time.sleep(1)
            self.time_up = True

        timer = 10  # Set the timer
        self.time_up = False
        thread = threading.Thread(target=countdown)
        thread.start()

        print(question["question"])
        for option in question["options"]:
            print(option)
        
        user_answer = None
        while not self.time_up and user_answer not in ['A', 'B', 'C', 'D']:
            user_answer = input("Your answer (A, B, C, or D): ").strip().upper()
        
        if self.time_up:
            print("\nTime's up!")
            correct_answer = question["answer"]
            print(f"The correct answer was {correct_answer}.\n")
        else:
            correct_answer = question["answer"]
            if user_answer == correct_answer:
                print(f"{correct_answer} is Correct!\n")
                self.score += 1
            else:
                print(f"Incorrect. The correct answer was {correct_answer}.\n")

    def play(self):
        for question in self.questions:
            self.ask_question(question)
        print(f"Your final score is: {self.score}/{len(self.questions)}")

def main():
    game = QuizGame()
    game.play()

if __name__ == "__main__":
    main()







