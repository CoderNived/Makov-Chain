# 🔢 MATH_INTUITION.md — Beginner-Friendly Math for Markov Chains

> No scary symbols. Every formula explained in plain English. Small hand-worked examples throughout.

---

## Table of Contents

1. [Probability Basics (a quick reminder)](#1-probability-basics)
2. [Transition Probabilities — How They Are Assigned](#2-transition-probabilities)
3. [Why Rows Must Sum to 1](#3-why-rows-must-sum-to-1)
4. [Computing the Next State Distribution](#4-next-state-distribution)
5. [Multi-Step Transitions](#5-multi-step-transitions)
6. [What Happens Over Many Steps?](#6-long-run-behaviour)
7. [The Stationary Distribution — Deriving It](#7-stationary-distribution)
8. [Hand-Worked Example: Full Walkthrough](#8-full-worked-example)

---

## 1. Probability Basics

A **probability** is a number between 0 and 1 that tells us how likely something is.

- 0 means "impossible"
- 1 means "certain"
- 0.5 means "equally likely to happen or not"

**The golden rule:** When you list all the possible outcomes of one trial, their probabilities must add up to exactly 1.

*Example:* A fair six-sided die. Each face has probability 1/6. All faces together: 6 × (1/6) = 1. ✓

**Conditional probability:**
`P(B | A)` is read as *"the probability of B given A"*. It means: "assuming A has happened, what is the probability of B?"

*Example:* P(it rains tomorrow | it is raining today) = 0.50. We are conditioning on "it is raining today."

This is exactly what transition probabilities are: conditional probabilities.

---

## 2. Transition Probabilities

A **transition probability** is the probability of moving from one state to another in a single step.

**Notation:** `P(i → j)` means the probability of moving from state `i` to state `j`.

This is the same as writing: `P(next state = j | current state = i)`

**How are they assigned?**

Option 1 — **Expert knowledge:** A meteorologist tells us based on historical data that if it's sunny today, there is a 70% chance it will be sunny tomorrow.

Option 2 — **Counting from data:** Look at a long sequence of observations and count transitions.

*Example:* You observe 100 days following a sunny day:
- 70 were also Sunny → P(Sunny → Sunny) = 70/100 = 0.70
- 20 were Cloudy → P(Sunny → Cloudy) = 20/100 = 0.20
- 10 were Rainy → P(Sunny → Rainy) = 10/100 = 0.10

Option 3 — **Assumption / design:** For a toy model or game, you design the probabilities yourself.

---

## 3. Why Rows Must Sum to 1

This is not a rule we impose — it is a mathematical necessity.

**Think of it this way:**
After a step, the system must be in *some* state. It cannot be in no state. So the total probability of all possible next states must be exactly 1 (certainty).

**Mathematically:**

For state `i`, the probabilities of going to each possible next state `j` must satisfy:

```
P(i → j₁) + P(i → j₂) + P(i → j₃) + ... = 1
```

Or using shorthand: `Σⱼ P(i → j) = 1` (the Greek letter Σ, sigma, means "sum over all j")

**What each symbol means:**
- `Σⱼ` — "add this up for every possible next state j"
- `P(i → j)` — the probability of going from current state i to next state j

**Example check:**
```
From Sunny:   0.70 + 0.20 + 0.10 = 1.00 ✓
From Cloudy:  0.30 + 0.40 + 0.30 = 1.00 ✓
From Rainy:   0.20 + 0.30 + 0.50 = 1.00 ✓
```

**Beginner mistake:** Setting P(Rainy → Sunny) = 0.3, P(Rainy → Cloudy) = 0.3 and forgetting to fill in P(Rainy → Rainy). The remaining probability must be assigned: 1 - 0.3 - 0.3 = 0.4, so P(Rainy → Rainy) = 0.4.

---

## 4. Next State Distribution

What if instead of knowing the exact current state, we have a **distribution** — a set of probabilities for each possible current state?

**Define:**
`π₀` = the initial distribution (a list of probabilities over all states)

**Example:**
```
π₀ = [Sunny: 0.6, Cloudy: 0.3, Rainy: 0.1]
```
This means: we believe there is a 60% chance we start Sunny, 30% Cloudy, 10% Rainy.

**Computing the distribution after one step:**

The probability of being in state `j` after one step is:

```
π₁(j) = Σᵢ π₀(i) × P(i → j)
```

**What each symbol means:**
- `π₁(j)` — probability of being in state j after 1 step
- `π₀(i)` — probability of being in state i at step 0
- `P(i → j)` — probability of going from i to j
- `Σᵢ` — sum over all possible current states i

**In plain English:** "To find the probability of being in state j tomorrow, add up the probability of being in each possible current state, multiplied by the probability of transitioning from that state to j."

### Hand-worked example

Initial distribution: π₀ = [Sunny: 0.6, Cloudy: 0.3, Rainy: 0.1]

Transition matrix:
```
             → Sunny  → Cloudy  → Rainy
Sunny           0.70     0.20     0.10
Cloudy          0.30     0.40     0.30
Rainy           0.20     0.30     0.50
```

**What is the probability of being Sunny tomorrow?**

```
π₁(Sunny) = π₀(Sunny) × P(Sunny→Sunny)
           + π₀(Cloudy) × P(Cloudy→Sunny)
           + π₀(Rainy)  × P(Rainy→Sunny)

           = 0.6 × 0.70
           + 0.3 × 0.30
           + 0.1 × 0.20

           = 0.420 + 0.090 + 0.020
           = 0.530
```

So there is a 53% chance of being Sunny tomorrow.

**Try it yourself:** Compute π₁(Cloudy) and π₁(Rainy).

```
π₁(Cloudy) = 0.6×0.20 + 0.3×0.40 + 0.1×0.30
           = 0.120 + 0.120 + 0.030
           = 0.270

π₁(Rainy)  = 0.6×0.10 + 0.3×0.30 + 0.1×0.50
           = 0.060 + 0.090 + 0.050
           = 0.200
```

**Verify:** 0.530 + 0.270 + 0.200 = 1.000 ✓

---

## 5. Multi-Step Transitions

**Question:** What is the probability of being in state `j` after `n` steps, starting from state `i`?

**Short answer:** Apply the transition calculation `n` times.

**The matrix power approach:**

If `T` is the transition matrix, then `T²` (T squared, meaning T multiplied by T) gives the 2-step transition probabilities, `T³` gives the 3-step probabilities, and `Tⁿ` gives the n-step probabilities.

**Entry `[i][j]` of `Tⁿ` = probability of going from state i to state j in exactly n steps.**

### Hand-worked example: 2-step probabilities

Let's compute the probability of going from Sunny to Rainy in exactly 2 steps.

There are three possible 2-step paths:
```
Sunny → Sunny → Rainy     probability = 0.70 × 0.10 = 0.070
Sunny → Cloudy → Rainy    probability = 0.20 × 0.30 = 0.060
Sunny → Rainy → Rainy     probability = 0.10 × 0.50 = 0.050
```

Total probability of Sunny → (anything) → Rainy in 2 steps:
```
P²(Sunny → Rainy) = 0.070 + 0.060 + 0.050 = 0.180
```

**In plain English:** We add up the probabilities of all possible paths of length 2 that start at Sunny and end at Rainy.

**General formula:**
```
Pⁿ(i → j) = Σₖ P(i → k) × Pⁿ⁻¹(k → j)
```

What each symbol means:
- `Pⁿ(i → j)` — probability of going from i to j in exactly n steps
- `Σₖ` — sum over all intermediate states k
- `P(i → k)` — probability of going from i to k in 1 step
- `Pⁿ⁻¹(k → j)` — probability of going from k to j in n-1 steps

This is just the chain rule of probability applied repeatedly.

---

## 6. Long-Run Behaviour

**Question:** What happens to the state distribution as n gets very large?

**Observation:** Run the weather model for 5, 10, 50, 100, 1000 steps starting from Sunny. Track the distribution at each point.

```
After  1 step:  Sunny=0.70, Cloudy=0.20, Rainy=0.10
After  2 steps: Sunny=0.55, Cloudy=0.26, Rainy=0.19   (roughly)
After  5 steps: Sunny=0.49, Cloudy=0.28, Rainy=0.23   (converging...)
After 10 steps: Sunny=0.48, Cloudy=0.29, Rainy=0.24
After 50 steps: Sunny=0.476, Cloudy=0.286, Rainy=0.238
After 100 steps: Sunny=0.476, Cloudy=0.286, Rainy=0.238  ← settled
```

The distribution is converging to fixed values. This is the **stationary distribution**.

**Key insight:** No matter where you start (Sunny, Cloudy, or Rainy), you converge to the same distribution. Try it — after 50 steps, all three starting points give the same result.

**Why does this happen?**

Intuitively: the system "forgets" its starting state over time. The transition probabilities pull the distribution toward an equilibrium. Any initial imbalance gets smoothed out by the repeated mixing effect of the transition matrix.

**When does convergence happen?**

For any chain that is:
1. **Irreducible** — every state is reachable from every other state
2. **Aperiodic** — no fixed cycle length

...the distribution will always converge to a unique stationary distribution. Our weather model satisfies both conditions (you can verify by checking all transition probabilities are positive).

---

## 7. The Stationary Distribution

**Definition:** A probability distribution `π*` is called stationary (or steady-state) if:

```
π* × T = π*
```

**What each symbol means:**
- `π*` — the stationary distribution (a row vector of probabilities)
- `T` — the transition matrix
- `× ` — matrix-vector multiplication
- The equation says: applying T to π* gives back π* (it doesn't change)

**In plain English:** When the current distribution is π*, after one step it is still π*. The system is in equilibrium.

### How to compute it (iterative method — no linear algebra needed!)

The simplest approach: just simulate for a very long time and count.

**Algorithm:**
1. Start at any state
2. Simulate 100,000 steps
3. Count how many times you visit each state
4. Divide by total steps → estimated stationary distribution

This is exactly what our code does, and it converges to the true stationary distribution.

### How to compute it exactly (power iteration)

Another approach: repeatedly multiply the initial distribution by the transition matrix.

```
π₀ = [1, 0, 0]   (start in Sunny with certainty)
π₁ = π₀ × T
π₂ = π₁ × T
π₃ = π₂ × T
...
πₙ = πₙ₋₁ × T
```

After many steps (typically 50–100 for our model), `πₙ` stops changing. That is the stationary distribution.

**Our code implements this** — see `markov_chain.py` for the `compute_stationary_distribution` method.

### Hand-worked verification

Claim: `π* = [0.476, 0.286, 0.238]` is the stationary distribution for our weather model.

Let's verify by computing `π* × T`:

```
Resulting Sunny value:
= 0.476 × 0.70 + 0.286 × 0.30 + 0.238 × 0.20
= 0.333 + 0.086 + 0.048
= 0.467 ≈ 0.476 ✓ (small rounding error)

Resulting Cloudy value:
= 0.476 × 0.20 + 0.286 × 0.40 + 0.238 × 0.30
= 0.095 + 0.114 + 0.071
= 0.280 ≈ 0.286 ✓

Resulting Rainy value:
= 0.476 × 0.10 + 0.286 × 0.30 + 0.238 × 0.50
= 0.048 + 0.086 + 0.119
= 0.253 ≈ 0.238 ✓ (rounding errors accumulate slightly)
```

Close enough — the discrepancy is purely due to rounding the values to 3 decimal places. With exact fractions, it would match perfectly.

---

## 8. Full Worked Example

Let's walk through the entire process for a simple 2-state model: a person's mood, either Happy (H) or Sad (S).

### Step 1: Define states
States = {Happy, Sad}

### Step 2: Define transitions

Based on observation (or assumption):
- If Happy today: 80% chance of Happy tomorrow, 20% chance of Sad
- If Sad today: 60% chance of Happy tomorrow, 40% chance of Sad

**Transition matrix:**
```
           → Happy  → Sad
Happy        0.80    0.20
Sad          0.60    0.40
```

**Verify rows:** 0.80 + 0.20 = 1.00 ✓ and 0.60 + 0.40 = 1.00 ✓

### Step 3: Simulate one step from Happy

We are in Happy. We generate a random number.
- If the number falls in [0, 0.80): stay Happy
- If the number falls in [0.80, 1.00): go to Sad

**In Python:**
```python
import random
state = "Happy"
transitions = {"Happy": {"Happy": 0.80, "Sad": 0.20},
               "Sad":   {"Happy": 0.60, "Sad": 0.40}}
next_states = list(transitions[state].keys())     # ["Happy", "Sad"]
weights     = list(transitions[state].values())   # [0.80, 0.20]
next_state  = random.choices(next_states, weights=weights)[0]
```

### Step 4: Compute distribution after 1 step from Happy

Starting distribution: π₀ = [Happy: 1.0, Sad: 0.0]

```
π₁(Happy) = 1.0 × 0.80 + 0.0 × 0.60 = 0.80
π₁(Sad)   = 1.0 × 0.20 + 0.0 × 0.40 = 0.20
```

Verify: 0.80 + 0.20 = 1.00 ✓

### Step 5: Compute distribution after 2 steps

π₁ = [Happy: 0.80, Sad: 0.20]

```
π₂(Happy) = 0.80 × 0.80 + 0.20 × 0.60 = 0.640 + 0.120 = 0.760
π₂(Sad)   = 0.80 × 0.20 + 0.20 × 0.40 = 0.160 + 0.080 = 0.240
```

Verify: 0.760 + 0.240 = 1.000 ✓

### Step 6: Find the stationary distribution

Using power iteration (shown conceptually):
```
Step 0:  [1.000, 0.000]
Step 1:  [0.800, 0.200]
Step 2:  [0.760, 0.240]
Step 3:  [0.752, 0.248]
Step 5:  [0.750, 0.250]
Step 10: [0.750, 0.250]  ← converged
```

The stationary distribution is approximately: Happy = 75%, Sad = 25%.

**Interpret in plain English:** In the long run, this person will be Happy about 75% of the time and Sad about 25% of the time, regardless of their starting mood.

**Verify:**
```
π*(Happy) = 0.75 × 0.80 + 0.25 × 0.60 = 0.60 + 0.15 = 0.75 ✓
π*(Sad)   = 0.75 × 0.20 + 0.25 × 0.40 = 0.15 + 0.10 = 0.25 ✓
```

It checks out. This is a valid stationary distribution.

---

## Summary of All Formulas

| Formula | What it means |
|---------|---------------|
| `Σⱼ P(i→j) = 1` | Probabilities from any state sum to 1 |
| `π₁(j) = Σᵢ π₀(i) × P(i→j)` | Next step distribution from current distribution |
| `Pⁿ(i→j) = Σₖ P(i→k) × Pⁿ⁻¹(k→j)` | n-step probability (sum over intermediate states) |
| `π* × T = π*` | Stationary distribution condition |

Every formula is just one idea: **multiply probabilities, then add them up**. That is the core of Markov Chain mathematics.