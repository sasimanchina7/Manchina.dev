import random

choices = ("rock", "paper", "scissors")
emojis = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}

while True:
    user_choice = input("Enter rock, paper or scissors?:").lower()
    if user_choice not in choices:
        print("Invalid choice. Please choose Rock, Paper, or Scissors.")
        continue

    computer_choice = random.choice(choices)

    print(f"You choose: {emojis[user_choice]}")
    print(f"Computer chooses: {emojis[computer_choice]}")

    if user_choice == computer_choice:
        print("It's a tie!")
    elif (
        (user_choice == "rock" and computer_choice == "scissors") or
        (user_choice == "paper" and computer_choice == "rock") or
        (user_choice == "scissors" and computer_choice == "paper")):
        print("You win!")
    else:
        print("You lose!")

    sould_continue = input("Do you want to play again? (yes/no): ").lower()

    if sould_continue == "no":
            print("Thanks for playing!")
            break
