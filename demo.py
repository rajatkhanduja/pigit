# This file demonstrates how `pigit` can be used

from pigit import Pigit


repo = Pigit.get_file_system_repository_from_directories('.', '/tmp/test')

# list all branches
print("Printing all branches")
for branch in repo.branches:
    print(branch.name)


HEAD_reference = repo.head
print("HEAD : {commit}".format(commit=HEAD_reference.commit))

for commit in repo.log:
    print(commit)

repo.checkout(branch='master')
