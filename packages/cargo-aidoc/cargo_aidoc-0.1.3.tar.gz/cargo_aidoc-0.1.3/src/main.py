import glob
import os
import shutil
import sys
import click
import toml
import tree_sitter_rust as tsrust
from termcolor import colored
from tree_sitter import Language, Parser
from mirascope import llm
import docgen, model
import subprocess

RUST_LANGUAGE = Language(tsrust.language())
ITEM_TYPES = {
    "fn": "function_item",
    "struct": "struct_item",
    "static": "static_item",
    "enum": "enum_item",
    "union": "union_item",
    "trait": "trait_item",
    "macro": "macro_definition",
}

def has_uncommitted_changes(path: str) -> bool:
    """Checks if the given file path has uncommitted changes in Git."""
    try:
        # Get the directory containing the file to run git command in the correct context
        directory = os.path.dirname(os.path.abspath(path))
        if not directory:
             directory = "." # Handle case where path is just a filename in cwd

        # Use git status --porcelain to check the status of the specific file
        # If the command's output is non-empty, the file has changes (staged or unstaged) or is untracked.
        result = subprocess.run(
            ['git', 'status', '--porcelain', path],
            capture_output=True,
            text=True,
            cwd=directory,
            check=True # Raise CalledProcessError if git command fails (e.g., not a repo)
        )
        # Return True if there is any output (indicating changes or untracked)
        return bool(result.stdout.strip())
    except FileNotFoundError:
        # Git command not found
        print(colored("Error: 'git' command not found. Make sure Git is installed and in your PATH.", "red"))
        return False # Assuming no changes if git is not available
    except subprocess.CalledProcessError:
        # Likely indicates the path is not within a git repository or other git error
        # In this context, we can treat it as "no uncommitted changes within a repo context"
        return False
    except Exception as e:
        # Catch unexpected errors
        print(colored(f"An error occurred checking git status for {path}: {e}", "red"))
        return False

@click.command()
@click.argument("crate_path")
@click.option("quiet", "-q", is_flag=True, help="Disable verbose output")
@click.option("dry_run", "--dry-run", help="Generate documentation without writing to file. The LLM results will be cached, and can be applied later. ", is_flag=True)
@click.option("force", "--force", help="Ignore `git` commit check, directly edit files.", is_flag=True)
@click.option("clean_cache", "-c", help="Clean cache after finished. ", is_flag=True)
def main(crate_path: str, quiet: bool, dry_run: bool, clean_cache: bool, force: bool):
    """
    AI Documentation Generationg for Rust Code Using LLMs.
    """
    if has_uncommitted_changes(crate_path) and not dry_run and not force:
        print(colored("Error: Uncommitted changes detected. Please commit or stash your changes before running this script.", "red"))
        exit(1)
    
    gitignore_path = os.path.join(crate_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r+") as f:
            lines = f.readlines()
            # Check if .cargo-aidoc is already ignored
            if not any(".cargo-aidoc/" in line.strip() for line in lines):
                # Ensure the file ends with a newline before appending
                if lines and not lines[-1].endswith('\n'):
                    f.write('\n')
                f.write(".cargo-aidoc/\n")
                if not quiet:
                    print(colored("Added '.cargo-aidoc' to .gitignore", "yellow"))
    
    config_path = os.path.join(crate_path, "cargo-aidoc.toml")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(toml.dumps({
                "llm" : {
                    "provider": "openai",
                    "model": "o3-mini",
                    "call_params": {},
                },
                "doc": {
                    "source": ["src/**/*.rs"],
                    "item_types": ["fn", "struct", "enum", "union", "trait", "macro", "static"],
                }
            }))
        
    with open(config_path, "r") as f:
        config = toml.load(f)
        model.LLM = llm.call(**config["llm"])
        source = [os.path.join(crate_path, *(i for i in s.split('/'))) for s in config["doc"]["source"]]
        item_types = [ITEM_TYPES[t] for t in config["doc"]["item_types"]]

    files = {}
    for src in source:
        for path in glob.glob(src, recursive=True):
            if not quiet:
                print(colored(f"Working on {path}", attrs=["bold"]))
            comments = docgen.docgen(crate_path, path, item_types)
            for line, comment in comments.items():
                if not quiet:
                    print(colored(f"Comment generated at {path}:{line + 1}", "green"))
                if not quiet:
                    print(comment)
            files[path] = comments

    if not dry_run:
        for path, comments in files.items():
            with open(path, "r") as f:
                lines = f.readlines()
            with open(path, "w") as f:
                for i, line in enumerate(lines):
                    if i in comments:
                        f.write(comments[i])
                    f.write(line)

    if clean_cache:
        print(colored("Cleaning cache...", "yellow"))
        try:
            shutil.rmtree(".cargo-aidoc")
        except Exception as e:
            pass
        print(colored("Cache cleaned.", "green"))

def cargo_main():
    if len(sys.argv) >= 2 and sys.argv[1] == "aidoc":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    main()

if __name__ == "__main__":
    main()