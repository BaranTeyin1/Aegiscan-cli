import argparse
import sys
from sast_engine.engine import SASTEngine
from sast_engine.rule_loader import load_rules
import git_utils
import os
import json
import yaml


def help_page():
    print("""
    -h, --help
        Display this help message and exit.

    --git-url <URL>
        Specifies the remote Git repository (HTTPS or SSH) to be cloned and scanned.
        Example: --git-url https://github.com/user/project.git

    --local-file <DIR>
        Specifies the path to a previously cloned local project directory.
        This option is used instead of --git-url.

    --rules <DIR>
        Specifies the path to the directory containing the static analysis rules.
        This directory should contain rule files in YAML or JSON format.

    --output <FILE>
        Specifies the output file path for the analysis results in JSON, YAML, or TEXT format.
        (Default: standard output)

    --severity <LEVEL>
        Filters results to show only vulnerabilities of the specified severity level.
        Accepted values: LOW, MEDIUM, HIGH, CRITICAL
    """)


def print_banner():
    banner = r"""
   +-----------------------------+
   |        Aegiscan             |
   +-----------------------------+
    """
    print(banner)


def load_code_from_local(path):
    code_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    code_files.append((filepath, f.read()))
    return code_files


def output_results(results, output_path=None, output_format=None):
    if output_path:
        if not output_format:
            ext = os.path.splitext(output_path)[1].lower()
            if ext == ".json":
                output_format = "json"
            elif ext in [".yaml", ".yml"]:
                output_format = "yaml"
            else:
                output_format = "text"

        if output_format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        elif output_format == "yaml":
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(results, f)
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                for res in results:
                    f.write(
                        f"[{res['severity']}] {res['filename']}:{res['line']} - {res['message']} (rule: {res['rule_id']})\n")
    else:
        for res in results:
            print(f"[{res['severity']}] {res['filename']}:{res['line']} - {res['message']} (rule: {res['rule_id']})")


def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Aegiscan - Simple SAST CLI Tool", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Display this help message and exit.")
    parser.add_argument("--git-url", type=str, help="Remote Git repository URL to clone and scan")
    parser.add_argument("--local-file", type=str, help="Local directory of previously cloned repo")
    parser.add_argument("--rules", type=str, default=None, help="Directory containing static analysis rules")
    parser.add_argument("--output", type=str, default=None, help="Output file path for results")
    parser.add_argument("--severity", type=str, choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], help="Filter results by severity level")
    parser.add_argument("-ai", type=str, help="Activate AI-assisted rule generation.")

    args = parser.parse_args()

    if args.help or (not args.git_url and not args.local_file):
        help_page()
        sys.exit(0)

    rules = load_rules(args.rules) if args.rules else load_rules()

    engine = SASTEngine(rules)

    code_files = []
    if args.git_url:
        clone_dir = "./temp_repo"
        if os.path.exists(clone_dir):
            import shutil
            shutil.rmtree(clone_dir)

        print(f"Cloning: {args.git_url}")
        git_utils.clone_repo(args.git_url, clone_dir)
        code_files = load_code_from_local(clone_dir)

    elif args.local_file:
        code_files = load_code_from_local(args.local_file)
    else:
        print("Error: --git-url or --local-file parameter is required")
        sys.exit(1)

    all_results = []
    for filepath, code in code_files:
        results = engine.run(code, filepath)

        if args.severity:
            results = [r for r in results if r['severity'] == args.severity]

        all_results.extend(results)

    output_results(all_results, args.output)


if __name__ == "__main__":
    main()
