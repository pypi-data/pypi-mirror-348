import os
import subprocess

from git_log_stat.app_logs.logger_service import IBMLogger
from git_log_stat.git_repo.git_log_format_service import GitLogFormatService
from git_log_stat.git_repo.git_repo_service import GitRepoService


class GitLogStatService:

    def __init__(self):
        self.log = IBMLogger("GitLogStatService").log
        self.repo_service = GitRepoService()
        self.git_log_format_service = GitLogFormatService()
        self.git_repo_service = GitRepoService()

    def get_commits(self, base_dir, author, start_date, end_date, check_pr, api_url, headers):
        try:
            self.log.debug("Getting Git commits in base dir: %s", base_dir)

            if not os.path.isdir(base_dir):
                raise ValueError(f"Invalid base directory: {base_dir}")

            all_outputs = []
            all_pr_outputs = []

            for root, dirs, files in os.walk(base_dir):
                if ".git" in dirs:
                    repo_name = os.path.basename(root)
                    self.log.info(f"📁 Repository: {repo_name}")

                    log_cmd = [
                        "git", "log",
                        f"--since={start_date}",
                        f"--until={end_date}",
                        f"--pretty={self.git_log_format_service.get_log_format_detailed()}",
                        "--date=short"
                    ]

                    if author != "*":
                        log_cmd.insert(3, f"--author={author}")

                    try:
                        output = subprocess.check_output(log_cmd, cwd=root).decode("utf-8").strip()
                        if output:
                            all_outputs.append(f"===== {repo_name} =====\n{output}\n")
                        else:
                            self.log.info(f"No commits found in {repo_name}")
                    except subprocess.CalledProcessError as e:
                        self.log.error(f"❌ Failed to get commits for {repo_name}: {e}")
                    except Exception as e:
                        self.log.error(f"Unexpected error in repo {repo_name}: {e}")

                    if check_pr:
                        repo_name = self.git_repo_service.get_github_repo_url(root)
                        pr_outputs = self.git_repo_service.get_pull_requests(api_url, repo_name, author,
                                                                                  headers, start_date, end_date)
                        all_pr_outputs.extend(pr_outputs)


            return "\n".join(all_outputs) if all_outputs else "No commits found.", all_pr_outputs

        except Exception as e:
            self.log.error(f"Exception in get_commits: {e}", exc_info=True)
            return None

    def get_pull_requests(self, api_url, repo_full_name, author, headers, start_date, end_date):
        return self.repo_service.get_pull_requests(api_url, repo_full_name, author, headers, start_date, end_date)
