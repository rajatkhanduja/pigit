# This file demonstrates how `pigit` can be used

from pigit import Pigit
# from pathlib import Path

# repo = Pigit.get_file_system_repository_from_directories(Path(".git"), Path('/tmp/test'))
repo = Pigit.repo('.')

# list all branches
print("Printing all branches")
for branch in repo.branches:
    print(branch.name)


HEAD_reference = repo.head
print("HEAD : {commit}".format(commit=HEAD_reference.commit))

commits_in_branch = [commit for commit in repo.log]

# repo.checkout(branch='master')

status = repo.get_status()
print(status)
