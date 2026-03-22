# 📝 NOTES.md — Markov Chains Revision Guide

> Quick-reference notes for revision. Read this after `README.md`. Do exercises as you go.

---

## Table of Contents

1. [What Is a Stochastic Process?](#1-what-is-a-stochastic-process)
2. [What Is a Markov Chain?](#2-what-is-a-markov-chain)
3. [The Markov Property](#3-the-markov-property)
4. [States and Transitions](#4-states-and-transitions)
5. [The Transition Matrix](#5-the-transition-matrix)
6. [Special Types of States](#6-special-types-of-states)
7. [Long-Run Behaviour and Stationary Distribution](#7-long-run-behaviour-and-stationary-distribution)
8. [Real-World Examples](#8-real-world-examples)
9. [Limitations of Markov Chains](#9-limitations-of-markov-chains)
10. [Code Concepts Summary](#10-code-concepts-summary)
11. [Mini Exercises with Answers](#11-mini-exercises-with-answers)
12. [Memory Tricks](#12-memory-tricks)
13. [Common Confusion Points](#13-common-confusion-points)
14. [What to Learn Next](#14-what-to-learn-next)

---

## 1. What Is a Stochastic Process?

**Definition:** A *stochastic process* is a sequence of events where each event has some randomness involved.

**Key word:** *Stochastic* just means *random* or *probabilistic*. It comes from the Greek word for "aim" or "guess."

**Simple analogy:** Imagine you roll a die every morning and write down the result. The sequence of numbers — 3, 1, 6, 2, 4, ... — is a stochastic process. Each result is random, but together they form a pattern we can study.

**More examples:**
- Daily temperature readings (random, but with patterns)
- A person's mood each hour (random, influenced by context)
- Whether the stock market goes up or down each day

The key idea: we are studying *sequences* of random outcomes, not just a single random outcome.

---

## 2. What Is a Markov Chain?

**Definition:** A *Markov Chain* is a special type of stochastic process where the system is always in one of a fixed set of *states*, and moves between states according to fixed *probabilities*.

**Intuition first:** Think of a board game. At any point, your piece is on a specific square (your *state*). When you roll the dice, you move to a new square. The rules of the game (the board layout) determine where you can go and how likely each move is. That rule system is a Markov Chain.

**Formal definition in plain English:**
A Markov Chain is a system that:
1. Has a finite (countable) set of possible situations called **states**
2. At each step, randomly moves from one state to another
3. The probability of where it goes next depends **only on where it is now**

**The word "chain"** comes from the idea that the sequence of states forms a chain:
```
State A → State B → State A → State C → State B → ...
```

---

## 3. The Markov Property

**This is the most important concept in the whole topic. Read it twice.**

**The Markov Property states:**
> *The future depends only on the present, not on the past.*

**Analogy — The Goldfish Memory Model:**
Imagine a goldfish navigating a fish tank. It only knows where it is right now. It has no memory of where it has been. The next place it swims to depends only on its current position, not on its route through the tank.

**Analogy — Traffic Lights:**
A traffic light cycles: Red → Green → Yellow → Red. To predict what comes next, you only need to know the current colour. You don't need to know how long it's been Red, or how many times it was Red before. The current state is all that matters.

**Why this simplifying assumption is powerful:**
Without the Markov Property, you'd need to remember the entire history of the system to predict the future. That's often impractical. The Markov assumption says: *just look at now*. This makes the maths tractable and the models computationally efficient.

**When is this assumption valid?**
When the current state truly captures all the relevant information. For example:
- A traffic light: the current colour tells you everything you need
- Weather: today's weather is a decent predictor of tomorrow's (though not perfect)

**When is it not valid?**
When history genuinely matters. For example:
- Predicting a person's income: knowing their current job is not enough; their education history matters too
- Language modelling: what comes after "bank" depends on whether we said "river bank" or "bank account"

---

## 4. States and Transitions

**State:** A specific situation the system can be in. States must be:
- *Clearly defined* — no ambiguity about which state you're in
- *Mutually exclusive* — you can only be in one state at a time
- *Exhaustive* — together, the states cover all possibilities

**Examples of states:**
| System | States |
|--------|--------|
| Weather | Sunny, Cloudy, Rainy |
| Traffic light | Red, Yellow, Green |
| Website page | Home, Products, Cart, Checkout, Exit |
| Customer mood | Happy, Neutral, Frustrated |

**Transition:** Moving from one state to another.

**Transition probability:** The probability (a number between 0 and 1) of moving from state A to state B in one step.

**Notation:** We write `P(A → B)` or `P(B | A)` (read: "probability of going to B given we are currently in A").

**Example — Weather:**
```
P(Sunny → Sunny)   = 0.70  (70% chance tomorrow is also sunny)
P(Sunny → Cloudy)  = 0.20  (20% chance it becomes cloudy)
P(Sunny → Rainy)   = 0.10  (10% chance it rains tomorrow)
```

Notice: 0.70 + 0.20 + 0.10 = 1.00. The probabilities from any state must sum to 1 because you have to go *somewhere*.

---

## 5. The Transition Matrix

**Definition:** A *transition matrix* (also called a *stochastic matrix*) is a table that organises all transition probabilities.

**Structure:**
- Each **row** represents the current state
- Each **column** represents the next state
- Entry `[i][j]` is the probability of going from state `i` to state `j`
- Every **row** must sum to exactly 1.0

**Weather model transition matrix:**

```
             → Sunny   → Cloudy  → Rainy
Sunny   (from)  0.70     0.20     0.10
Cloudy  (from)  0.30     0.40     0.30
Rainy   (from)  0.20     0.30     0.50
```

**How to read it:**
- Look at row "Rainy": if today is Rainy, tomorrow is Sunny with probability 0.20, Cloudy with 0.30, Rainy again with 0.50.
- The row sums: 0.20 + 0.30 + 0.50 = 1.0 ✓

**In Python (as a dictionary of dictionaries):**
```python
transitions = {
    "Sunny":  {"Sunny": 0.70, "Cloudy": 0.20, "Rainy": 0.10},
    "Cloudy": {"Sunny": 0.30, "Cloudy": 0.40, "Rainy": 0.30},
    "Rainy":  {"Sunny": 0.20, "Cloudy": 0.30, "Rainy": 0.50},
}
```

**Checkpoint — can you answer these?**
- What does row "Cloudy" tell you?
- What must every row sum to?
- If `P(Rainy → Sunny) = 0.20`, what does that mean in plain English?

---

## 6. Special Types of States

### Absorbing States

**Definition:** A state from which you can never leave. Once you enter it, you stay forever.

**Probability:** `P(absorbing → absorbing) = 1.0`

**Real examples:**
- "Game Over" in a video game
- "Dead" in a biological model
- "Account closed" in a banking model

**In a matrix:** An absorbing state has a 1.0 on its diagonal and 0 everywhere else in its row.

---

### Irreducibility (explained simply)

A Markov Chain is **irreducible** if you can eventually get from *any* state to *any other* state.

**Analogy:** If you're in a city with a complete road network — you can reach any district from any other district — the network is irreducible.

**Why it matters:** Irreducible chains have nicer mathematical properties and always reach a stable long-run distribution.

**Counter-example:** If "Sunny → Rainy" is impossible (probability 0), the chain is not irreducible.

---

### Periodicity (explained simply)

A state has **period** `d` if you can only return to it in multiples of `d` steps.

**Example:** A traffic light cycles Red → Green → Yellow → Red. You can only return to Red in steps 3, 6, 9, ... so it has period 3.

**Aperiodic** means period = 1 (you can return to any state in any number of steps). Most practical models are aperiodic.

**Why it matters:** Aperiodic, irreducible chains are the "nicely behaved" ones — they always converge to a stationary distribution.

---

## 7. Long-Run Behaviour and Stationary Distribution

### Intuition

Imagine you run the weather simulation for 10,000 days. At the end, you count: how many days were Sunny? Cloudy? Rainy? If you repeat this experiment many times, those proportions converge to fixed values. Those values form the **stationary distribution**.

**Definition:** A *stationary distribution* (also called *steady-state distribution*) is a probability distribution over states that, once reached, does not change with further transitions.

**In plain English:** It's the long-run fraction of time the system spends in each state.

**Key insight:** The stationary distribution does **not** depend on the starting state (for well-behaved chains). Whether you start Sunny or Rainy, after enough steps, the proportions converge to the same values.

### How to find it (intuitively)

The stationary distribution `π` satisfies: `π × T = π`

In words: if you apply the transition matrix to the stationary distribution, you get the same distribution back. It is a fixed point of the system.

For our weather model, the stationary distribution is approximately:
- Sunny: 47.6%
- Cloudy: 28.6%
- Rainy: 23.8%

**Checkpoint:** If you run the simulation for 1,000 steps and count states, do you expect to see roughly 476 Sunny days, 286 Cloudy days, and 238 Rainy days? Yes — that is exactly the prediction.

---

## 8. Real-World Examples

| Domain | States | What it models |
|--------|--------|----------------|
| Weather | Sunny, Cloudy, Rainy | Day-to-day weather patterns |
| Web browsing | Page A, B, C, ..., Exit | How users navigate a website |
| Text generation | Words or characters | Which word comes after another |
| Customer journey | Aware, Interested, Purchased, Churned | Marketing funnel |
| Finance | Bull market, Bear market, Flat | Market regime modelling |
| Biology | Healthy, Sick, Recovered, Dead | Disease progression |
| Games | Board positions | AI for simple games |
| Speech | Phonemes | Speech recognition (Hidden Markov Models) |

**PageRank (Google):** Google's original page ranking algorithm models the web as a Markov Chain. Each web page is a state. A "random surfer" clicks links at random. The stationary distribution gives each page a rank — the probability that the surfer is on that page at any given moment. Pages that are linked to frequently have higher rank.

---

## 9. Limitations of Markov Chains

Understanding limitations is just as important as understanding the strengths.

**1. The Markov assumption is often violated**
Real systems often do depend on history. A person's health tomorrow depends on more than just today's condition. Language depends on long-range context ("The bank I grew up near..." — "bank" can't be interpreted without context).

**2. States must be discrete and predefined**
Markov Chains (in their basic form) require a fixed, finite set of states defined in advance. Continuous or unknown state spaces require extensions (e.g. Gaussian processes, particle filters).

**3. Transition probabilities are assumed fixed**
Basic Markov Chains assume the probabilities don't change over time. In reality, weather patterns change with seasons, customer behaviour shifts with trends.

**4. The model is only as good as your transition matrix**
If you hand-craft the probabilities (as we do in this project), the model reflects your assumptions, not reality. Learning transitions from data is better, but requires data.

**5. Long chains can have slow convergence**
For some chains, reaching the stationary distribution takes a very long time (this is called slow mixing). This is a problem in applications like Markov Chain Monte Carlo (MCMC).

---

## 10. Code Concepts Summary

| Concept | Python representation |
|---------|----------------------|
| States | List of strings: `["Sunny", "Cloudy", "Rainy"]` |
| Transition matrix | Dict of dicts: `{"Sunny": {"Cloudy": 0.2, ...}}` |
| Current state | String variable: `current = "Sunny"` |
| Next state | `random.choices(states, weights=probs)` |
| Simulation | Loop: repeat `current = next_state(current)` |
| Stationary distribution | Count states over long run, divide by total steps |

**Key Python modules used:**
- `random` — for random choices weighted by probability
- `collections.Counter` — for counting state visits
- `math` — for validation checks

---

## 11. Mini Exercises with Answers

### Exercise 1 — Read a transition matrix

Given this matrix for a traffic light:
```
              → Red   → Green  → Yellow
Red    (from)  0.00    1.00     0.00
Green  (from)  0.00    0.00     1.00
Yellow (from)  1.00    0.00     0.00
```

**Questions:**
a) What comes after Red?  
b) What comes after Yellow?  
c) Is this Markov Chain irreducible?  
d) What is the period of each state?

**Answers:**
a) Always Green (probability 1.0)  
b) Always Red (probability 1.0)  
c) Yes — you can reach any state from any other state eventually  
d) Period 3 for all states (you return to any state in steps 3, 6, 9, ...)

---

### Exercise 2 — Validate a row

A student writes this transition row for "Cloudy":
```python
{"Sunny": 0.25, "Cloudy": 0.45, "Rainy": 0.25}
```

**Question:** Is this valid? Why or why not?

**Answer:** No. The probabilities sum to 0.25 + 0.45 + 0.25 = 0.95, not 1.0. Every row must sum to exactly 1.0 (within floating-point tolerance).

---

### Exercise 3 — Trace a simulation by hand

Starting from "Sunny", trace 3 steps using these rules:
- From Sunny: go to Cloudy (probability 1.0, for simplicity)
- From Cloudy: go to Rainy (probability 1.0)
- From Rainy: go to Sunny (probability 1.0)

**Question:** What is the state after 7 steps?

**Answer:**
Step 0: Sunny  
Step 1: Cloudy  
Step 2: Rainy  
Step 3: Sunny  
Step 4: Cloudy  
Step 5: Rainy  
Step 6: Sunny  
Step 7: **Cloudy**  
(This is a periodic chain with period 3.)

---

### Exercise 4 — Identify the absorbing state

```python
transitions = {
    "Browsing":   {"Browsing": 0.60, "Cart": 0.30, "Exit": 0.10},
    "Cart":       {"Browsing": 0.20, "Cart": 0.50, "Checkout": 0.20, "Exit": 0.10},
    "Checkout":   {"Checkout": 0.00, "Purchased": 0.80, "Exit": 0.20},
    "Purchased":  {"Purchased": 1.00},
    "Exit":       {"Exit": 1.00},
}
```

**Question:** Which states are absorbing?

**Answer:** "Purchased" and "Exit" — both have probability 1.0 of staying in themselves. Once a customer purchases or exits, they stay in that state in this model.

---

### Exercise 5 — Conceptual

**Question:** Why can't the following be a valid Markov Chain transition matrix row?
```
P(A → A) = 0.4,  P(A → B) = 0.7
```

**Answer:** The probabilities sum to 1.1, which is greater than 1.0. Probabilities can never exceed 1.0 in total because they represent the complete set of possible outcomes from state A.

---

## 12. Memory Tricks

- **"Markov = Memoryless"** — the chain only cares about NOW
- **"Rows sum to 1"** — every row is a complete probability distribution
- **"Columns = destinations, Rows = origins"** — when reading the matrix
- **"Stationary = settled"** — the long-run proportions that don't change
- **"Absorbing = Hotel California"** — you can check in but you can't check out
- **"Irreducible = connected"** — every state can reach every other state

---

## 13. Common Confusion Points

**"Does the chain remember anything?"**
No. This is the whole point of the Markov property. Each step only looks at the current state. The path taken to get there is irrelevant.

**"Do rows or columns sum to 1?"**
Rows sum to 1. Each row represents the distribution of next states *given* the current state. Columns do not need to sum to 1.

**"Is the stationary distribution the same as the initial distribution?"**
No (usually). The initial distribution is where you start. The stationary distribution is where the chain ends up after many steps. They're the same only if you happen to start in the stationary distribution.

**"Does every Markov Chain have a stationary distribution?"**
Not exactly. Every finite Markov Chain has at least one stationary distribution. But it is unique and the chain converges to it only if the chain is irreducible and aperiodic.

**"Can a state have P(state → state) > 0?"**
Yes! This is called a *self-loop*. "Sunny → Sunny" with probability 0.70 is a self-loop. It means the chain stays in the same state with that probability.

**"What if I make a probability slightly wrong, like 0.999 instead of 1.0?"**
Your simulation will still run but will produce subtly wrong results. Always validate that rows sum to 1.0 (within a small tolerance like 1e-9) before running.

---

## 14. What to Learn Next

**Immediate next steps (beginner):**
- Learn the matrix power method for computing multi-step probabilities
- Build a Markov Chain that learns from a text file (count word transitions)
- Visualise your chain as a directed graph using `networkx` or `matplotlib`

**Intermediate:**
- **Hidden Markov Models (HMMs):** The state is not directly observable; you only see "emissions." Used heavily in speech recognition and bioinformatics.
- **Markov Decision Processes (MDPs):** Add a decision-maker who chooses actions. The foundation of reinforcement learning.

**Advanced:**
- **MCMC (Markov Chain Monte Carlo):** Use Markov Chains to sample from complex probability distributions. The backbone of Bayesian inference.
- **PageRank algorithm:** Read the original Google paper and re-implement it
- **Mixing times:** How long does a chain take to approach its stationary distribution?

**Good resources:**
- *Introduction to Probability* by Blitzstein & Hwang (free online)
- 3Blue1Brown YouTube: "Markov chains" video
- Wikipedia: "Markov chain" (the diagrams are very helpful)