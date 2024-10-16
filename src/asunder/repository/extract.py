from os import path

from pydriller import Repository

from asunder.metrics.structure_metrics import (
    RepoMetrics,
    SubmoduleMetrics,
    FileMetrics,
)
from asunder.analysis.analyze_content import analyze_file_content


def extract_repo_data(repo_path: str, since_date, to_date) -> RepoMetrics:
    repo_data = RepoMetrics()
    repo = Repository(repo_path, since=since_date, to=to_date)

    for commit in repo.traverse_commits():
        for file in commit.modified_files:
            if file.filename.endswith(".py"):
                file_path = path.normpath(path.join(repo_path, file.filename))
                repo_name = path.basename(path)
                submodule = path.dirname(file_path)
                module = path.basename(path.dirname(submodule))
                repo_data.modules.setdefault(repo_name, RepoMetrics())
                # Create or get existing metrics for module, submodule, and file
                module_metrics = repo_data.submodules.setdefault(module, SubmoduleMetrics())
                submodule_metrics = module_metrics.files.setdefault(submodule, SubmoduleMetrics())
                file_metrics = submodule_metrics.files.setdefault(file_path, FileMetrics())

                # Update file-level metrics
                file_metrics.commits.append(commit.hash)
                file_metrics.authors.add(commit.author.name)
                file_metrics.change_set.update(commit)
                file_metrics.code_churn.update(file.added_lines, file.deleted_lines)
                file_metrics.bug_fixing_comment.update(commit.msg)

                # Analyze the content of the file for classes and methods
                if file.source_code:
                    analyze_file_content(file_metrics, file_path, file.source_code, commit)

                # Aggregate class and method metrics into file metrics
                for class_metrics in file_metrics.classes.values():
                    file_metrics.change_set.aggregate(class_metrics.change_set)
                    file_metrics.code_churn.aggregate(class_metrics.code_churn)
                    file_metrics.bug_fixing_comment.aggregate(class_metrics.bug_fixing_comment)
                    # Further aggregate any method-level metrics inside the class
                    for method_metrics in class_metrics.methods.values():
                        file_metrics.change_set.aggregate(method_metrics.change_set)
                        file_metrics.code_churn.aggregate(method_metrics.code_churn)
                        file_metrics.bug_fixing_comment.aggregate(method_metrics.bug_fixing_comment)

    return repo_data
