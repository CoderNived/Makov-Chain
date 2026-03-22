"""
markov_chain.py
---------------
The core Markov Chain class.

This file contains everything needed to represent a Markov Chain,
validate it, run simulations, and compute distributions.

No external libraries are used — only Python's standard 'random' module.

How to use this file:
    from markov_chain import MarkovChain
    mc = MarkovChain(transitions)
    mc.simulate(start_state="Sunny", steps=20)
"""

import random
from collections import Counter


class MarkovChain:
    """
    Represents a discrete-time, finite-state Markov Chain.

    A Markov Chain is a system that:
    - Exists in one of a fixed set of states at any time
    - Moves between states randomly at each step
    - The next state depends only on the current state (Markov property)

    Parameters
    ----------
    transitions : dict of dict
        A dictionary where:
          - Each key is a state name (string or int)
          - Each value is a dictionary mapping next states to probabilities

        Example:
            {
                "Sunny":  {"Sunny": 0.7, "Cloudy": 0.2, "Rainy": 0.1},
                "Cloudy": {"Sunny": 0.3, "Cloudy": 0.4, "Rainy": 0.3},
                "Rainy":  {"Sunny": 0.2, "Cloudy": 0.3, "Rainy": 0.5},
            }
    """

    def __init__(self, transitions):
        """
        Initialise the Markov Chain with a transition dictionary.

        This method:
        1. Stores the transitions
        2. Extracts the list of states
        3. Validates the transition probabilities
        """

        # Store the transition dictionary
        self.transitions = transitions

        # Extract all state names as a sorted list (sorted for consistency)
        self.states = sorted(transitions.keys())

        # Validate that the transition probabilities are correct
        # This will raise an error if anything is wrong
        self._validate()

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def _validate(self):
        """
        Check that the transition matrix is valid.

        A valid transition matrix must satisfy:
        1. Every state in the matrix must be a key in 'transitions'
        2. All probabilities must be between 0 and 1
        3. Each row (set of outgoing probabilities) must sum to 1.0
        4. All destination states must be defined states
        """

        # A small tolerance for floating-point rounding errors
        # For example, 0.1 + 0.2 + 0.7 in Python may equal 0.9999999...
        TOLERANCE = 1e-9

        for state in self.states:
            row = self.transitions[state]

            # Check: every destination must be a known state
            for dest in row:
                if dest not in self.transitions:
                    raise ValueError(
                        f"State '{dest}' appears as a destination from '{state}' "
                        f"but is not defined as a starting state. "
                        f"Every destination must be a defined state."
                    )

            # Check: all probabilities are non-negative
            for dest, prob in row.items():
                if prob < 0:
                    raise ValueError(
                        f"Negative probability found: P({state} → {dest}) = {prob}. "
                        f"Probabilities must be between 0 and 1."
                    )

            # Check: each row sums to 1.0 (within floating-point tolerance)
            total = sum(row.values())
            if abs(total - 1.0) > TOLERANCE:
                raise ValueError(
                    f"Probabilities from state '{state}' sum to {total:.6f}, "
                    f"not 1.0. Each row must sum to exactly 1.0.\n"
                    f"Current values: {row}"
                )

    # ------------------------------------------------------------------
    # SINGLE STEP
    # ------------------------------------------------------------------

    def next_state(self, current_state):
        """
        Given the current state, randomly select the next state.

        This is the heart of the simulation. We use Python's
        random.choices() function which accepts a list of options
        and a matching list of weights (probabilities).

        Parameters
        ----------
        current_state : str or int
            The state the chain is currently in.

        Returns
        -------
        str or int
            The randomly chosen next state.

        Example
        -------
        >>> mc.next_state("Sunny")
        'Sunny'   # (random — could also be 'Cloudy' or 'Rainy')
        """

        if current_state not in self.transitions:
            raise ValueError(
                f"Unknown state: '{current_state}'. "
                f"Valid states are: {self.states}"
            )

        # Get the possible next states and their probabilities
        row = self.transitions[current_state]
        next_states = list(row.keys())       # e.g. ["Sunny", "Cloudy", "Rainy"]
        probabilities = list(row.values())   # e.g. [0.70, 0.20, 0.10]

        # random.choices(population, weights) picks one item from population
        # where each item's chance of being picked is proportional to its weight.
        # It returns a list, so we take [0] to get just the string.
        chosen = random.choices(next_states, weights=probabilities, k=1)[0]

        return chosen

    # ------------------------------------------------------------------
    # SIMULATION
    # ------------------------------------------------------------------

    def simulate(self, start_state, steps, verbose=True):
        """
        Simulate the Markov Chain for a given number of steps.

        Starting from 'start_state', we take 'steps' transitions
        and record every state visited.

        Parameters
        ----------
        start_state : str or int
            The initial state to begin the simulation from.
        steps : int
            How many transitions to make.
        verbose : bool
            If True, print each step as it happens.

        Returns
        -------
        list
            The full sequence of states visited, including the start state.
            Length is (steps + 1).

        Example
        -------
        >>> path = mc.simulate("Sunny", steps=5)
        Step  1: Sunny
        Step  2: Sunny
        Step  3: Cloudy
        Step  4: Rainy
        Step  5: Rainy
        """

        if start_state not in self.transitions:
            raise ValueError(f"Unknown start state: '{start_state}'")

        if steps <= 0:
            raise ValueError("'steps' must be a positive integer.")

        # The path starts with the initial state
        path = [start_state]

        # Current state at this point in the simulation
        current = start_state

        # Take 'steps' transitions
        for step_number in range(1, steps + 1):
            current = self.next_state(current)
            path.append(current)

            if verbose:
                print(f"  Step {step_number:3d}: {current}")

        return path

    # ------------------------------------------------------------------
    # FREQUENCY COUNTING
    # ------------------------------------------------------------------

    def empirical_frequencies(self, start_state, steps):
        """
        Run a long simulation and estimate the fraction of time spent
        in each state. This estimates the stationary distribution.

        The more steps we use, the more accurate the estimate.
        For a good estimate, use at least 10,000 steps.

        Parameters
        ----------
        start_state : str or int
            Starting state for the simulation.
        steps : int
            Number of steps to simulate.

        Returns
        -------
        dict
            A dictionary mapping each state to its empirical frequency (0–1).

        Example
        -------
        >>> mc.empirical_frequencies("Sunny", 10000)
        {'Sunny': 0.473, 'Cloudy': 0.286, 'Rainy': 0.241}
        """

        # Run the simulation silently (verbose=False)
        path = self.simulate(start_state, steps, verbose=False)

        # Count how many times each state was visited
        # Counter is like a dictionary that counts occurrences
        counts = Counter(path)

        # Total number of observations = steps + 1 (includes start state)
        total = len(path)

        # Convert counts to frequencies (fractions between 0 and 1)
        frequencies = {state: counts.get(state, 0) / total
                       for state in self.states}

        return frequencies

    # ------------------------------------------------------------------
    # STATIONARY DISTRIBUTION (POWER ITERATION)
    # ------------------------------------------------------------------

    def compute_stationary_distribution(self, iterations=1000):
        """
        Compute the stationary distribution using power iteration.

        Power iteration works by repeatedly applying the transition
        matrix to a distribution until it stops changing.

        Intuitively: start with any distribution, apply the Markov
        Chain many times, and watch the distribution converge to
        the stationary distribution.

        Parameters
        ----------
        iterations : int
            Number of times to apply the transition matrix.
            1000 is more than enough for most practical chains.

        Returns
        -------
        dict
            The stationary distribution: state → probability.

        Example
        -------
        >>> mc.compute_stationary_distribution()
        {'Sunny': 0.476, 'Cloudy': 0.286, 'Rainy': 0.238}
        """

        n = len(self.states)

        # Start with a uniform distribution: equal probability for all states
        # For example, with 3 states: [1/3, 1/3, 1/3]
        # (The starting distribution does not affect the final result)
        distribution = {state: 1.0 / n for state in self.states}

        # Apply the transition matrix 'iterations' times
        for _ in range(iterations):
            new_distribution = {}

            # For each possible next state j...
            for next_state in self.states:
                # Compute the new probability of being in next_state
                # by summing over all current states
                # π₁(j) = Σᵢ π₀(i) × P(i → j)
                new_prob = 0.0
                for current_state in self.states:
                    # Probability of being in current_state right now
                    p_current = distribution[current_state]

                    # Probability of transitioning from current_state to next_state
                    # Use .get() with default 0 in case the transition doesn't exist
                    p_transition = self.transitions[current_state].get(next_state, 0.0)

                    new_prob += p_current * p_transition

                new_distribution[next_state] = new_prob

            distribution = new_distribution

        return distribution

    # ------------------------------------------------------------------
    # ONE-STEP DISTRIBUTION
    # ------------------------------------------------------------------

    def next_distribution(self, current_distribution):
        """
        Given a probability distribution over current states,
        compute the distribution after one step.

        Parameters
        ----------
        current_distribution : dict
            Probability of being in each state right now.
            Must sum to 1.0.

        Returns
        -------
        dict
            Probability of being in each state after one step.

        Example
        -------
        If we know:
            current_distribution = {"Sunny": 1.0, "Cloudy": 0.0, "Rainy": 0.0}
        Then after one step:
            next_distribution = {"Sunny": 0.70, "Cloudy": 0.20, "Rainy": 0.10}
        """

        new_dist = {}

        for next_state in self.states:
            new_prob = 0.0
            for curr_state, curr_prob in current_distribution.items():
                p_transition = self.transitions[curr_state].get(next_state, 0.0)
                new_prob += curr_prob * p_transition
            new_dist[next_state] = new_prob

        return new_dist

    # ------------------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------------------

    def __str__(self):
        """
        Return a human-readable summary of the Markov Chain.
        This is what gets printed when you do print(mc).
        """
        lines = [f"MarkovChain with {len(self.states)} states: {self.states}"]
        for state in self.states:
            lines.append(f"  From '{state}':")
            for dest, prob in self.transitions[state].items():
                lines.append(f"    → '{dest}': {prob:.3f}")
        return "\n".join(lines)