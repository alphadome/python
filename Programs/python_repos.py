import requests

#Make an API call and store the reponse.

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print("Status code:", r.status_code)

#Store API response in a variable.
response_dict = r.json()
print("Total repositories:", response_dict['total_count'])

#explore information about the repositories.
repo_dicts = response_dict['items']
print("Repositories returned:", len(repo_dicts))

#examine the first repository.
print("\nSelected information about first repository:")
for repo_dict in repo_dicts:
	print('\nName:', repo_dict['name'])
	print('Owner:', repo_dict['owner']['login'])
	print('Stars:', repo_dict['stargazers_count'])
	print('Repository:', repo_dict['html_url'])
	print('Description:', repo_dict['description'])



