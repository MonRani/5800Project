"""
Optimal Solution Comparison: Dynamic Programming vs Greedy
Created by: Jinyu Chen

This module compares the DP (optimal) and Greedy (heuristic) solutions
for the job application knapsack problem on the same dataset, demonstrating
when and why they diverge.
"""

from dataset import JobApplication, create_job_dataset, get_dataset_summary
from greedy_algorithm import greedy_knapsack
from dp_algorithm import dp_knapsack


def compare_solutions(jobs, capacity):
    """
    Run both DP and Greedy on the same input and compare results.
    
    Args:
        jobs (list): List of JobApplication objects
        capacity (int): Total available preparation time in hours
        
    Returns:
        tuple: (dp_solution, greedy_solution, gap)
    """
    dp_sol = dp_knapsack(jobs, capacity)
    greedy_sol = greedy_knapsack(jobs, capacity)
    gap = dp_sol.total_expected_value - greedy_sol.total_expected_value
    
    return dp_sol, greedy_sol, gap


def print_solution_detail(label, solution, capacity, color_marker=""):
    """Print detailed breakdown of a solution."""
    print(f"\n  {color_marker}{label}")
    print(f"  {'─' * 70}")
    print(f"  Total Expected Value: ${solution.total_expected_value:,.0f}")
    print(f"  Applications selected: {solution.num_applications}")
    print(f"  Prep time used: {solution.total_prep_time}h / {capacity}h "
          f"({capacity - solution.total_prep_time}h unused)")
    print()
    print(f"  {'Company':<20} {'Role':<25} {'Prep(h)':<8} {'EV':>10}  {'EV/h':>8}")
    print(f"  {'─'*20} {'─'*25} {'─'*8} {'─'*10}  {'─'*8}")
    for job in solution.selected_jobs:
        print(f"  {job.company:<20} {job.role:<25} {job.prep_time:<8} "
              f"${job.expected_value:>9,.0f}  ${job.value_per_hour:>7,.0f}")


def run_full_comparison():
    """
    Run a comprehensive comparison of DP vs Greedy on the project dataset.
    """
    jobs = create_job_dataset()
    summary = get_dataset_summary(jobs)
    
    print("=" * 80)
    print("  OPTIMAL SOLUTION COMPARISON: DP vs GREEDY")
    print("  0/1 Knapsack Applied to Job Application Strategy")
    print("=" * 80)
    
    print(f"\n  Dataset: {summary['total_applications']} job applications")
    print(f"  Total prep time if applying to all: {summary['total_prep_time_hours']} hours")
    print(f"  Salary range: ${summary['min_salary']:,} – ${summary['max_salary']:,}")
    
    # ─────────────────────────────────────────────────────────────────────
    # Part 1: Compare across multiple capacity values
    # ─────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("  PART 1: COMPARISON ACROSS CAPACITY VALUES")
    print("=" * 80)
    
    capacities = [40, 60, 80, 100, 120, 150]
    
    print(f"\n  {'Capacity':>10} {'DP Optimal':>14} {'Greedy':>14} {'Gap':>10} {'Gap %':>8}  {'Match?':>8}")
    print(f"  {'─'*10} {'─'*14} {'─'*14} {'─'*10} {'─'*8}  {'─'*8}")
    
    for cap in capacities:
        dp_sol, greedy_sol, gap = compare_solutions(jobs, cap)
        pct = (gap / greedy_sol.total_expected_value * 100) if greedy_sol.total_expected_value > 0 else 0
        match = "✓ Yes" if gap == 0 else "✗ No"
        print(f"  {cap:>8}h ${dp_sol.total_expected_value:>12,.0f} ${greedy_sol.total_expected_value:>12,.0f} "
              f"${gap:>8,.0f} {pct:>7.1f}%  {match:>8}")
    
    # ─────────────────────────────────────────────────────────────────────
    # Part 2: Detailed comparison at primary capacity (T=100)
    # ─────────────────────────────────────────────────────────────────────
    primary_cap = 100
    dp_sol, greedy_sol, gap = compare_solutions(jobs, primary_cap)
    
    print("\n" + "=" * 80)
    print(f"  PART 2: DETAILED COMPARISON (T = {primary_cap} hours)")
    print("=" * 80)
    
    print_solution_detail("DP OPTIMAL SOLUTION", dp_sol, primary_cap, "★ ")
    print_solution_detail("GREEDY HEURISTIC SOLUTION", greedy_sol, primary_cap, "◆ ")
    
    # Show which jobs differ
    dp_companies = {job.company for job in dp_sol.selected_jobs}
    greedy_companies = {job.company for job in greedy_sol.selected_jobs}
    
    only_dp = dp_companies - greedy_companies
    only_greedy = greedy_companies - dp_companies
    both = dp_companies & greedy_companies
    
    print(f"\n  {'─' * 70}")
    print(f"  SELECTION DIFFERENCES")
    print(f"  {'─' * 70}")
    print(f"  Selected by both:    {', '.join(sorted(both)) if both else 'None'}")
    print(f"  Only in DP:          {', '.join(sorted(only_dp)) if only_dp else 'None'}")
    print(f"  Only in Greedy:      {', '.join(sorted(only_greedy)) if only_greedy else 'None'}")
    
    print(f"\n  Gap: ${gap:,.0f}", end="")
    if gap == 0:
        print(" — Both algorithms agree on this capacity.")
    else:
        pct = gap / greedy_sol.total_expected_value * 100
        print(f" — DP is {pct:.1f}% better than Greedy.")
    
    # ─────────────────────────────────────────────────────────────────────
    # Part 3: Counterexample from the project
    # ─────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("  PART 3: COUNTEREXAMPLE — WHY GREEDY FAILS")
    print("=" * 80)
    
    counter_jobs = [
        JobApplication("Company A", "High EV/hour", 18, 0.35, 160000),   # EV=56000, EV/h=3111
        JobApplication("Company B", "Medium EV/hour", 10, 0.40, 70000),  # EV=28000, EV/h=2800
        JobApplication("Company C", "Medium EV/hour", 10, 0.45, 65000),  # EV=29250, EV/h=2925
    ]
    counter_cap = 20
    
    print(f"\n  Scenario: {counter_cap} hours available, 3 job applications")
    print(f"\n  {'Company':<15} {'Prep(h)':<10} {'P(offer)':<10} {'Salary':<12} {'EV':<12} {'EV/h':<10}")
    print(f"  {'─'*15} {'─'*10} {'─'*10} {'─'*12} {'─'*12} {'─'*10}")
    for job in counter_jobs:
        print(f"  {job.company:<15} {job.prep_time:<10} {job.offer_prob:<10.2f} "
              f"${job.salary:<11,} ${job.expected_value:<11,.0f} ${job.value_per_hour:<10,.0f}")
    
    dp_c, greedy_c, gap_c = compare_solutions(counter_jobs, counter_cap)
    
    print(f"\n  GREEDY selects: {[j.company for j in greedy_c.selected_jobs]}")
    print(f"    → Total EV: ${greedy_c.total_expected_value:,.0f}  "
          f"| Time: {greedy_c.total_prep_time}h / {counter_cap}h  "
          f"| {counter_cap - greedy_c.total_prep_time}h wasted")
    
    print(f"\n  DP OPTIMAL selects: {[j.company for j in dp_c.selected_jobs]}")
    print(f"    → Total EV: ${dp_c.total_expected_value:,.0f}  "
          f"| Time: {dp_c.total_prep_time}h / {counter_cap}h  "
          f"| {counter_cap - dp_c.total_prep_time}h wasted")
    
    pct_c = (gap_c / greedy_c.total_expected_value * 100) if greedy_c.total_expected_value > 0 else 0
    print(f"\n  Gap: ${gap_c:,.0f} — DP is {pct_c:.1f}% better than Greedy")
    
    print(f"\n  ROOT CAUSE:")
    print(f"  {'─' * 70}")
    print(f"  Greedy picks Company A (highest ratio: $3,111/hr) first, consuming")
    print(f"  18 of 20 hours. Only 2 hours remain — not enough for any other job.")
    print(f"  DP instead picks B + C (10h + 10h = 20h exactly) for $57,250 total.")
    print(f"")
    print(f"  The greedy-choice property does NOT hold for 0/1 Knapsack because")
    print(f"  items are indivisible. A locally optimal ratio choice can block a")
    print(f"  globally better combination.")
    
    # ─────────────────────────────────────────────────────────────────────
    # Part 4: Complexity summary
    # ─────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("  PART 4: COMPLEXITY ANALYSIS")
    print("=" * 80)
    
    n = len(jobs)
    T = primary_cap
    
    print(f"""
  ┌───────────────────────────────────────────────────────────────────┐
  │  Algorithm            Time            Space      Optimal?        │
  ├───────────────────────────────────────────────────────────────────┤
  │  Dynamic Programming  O(n × T)        O(n × T)   ✓ Yes          │
  │  Greedy Heuristic     O(n log n)      O(n)       ✗ No           │
  └───────────────────────────────────────────────────────────────────┘

  For our dataset (n={n}, T={T}):
    DP table size:   {n} × {T} = {n * T:,} cells
    Greedy sorts:    {n} × log({n}) ≈ {n * 4:.0f} comparisons

  Both run in under 1ms. DP is always preferable at this scale.

  Note: O(n × T) is pseudo-polynomial — exponential in the bit-length
  of T. This is why 0/1 Knapsack is NP-hard despite having a
  "polynomial-looking" DP solution.""")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    run_full_comparison()
