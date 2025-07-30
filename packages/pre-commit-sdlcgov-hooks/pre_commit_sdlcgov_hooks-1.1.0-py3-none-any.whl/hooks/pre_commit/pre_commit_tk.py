"""
Toolkit of programs/hooks for the ``pre-commit`` stage.
"""

from typing import Optional
import sys
import argparse
import re

import git

from hooks._lib.git import (
    get_current_git_repo,
    get_active_branch,
    is_merging,
    get_merging_branches,
)
from hooks._lib.gitlab import (
    GLIssueRef,
    get_gl_issue_ref_from_branch_name,
)


def safety_guard() -> None:
    """
    Prevents a commit to materialized if the staged changes contain a given safety guard phrase.

    This phrase is set by default to ``DO NOT COMMIT``, but can be changed by passing it as the
    first argument to this hook.

    It is case-sensitive and does not accept wildcards or regular expressions.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-g', '--guard-phrase', default='DO NOT COMMIT')
    args = parser.parse_args()
    guard_phrase: str = args.guard_phrase
    failed_job: bool = False
    this_repo: git.Repo = get_current_git_repo()
    staged_blobs = this_repo.index.diff(this_repo.head.commit, create_patch=True)
    for staged_blob in staged_blobs:
        if staged_blob.a_blob:
            try:
                new_blob: str = staged_blob.a_blob.data_stream.read().decode('utf-8')
                if guard_phrase in new_blob:
                    print(
                        f'File {staged_blob.a_path} contains guard phrase '
                        f'"{guard_phrase}":\n{new_blob}'
                    )
                    failed_job = True
            except UnicodeDecodeError:
                # Ignore binary files
                pass

    if failed_job:
        print('Some changes in the stage are marked as protected from committing')
        sys.exit(1)

def enforce_committing_to_issue() -> None:
    """
    Enforce changes are only committed to issue branches.
    """
    active_branch_name: Optional[str] = get_active_branch()
    if not active_branch_name:
        print('An active branch could not be determined from the current directory')
        sys.exit(1)

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--allow-branches', nargs='*', default=[])
    args = parser.parse_args()
    allow_branches: list[str] = args.allow_branches
    for branch in allow_branches:
        if re.match(branch, active_branch_name, re.IGNORECASE):
            print(f'Branch "{active_branch_name}" is allowed to be committed to. Skipping...')
            sys.exit(0)

    # TODO: Support other formats like GL-xxx
    branch_issue_ref: Optional[GLIssueRef] = get_gl_issue_ref_from_branch_name(active_branch_name)
    if not branch_issue_ref:
        print(
            f'Branch "{active_branch_name}" does not seem to be an issue branch. '
            'Changes must be committed to issue branches only.'
        )
        sys.exit(1)

def enforce_merge_directions() -> None:
    """
    Enforce the direction of merges.
    """
    this_repo: Optional[git.Repo] = get_current_git_repo()
    if not this_repo:
        print('Not in a git repository')
        sys.exit(1)

    if not is_merging():
        print('Not in a merging state')
        sys.exit(0)

    merging_branches: Optional[tuple[str, ...]] = get_merging_branches()
    if not merging_branches:
        print('No branches are being merged')
        sys.exit(0)

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('rules', nargs='*', default=[])
    args = parser.parse_args()
    rules: list[str] = args.rules
    for rule in rules:
        if not re.match(r'.+::.+', rule):
            print(f'Rule "{rule}" is not valid. Must be in the form "from_branch::into_branch"')
            sys.exit(1)

    for rule in rules:
        from_branch, into_branch = rule.split('::')
        if re.match(into_branch, merging_branches[0], re.IGNORECASE) and all(
            re.match(from_branch, branch, re.IGNORECASE)
            for branch
            in merging_branches[1:]
        ):
            sys.exit(0)
    print(
        f'No rules matched merging branches {merging_branches[1:]} '
        f'into branch {merging_branches[0]}.'
    )
    sys.exit(1)
