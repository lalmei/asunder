from typing import Dict, Set

from pydantic import BaseModel, Field

from asunder.metrics.process_metrics import (
    ChangeSetMetric,
    BugFixingCommentsMetric,
    HunksCountMetric,
    LinesCountMetric,
    ContributorsCountMetric,
    ContributorsExperienceMetric,
    CodeChurnMetric,
)


class MethodMetrics(BaseModel):
    commits: List[str] = Field(default_factory=list)
    authors: Set[str] = Field(default_factory=set)
    complexity: int = 0
    length: int = 0
    change_set: ChangeSetMetric = Field(default_factory=ChangeSetMetric)
    code_churn: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    commits_count: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    contributors_count: ContributorsCountMetric = Field(default_factory=ContributorsCountMetric)
    contributors_experience: ContributorsExperienceMetric = Field(default_factory=ContributorsExperienceMetric)
    hunks_count: HunksCountMetric = Field(default_factory=HunksCountMetric)
    lines_count: LinesCountMetric = Field(default_factory=LinesCountMetric)
    bug_fixing_comment: BugFixingCommentsMetric = Field(default_factory=BugFixingCommentsMetric)


class ClassMetrics(BaseModel):
    commits: List[str] = Field(default_factory=list)
    authors: Set[str] = Field(default_factory=set)
    methods: Dict[str, MethodMetrics] = Field(default_factory=dict)
    change_set: ChangeSetMetric = Field(default_factory=ChangeSetMetric)
    code_churn: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    commits_count: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    contributors_count: ContributorsCountMetric = Field(default_factory=ContributorsCountMetric)
    contributors_experience: ContributorsExperienceMetric = Field(default_factory=ContributorsExperienceMetric)
    hunks_count: HunksCountMetric = Field(default_factory=HunksCountMetric)
    lines_count: LinesCountMetric = Field(default_factory=LinesCountMetric)
    bug_fixing_comment: BugFixingCommentsMetric = Field(default_factory=BugFixingCommentsMetric)


class FileMetrics(BaseModel):
    commits: List[str] = Field(default_factory=list)
    authors: Set[str] = Field(default_factory=set)
    change_set: ChangeSetMetric = Field(default_factory=ChangeSetMetric)
    code_churn: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    commits_count: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    contributors_count: ContributorsCountMetric = Field(default_factory=ContributorsCountMetric)
    contributors_experience: ContributorsExperienceMetric = Field(default_factory=ContributorsExperienceMetric)
    hunks_count: HunksCountMetric = Field(default_factory=HunksCountMetric)
    lines_count: LinesCountMetric = Field(default_factory=LinesCountMetric)
    bug_fixing_comment: BugFixingCommentsMetric = Field(default_factory=BugFixingCommentsMetric)
    classes: Dict[str, ClassMetrics] = Field(default_factory=dict)


class SubmoduleMetrics(BaseModel):
    files: Dict[str, FileMetrics] = Field(default_factory=dict)


class ModuleMetrics(BaseModel):
    submodules: Dict[str, SubmoduleMetrics] = Field(default_factory=dict)


class RepoMetrics(BaseModel):
    modules: Dict[str, ModuleMetrics] = Field(default_factory=dict)
