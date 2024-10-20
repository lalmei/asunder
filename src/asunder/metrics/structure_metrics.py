from pydantic import BaseModel, Field

from asunder.metrics.process_metrics import (
    ChangeSetMetric,
    CodeChurnMetric,
    BugFixingCommentsMetric,
    HunksCountMetric,
    LinesCountMetric,
    ContributorsCountMetric,
    ContributorsExperienceMetric,
    CodeChurnMetric,
)


class MethodMetrics(BaseModel):
    commits: list[str] = Field(default_factory=list)
    authors: set[str] = Field(default_factory=set)
    complexity: int = 0
    length: int = 0
    change_set: ChangeSetMetric = Field(default_factory=ChangeSetMetric)
    code_churn: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    bug_fixing_comment: BugFixingCommentsMetric = Field(default_factory=BugFixingCommentsMetric)


class ClassMetrics(BaseModel):
    commits: list[str] = Field(default_factory=list)
    authors: set[str] = Field(default_factory=set)
    methods: dict[str, MethodMetrics] = Field(default_factory=dict)


class FileMetrics(BaseModel):
    commits: list[str] = Field(default_factory=list)
    authors: set[str] = Field(default_factory=set)
    change_set: ChangeSetMetric = Field(default_factory=ChangeSetMetric)
    code_churn: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    commits_count: CodeChurnMetric = Field(default_factory=CodeChurnMetric)
    contributors_count: ContributorsCountMetric = Field(default_factory=ContributorsCountMetric)
    contributors_experience: ContributorsExperienceMetric = Field(default_factory=ContributorsExperienceMetric)
    hunks_count: HunksCountMetric = Field(default_factory=HunksCountMetric)
    lines_count: LinesCountMetric = Field(default_factory=LinesCountMetric)
    bug_fixing_comment: BugFixingCommentsMetric = Field(default_factory=BugFixingCommentsMetric)
    classes: dict[str, ClassMetrics] = Field(default_factory=dict)


class SubmoduleMetrics(BaseModel):
    files: dict[str, FileMetrics] = Field(default_factory=dict)


class ModuleMetrics(BaseModel):
    submodules: dict[str, SubmoduleMetrics] = Field(default_factory=dict)


class RepoMetrics(BaseModel):
    modules: dict[str, ModuleMetrics] = Field(default_factory=dict)
