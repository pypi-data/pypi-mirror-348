
import ast
import requests
from urllib.parse import urlparse

class GitHubAPIAnalyzer:
    def __init__(self, github_user, repo_name, token=None, branch='main'):   
        self.github_user = github_user
        self.total_files = 0
        self.repo_name = repo_name
        self.base_api = f"https://api.github.com/repos/{github_user}/{repo_name}/contents"
        self.branch = branch
        self.github_token = token
        self.results = []
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        } if token else {}
        
    def fetch_repo_files(self, path=""):
        """Fetch all files recursively and build the directory structure."""
        url = f"{self.base_api}/{path}?ref={self.branch}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return {}

        files = response.json()
        file_structure = {}

        for file in files:
            if file['type'] == 'file' and file['name'].endswith('.py'):
                file_structure[file['path']] = {
                    'type': 'file',
                    'url': file['download_url'],
                    'html_url': file['html_url']
                }
                self.total_files += 1 
            elif file['type'] == 'dir':
                file_structure[file['path']] = {
                    'type': 'dir',
                    'children': self.fetch_repo_files(file['path'])  # Recurse
                }

        return file_structure

    def traverse_and_analyze(self, node, path_prefix=""):
        """Recursively traverse the file tree and analyze .py files."""
        results = []
        for name, info in node.items():
            if info['type'] == 'file':
                response = requests.get(info['url'], headers=self.headers)
                if response.status_code == 200:
                    content = response.text
                    analysis = self.analyze_code(content, name)
                    if analysis:
                        commit_info = self.get_file_commit_details(info['html_url'])
                        results.append({
                            'repo': f"{self.github_user}/{self.repo_name}",
                            'repo_url': f"https://github.com/{self.github_user}/{self.repo_name}",
                            'file_url': analysis['file_url'],
                            'imports': analysis['imports'],
                            'classes': analysis['classes'],
                            'last_modified_time': commit_info.get('last_modified_time'),
                            'commit_message': commit_info.get('commit_message'),
                            'committer_name': commit_info.get('committer_name')
                        })
            elif info['type'] == 'dir':
                results.extend(self.traverse_and_analyze(info['children'], path_prefix=name + '/'))
        return results

    def analyze_code(self, file_content, file_url):
        """Analyze Python code for imports and classes."""
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            print(f"Syntax error in file {file_url}: {e}")
            return {}

        imports = []
        classes = {}

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                methods = []
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        methods.append(n.name)
                classes[class_name] = methods

        return {
            "file_url": file_url,
            "imports": imports,
            "classes": classes
        }

    def get_file_commit_details(self, github_file_url: str):
        """
        Fetch file's last modified time, commit message, and committer name from GitHub file URL.
        """
        parsed = urlparse(github_file_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) < 5 or path_parts[2] != 'blob':
            raise ValueError("Invalid GitHub file URL. Expected format: https://github.com/{owner}/{repo}/blob/{branch}/{file_path}")

        owner, repo, _, branch_from_url, *file_path_parts = path_parts
        repo_full_name = f"{owner}/{repo}"
        file_path = '/'.join(file_path_parts)

        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        params = {"path": file_path, "sha": branch_from_url, "per_page": 1}
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                commit = data[0]['commit']
                author = commit['author']
                return {
                    "last_modified_time": commit['committer']['date'],
                    "commit_message": commit['message'],
                    "committer_name": author['name']
                }
            else:
                return {
                    "last_modified_time": None,
                    "commit_message": None,
                    "committer_name": None
                }
        else:
            print(f"Failed to fetch commit info for {file_path}: {response.status_code}")
            return {
                "last_modified_time": None,
                "commit_message": None,
                "committer_name": None
            }

    def analyze_repo(self):
        """Analyze the entire repository."""
        file_structure = self.fetch_repo_files()
        return self.traverse_and_analyze(file_structure)
