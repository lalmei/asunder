from abc import abstractmethod

# from pydantic import BaseModel, Field
from typing import Dict, Protocol, Any


# Base Metric class with Pydantic
class Metric(Protocol):
    def __init__(self, name):
        self.name = name

    def calculate(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def reset(self):
        pass


# Specific metric: Change Frequency
class ChangeFrequency(Metric):
    def __init__(self):
        super().__init__("Change Frequency")
        self.changes = 0

    def calculate(self):
        return self.changes

    def update(self):
        self.changes += 1

    def reset(self):
        self.changes = 0


# Specific metric: Comment Density
class CommentDensityMetric(Metric):
    def __init__(self):
        super().__init__("Comment Density")
        self.comment_lines = 0
        self.total_lines = 0

    def calculate(self):
        return self.comment_lines / self.total_lines if self.total_lines > 0 else 0

    def update(self, comment_lines, total_lines):
        self.comment_lines += comment_lines
        self.total_lines += total_lines

    def reset(self):
        self.comment_lines = 0
        self.total_lines = 0


class ChangeSetMetric(Metric):
    name: str = "change_set"

    def calculate(self, data: Dict[str, Any]) -> float:
        # The size of the change set is often defined as the number of files modified in a commit
        return data.get("change_set_size", 0)


class CodeChurnMetric(Metric):
    name: str = "code_churn"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Code churn is typically the sum of lines added and lines removed
        additions = data.get("additions", 0)
        deletions = data.get("deletions", 0)
        return additions + deletions


class CommitsCountMetric(Metric):
    name: str = "commits_count"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Number of commits impacting a particular entity (submodule, file, etc.)
        return len(data.get("commits", []))


class ContributorsCountMetric(Metric):
    name: str = "contributors_count"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Number of unique contributors/authors
        return len(set(data.get("authors", [])))


class ContributorsExperienceMetric(Metric):
    name: str = "contributors_experience"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Calculate the average experience (number of commits) of each contributor
        author_commits = data.get("author_commit_counts", {})
        if not author_commits:
            return 0
        total_commits = sum(author_commits.values())
        num_contributors = len(author_commits)
        return total_commits / num_contributors if num_contributors > 0 else 0


class HunksCountMetric(Metric):
    name: str = "hunks_count"

    def calculate(self, data: Dict[str, Any]) -> float:
        # A hunk is typically a contiguous block of changes in a diff
        return data.get("hunks_count", 0)


class LinesCountMetric(Metric):
    name: str = "lines_count"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Total number of lines in the entity (could be file or class)
        return data.get("lines_count", 0)


class BugFixingCommentsMetric(Metric):
    name: str = "bug_fixing_comments"

    def calculate(self, data: Dict[str, Any]) -> float:
        # Counting comments or commit messages that indicate a bug fix
        return sum(
            1
            for comment in data.get("comments", [])
            if "fix" in comment.lower() or "bug" in comment.lower()
        )
