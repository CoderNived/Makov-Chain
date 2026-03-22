"""
example_data.py
---------------
A collection of pre-built Markov Chain transition matrices to experiment with.

Each example comes with:
- A description of what it models
- The transition dictionary
- Optional: state emoji for display
- Notes on interesting behaviour to look for

These are all hand-crafted toy models, not learned from real data.
They are designed to illustrate different properties of Markov Chains.

Usage:
    from example_data import WEATHER_MODEL, CUSTOMER_JOURNEY, MOOD_MODEL
"""


# =============================================================================
# EXAMPLE 1: Weather Model (the main project model)
# =============================================================================

WEATHER_MODEL = {
    "name": "Weather Model",

    "description": (
        "A simple 3-state weather model. Each day is Sunny, Cloudy, or Rainy. "
        "Tomorrow's weather depends only on today's weather. "
        "\nInteresting: watch how the system converges to roughly 48% Sunny, "
        "29% Cloudy, 24% Rainy regardless of where you start."
    ),

    # The transition matrix
    # Read each row as: "If I am in state X today, tomorrow I go to..."
    "transitions": {
        "Sunny":  {"Sunny": 0.70, "Cloudy": 0.20, "Rainy": 0.10},
        "Cloudy": {"Sunny": 0.30, "Cloudy": 0.40, "Rainy": 0.30},
        "Rainy":  {"Sunny": 0.20, "Cloudy": 0.30, "Rainy": 0.50},
    },

    # Optional emoji for visual display
    "emoji": {
        "Sunny": "☀️",
        "Cloudy": "⛅",
        "Rainy": "🌧️",
    }
}


# =============================================================================
# EXAMPLE 2: Traffic Light
# =============================================================================

TRAFFIC_LIGHT = {
    "name": "Traffic Light",

    "description": (
        "A deterministic (no randomness) 3-state Markov Chain. "
        "Each transition has probability 1.0. "
        "\nInteresting: this chain is periodic (period 3). "
        "It will never reach a stationary distribution — "
        "it just cycles forever: Red → Green → Yellow → Red → ..."
    ),

    "transitions": {
        "Red":    {"Red": 0.00, "Green": 1.00, "Yellow": 0.00},
        "Green":  {"Red": 0.00, "Green": 0.00, "Yellow": 1.00},
        "Yellow": {"Red": 1.00, "Green": 0.00, "Yellow": 0.00},
    },

    "emoji": {
        "Red": "🔴",
        "Green": "🟢",
        "Yellow": "🟡",
    }
}


# =============================================================================
# EXAMPLE 3: Customer Journey (with absorbing states)
# =============================================================================

CUSTOMER_JOURNEY = {
    "name": "Customer Journey Model",

    "description": (
        "A model of how a customer moves through a shopping website. "
        "'Purchased' and 'Exit' are absorbing states — once reached, "
        "the customer never leaves them (in this model). "
        "\nInteresting: no matter where a customer starts, they will "
        "eventually either Purchase or Exit. Try running a long simulation "
        "and see how often they end up in each absorbing state."
    ),

    "transitions": {
        "Browsing":  {
            "Browsing":  0.50,
            "Cart":      0.30,
            "Exit":      0.20,
        },
        "Cart":  {
            "Browsing":  0.20,
            "Cart":      0.30,
            "Checkout":  0.30,
            "Exit":      0.20,
        },
        "Checkout":  {
            "Cart":      0.10,
            "Purchased": 0.70,
            "Exit":      0.20,
        },
        "Purchased": {
            "Purchased": 1.00,  # Absorbing state — once purchased, stays purchased
        },
        "Exit": {
            "Exit": 1.00,       # Absorbing state — once exited, stays exited
        },
    },

    "emoji": {
        "Browsing":  "👀",
        "Cart":      "🛒",
        "Checkout":  "💳",
        "Purchased": "✅",
        "Exit":      "🚪",
    }
}


# =============================================================================
# EXAMPLE 4: Mood Model (simple 2-state)
# =============================================================================

MOOD_MODEL = {
    "name": "Mood Model",

    "description": (
        "A simple 2-state model of a person's daily mood. "
        "\nInteresting: this is the same model worked through in MATH_INTUITION.md. "
        "Stationary distribution: Happy ≈ 75%, Sad ≈ 25%. "
        "Notice how even if you start Sad, you quickly converge to mostly Happy."
    ),

    "transitions": {
        "Happy": {"Happy": 0.80, "Sad": 0.20},
        "Sad":   {"Happy": 0.60, "Sad": 0.40},
    },

    "emoji": {
        "Happy": "😊",
        "Sad":   "😔",
    }
}


# =============================================================================
# EXAMPLE 5: Board Game Movement
# =============================================================================

BOARD_GAME = {
    "name": "Board Game Squares (4-state)",

    "description": (
        "A simplified board game with 4 squares (A, B, C, D). "
        "A dice roll moves you to adjacent squares with given probabilities. "
        "\nInteresting: notice that from Square_A you can only go forward, "
        "while Square_C lets you go backward to A. This creates an "
        "interesting asymmetric flow in the stationary distribution."
    ),

    "transitions": {
        "Square_A": {"Square_A": 0.20, "Square_B": 0.50, "Square_C": 0.20, "Square_D": 0.10},
        "Square_B": {"Square_A": 0.10, "Square_B": 0.30, "Square_C": 0.40, "Square_D": 0.20},
        "Square_C": {"Square_A": 0.30, "Square_B": 0.20, "Square_C": 0.30, "Square_D": 0.20},
        "Square_D": {"Square_A": 0.20, "Square_B": 0.30, "Square_C": 0.30, "Square_D": 0.20},
    },

    "emoji": {
        "Square_A": "🟦",
        "Square_B": "🟩",
        "Square_C": "🟨",
        "Square_D": "🟥",
    }
}


# =============================================================================
# EXAMPLE 6: A Broken (Invalid) Model — for testing validation
# =============================================================================

BROKEN_MODEL = {
    "name": "Broken Model (Invalid — for testing)",

    "description": (
        "This model has an error: the 'Cloudy' row sums to 0.95, not 1.0. "
        "Trying to create a MarkovChain from this will raise a ValueError. "
        "\nTry: mc = MarkovChain(BROKEN_MODEL['transitions']) "
        "and see the error message."
    ),

    "transitions": {
        "Sunny":  {"Sunny": 0.70, "Cloudy": 0.20, "Rainy": 0.10},
        "Cloudy": {"Sunny": 0.25, "Cloudy": 0.45, "Rainy": 0.25},  # sums to 0.95 — INVALID
        "Rainy":  {"Sunny": 0.20, "Cloudy": 0.30, "Rainy": 0.50},
    },
}


# =============================================================================
# CONVENIENCE: All valid examples in a list for easy iteration
# =============================================================================

ALL_EXAMPLES = [
    WEATHER_MODEL,
    TRAFFIC_LIGHT,
    CUSTOMER_JOURNEY,
    MOOD_MODEL,
    BOARD_GAME,
]