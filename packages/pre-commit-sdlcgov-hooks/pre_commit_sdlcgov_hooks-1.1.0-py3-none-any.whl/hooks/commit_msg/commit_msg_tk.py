"""
Toolkit of programs/hooks for the ``commit-msg`` stage.
"""

from typing import Optional, List
import sys
import argparse

from hooks._lib.git import (
    get_active_branch,
    read_commit_msg,
    get_commit_message_subject,
)
from hooks._lib.gitlab import (
    GLIssueRef,
    get_gl_issue_ref_from_branch_name,
    extract_gl_issue_refs_from_commit_msg,
    gl_issue_ref_to_str,
)


def enforce_subject_length() -> None:
    """
    Enforces the subject length to be between 4 and a given length (up to 70).
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int, default=70)
    parser.add_argument('commit_msg_filename')
    args = parser.parse_args()
    max_length: int = min(max(args.length, 4), 70)
    commit_msg_filename: str = args.commit_msg_filename
    commit_msg: str = read_commit_msg(commit_msg_filename)
    subject: str = get_commit_message_subject(commit_msg)

    if 4 <= len(subject) <= max_length:
        return

    print(f'Subject length ({len(subject)}) must be between 4 and {max_length} characters')
    sys.exit(1)

def enforce_gl_issue_ref() -> None:
    """
    Enforces a reference to a GitLab issue is included in the commit message.

    If the currently active branch is deemed an issue branch, a reference to such issue must be
    included.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('commit_msg_filename')
    args = parser.parse_args()
    commit_msg_filename: str = args.commit_msg_filename
    commit_msg: str = read_commit_msg(commit_msg_filename)

    active_branch_name: Optional[str] = get_active_branch()
    if not active_branch_name:
        print('An active branch could not be determined from the current directory')
        sys.exit(1)

    # TODO: Support other formats like GL-xxx
    branch_issue_ref: Optional[GLIssueRef] = get_gl_issue_ref_from_branch_name(active_branch_name)
    if not branch_issue_ref:
        print(f'Branch "{active_branch_name}" does not seem to be an issue branch. Skipping...')
        sys.exit(0)

    commit_msg_issue_refs: List[GLIssueRef] = extract_gl_issue_refs_from_commit_msg(commit_msg)
    if len(commit_msg_issue_refs) == 0:
        print('At least an issue reference must be included in the commit message')
        sys.exit(1)

    if branch_issue_ref not in commit_msg_issue_refs:
        print(
            'When in an issue branch, a reference to its associated issue '
            f'({gl_issue_ref_to_str(branch_issue_ref)}) must be included in the commit message'
        )
        sys.exit(1)
