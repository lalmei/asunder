from datetime import datetime
from pydriller import Repository


def get_time_period_since_first_commit(repo: Repository) -> int:
    """
    Calculates the number of days between the current date
    and the date of the first commit in the repository.

    Args:
        repo: A `Repository` object representing the Git repository.

    Returns:
        The number of days since the first commit.
    """
    first_commit_date = next(repo.traverse_commits()).committer_date
    current_date = datetime.now()
    time_difference = current_date - first_commit_date
    return time_difference.days
