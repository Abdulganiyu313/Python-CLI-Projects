print("Welcome to the Guessing Game!")
import random
def play_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed_correctly = False
    level = input("Choose difficulty level (easy/medium/hard): ").strip().lower()
   
    while not guessed_correctly:
        try:
            guess = int(input("Guess a number between 1 and 100: "))

            if level == 'easy':
                max_attempts = 10
            elif level == 'medium':
                max_attempts = 7
            elif level == 'hard':
                max_attempts = 5
            else:
                print("Invalid level. Defaulting to easy mode with 10 attempts.")
                max_attempts = 10
            if attempts >= max_attempts:
                print(f"You've reached the maximum attempts of {max_attempts}. The number was {number_to_guess}.")
                return
            if attempts < max_attempts:
                print(f"Attempts left: {max_attempts - attempts}")
                
            if guess < 1 or guess > 100:
                print("Please guess a number between 1 and 100.")
                continue
            attempts += 1
            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                guessed_correctly = True
                print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
if __name__ == "__main__":
    play_game() 
    