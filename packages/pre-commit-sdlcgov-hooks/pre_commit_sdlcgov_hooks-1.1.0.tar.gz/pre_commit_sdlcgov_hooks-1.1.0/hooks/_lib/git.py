"""
Utility functions for git-related operations.
"""

from typing import Optional
from pathlib import Path

import git


def get_current_git_repo() -> Optional[git.Repo]:
    """
    Gets the git repo at the current working directory.

    :return: The git repo if currently in a cloned git repo; ``None`` otherwise.
    :rtype: Optional[git.Repo]
    """
    try:
        return git.Repo('.')
    except git.exc.InvalidGitRepositoryError:
        print('Looks like the current directory is not in a git repo')
        return None

def get_active_branch() -> Optional[str]:
    """
    Gets the currently active branch in the current git repo.

    :return: The active branch name if in a repo with a non-detached HEAD; ``None`` otherwise.
    :rtype: Optional[str]
    """
    this_repo: Optional[git.Repo] = get_current_git_repo()
    if not this_repo:
        return None
    try:
        return this_repo.active_branch.name
    except TypeError:
        print('Current repo is in a detached state')
        return None

def read_commit_msg(commit_msg_filename: str) -> str:
    """
    Reads the commit message file to a string.

    :param commit_msg_filename: The commit message file name.
    :type commit_msg_filename: str
    :return: The commit message as a string.
    :rtype: str
    """
    with open(commit_msg_filename, "rt", encoding='utf-8') as commit_msg_file:
        return commit_msg_file.read()

def write_commit_msg(commit_msg_filename: str, commit_msg: str) -> None:
    """
    Writes a string into a commit message file.

    :param commit_msg_filename: The commit message filename.
    :type commit_msg_filename: str
    :param commit_msg: The commit message to write.
    :type commit_msg: str
    """
    with open(commit_msg_filename, "wt", encoding='utf-8') as commit_msg_file:
        commit_msg_file.write(commit_msg)

def get_commit_message_subject(commit_msg: str) -> str:
    """
    Extracts the subject from the commit message.

    :param commit_msg: The commit message.
    :type commit_msg: str
    :return: The commit message subject.
    :rtype: str
    """
    return commit_msg.partition('\n')[0]

def is_merging() -> bool:
    """
    Checks if the current git repo is in a merging state.

    :return: ``True`` if the current repo is in a merging state; ``False`` otherwise.
    :rtype: bool
    """
    this_repo: Optional[git.Repo] = get_current_git_repo()
    if not this_repo:
        return False
    try:
        this_repo.git.rev_parse('--verify', 'MERGE_HEAD')
    except git.exc.GitCommandError:
        return False
    return True

def get_merging_branches() -> Optional[tuple[str, ...]]:
    """
    Gets the branches involved in a merge.

    The first element of the tuple is the current branch, and the remaining elements are the
    branches being merged into it.

    :return: A tuple of the current branch and the other branches being merged into it. Will return
        ``None`` if the current repo is not in a merging state.
    :rtype: Optional[tuple[str, ...]]
    """
    this_repo: Optional[git.Repo] = get_current_git_repo()
    if not this_repo:
        return None
    if not is_merging():
        return None

    with open(Path(this_repo.git_dir) / Path('MERGE_HEAD'), encoding='ascii') as f:
        shas: list[str] = [line.strip() for line in f if line.strip()]
    merging_branches: list[str] = []
    for sha in shas:
        # 1) local heads
        for head in this_repo.heads:
            if head.commit.hexsha == sha:
                merging_branches.append(head.name)
        # 2) remote heads
        for remote in this_repo.remotes:
            for ref in remote.refs:
                if ref.commit.hexsha == sha:
                    merging_branches.append(f"{remote.name}/{ref.remote_head}")
        # 3) fallback to git name-rev
        if not any(
            sha == ref.commit.hexsha
            for ref
            in this_repo.heads + sum((r.refs for r in this_repo.remotes), [])
        ):
            try:
                name = this_repo.git.name_rev("--name-only", sha).strip()
                merging_branches.append(name)
            except git.GitCommandError:
                merging_branches.append(sha[:7])
    return (this_repo.active_branch.name, *merging_branches)


__all__ = [
    'get_current_git_repo',
    'get_active_branch',
    'read_commit_msg',
    'write_commit_msg',
    'get_commit_message_subject',
    'is_merging',
    'get_merging_branches',
]
