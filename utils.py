"""
utils.py
--------
Helper functions for displaying, validating, and analysing Markov Chains.

These are utility functions — they don't add new logic, they make
things easier to read and display. Think of them as the "formatting
and display" layer of our project.

Functions in this file:
    - print_transition_matrix()  → display the matrix as a table
    - print_distribution()       → display a probability distribution
    - compare_distributions()    → side-by-side comparison of two dists
    - print_path()               → display a simulation path
    - check_row_sums()           → quick sanity check
    - bar_chart()                → simple ASCII bar chart
"""


def print_transition_matrix(transitions, title="Transition Matrix"):
    """
    Print the transition matrix as a neat, aligned table.

    Parameters
    ----------
    transitions : dict of dict
        The transition dictionary from a MarkovChain.
    title : str
        A title to display above the matrix.

    Example output:
        Transition Matrix
        ─────────────────────────────────
                   Sunny   Cloudy   Rainy
        Sunny      0.700    0.200   0.100
        Cloudy     0.300    0.400   0.300
        Rainy      0.200    0.300   0.500
    """
    states = sorted(transitions.keys())
    col_width = 8  # Width of each column

    print(f"\n{title}")
    print("─" * (len(title) + 10))

    # Print column headers (destination states)
    header = " " * (col_width + 2)  # Indent for row labels
    for s in states:
        header += s.rjust(col_width)
    print(header)

    # Print each row
    for from_state in states:
        row_str = from_state.ljust(col_width + 2)  # Row label
        for to_state in states:
            # Get the probability, defaulting to 0.0 if not defined
            prob = transitions[from_state].get(to_state, 0.0)
            row_str += f"{prob:.3f}".rjust(col_width)
        print(row_str)

    print()  # Blank line after matrix


def print_distribution(distribution, title="Distribution", sort=True):
    """
    Print a probability distribution as a percentage breakdown.

    Parameters
    ----------
    distribution : dict
        A dictionary mapping state names to probabilities.
    title : str
        A title for the display.
    sort : bool
        If True, sort states alphabetically for consistent display.

    Example output:
        Distribution
        ─────────────────────
        Sunny     47.60%
        Cloudy    28.60%
        Rainy     23.80%
    """
    print(f"\n{title}")
    print("─" * max(len(title) + 10, 30))

    states = sorted(distribution.keys()) if sort else list(distribution.keys())

    for state in states:
        prob = distribution[state]
        # Show as percentage with 2 decimal places
        print(f"  {state:<15} {prob * 100:.2f}%")

    # Verify the distribution sums to 1
    total = sum(distribution.values())
    print(f"  {'─'*20}")
    print(f"  {'Total':<15} {total * 100:.2f}%")
    print()


def compare_distributions(dist1, dist2, label1="Distribution 1",
                          label2="Distribution 2", title="Comparison"):
    """
    Print two distributions side by side for comparison.

    Useful for comparing:
    - Empirical (simulation) vs. Theoretical (power iteration) distributions

    Parameters
    ----------
    dist1 : dict
        First distribution.
    dist2 : dict
        Second distribution.
    label1 : str
        Name for the first distribution.
    label2 : str
        Name for the second distribution.
    title : str
        A title for the comparison table.

    Example output:
        Comparison
        ─────────────────────────────────────────────────────
        State            Empirical     Theoretical   Difference
        Sunny            47.30%        47.60%        -0.30%
        Cloudy           28.60%        28.60%         0.00%
        Rainy            24.10%        23.80%        +0.30%
    """
    print(f"\n{title}")
    print("─" * 56)

    # Header row
    print(f"  {'State':<15} {label1:>13} {label2:>13}  {'Diff':>8}")
    print(f"  {'─'*14} {'─'*12} {'─'*12}  {'─'*8}")

    states = sorted(dist1.keys())

    for state in states:
        p1 = dist1.get(state, 0.0)
        p2 = dist2.get(state, 0.0)
        diff = p1 - p2
        sign = "+" if diff >= 0 else ""
        print(f"  {state:<15} {p1*100:>12.2f}% {p2*100:>12.2f}%  "
              f"{sign}{diff*100:>6.2f}%")

    print()


def print_path(path, states_emoji=None):
    """
    Print the simulation path step by step.

    Parameters
    ----------
    path : list
        List of states from a simulation (e.g. ["Sunny", "Cloudy", "Rainy"]).
    states_emoji : dict, optional
        Optional dictionary mapping state names to emoji for display.
        Example: {"Sunny": "☀️", "Cloudy": "⛅", "Rainy": "🌧️"}

    Example output (with emoji):
        Step  0 [Start]: Sunny  ☀️
        Step  1        : Sunny  ☀️
        Step  2        : Cloudy ⛅
        Step  3        : Rainy  🌧️
    """
    if states_emoji is None:
        states_emoji = {}

    print()
    for i, state in enumerate(path):
        emoji = states_emoji.get(state, "")
        if i == 0:
            label = "[Start]"
        else:
            label = "       "
        print(f"  Step {i:3d} {label}: {state:<12} {emoji}")
    print()


def check_row_sums(transitions):
    """
    Print a quick check of whether all rows sum to 1.0.

    Useful for debugging a hand-crafted transition matrix.

    Parameters
    ----------
    transitions : dict of dict
        The transition dictionary.

    Example output:
        Row sum check:
          Sunny    → sum = 1.000000  ✓
          Cloudy   → sum = 1.000000  ✓
          Rainy    → sum = 0.950000  ✗  ← ERROR
    """
    print("\nRow sum check:")
    all_ok = True
    for state in sorted(transitions.keys()):
        total = sum(transitions[state].values())
        ok = abs(total - 1.0) < 1e-9
        symbol = "✓" if ok else "✗  ← ERROR"
        print(f"  {state:<12} → sum = {total:.6f}  {symbol}")
        if not ok:
            all_ok = False
    print()
    return all_ok


def bar_chart(distribution, title="State Distribution", width=30):
    """
    Print a simple ASCII bar chart of a probability distribution.

    Each bar's length is proportional to the probability of that state.

    Parameters
    ----------
    distribution : dict
        A distribution dictionary: state → probability.
    title : str
        A title for the chart.
    width : int
        Maximum bar width in characters.

    Example output:
        State Distribution
        ──────────────────────────────────────────
        Sunny    ████████████████████░░░░░  47.60%
        Cloudy   █████████████░░░░░░░░░░░  28.60%
        Rainy    ███████████░░░░░░░░░░░░░  23.80%
    """
    print(f"\n{title}")
    print("─" * (width + 30))

    states = sorted(distribution.keys())
    max_prob = max(distribution.values()) if distribution else 1.0

    for state in states:
        prob = distribution[state]
        # Scale bar length to the maximum probability
        filled = int((prob / max_prob) * width) if max_prob > 0 else 0
        empty = width - filled
        bar = "█" * filled + "░" * empty
        print(f"  {state:<12} {bar}  {prob * 100:.2f}%")

    print()


def format_probability(prob):
    """
    Format a probability as a nicely rounded percentage string.

    Parameters
    ----------
    prob : float
        A probability between 0 and 1.

    Returns
    -------
    str
        Formatted as e.g. "47.60%"

    Example
    -------
    >>> format_probability(0.4762)
    '47.62%'
    """
    return f"{prob * 100:.2f}%"