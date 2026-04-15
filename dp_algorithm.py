"""
Dynamic Programming Implementation for Job Application Optimization
Created by: Jinyu Chen

This module implements the 0/1 Knapsack dynamic programming solution
applied to job application strategy. The DP approach guarantees the
globally optimal subset of applications within a given time budget.
"""

from typing import List, Tuple
from dataset import JobApplication, create_job_dataset


class DPSolution:
    """Represents the solution from the dynamic programming algorithm."""
    
    def __init__(self, selected_jobs, total_expected_value, total_prep_time, dp_table=None):
        """
        Initialize a DP solution.
        
        Args:
            selected_jobs (list): List of selected JobApplication objects
            total_expected_value (float): Sum of expected values
            total_prep_time (int): Sum of preparation times
            dp_table (list): The full DP table (optional, for visualization)
        """
        self.selected_jobs = selected_jobs
        self.total_expected_value = total_expected_value
        self.total_prep_time = total_prep_time
        self.num_applications = len(selected_jobs)
        self.dp_table = dp_table
    
    def __repr__(self):
        return (f"DPSolution(num_applications={self.num_applications}, "
                f"total_EV=${self.total_expected_value:,.0f}, "
                f"total_prep_time={self.total_prep_time}h)")


def dp_knapsack(jobs: List[JobApplication], capacity: int) -> DPSolution:
    """
    Solve the job application problem using bottom-up dynamic programming.
    
    This is the standard 0/1 Knapsack DP algorithm. We define:
        dp[i][w] = maximum expected value using items {0, ..., i-1} with capacity w
    
    Recurrence:
        dp[i][w] = max(dp[i-1][w],                         # skip item i
                       dp[i-1][w - w_i] + v_i)              # take item i (if w_i <= w)
    
    Base case:
        dp[0][w] = 0 for all w
    
    After filling the table, we backtrack from dp[n][capacity] to recover
    the selected subset.
    
    Time Complexity:  O(n * T) where n = number of jobs, T = capacity
    Space Complexity: O(n * T) for the full DP table
    
    Note on pseudo-polynomial time:
        The input size of T is O(log T) bits, so O(n * T) is exponential in
        the bit-length of T. This is why 0/1 Knapsack remains NP-hard despite
        having a "polynomial-looking" DP solution.
    
    Args:
        jobs (list): List of JobApplication objects
        capacity (int): Total available preparation time in hours
        
    Returns:
        DPSolution: The optimal solution with selected applications and DP table
    """
    if capacity <= 0:
        return DPSolution([], 0, 0)
    
    if not jobs:
        return DPSolution([], 0, 0)
    
    n = len(jobs)
    
    # Build DP table: dp[i][w] = max expected value using items 0..i-1 with capacity w
    dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        job = jobs[i - 1]
        for w in range(capacity + 1):
            # Option 1: skip item i
            dp[i][w] = dp[i - 1][w]
            # Option 2: take item i (if it fits)
            if job.prep_time <= w:
                value_with_item = dp[i - 1][w - job.prep_time] + job.expected_value
                if value_with_item > dp[i][w]:
                    dp[i][w] = value_with_item
    
    # Backtrack to find selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(jobs[i - 1])
            w -= jobs[i - 1].prep_time
    
    selected.reverse()
    
    total_ev = dp[n][capacity]
    total_time = sum(job.prep_time for job in selected)
    
    return DPSolution(selected, total_ev, total_time, dp_table=dp)


def test_dp_algorithm():
    """
    Test the DP algorithm with various scenarios.
    """
    print("=" * 80)
    print("DYNAMIC PROGRAMMING ALGORITHM TESTING")
    print("=" * 80)
    
    # Test Case 1: Simple example
    print("\nTest Case 1: Simple 3-job example")
    print("-" * 80)
    test_jobs_1 = [
        JobApplication("Company A", "Role A", 10, 0.5, 100000),
        JobApplication("Company B", "Role B", 20, 0.4, 150000),
        JobApplication("Company C", "Role C", 15, 0.6, 120000),
    ]
    
    capacity_1 = 25
    solution_1 = dp_knapsack(test_jobs_1, capacity_1)
    
    print(f"Available time: {capacity_1} hours")
    print(f"\nAll jobs:")
    for job in test_jobs_1:
        print(f"  {job.company}: EV=${job.expected_value:,.0f}, "
              f"Time={job.prep_time}h, EV/h=${job.value_per_hour:,.0f}")
    
    print(f"\nDP optimal solution: {solution_1}")
    print(f"Selected companies:")
    for job in solution_1.selected_jobs:
        print(f"  - {job.company} ({job.role})")
    
    # Test Case 2: Edge case - capacity 0
    print("\n" + "=" * 80)
    print("Test Case 2: Zero capacity")
    print("-" * 80)
    solution_2 = dp_knapsack(test_jobs_1, 0)
    print(f"Capacity: 0 hours")
    print(f"Solution: {solution_2}")
    assert solution_2.num_applications == 0, "Should select no jobs"
    print("PASSED")
    
    # Test Case 3: Edge case - empty job list
    print("\n" + "=" * 80)
    print("Test Case 3: Empty job list")
    print("-" * 80)
    solution_3 = dp_knapsack([], 50)
    print(f"Capacity: 50 hours")
    print(f"Solution: {solution_3}")
    assert solution_3.num_applications == 0, "Should select no jobs"
    print("PASSED")
    
    # Test Case 4: Capacity exceeds total prep time (should select all)
    print("\n" + "=" * 80)
    print("Test Case 4: Capacity exceeds total prep time")
    print("-" * 80)
    total_time = sum(job.prep_time for job in test_jobs_1)
    solution_4 = dp_knapsack(test_jobs_1, total_time + 100)
    print(f"Total prep time for all jobs: {total_time} hours")
    print(f"Available capacity: {total_time + 100} hours")
    print(f"Solution: {solution_4}")
    assert solution_4.num_applications == len(test_jobs_1), "Should select all jobs"
    print(f"Selected all jobs: True")
    print("PASSED")
    
    # Test Case 5: Single job that fits
    print("\n" + "=" * 80)
    print("Test Case 5: Single job that fits")
    print("-" * 80)
    single_job = [JobApplication("Solo Company", "Solo Role", 10, 0.3, 80000)]
    solution_5 = dp_knapsack(single_job, 15)
    print(f"Solution: {solution_5}")
    assert solution_5.num_applications == 1, "Should select the one job"
    print("PASSED")
    
    # Test Case 6: Single job that doesn't fit
    print("\n" + "=" * 80)
    print("Test Case 6: Single job that doesn't fit")
    print("-" * 80)
    solution_6 = dp_knapsack(single_job, 5)
    print(f"Solution: {solution_6}")
    assert solution_6.num_applications == 0, "Should select no jobs"
    print("PASSED")
    
    # Test Case 7: Verify DP beats greedy on the counterexample from greedy_algorithm.py
    print("\n" + "=" * 80)
    print("Test Case 7: Counterexample verification (capacity=20)")
    print("-" * 80)
    counterexample_jobs = [
        JobApplication("Company A", "High EV/hour", 18, 0.35, 160000),   # EV=56000
        JobApplication("Company B", "Medium EV/hour", 10, 0.40, 70000),  # EV=28000
        JobApplication("Company C", "Medium EV/hour", 10, 0.45, 65000),  # EV=29250
    ]
    solution_7 = dp_knapsack(counterexample_jobs, 20)
    print(f"DP optimal: {solution_7}")
    print(f"Selected: {[job.company for job in solution_7.selected_jobs]}")
    print(f"DP EV: ${solution_7.total_expected_value:,.0f}")
    assert solution_7.total_expected_value == 57250.0, \
        f"Expected $57,250 but got ${solution_7.total_expected_value:,.0f}"
    print("PASSED — DP correctly finds B+C ($57,250) over greedy's A ($56,000)")
    
    print("\n" + "=" * 80)
    print("All test cases completed successfully!")
    print("=" * 80)


def demonstrate_dp_on_dataset():
    """
    Run the DP algorithm on the full job application dataset
    with various capacity values.
    """
    jobs = create_job_dataset()
    
    print("\n" + "=" * 80)
    print("DP ALGORITHM ON FULL DATASET")
    print("=" * 80)
    
    for capacity in [50, 80, 100, 120]:
        solution = dp_knapsack(jobs, capacity)
        
        print(f"\n{'─' * 80}")
        print(f"Capacity: {capacity} hours")
        print(f"{'─' * 80}")
        print(f"Optimal EV: ${solution.total_expected_value:,.0f}")
        print(f"Prep time used: {solution.total_prep_time}h / {capacity}h")
        print(f"Applications selected ({solution.num_applications}):")
        
        for job in solution.selected_jobs:
            print(f"  {job.company:<20} {job.role:<25} "
                  f"Time={job.prep_time:>3}h  EV=${job.expected_value:>10,.0f}  "
                  f"EV/h=${job.value_per_hour:>8,.0f}")


if __name__ == "__main__":
    test_dp_algorithm()
    demonstrate_dp_on_dataset()
