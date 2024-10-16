import os
from pydriller import Repository
from datetime import datetime, timedelta
from collections import defaultdict
import ast


class HierarchicalRiskAnalyzer:
    def __init__(self, repo_path, analysis_period_days=360):
        self.repo_path = repo_path
        self.analysis_period = analysis_period_days
        self.risk_data = defaultdict(
            lambda: {
                "commits": 0,
                "authors": set(),
                "classes": defaultdict(
                    lambda: {
                        "commits": 0,
                        "authors": set(),
                        "methods": defaultdict(
                            lambda: {
                                "commits": 0,
                                "authors": set(),
                                "complexity": 0,
                                "length": 0,
                            }
                        ),
                    }
                ),
            }
        )

    def generate_hierarchical_data(self):
        def calculate_risk_score(commits, authors, complexity=0, length=0):
            return (commits * 0.5) + (len(authors) == 1) * 2 + (complexity * 0.1) + (length * 0.05)

        hierarchical_data = []

        for submodule, submodule_data in self.risk_data.items():
            submodule_risk = calculate_risk_score(submodule_data["commits"], submodule_data["authors"])
            submodule_node = {
                "name": os.path.basename(submodule),
                "full_path": submodule,
                "risk_score": submodule_risk,
                "children": [],
            }

            for file_path, file_data in submodule_data["classes"].items():
                file_risk = calculate_risk_score(file_data["commits"], file_data["authors"])
                file_node = {
                    "name": os.path.basename(file_path),
                    "full_path": file_path,
                    "risk_score": file_risk,
                    "children": [],
                }

                for class_name, class_data in file_data["methods"].items():
                    if isinstance(class_data, dict) and "methods" in class_data:
                        class_risk = calculate_risk_score(class_data["commits"], class_data["authors"])
                        class_node = {
                            "name": class_name,
                            "full_path": f"{file_path}::{class_name}",
                            "risk_score": class_risk,
                            "children": [],
                        }

                        for method_name, method_data in class_data["methods"].items():
                            method_risk = calculate_risk_score(
                                method_data["commits"],
                                method_data["authors"],
                                method_data["complexity"],
                                method_data["length"],
                            )
                            method_node = {
                                "name": method_name,
                                "full_path": f"{file_path}::{class_name}::{method_name}",
                                "risk_score": method_risk,
                            }
                            class_node["children"].append(method_node)

                        file_node["children"].append(class_node)
                    else:
                        # This is a function at file level, not in a class
                        method_risk = calculate_risk_score(
                            class_data["commits"],
                            class_data["authors"],
                            class_data["complexity"],
                            class_data["length"],
                        )
                        method_node = {
                            "name": class_name,
                            "full_path": f"{file_path}::{class_name}",
                            "risk_score": method_risk,
                        }
                        file_node["children"].append(method_node)

                submodule_node["children"].append(file_node)

            hierarchical_data.append(submodule_node)

        return hierarchical_data

    def analyze_repository(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.analysis_period)

        try:
            repo = Repository(self.repo_path, since=start_date, to=end_date)
        except Exception as e:
            print(f"Error opening repository: {e}")
            return

        for commit in repo.traverse_commits():
            self.process_commit(commit)

    def update_commit_data(self, submodule, file_path, commit):
        # Update submodule level data
        self.risk_data[submodule]["commits"] += 1
        self.risk_data[submodule]["authors"].add(commit.author.name)

        # Update file level data
        file_data = self.risk_data[submodule]["files"][file_path]
        file_data["commits"] += 1
        file_data["authors"].add(commit.author.name)

    def process_commit(self, commit):
        for file in commit.modified_files:
            if file.filename.endswith(".py"):
                file_path = os.path.normpath(os.path.join(self.repo_path, file.filename))
                submodule = os.path.dirname(file_path)

                # Update submodule and file data
                self.update_commit_data(submodule, file_path, commit)

                # Analyze file content if available
                if file.source_code:
                    self.analyze_file_content(submodule, file_path, file.source_code, commit.author.name)

    def analyze_file_content(self, submodule, file_path, content, author):
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.process_class(node, submodule, file_path, author)
                elif isinstance(node, ast.FunctionDef):
                    self.process_function(node, submodule, file_path, author)
        except SyntaxError:
            print(f"Syntax error in file: {file_path}")
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")

    def process_class(self, node, submodule, file_path, author):
        class_name = node.name
        class_data = self.risk_data[submodule]["files"][file_path]["classes"][class_name]
        class_data["commits"] += 1
        class_data["authors"].add(author)

        for sub_node in node.body:
            if isinstance(sub_node, ast.FunctionDef):
                self.process_function(sub_node, submodule, file_path, author, class_name)

    def process_function(self, node, submodule, file_path, author, class_name=None):
        method_name = f"{class_name}::{node.name}" if class_name else node.name
        target_data = (
            self.risk_data[submodule]["files"][file_path]["classes"][class_name]["methods"][method_name]
            if class_name
            else self.risk_data[submodule]["files"][file_path]["methods"][method_name]
        )

        target_data["commits"] += 1
        target_data["authors"].add(author)
        target_data["complexity"] = ast.dump(node).count("ast.")
        target_data["length"] = len(node.body)

    def calculate_risk_score(self, commits, authors, complexity=0, length=0):
        solo_author_bonus = (len(authors) == 1) * 2
        return (commits * 0.5) + solo_author_bonus + (complexity * 0.1) + (length * 0.05)

    def generate_hierarchical_data(self):
        def create_node(name, full_path, risk_score, children=[]):
            return {
                "name": name,
                "full_path": full_path,
                "risk_score": risk_score,
                "children": children,
            }

        hierarchical_data = []

        for submodule, submodule_data in self.risk_data.items():
            submodule_node = create_node(
                os.path.basename(submodule),
                submodule,
                self.calculate_risk_score(submodule_data["commits"], submodule_data["authors"]),
            )

            for file_path, file_data in submodule_data["files"].items():
                file_node = create_node(
                    os.path.basename(file_path),
                    file_path,
                    self.calculate_risk_score(file_data["commits"], file_data["authors"]),
                )

                for class_name, class_data in file_data["classes"].items():
                    class_node = create_node(
                        class_name,
                        f"{file_path}::{class_name}",
                        self.calculate_risk_score(class_data["commits"], class_data["authors"]),
                    )

                    for method_name, method_data in class_data["methods"].items():
                        method_node = create_node(
                            method_name,
                            f"{file_path}::{class_name}::{method_name}",
                            self.calculate_risk_score(
                                method_data["commits"],
                                method_data["authors"],
                                method_data["complexity"],
                                method_data["length"],
                            ),
                        )
                        class_node["children"].append(method_node)

                    file_node["children"].append(class_node)

                submodule_node["children"].append(file_node)

            hierarchical_data.append(submodule_node)

        return hierarchical_data

    def generate_risk_report(self):
        report = {"submodules": [], "files": [], "classes": [], "methods": []}

        for submodule, submodule_data in self.risk_data.items():
            report["submodules"].append(
                (
                    submodule,
                    self.calculate_risk_score(submodule_data["commits"], submodule_data["authors"]),
                )
            )

            for file_path, file_data in submodule_data["files"].items():
                report["files"].append(
                    (
                        file_path,
                        self.calculate_risk_score(file_data["commits"], file_data["authors"]),
                    )
                )

                for class_name, class_data in file_data["classes"].items():
                    report["classes"].append(
                        (
                            f"{file_path}::{class_name}",
                            self.calculate_risk_score(class_data["commits"], class_data["authors"]),
                        )
                    )

                    for method_name, method_data in class_data["methods"].items():
                        report["methods"].append(
                            (
                                f"{file_path}::{class_name}::{method_name}",
                                self.calculate_risk_score(
                                    method_data["commits"],
                                    method_data["authors"],
                                    method_data["complexity"],
                                    method_data["length"],
                                ),
                            )
                        )

        for category in report:
            report[category] = sorted(report[category], key=lambda x: x[1], reverse=True)

        return report
