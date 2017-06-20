from pigit import RepositoryFactory


repo = RepositoryFactory.get_file_system_repository_from_directories('.', '/tmp/test')

# list all branches
print("Printing all branches")
for branch in repo.get_branches(include_remote=True):
    print(branch.name)


HEAD_reference = repo.get_head()
print("HEAD : {commit}".format(commit=HEAD_reference.commit))

for commit in repo.get_logs():
    print(commit)

repo.checkout(branch='master')
