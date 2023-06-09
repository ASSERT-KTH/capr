import csv
from pathlib import Path
from subprocess import PIPE, run

test_framework = "defects4j"
shell_scripts_folder = Path(__file__).parent.parent / "frameworks"
output_file="bug_types.csv"
tmp_dir = "/tmp/defects4j"
java_home = "/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home"
d4j_path = "/Users/davidhidvegi/Desktop/defects4j/framework/bin"

def label_bugs(project):
    project = str(project)

    list_of_bugs = [
        ("Chart", [i for i in range(1, 27)]),
        ("Closure", [i for i in range(1, 177) if i != 63 and i != 93]),
        ("Lang", [i for i in range(1, 66) if i != 2]),
        ("Math", [i for i in range(1, 107)]),
        ("Mockito", [i for i in range(1, 39)]),
        ("Time", [i for i in range(1, 28) if i != 21])
    ]

    if project != "all":
        list_of_bugs = [l for l in list_of_bugs if l[0] == project]

    for project, ids in list_of_bugs:
        for bug_id in ids:
            work_dir = f"{tmp_dir}/{project}-{bug_id}"

            print(f"Checking out {project}-{bug_id}")
            bug_type = run_bash("checkout_bug", work_dir, project, bug_id)
            print(f"Extracting bug type of {project}-{bug_id}")
            bug_type = run_bash("get_bug_type", work_dir, project, bug_id)

            with open(f"{output_file}", "a") as f:
                writer = csv.writer(f)
                writer.writerow([project, bug_id, bug_type.stdout])


def run_bash(function, work_dir, project, bug_id, extra_arg=None):
    command = ['bash', f'{shell_scripts_folder}/{test_framework}.sh', function, f"{project}", f"{bug_id}", f"{work_dir}", f"{java_home}", f"{d4j_path}", f"{extra_arg}"]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    assert result.returncode == 0
    result.stdout = result.stdout[:-1]
    return result

if __name__ == "__main__":
    import sys
    arg = None
    if (len(sys.argv) > 1):
        arg = Path(sys.argv[1])
    label_bugs(arg)
