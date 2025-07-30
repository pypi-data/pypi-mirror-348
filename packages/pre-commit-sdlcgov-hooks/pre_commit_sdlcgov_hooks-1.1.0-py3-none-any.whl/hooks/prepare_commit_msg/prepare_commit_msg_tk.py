"""
Toolkit of programs/hooks for the ``prepare-commit-msg`` stage.
"""

from typing import Optional, List
import sys
import argparse

from hooks._lib.git import (
    get_active_branch,
    read_commit_msg,
    write_commit_msg,
    get_commit_message_subject,
)
from hooks._lib.gitlab import (
    GLIssueRef,
    get_gl_issue_ref_from_branch_name,
    extract_gl_issue_refs_from_commit_msg,
    gl_issue_ref_to_str,
    gl_issue_ref_to_readable_str,
)


def ellipsize_subject() -> None:
    """
    Trims the length of the subject to a maximum of 70 chars.

    If the subject of the commit message is longer than 70 chars, an ellipsized copy of the first
    message line is prepended to the commit message.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int, default=70)
    parser.add_argument('commit_msg_filename')
    args = parser.parse_args()
    max_length: int = min(max(args.length, 4), 70)
    commit_msg_filename: str = args.commit_msg_filename
    commit_msg: str = read_commit_msg(commit_msg_filename)
    subject: str = get_commit_message_subject(commit_msg)

    if len(subject) <= max_length:
        return

    print(f'Subject exceedes {max_length} characters. Ellipsizing...')
    last_space: int = subject.rfind(' ', 0, max_length - 3)
    if last_space < 0:
        subject = f'{subject[:max_length - 3]}...'
    else:
        subject = f'{subject[:last_space]}...'
    commit_msg = f'{subject}\n\n{commit_msg}'
    print(f'Subject ellipsized to "{subject}"')

    write_commit_msg(commit_msg_filename, commit_msg)

def add_gl_issue_ref() -> None:
    """
    Adds a GitLab issue reference to the commit message if none is set and the current branch is an
    issue branch.

    Issue branches are expected to have the format ``<ISSUE_NUM>-issue[-at-<PROJECT_NAME>]``, where
    ``<ISSUE_NUM>`` is an integer with the issue number, and ``<PROJECT_NAME>`` an optional
    reference to another project (e.g. ``an_owner/a_repo``).

    Examples of valid issue branches are:

    - ``123-issue``
    - ``456-issue-at-an_owner/a_repo``

    If the active branch is an issue branch and no GitLab issue references are found in the commit
    message, one will be added at the end of the commit message to the currently active issue
    branch.

    If any GitLab issue reference is found, but none to the active issue branch, a warning will be
    printed but the message will still be left intact, in case it is a false positive.

    Otherwise, the commit message remains unchanged.
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
        commit_msg = commit_msg.rstrip(' \n\t')
        commit_msg += f'\n\nIssue {gl_issue_ref_to_str(branch_issue_ref)}\n'
        print(
            f'Added reference to issue {gl_issue_ref_to_readable_str(branch_issue_ref)}'
        )
        write_commit_msg(commit_msg_filename, commit_msg)
    elif branch_issue_ref not in commit_msg_issue_refs:
        print(
            'Other issue references were found, but none to '
            f'{gl_issue_ref_to_readable_str(branch_issue_ref)}.'
        )
        print(
            '\nNo issue reference added, though it may be a symptom that either the branch or the '
            'commit message references are wrong. Please, review.'
        )
