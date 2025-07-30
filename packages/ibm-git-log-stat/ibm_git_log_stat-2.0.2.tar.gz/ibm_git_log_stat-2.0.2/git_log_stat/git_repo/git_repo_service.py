import subprocess

import requests

from git_log_stat.app_logs.logger_service import IBMLogger


class GitRepoService:

    def __init__(self):
        self.log = IBMLogger("GitRepoService").get_logger()

    def get_github_repo_url(self, cwd_dir):
        """Extract GitHub org/repo name from git config"""
        try:
            self.log.debug("Fetching remote url for base git repo")
            remotes = subprocess.check_output(["git", "remote", "-v"], cwd=cwd_dir).decode()
            self.log.debug("")
            for line in remotes.splitlines():
                if "github.ibm.com" in line:
                    url = line.split()[1]
                    url = (url.replace("git@github.ibm.com:", "")
                           .replace("https://github.ibm.com/", "")
                           .replace(".git", ""))
                    self.log.debug("url decoded: %s", url)
                    return url.strip()
        except Exception as e:
            self.log.error(str(e), exc_info=True)
            return None

    def get_pull_requests(self, api_url, repo_full_name, author, headers, start_date, end_date):
        """
        Fetch PRs by user for a given repo

        :param api_url: base github api url. for ibm it is https://api.github.ibm.com
        :param repo_full_name: repo full name e.g. parent-project/project-name
        :param author: github username to search PRs by.
        :param headers: headers to pass to api
        :param start_date: start_date (inclusive)
        :param end_date: end_date (exclusive)

        """
        self.log.debug("Fetching PRs for repo %s for user: %s for period - %s to %s", repo_full_name, author,
                       start_date, end_date)
        prs = []
        try:
            url = f"{api_url}/repos/{repo_full_name}/pulls?state=all&per_page=100"
            self.log.debug("Full URL: %s", url)
            while url:
                res = requests.get(url, headers=headers)
                if res.status_code != 200:
                    return []
                for pr in res.json():
                    created_at = pr["created_at"][:10]
                    self.log.debug("Current PR Author %s and created at %s", pr["user"]["login"], created_at)
                    if start_date <= created_at <= end_date:
                        if author == "*":
                            prs.append(f"[#{pr['number']}] {pr["user"]["login"]} {pr['title']} ({created_at})")
                        else:
                            if str(pr["user"]["login"]).lower() == str(author).lower():
                                prs.append(f"[#{pr['number']}] {pr["user"]["login"]} {pr['title']} ({created_at})")
                # Pagination
                url = res.links.get('next', {}).get('url')
                self.log.debug("Paginated URL: %s", url)
        except Exception as e:
            self.log.error(str(e), exc_info=True)
        return prs
