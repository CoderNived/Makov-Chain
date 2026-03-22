# 🔗 Markov Chains: From Zero to Python

> **A beginner-friendly, project-based learning repository for understanding and building Markov Chains entirely from scratch in Python.**

---

## 🧭 What This Project Teaches

This repository is a complete self-contained learning package. By working through it, you will:

- Understand what a **Markov Chain** is — intuitively, mathematically, and in code
- Learn what **states**, **transitions**, and **probabilities** mean
- Understand the **Markov property** (why "only the present matters")
- Build a Markov Chain simulator entirely from scratch using only Python's standard library
- Run a real mini-project: a **weather prediction toy model**
- Compare theoretical predictions with simulation results
- Know the limitations of Markov Chains and what to learn next

---

## 👤 Who Is This For?

- Beginners learning Python (you should know functions, loops, and dictionaries)
- Students curious about probability, AI, or data science
- Anyone who wants to understand how simple probabilistic models work
- People who learn best by building, not just reading

No prior knowledge of probability theory or advanced math is needed.

---

## 🎯 Learning Outcomes

After completing this project, you will be able to:

1. Explain what a Markov Chain is to someone else
2. Build a transition matrix from raw data or intuition
3. Write a Python program to simulate state transitions
4. Estimate long-run probabilities from simulation
5. Identify real-world scenarios where Markov Chains apply
6. Recognise the limitations of the Markov assumption

---

## 📁 File Structure

```
markov_chain_project/
│
├── README.md             ← You are here. Start here.
├── NOTES.md              ← Revision notes, definitions, exercises
├── MATH_INTUITION.md     ← Beginner-friendly math walkthrough
│
├── markov_chain.py       ← Core Markov Chain class
├── utils.py              ← Helper functions (display, validation, stats)
├── example_data.py       ← Pre-built transition matrices to experiment with
└── main.py               ← Run this to see everything in action
```

---

## ▶️ How to Run

Python 3.7 or newer. No extra libraries needed.

```bash
python main.py
```

The program will show a transition matrix, simulate steps, run long simulations, and compare results with theoretical predictions.

---

## 📋 Example Output

```
=== Markov Chain: Weather Model ===

Transition Matrix:
         Sunny   Cloudy   Rainy
Sunny    0.70    0.20     0.10
Cloudy   0.30    0.40     0.30
Rainy    0.20    0.30     0.50

--- Simulating 20 steps from: Sunny ---
Step  1: Sunny  ☀️
Step  2: Sunny  ☀️
Step  3: Cloudy ⛅
...

--- Empirical frequencies after 10,000 steps ---
Sunny:   47.3%    Cloudy:  28.6%    Rainy:   24.1%

--- Theoretical stationary distribution ---
Sunny:   47.6%    Cloudy:  28.6%    Rainy:   23.8%

✓ Simulation closely matches theory!
```

---

## 🔑 Key Takeaways

- A Markov Chain models a system moving between states randomly
- The **next state depends only on the current state** — not history
- A **transition matrix** stores all the probabilities
- Given enough time, a chain settles into a **stationary distribution**

---

## 📚 How to Study This in 2 Days

**Day 1 — Understand the concept**
1. Read `README.md` → `NOTES.md` sections 1–3 → `MATH_INTUITION.md`
2. Open `example_data.py`, study the matrices
3. Run `main.py`, observe the output
4. Try the mini exercises in `NOTES.md`

**Day 2 — Build and experiment**
1. Read `markov_chain.py` line by line, then `utils.py`, then `main.py`
2. Change some probabilities in the weather model
3. Add a new state (e.g. "Stormy") to the model
4. Write your own transition matrix for a different domain

---

## 🏆 How to Make This Resume-Worthy

1. **Swap the domain** — use real data (stock prices, text corpora, game states)
2. **Add visualisation** — matplotlib heatmap of the matrix, convergence line chart
3. **Learn transitions from data** — count transitions in a sequence instead of hand-crafting them
4. **Write a clear README** — explain what surprised you
5. **Push to GitHub** with a clean commit history

---

## 🔭 Next Steps

- **Hidden Markov Models** — when the state is hidden
- **Markov Decision Processes** — add actions & rewards (core of reinforcement learning)
- **PageRank** — Google's original algorithm, a direct Markov Chain application
- **Monte Carlo methods** — simulation-based probability estimation
- **N-gram language models** — early NLP, built on the same idea