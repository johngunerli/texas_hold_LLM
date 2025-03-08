import random
import os
from itertools import combinations
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq()

# Define the card deck
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]

# Hand ranking helper
hand_ranks = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10,
}


def deal_cards(deck, num):

    return [deck.pop() for _ in range(num)]


def get_hand_rank(hand):

    values = sorted([ranks.index(card.split()[0]) for card in hand], reverse=True)
    suits = [card.split()[-1] for card in hand]
    unique_values = set(values)

    is_flush = len(set(suits)) == 1
    is_straight = len(unique_values) == 5 and max(values) - min(values) == 4

    if is_flush and is_straight:
        return "Royal Flush" if max(values) == ranks.index("A") else "Straight Flush"
    elif len(unique_values) == 2:
        return "Four of a Kind" if values.count(values[0]) in [4, 1] else "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif any(values.count(v) == 3 for v in unique_values):
        return "Three of a Kind"
    elif len(unique_values) == 3:
        return "Two Pair"
    elif len(unique_values) == 4:
        return "One Pair"
    return "High Card"


def get_computer_advice(player_hand, community_cards):

    messages = [
        {
            "role": "system",
            "content": "You are a poker strategy assistant providing advice on the best move.",
        },
        {
            "role": "user",
            "content": f"My hand: {player_hand}. Community cards: {community_cards}. What should I do?",
        },
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response


def play_poker():

    global deck
    random.shuffle(deck)

    player_chips = 100
    computer_chips = 100
    pot = 0

    use_llm = input("Would you like AI hints? (yes/no): ").strip().lower() == "yes"

    while player_chips > 0 and computer_chips > 0:
        print("\nNew round starts!")
        player_hand = deal_cards(deck, 2)
        computer_hand = deal_cards(deck, 2)
        community_cards = deal_cards(deck, 3)  # Flop

        print(f"Your hand: {player_hand}")
        print(f"Community cards: {community_cards}")

        if use_llm:
            advice = get_computer_advice(player_hand, community_cards)
            print("Advice:", advice)

        action = input("Do you want to (fold/call/raise)? ").strip().lower()

        if action == "raise":
            bet = int(input("How much do you want to raise? "))
            pot += bet * 2
            player_chips -= bet
            computer_chips -= bet
        elif action == "call":
            pot += 20  # Default bet size
            player_chips -= 10
            computer_chips -= 10
        elif action == "fold":
            print("You folded! Computer wins the pot.")
            computer_chips += pot
            pot = 0
            continue

        community_cards += deal_cards(deck, 2)
        print(f"Updated community cards: {community_cards}")

        computer_action = random.choice(["fold", "call", "raise"])
        print(f"Computer chooses to {computer_action}.")

        if computer_action == "fold":
            print("Computer folds! You win the pot.")
            player_chips += pot
            pot = 0
            continue
        elif computer_action == "call":
            print("Computer calls.")
        elif computer_action == "raise":
            computer_bet = 20  # Fixed raise amount
            pot += computer_bet * 2
            computer_chips -= computer_bet
            player_chips -= computer_bet
            print(f"Computer raises {computer_bet} chips.")

        player_best = get_hand_rank(player_hand + community_cards)
        computer_best = get_hand_rank(computer_hand + community_cards)
        print(f"Your best hand: {player_best}")
        print(f"Computer's best hand: {computer_best}")

        if hand_ranks[player_best] > hand_ranks[computer_best]:
            print("You win the pot!")
            player_chips += pot
        else:
            print("Computer wins the pot!")
            computer_chips += pot

        pot = 0
        print(f"Your chips: {player_chips}, Computer chips: {computer_chips}")

    print("Game over! You" + (" won!" if player_chips > 0 else " lost."))


if __name__ == "__main__":
    play_poker()
