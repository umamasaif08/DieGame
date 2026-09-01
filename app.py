import random
import time

# Define the ASCII art faces for a 6-sided die
dice_faces = {
    1: [" ----- ", "|     |", "|  o  |", "|     |", " ----- "],
    2: [" ----- ", "| o   |", "|     |", "|   o |", " ----- "],
    3: [" ----- ", "| o   |", "|  o  |", "|   o |", " ----- "],
    4: [" ----- ", "| o o |", "|     |", "| o o |", " ----- "],
    5: [" ----- ", "| o o |", "|  o  |", "| o o |", " ----- "],
    6: [" ----- ", "| o o |", "| o o |", "| o o |", " ----- "]
}

print("Rolling the dice...")
time.sleep(1)  # Adds a cool dramatic pause

# Generate two random dice numbers
die1 = random.randint(1, 6)
die2 = random.randint(1, 6)

# Print the dice side-by-side
print(f"\nYou rolled a {die1} and a {die2}!")
for i in range(5):
    print(dice_faces[die1][i] + "   " + dice_faces[die2][i])
