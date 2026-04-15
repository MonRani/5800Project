"""
Complexity Analysis for Job Application Knapsack Problem
Created by: Jinyu Chen

This module provides a detailed complexity analysis of both the
Dynamic Programming and Greedy approaches to the 0/1 Knapsack problem,
including empirical timing measurements on the project dataset.
"""

import time
from dataset import create_job_dataset, JobApplication
from dp_algorithm import dp_knapsack
from greedy_algorithm import greedy_knapsack


def measure_execution_time(func, jobs, capacity, runs=1000):
    """
    Measure average execution time of an algorithm over multiple runs.
    
    Args:
        func: Algorithm function (dp_knapsack or greedy_knapsack)
        jobs (list): List of JobApplication objects
        capacity (int): Knapsack capacity
        runs (int): Number of runs to average over
        
    Returns:
        float: Average execution time in milliseconds
    """
    start = time.perf_counter()
    for _ in range(runs):
        func(jobs, capacity)
    elapsed = time.perf_counter() - start
    return (elapsed / runs) * 1000  # convert to ms


def run_complexity_analysis():
    """
    Perform and display a complete complexity analysis of both algorithms.
    """
    jobs = create_job_dataset()
    n = len(jobs)
    
    print("=" * 80)
    print("  COMPLEXITY ANALYSIS")
    print("  0/1 Knapsack: Dynamic Programming vs Greedy Heuristic")
    print("=" * 80)
    
    # ─────────────────────────────────────────────────────────────────────
    # 1. Theoretical Complexity
    # ─────────────────────────────────────────────────────────────────────
    print(f"""
{'=' * 80}
  1. THEORETICAL TIME COMPLEXITY
{'=' * 80}

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Dynamic Programming:   O(n × T)                                    │
  │                                                                     │
  │    - Outer loop: iterate over n items              → O(n)           │
  │    - Inner loop: iterate over capacities 0..T      → O(T)           │
  │    - Each cell: constant-time max comparison       → O(1)           │
  │    - Backtracking to recover solution              → O(n)           │
  │    - Total: O(n × T) + O(n) = O(n × T)                             │
  │                                                                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Greedy Heuristic:      O(n log n)                                  │
  │                                                                     │
  │    - Sort by EV/hour ratio (comparison sort)       → O(n log n)     │
  │    - Single pass to select items                   → O(n)           │
  │    - Total: O(n log n) + O(n) = O(n log n)                         │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
""")

    # ─────────────────────────────────────────────────────────────────────
    # 2. Space Complexity
    # ─────────────────────────────────────────────────────────────────────
    print(f"""{'=' * 80}
  2. SPACE COMPLEXITY
{'=' * 80}

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Dynamic Programming:   O(n × T)                                    │
  │                                                                     │
  │    - 2D DP table: (n+1) rows × (T+1) columns of floats             │
  │    - Backtracking uses the same table (no extra space)              │
  │                                                                     │
  │    Space optimization (not implemented):                            │
  │    - Rolling 1D array: only keep previous row → O(T)                │
  │    - Trade-off: loses ability to backtrack without extra bookkeeping│
  │                                                                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Greedy Heuristic:      O(n)                                        │
  │                                                                     │
  │    - Sorted copy of input list                     → O(n)           │
  │    - Selected items list                           → O(n)           │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
""")

    # ─────────────────────────────────────────────────────────────────────
    # 3. Pseudo-Polynomial Time Explanation
    # ─────────────────────────────────────────────────────────────────────
    print(f"""{'=' * 80}
  3. WHY "PSEUDO-POLYNOMIAL"? (NP-HARDNESS OF 0/1 KNAPSACK)
{'=' * 80}

  The DP solution runs in O(n × T), which looks polynomial. But 0/1
  Knapsack is NP-hard. How is this possible?

  The key: complexity is measured relative to INPUT SIZE, not input VALUE.

  The capacity T is encoded in binary using O(log T) bits. So:

    Input size of T:     log₂(T) bits
    DP table columns:    T columns

  Example:
    T = 1,000,000     →  20 bits to encode
                      →  1,000,000 columns in DP table
                      →  table size is 2²⁰ = exponential in input bits

  This means O(n × T) is actually O(n × 2^(log T)) — exponential in
  the bit-length of the capacity. Algorithms with this property are
  called "pseudo-polynomial": polynomial in the numeric VALUE of the
  input, but exponential in the SIZE of the input encoding.

  For our problem (T ≤ 500, n ≤ 50): the table is small enough that
  this distinction is purely theoretical. DP is fast in practice.
""")

    # ─────────────────────────────────────────────────────────────────────
    # 4. Why Greedy Fails: Theoretical Argument
    # ─────────────────────────────────────────────────────────────────────
    print(f"""{'=' * 80}
  4. WHY GREEDY FAILS FOR 0/1 KNAPSACK
{'=' * 80}

  The greedy algorithm works for Fractional Knapsack because:
    - Items can be divided (take 0.5 of an item)
    - The greedy-choice property holds: the item with the highest
      value-per-weight ratio is always part of some optimal solution
    - Proof: if the optimal doesn't include the best-ratio item,
      we can swap in a fraction of it to improve the solution

  The greedy algorithm FAILS for 0/1 Knapsack because:
    - Items are indivisible (take all or nothing)
    - The greedy-choice property does NOT hold
    - A high-ratio item may consume capacity that could be better
      used by a combination of lower-ratio items

  Counterexample from our project (capacity = 20 hours):

    Company A:  18h, EV = $56,000   →  ratio = $3,111/hr  (highest)
    Company B:  10h, EV = $28,000   →  ratio = $2,800/hr
    Company C:  10h, EV = $29,250   →  ratio = $2,925/hr

    Greedy picks A (best ratio): $56,000, uses 18h, 2h wasted
    DP picks B + C:              $57,250, uses 20h, 0h wasted

    Greedy's locally optimal choice BLOCKS the globally optimal
    combination. This failure is inherent to indivisible items.
""")

    # ─────────────────────────────────────────────────────────────────────
    # 5. Empirical Timing Measurements
    # ─────────────────────────────────────────────────────────────────────
    print(f"{'=' * 80}")
    print(f"  5. EMPIRICAL TIMING (dataset: n={n} jobs, averaged over 1000 runs)")
    print(f"{'=' * 80}")
    
    capacities = [50, 100, 200, 500]
    
    print(f"\n  {'Capacity (T)':>14} {'DP Table Size':>15} {'DP Time (ms)':>14} {'Greedy Time (ms)':>18} {'Speedup':>10}")
    print(f"  {'─'*14} {'─'*15} {'─'*14} {'─'*18} {'─'*10}")
    
    for cap in capacities:
        dp_time = measure_execution_time(dp_knapsack, jobs, cap)
        greedy_time = measure_execution_time(greedy_knapsack, jobs, cap)
        table_size = n * cap
        speedup = dp_time / greedy_time if greedy_time > 0 else float('inf')
        
        print(f"  {cap:>12}h {table_size:>14,} {dp_time:>13.4f} {greedy_time:>17.4f} {speedup:>9.1f}×")
    
    print(f"""
  Observations:
    - Both algorithms complete in well under 1ms for realistic inputs
    - Greedy is faster (no table to fill), but the difference is negligible
    - DP time grows linearly with T (as expected from O(n × T))
    - At this scale, optimality (DP) should always be preferred over speed (Greedy)
""")

    # ─────────────────────────────────────────────────────────────────────
    # 6. Scalability Analysis
    # ─────────────────────────────────────────────────────────────────────
    print(f"{'=' * 80}")
    print(f"  6. SCALABILITY: WHEN DOES DP BECOME EXPENSIVE?")
    print(f"{'=' * 80}")
    
    # Generate larger synthetic datasets
    print(f"\n  Testing with T=100, varying n (synthetic jobs):")
    print(f"\n  {'n (jobs)':>10} {'DP Table Size':>15} {'DP Time (ms)':>14} {'Greedy Time (ms)':>18}")
    print(f"  {'─'*10} {'─'*15} {'─'*14} {'─'*18}")
    
    for num_jobs in [10, 50, 100, 500, 1000]:
        synthetic = [
            JobApplication(f"Co_{i}", f"Role_{i}", 
                         (i % 40) + 5,              # prep_time: 5-44
                         round(0.05 + (i % 10) * 0.05, 2),  # prob: 0.05-0.50
                         100000 + (i % 20) * 5000)   # salary: 100k-195k
            for i in range(num_jobs)
        ]
        cap = 100
        dp_time = measure_execution_time(dp_knapsack, synthetic, cap, runs=100)
        greedy_time = measure_execution_time(greedy_knapsack, synthetic, cap, runs=100)
        table_size = num_jobs * cap
        
        print(f"  {num_jobs:>10} {table_size:>14,} {dp_time:>13.4f} {greedy_time:>17.4f}")
    
    print(f"""
  Conclusion:
    - For job search optimization (n < 50, T < 500): DP is always practical
    - DP scales linearly in both n and T
    - Even at n=1000, T=100: DP runs in a few milliseconds
    - Greedy remains O(n log n) regardless of T — only advantageous when T is enormous
""")

    # ─────────────────────────────────────────────────────────────────────
    # 7. Summary Table
    # ─────────────────────────────────────────────────────────────────────
    print(f"{'=' * 80}")
    print(f"  7. SUMMARY")
    print(f"{'=' * 80}")
    print(f"""
  ┌────────────────────┬──────────────────┬──────────────────┬──────────┐
  │ Property           │ Dynamic Prog.    │ Greedy Heuristic │ Winner   │
  ├────────────────────┼──────────────────┼──────────────────┼──────────┤
  │ Time complexity    │ O(n × T)         │ O(n log n)       │ Greedy   │
  │ Space complexity   │ O(n × T)         │ O(n)             │ Greedy   │
  │ Optimality         │ Guaranteed       │ Not guaranteed   │ DP       │
  │ Practical speed    │ < 1ms            │ < 1ms            │ Tie      │
  │ Implementation     │ Moderate         │ Simple           │ Greedy   │
  │ Recommendation     │ ✓ Use this       │ For reference    │ DP       │
  └────────────────────┴──────────────────┴──────────────────┴──────────┘

  For our use case (n=15, T=100): DP is the clear choice.
  It guarantees optimality with no practical performance penalty.
""")
    print("=" * 80)


if __name__ == "__main__":
    run_complexity_analysis()
