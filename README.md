# Job Application Optimization using 0/1 Knapsack

**CS 5800 - Algorithm Analysis Final Project**  
**By: Jinyu Chen & Monisha Dhana Vijeya**

## Overview

This project applies the 0/1 Knapsack problem to optimize job application strategy for graduate students with limited preparation time.

## Problem

Given:
- Multiple job applications with different preparation times, offer probabilities, and salaries
- Limited time budget for interview preparation

Find: Which applications to prepare for to maximize expected value?

**Expected Value = P(offer) × Salary**

## Implementation Status

### ✅ Completed (Monisha's Components)
- **Dataset** (`dataset.py`): 15 realistic job applications from FAANG, unicorns, mid-size companies, and startups
  - Data sources: Levels.fyi (salaries), Glassdoor (companies)
  - Salary range: $110K - $180K
  - Prep time range: 12-40 hours
  
- **Greedy Algorithm** (`greedy_algorithm.py`): O(n log n) heuristic
  - Selects applications by highest expected-value-per-hour ratio
  - 6 comprehensive test cases
  - Counterexample showing greedy fails by 2.2%

### 🔄 In Progress (Jinyu's Components)
- Dynamic programming implementation
- Optimal solution comparison

## Usage

**View dataset:**
```bash
python3 dataset.py
```

**Run greedy algorithm with tests:**
```bash
python3 greedy_algorithm.py
```

## Key Result: Greedy Counterexample

**Scenario**: 20 hours available

| Company | Prep Time | P(offer) | Salary | Expected Value | EV/hour |
|---------|-----------|----------|---------|----------------|---------|
| Company A | 18h | 35% | $160K | $56K | $3,111 ⭐ |
| Company B | 10h | 40% | $70K | $28K | $2,800 |
| Company C | 10h | 45% | $65K | $29.25K | $2,925 |

- **Greedy selects**: Company A → EV = $56,000
- **Optimal selects**: Companies B + C → EV = $57,250
- **Greedy is 2.2% suboptimal**

**Why?** Indivisibility! Company A has the best ratio but blocks the better combination B+C.

## Course Connection

- **Dynamic Programming**: Optimal substructure, overlapping subproblems
- **Greedy Algorithms**: When greedy works vs. fails (0/1 vs Fractional Knapsack)
- **Complexity Analysis**: Pseudo-polynomial time, NP-hardness

## Authors

- **Monisha Dhana Vijeya**: Dataset creation, greedy algorithm, testing
- **Jinyu Chen**: DP implementation, complexity analysis, code documentation
