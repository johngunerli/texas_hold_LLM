# Texas Hold LLM

A command-line implementation of Texas Hold'em Poker with an AI-powered advisor using the Groq LLM API.

## Features

- Single player game against a computer opponent
- AI-powered advice system using Groq LLM
- Complete poker hand evaluation (Royal Flush to High Card)
- Chip-based betting system
- Standard Texas Hold'em gameplay mechanics

## Requirements

- Python 3.x
- `groq` Python package
- `python-dotenv`

## Setup

1. Install required packages:

```bash
pip install groq python-dotenv
```

2. Create a `.env` file with your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

## How to Play

1. Run the game:

```bash
python main.py
```

2. Choose whether you want AI hints
3. Each round:
   - View your hand and community cards
   - Choose to fold, call, or raise
   - If AI hints are enabled, receive strategic advice
   - See the final hands and winner

## Game Rules

- Each player starts with 100 chips
- Standard Texas Hold'em hand rankings apply
- The game continues until one player runs out of chips
- Default bet size is 10 chips for calls
- Raises can be any amount within your chip stack

## Hand Rankings (highest to lowest)

1. Royal Flush
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. One Pair
10. High Card
