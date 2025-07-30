"""
Utility functions for GitLab-related operations.
"""

from typing import Optional, Tuple, Dict, List
import re


GLIssueRef = Tuple[int, Optional[str]]

def get_gl_issue_ref_from_branch_name(branch_name: str) -> Optional[GLIssueRef]:
    """
    Gets a GitLab issue reference from an appropriately formatted git branch name.

    :param branch_name: The git branch name.
    :type branch_name: str
    :return: A GitLab issue reference tuple, or ``None`` if the branch is not correctly formatted
    as a GitLab issue branch.
    :rtype: Optional[GLIssueRef]
    """
    issue_branch_regex: str = r'^(?P<ISSUE_REF>\d+)-issue(?:-at-(?P<PRJ_REF>[-_./a-zA-Z0-9]+))?$'
    branch_name_match: Optional[re.Match] = re.match(
        issue_branch_regex,
        branch_name,
        re.IGNORECASE,
    )
    if not branch_name_match:
        return None
    groups: Dict[str, str] = branch_name_match.groupdict()
    return (
        int(groups['ISSUE_REF']),
        groups.get('PRJ_REF', None),
    )

def extract_gl_issue_refs_from_commit_msg(commit_msg: str) -> List[GLIssueRef]:
    """
    Extracts the GitLab issue references from a given commit message.

    :param commit_msg: The commit message.
    :type commit_msg: str
    :return: A list with every GitLab issue reference found.
    :rtype: List[GLIssueRef]
    """
    issue_ref_regex: str = r'(?P<PRJ_REF>\b[-_./a-zA-Z0-9]+|\b)?#(?P<ISSUE_REF>\d+)\b'
    matches: List[Tuple[str, str]] = re.findall(
        issue_ref_regex,
        commit_msg,
        re.IGNORECASE | re.MULTILINE,
    )
    if not matches:
        return []
    issue_refs: List[GLIssueRef] = []
    for prj_ref, issue_ref in matches:
        issue_refs.append(
            (
                int(issue_ref),
                prj_ref if prj_ref else None,
            )
        )
    return issue_refs

def gl_issue_ref_to_str(issue_ref: GLIssueRef) -> str:
    """
    String representation of a GitLab issue reference.

    :param issue_ref: The GitLab issue reference.
    :type issue_ref: GLIssueRef
    :return: The string representation of the GitLab issue reference.
    :rtype: str
    """
    return f'{issue_ref[1] if issue_ref[1] else ""}#{issue_ref[0]}'

def gl_issue_ref_to_readable_str(issue_ref: GLIssueRef) -> str:
    """
    Readable string for a GitLab issue reference.

    :param issue_ref: The GitLab issue reference.
    :type issue_ref: GLIssueRef
    :return: The readable string for the GitLab issue reference.
    :rtype: str
    """
    return f'#{issue_ref[0]}' + (f' at {issue_ref[1]}' if issue_ref[1] else '')


__all__ = [
    'GLIssueRef',
    'get_gl_issue_ref_from_branch_name',
    'extract_gl_issue_refs_from_commit_msg',
    'gl_issue_ref_to_str',
    'gl_issue_ref_to_readable_str',
]
