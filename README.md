# Job Application Optimization using 0/1 Knapsack

**CS 5800 - Algorithm Analysis Final Project**  
**By: Jinyu Chen & Monisha Dhana Vijeya**

## Overview

This project applies the 0/1 Knapsack problem to optimize job application strategy for graduate students with limited preparation time. Given a set of job applications — each requiring different preparation hours and offering different expected values — we find the optimal subset that maximizes total expected value within a fixed time budget.

## Problem

Given:
- Multiple job applications with different preparation times, offer probabilities, and salaries
- Limited time budget for interview preparation

Find: Which applications to prepare for to maximize expected value?

**Expected Value = P(offer) × Salary**

This maps directly to 0/1 Knapsack: preparation hours → item weight, expected value → item value, time budget → knapsack capacity. Each application is either fully prepared for or not (indivisible).

## Project Structure

```
5800Project/
├── README.md               ← This file (code documentation)
├── dataset.py              ← Job application dataset (15 realistic entries)
├── greedy_algorithm.py     ← Greedy heuristic: O(n log n), not optimal
├── dp_algorithm.py         ← Dynamic programming: O(n×T), guaranteed optimal
├── comparison.py           ← Side-by-side DP vs Greedy comparison
└── complexity_analysis.py  ← Theoretical + empirical complexity analysis
```

## File Descriptions

### `dataset.py` (Monisha)
Defines the `JobApplication` class and builds a dataset of 15 realistic job applications across five tiers: FAANG, tech unicorns, mid-size companies, growing startups, and consulting/traditional tech. Data sourced from Levels.fyi and Glassdoor.

**Key class:**
- `JobApplication(company, role, prep_time, offer_prob, salary)` — automatically computes `expected_value` and `value_per_hour`

**Key functions:**
- `create_job_dataset()` → returns `list[JobApplication]` (15 jobs)
- `get_dataset_summary(jobs)` → returns dict with aggregate statistics

### `greedy_algorithm.py` (Monisha)
Implements the greedy heuristic: sort by EV/hour ratio descending, greedily pick items that fit. Returns a `GreedySolution` object.

**Key functions:**
- `greedy_knapsack(jobs, capacity)` → `GreedySolution`
- `demonstrate_greedy_limitation()` — runs the counterexample showing greedy fails

### `dp_algorithm.py` (Jinyu)
Implements the bottom-up dynamic programming solution for 0/1 Knapsack. Builds the full DP table, then backtracks to recover the optimal subset. Returns a `DPSolution` object.

**Recurrence:**
```
dp[i][w] = max(dp[i-1][w], dp[i-1][w - wᵢ] + vᵢ)   if wᵢ ≤ w
dp[i][w] = dp[i-1][w]                                  otherwise
```

**Key functions:**
- `dp_knapsack(jobs, capacity)` → `DPSolution` (includes `.dp_table` for visualization)
- `test_dp_algorithm()` — 7 test cases including counterexample verification

### `comparison.py` (Jinyu)
Runs both algorithms on the same dataset and compares results across multiple capacity values. Includes:
- Part 1: Comparison table across T = 40, 60, 80, 100, 120, 150
- Part 2: Detailed side-by-side at T = 100 (which jobs each picks)
- Part 3: Counterexample demonstration (capacity = 20, greedy fails by 2.2%)
- Part 4: Complexity summary table

**Key functions:**
- `compare_solutions(jobs, capacity)` → `(DPSolution, GreedySolution, gap)`
- `run_full_comparison()` — runs the full analysis

### `complexity_analysis.py` (Jinyu)
Detailed theoretical and empirical complexity analysis:
- Time and space complexity for both algorithms
- Pseudo-polynomial time explanation (why O(n×T) is NP-hard)
- Why greedy fails for 0/1 but works for Fractional Knapsack
- Empirical timing benchmarks on the dataset
- Scalability analysis with synthetic larger datasets

**Key function:**
- `run_complexity_analysis()` — prints full analysis with benchmarks

## Usage

**Prerequisites:** Python 3.8+ (no external dependencies)

```bash
# View the dataset
python3 dataset.py

# Run greedy algorithm with tests and counterexample
python3 greedy_algorithm.py

# Run DP algorithm with tests
python3 dp_algorithm.py

# Compare DP vs Greedy on the same dataset
python3 comparison.py

# Run complexity analysis with empirical benchmarks
python3 complexity_analysis.py
```

## Key Results

### Main Dataset (T = 100 hours)
Both DP and Greedy select the same 5 applications for $163,450 total EV. At T = 120, DP finds a solution $800 better than Greedy.

### Counterexample (T = 20 hours)

| Company | Prep Time | P(offer) | Salary | Expected Value | EV/hour |
|---------|-----------|----------|---------|----------------|---------|
| Company A | 18h | 35% | $160K | $56,000 | $3,111 ⭐ |
| Company B | 10h | 40% | $70K | $28,000 | $2,800 |
| Company C | 10h | 45% | $65K | $29,250 | $2,925 |

- **Greedy selects**: Company A → EV = $56,000 (2h wasted)
- **DP selects**: Companies B + C → EV = $57,250 (0h wasted)
- **DP is 2.2% better**

**Root cause:** Greedy's best-ratio choice (A) consumes 18 of 20 hours, blocking the better combination B+C. Items are indivisible — the greedy-choice property does not hold for 0/1 Knapsack.

### Complexity Summary

| Property | Dynamic Programming | Greedy Heuristic |
|----------|-------------------|-----------------|
| Time | O(n × T) | O(n log n) |
| Space | O(n × T) | O(n) |
| Optimal? | ✓ Yes (guaranteed) | ✗ No |
| Practical speed (n=15, T=100) | < 1ms | < 1ms |

O(n × T) is pseudo-polynomial: exponential in the bit-length of T, which is why 0/1 Knapsack is NP-hard despite having a "polynomial-looking" DP solution.

## Course Connection

- **Dynamic Programming**: Optimal substructure, overlapping subproblems, bottom-up table construction, backtracking
- **Greedy Algorithms**: When greedy works (Fractional Knapsack) vs. when it fails (0/1 Knapsack)
- **Complexity Analysis**: Pseudo-polynomial time, NP-hardness, empirical vs theoretical complexity

## Authors

- **Monisha Dhana Vijeya**: Dataset creation, greedy algorithm, testing, visualization/demo, presentation design
- **Jinyu Chen**: DP implementation, complexity analysis, counterexample construction, code documentation, comparison
