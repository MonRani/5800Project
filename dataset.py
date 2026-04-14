"""
Job Application Dataset
Created by: Monisha Dhana Vijeya

This module contains realistic job application data based on:
- Levels.fyi for salary data
- Glassdoor for company information
- Personal experience for preparation time estimates
- Industry statistics for offer probability estimates
"""

class JobApplication:
    """Represents a single job application with associated metrics."""
    
    def __init__(self, company, role, prep_time, offer_prob, salary):
        """
        Initialize a job application.
        
        Args:
            company (str): Company name
            role (str): Job role/position
            prep_time (int): Estimated preparation time in hours
            offer_prob (float): Probability of receiving an offer (0-1)
            salary (int): Expected salary in USD
        """
        self.company = company
        self.role = role
        self.prep_time = prep_time
        self.offer_prob = offer_prob
        self.salary = salary
        self.expected_value = offer_prob * salary
        self.value_per_hour = self.expected_value / prep_time if prep_time > 0 else 0
    
    def __repr__(self):
        return (f"JobApplication(company='{self.company}', role='{self.role}', "
                f"prep_time={self.prep_time}h, offer_prob={self.offer_prob:.2f}, "
                f"salary=${self.salary:,}, EV=${self.expected_value:,.0f})")
    
    def to_dict(self):
        """Convert to dictionary for easy display."""
        return {
            'company': self.company,
            'role': self.role,
            'prep_time_hours': self.prep_time,
            'offer_probability': self.offer_prob,
            'salary': self.salary,
            'expected_value': self.expected_value,
            'value_per_hour': self.value_per_hour
        }


def create_job_dataset():
    """
    Create a realistic dataset of job applications.
    
    Data sources:
    - Salaries: Levels.fyi (2024-2025 data for new grad/entry-level roles)
    - Offer probabilities: Based on typical acceptance rates and competition levels
    - Prep times: Estimated based on interview process complexity
    
    Returns:
        list: List of JobApplication objects
    """
    jobs = [
        # FAANG companies - high salary, low probability, high prep time
        JobApplication(
            company="Google",
            role="Software Engineer L3",
            prep_time=40,
            offer_prob=0.08,
            salary=180000
        ),
        JobApplication(
            company="Meta",
            role="Software Engineer E3",
            prep_time=38,
            offer_prob=0.10,
            salary=175000
        ),
        JobApplication(
            company="Amazon",
            role="SDE I",
            prep_time=30,
            offer_prob=0.15,
            salary=155000
        ),
        JobApplication(
            company="Apple",
            role="Software Engineer",
            prep_time=35,
            offer_prob=0.09,
            salary=170000
        ),
        
        # Tech unicorns - high salary, moderate probability, moderate prep
        JobApplication(
            company="Stripe",
            role="Software Engineer",
            prep_time=28,
            offer_prob=0.12,
            salary=165000
        ),
        JobApplication(
            company="Databricks",
            role="Software Engineer",
            prep_time=32,
            offer_prob=0.11,
            salary=168000
        ),
        
        # Mid-size tech companies - good salary, better probability, moderate prep
        JobApplication(
            company="Salesforce",
            role="Software Engineer (MTS)",
            prep_time=25,
            offer_prob=0.18,
            salary=145000
        ),
        JobApplication(
            company="LinkedIn",
            role="Software Engineer",
            prep_time=27,
            offer_prob=0.14,
            salary=152000
        ),
        JobApplication(
            company="Snowflake",
            role="Software Engineer",
            prep_time=30,
            offer_prob=0.13,
            salary=160000
        ),
        
        # Growing startups - moderate salary, higher probability, lower prep
        JobApplication(
            company="Notion",
            role="Software Engineer",
            prep_time=20,
            offer_prob=0.22,
            salary=135000
        ),
        JobApplication(
            company="Discord",
            role="Software Engineer",
            prep_time=22,
            offer_prob=0.20,
            salary=140000
        ),
        
        # Smaller companies/startups - lower salary, highest probability, lowest prep
        JobApplication(
            company="Local Startup A",
            role="Full Stack Developer",
            prep_time=12,
            offer_prob=0.35,
            salary=110000
        ),
        JobApplication(
            company="Local Startup B",
            role="Backend Engineer",
            prep_time=15,
            offer_prob=0.30,
            salary=120000
        ),
        
        # Consulting/Traditional tech - moderate salary, moderate probability
        JobApplication(
            company="Accenture",
            role="Technology Consultant",
            prep_time=18,
            offer_prob=0.25,
            salary=125000
        ),
        JobApplication(
            company="IBM",
            role="Software Developer",
            prep_time=20,
            offer_prob=0.22,
            salary=115000
        ),
    ]
    
    return jobs


def get_dataset_summary(jobs):
    """
    Generate a summary of the dataset.
    
    Args:
        jobs (list): List of JobApplication objects
        
    Returns:
        dict: Summary statistics
    """
    total_prep_time = sum(job.prep_time for job in jobs)
    total_expected_value = sum(job.expected_value for job in jobs)
    avg_prep_time = total_prep_time / len(jobs)
    avg_salary = sum(job.salary for job in jobs) / len(jobs)
    avg_offer_prob = sum(job.offer_prob for job in jobs) / len(jobs)
    
    return {
        'total_applications': len(jobs),
        'total_prep_time_hours': total_prep_time,
        'avg_prep_time_hours': avg_prep_time,
        'total_expected_value': total_expected_value,
        'avg_salary': avg_salary,
        'avg_offer_probability': avg_offer_prob,
        'min_prep_time': min(job.prep_time for job in jobs),
        'max_prep_time': max(job.prep_time for job in jobs),
        'min_salary': min(job.salary for job in jobs),
        'max_salary': max(job.salary for job in jobs)
    }


if __name__ == "__main__":
    jobs = create_job_dataset()
    
    print("=" * 80)
    print("JOB APPLICATION DATASET")
    print("=" * 80)
    print(f"\nTotal Applications: {len(jobs)}\n")
    
    print(f"{'Company':<20} {'Role':<25} {'Prep(h)':<10} {'P(offer)':<12} {'Salary':<15} {'EV':<15} {'EV/h':<10}")
    print("-" * 120)
    
    for job in jobs:
        print(f"{job.company:<20} {job.role:<25} {job.prep_time:<10} "
              f"{job.offer_prob:<12.2f} ${job.salary:<14,} "
              f"${job.expected_value:<14,.0f} ${job.value_per_hour:<10,.0f}")
    
    print("\n" + "=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)
    
    summary = get_dataset_summary(jobs)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        elif isinstance(value, int) and value > 1000:
            print(f"{key}: {value:,}")
        else:
            print(f"{key}: {value}")
