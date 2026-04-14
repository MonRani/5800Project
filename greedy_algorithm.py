"""
Greedy Algorithm Implementation for Job Application Optimization
Created by: Monisha Dhana Vijeya

This module implements a greedy heuristic for the 0/1 Knapsack problem
applied to job application strategy. The greedy approach selects applications
in descending order of expected-value-per-hour ratio.
"""

from typing import List, Tuple
from dataset import JobApplication


class GreedySolution:
    """Represents the solution from the greedy algorithm."""
    
    def __init__(self, selected_jobs, total_expected_value, total_prep_time):
        """
        Initialize a greedy solution.
        
        Args:
            selected_jobs (list): List of selected JobApplication objects
            total_expected_value (float): Sum of expected values
            total_prep_time (int): Sum of preparation times
        """
        self.selected_jobs = selected_jobs
        self.total_expected_value = total_expected_value
        self.total_prep_time = total_prep_time
        self.num_applications = len(selected_jobs)
    
    def __repr__(self):
        return (f"GreedySolution(num_applications={self.num_applications}, "
                f"total_EV=${self.total_expected_value:,.0f}, "
                f"total_prep_time={self.total_prep_time}h)")


def greedy_knapsack(jobs: List[JobApplication], capacity: int) -> GreedySolution:
    """
    Solve the job application problem using a greedy heuristic.
    
    Strategy: Select applications in descending order of expected-value-per-hour
    ratio until the time budget is exhausted.
    
    Time Complexity: O(n log n) for sorting + O(n) for selection = O(n log n)
    Space Complexity: O(n) for storing sorted list
    
    Args:
        jobs (list): List of JobApplication objects
        capacity (int): Total available preparation time in hours
        
    Returns:
        GreedySolution: The greedy solution with selected applications
        
    Note:
        This greedy approach does NOT guarantee optimal solution for 0/1 Knapsack
        because items are indivisible. It works optimally for Fractional Knapsack
        but can fail for 0/1 variant.
    """
    if capacity <= 0:
        return GreedySolution([], 0, 0)
    
    if not jobs:
        return GreedySolution([], 0, 0)
    
    # Sort jobs by value-per-hour ratio in descending order
    # This is the greedy criterion
    sorted_jobs = sorted(jobs, key=lambda job: job.value_per_hour, reverse=True)
    
    selected = []
    total_value = 0
    total_time = 0
    
    # Greedily select jobs until capacity is reached
    for job in sorted_jobs:
        if total_time + job.prep_time <= capacity:
            selected.append(job)
            total_value += job.expected_value
            total_time += job.prep_time
    
    return GreedySolution(selected, total_value, total_time)


def test_greedy_algorithm():
    """
    Test the greedy algorithm with various scenarios.
    """
    print("=" * 80)
    print("GREEDY ALGORITHM TESTING")
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
    solution_1 = greedy_knapsack(test_jobs_1, capacity_1)
    
    print(f"Available time: {capacity_1} hours")
    print(f"\nAll jobs sorted by EV/hour:")
    for job in sorted(test_jobs_1, key=lambda j: j.value_per_hour, reverse=True):
        print(f"  {job.company}: EV=${job.expected_value:,.0f}, "
              f"Time={job.prep_time}h, EV/h=${job.value_per_hour:,.0f}")
    
    print(f"\nGreedy solution: {solution_1}")
    print(f"Selected companies:")
    for job in solution_1.selected_jobs:
        print(f"  - {job.company} ({job.role})")
    
    # Test Case 2: Edge case - capacity 0
    print("\n" + "=" * 80)
    print("Test Case 2: Zero capacity")
    print("-" * 80)
    solution_2 = greedy_knapsack(test_jobs_1, 0)
    print(f"Capacity: 0 hours")
    print(f"Solution: {solution_2}")
    
    # Test Case 3: Edge case - empty job list
    print("\n" + "=" * 80)
    print("Test Case 3: Empty job list")
    print("-" * 80)
    solution_3 = greedy_knapsack([], 50)
    print(f"Capacity: 50 hours")
    print(f"Solution: {solution_3}")
    
    # Test Case 4: Capacity exceeds total prep time
    print("\n" + "=" * 80)
    print("Test Case 4: Capacity exceeds total prep time")
    print("-" * 80)
    total_time = sum(job.prep_time for job in test_jobs_1)
    solution_4 = greedy_knapsack(test_jobs_1, total_time + 100)
    print(f"Total prep time for all jobs: {total_time} hours")
    print(f"Available capacity: {total_time + 100} hours")
    print(f"Solution: {solution_4}")
    print(f"Selected all jobs: {len(solution_4.selected_jobs) == len(test_jobs_1)}")
    
    # Test Case 5: Single job that fits
    print("\n" + "=" * 80)
    print("Test Case 5: Single job that fits")
    print("-" * 80)
    single_job = [JobApplication("Solo Company", "Solo Role", 10, 0.3, 80000)]
    solution_5 = greedy_knapsack(single_job, 15)
    print(f"Solution: {solution_5}")
    
    # Test Case 6: Single job that doesn't fit
    print("\n" + "=" * 80)
    print("Test Case 6: Single job that doesn't fit")
    print("-" * 80)
    solution_6 = greedy_knapsack(single_job, 5)
    print(f"Solution: {solution_6}")
    
    print("\n" + "=" * 80)
    print("All test cases completed successfully!")
    print("=" * 80)


def demonstrate_greedy_limitation():
    """
    Demonstrate a counterexample where greedy fails to find optimal solution.
    
    This is a classic counterexample for 0/1 Knapsack:
    The greedy algorithm selects the item with highest value-per-weight ratio,
    but this may prevent selecting a better combination.
    """
    print("\n" + "=" * 80)
    print("GREEDY ALGORITHM LIMITATION - COUNTEREXAMPLE")
    print("=" * 80)
    
    # Construct a counterexample
    # Job A: High EV/hour but takes most capacity
    # Jobs B + C: Lower EV/hour individually but together give more total EV
    counterexample_jobs = [
        JobApplication("Company A", "High EV/hour", 18, 0.35, 160000),  # EV=56000, EV/h=3111
        JobApplication("Company B", "Medium EV/hour", 10, 0.40, 70000),  # EV=28000, EV/h=2800
        JobApplication("Company C", "Medium EV/hour", 10, 0.45, 65000),  # EV=29250, EV/h=2925
    ]
    
    capacity = 20
    
    print(f"\nScenario: You have {capacity} hours to prepare for interviews.")
    print("\nAvailable applications:")
    print(f"{'Company':<15} {'Prep Time':<12} {'P(offer)':<12} {'Salary':<15} {'EV':<15} {'EV/hour':<12}")
    print("-" * 90)
    
    for job in counterexample_jobs:
        print(f"{job.company:<15} {job.prep_time:<12}h {job.offer_prob:<12.2f} "
              f"${job.salary:<14,} ${job.expected_value:<14,.0f} ${job.value_per_hour:<12,.0f}")
    
    # Run greedy
    greedy_sol = greedy_knapsack(counterexample_jobs, capacity)
    
    print(f"\n{'-'*80}")
    print("GREEDY APPROACH:")
    print(f"{'-'*80}")
    print(f"Strategy: Select by highest EV/hour ratio")
    print(f"\nGreedy selects: {[job.company for job in greedy_sol.selected_jobs]}")
    print(f"Total Expected Value: ${greedy_sol.total_expected_value:,.0f}")
    print(f"Total Prep Time: {greedy_sol.total_prep_time} hours")
    print(f"Unused Time: {capacity - greedy_sol.total_prep_time} hours")
    
    # Calculate alternative (optimal) solution manually
    optimal_jobs = [counterexample_jobs[1], counterexample_jobs[2]]  # B + C
    optimal_ev = sum(job.expected_value for job in optimal_jobs)
    optimal_time = sum(job.prep_time for job in optimal_jobs)
    
    print(f"\n{'-'*80}")
    print("OPTIMAL SOLUTION (for comparison):")
    print(f"{'-'*80}")
    print(f"Optimal selects: {[job.company for job in optimal_jobs]}")
    print(f"Total Expected Value: ${optimal_ev:,.0f}")
    print(f"Total Prep Time: {optimal_time} hours")
    
    print(f"\n{'-'*80}")
    print("ANALYSIS:")
    print(f"{'-'*80}")
    print(f"Greedy EV: ${greedy_sol.total_expected_value:,.0f}")
    print(f"Optimal EV: ${optimal_ev:,.0f}")
    print(f"Difference: ${optimal_ev - greedy_sol.total_expected_value:,.0f}")
    print(f"Greedy is {(optimal_ev - greedy_sol.total_expected_value) / greedy_sol.total_expected_value * 100:.1f}% worse than optimal")
    
    print(f"\n{'-'*80}")
    print("WHY GREEDY FAILS:")
    print(f"{'-'*80}")
    print("The greedy algorithm selects Company A because it has the highest EV/hour")
    print("ratio. However, Company A uses 18 of our 20 hours, leaving only 2 hours")
    print("unused - not enough for any other application.")
    print()
    print("The optimal solution skips Company A (even though it has the best ratio)")
    print("and instead selects Companies B and C. Together, they:")
    print(f"  - Use exactly {optimal_time} hours (fit perfectly in our budget)")
    print(f"  - Provide ${optimal_ev:,.0f} total EV vs ${greedy_sol.total_expected_value:,.0f} from greedy")
    print()
    print("This demonstrates why 0/1 Knapsack requires dynamic programming:")
    print("Items are INDIVISIBLE - we can't take 'half' of Company A.")
    print("A locally optimal choice (best ratio) can block globally optimal combinations.")
    
    return counterexample_jobs, capacity, greedy_sol


if __name__ == "__main__":
    test_greedy_algorithm()
    demonstrate_greedy_limitation()
