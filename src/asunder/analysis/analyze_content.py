import ast

from asunder.metrics.structure_metrics import FileMetrics, ClassMetrics, MethodMetrics


def analyze_file_content(file_metrics: FileMetrics, file_path: str, content: str, commit):
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_data = file_metrics.classes.setdefault(class_name, ClassMetrics())

                # Update class metrics
                class_data.commits.append(commit.hash)
                class_data.authors.add(commit.author.name)
                class_data.change_set.update(commit)
                class_data.code_churn.update(sum(1 for _ in ast.walk(node)))

                for sub_node in node.body:
                    if isinstance(sub_node, ast.FunctionDef):
                        method_name = sub_node.name
                        method_data = class_data.methods.setdefault(method_name, MethodMetrics())

                        # Update method metrics
                        method_data.commits.append(commit.hash)
                        method_data.authors.add(commit.author.name)
                        method_data.complexity = ast.dump(sub_node).count("ast.")
                        method_data.length = len(sub_node.body)
                        method_data.change_set.update(commit)
                        method_data.code_churn.update(len(sub_node.body))
                        method_data.bug_fixing_comment.update(commit.msg)

            elif isinstance(node, ast.FunctionDef):
                method_name = node.name
                method_data = file_metrics.classes.setdefault("<file_level>", ClassMetrics()).methods.setdefault(
                    method_name, MethodMetrics()
                )

                # Update method-level metrics for top-level functions (not inside classes)
                method_data.commits.append(commit.hash)
                method_data.authors.add(commit.author.name)
                method_data.complexity = ast.dump(node).count("ast.")
                method_data.length = len(node.body)
                method_data.change_set.update(commit)
                method_data.code_churn.update(len(node.body))
                method_data.bug_fixing_comment.update(commit.msg)

    except SyntaxError:
        print(f"Syntax error in file: {file_path}")
    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")
