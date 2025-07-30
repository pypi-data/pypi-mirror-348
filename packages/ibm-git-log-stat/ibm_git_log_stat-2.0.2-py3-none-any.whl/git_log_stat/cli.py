import argparse
import os
from datetime import datetime

from git_log_stat.git_log_stat_service import GitLogStatService
from git_log_stat.git_repo.git_output_service import GitOutputService
from git_log_stat.git_repo.git_repo_service import GitRepoService
from git_log_stat.jira_exporter import jira_exporter


def parse_args():
    """
    Parses arguments
    --base-dir base directory where to search git repo
    --author email of the user for git log search
    --github-user username of author for PR search
    --start-date start date in YYYY-MM-DD format
    --end-date end date in YYYY-MM-DD format
    """
    parser = argparse.ArgumentParser(description="Track git commits and GitHub PRs for a given user and date range.")

    parser.add_argument(
        "--check-pr", default=os.getenv("CHECK_PR", ""), action="store_true",
        help="Include PR info in output"
    )
    parser.add_argument(
        "--github-url", default=os.getenv("GITHUB_URL", "https://api.github.ibm.com"),
        help="Override default github url if you are not an IBMer"
    )
    parser.add_argument(
        "--jira-url", default=os.getenv("JIRA_URL", "https://jsw.ibm.com"),
        help="Override default github url if you are not an IBMer"
    )
    parser.add_argument(
        "--check-jira", default=os.getenv("CHECK_JIRA", ""), action="store_true",
        help="Include JIRA info in output"
    )
    parser.add_argument(
        "--output-format", default=os.getenv("OUTPUT_FORMAT", "txt"),
        help="Output Format: txt, xls, pdf, ppt, csv, tsv, docx"
    )
    parser.add_argument(
        "--base-dir", default=os.getenv("BASE_DIR", os.path.expanduser("~/projects")),
        help="Base directory to search for git repositories"
    )
    parser.add_argument(
        "--author", default=os.getenv("AUTHOR", ""),
        help="Git commit author email (used in git log)"
    )
    parser.add_argument(
        "--github-user", default=os.getenv("GITHUB_USER", ""),
        help="GitHub username (used to filter PRs)"
    )
    parser.add_argument(
        "--start-date", default=os.getenv("START_DATE", "2025-04-01"),
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", default=os.getenv("END_DATE", "2025-04-30"),
        help="End date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--use-nlp", default=os.getenv("USE_NLP", ""), action="store_true",
        help="Set to true to use nlp. remove the arg to not use"
    )


    return parser.parse_args()


def main():
    # Settings
    args = parse_args()
    use_nlp = args.use_nlp
    check_pr = args.check_pr
    check_jira = args.check_jira
    git_url = args.github_url
    jira_url = args.jira_url
    base_dir = os.path.expanduser(args.base_dir)
    assert base_dir
    author = args.author
    if author is None or len(author) == 0:
        author = "*"
    github_user = args.github_user
    if github_user is None or len(github_user) == 0:
        github_user = "*"
    since = args.start_date
    if since is None:
        since = "1970-01-01"
    until = args.end_date
    if until is None:
        until = datetime.now().strftime("YYYY-MM-DD")
    github_token = os.getenv("GITHUB_TOKEN", "")
    if github_token is None:
        raise Exception("Github token needs to provided.")

    jira_token = os.getenv("JIRA_TOKEN", "")
    if author == "*" and check_jira:
        raise Exception("Author cannot be all when checking JIRA. Author needs to be a valid email address.")
    if check_jira:
        if jira_token is None:
            raise Exception("Jira token needs to provided.")

    HEADERS = {"Authorization": f"token {github_token}"}

    # GitHub API base
    github_api = git_url

    git_log_stat_service = GitLogStatService()
    git_repo_service = GitRepoService()
    git_output_service = GitOutputService()
    print(f"\n🔍 Git commits by {author if author is not None else "All"} from {since} to {until}\n")
    output, pr_output = git_log_stat_service.get_commits(base_dir, author, since, until, check_pr, github_api, HEADERS)
    print(output)
    print(pr_output)

    if args.output_format:
        output_format = args.output_format
        include_summary = True if use_nlp else False
        output_file_name = (f"./{author if not author == "*" else "all"}-"
                                f"{github_user if not github_user == "*" else "all"}-{datetime.now().strftime("%y-%m-%d")}-git-commits.{output_format}")
        git_output_service.generate_output_file(output_format, output_file_name, commit_output=output, author=author,
                                                pr_output=pr_output, start_date=since, end_date=until, include_summary=include_summary)
    try:
        if pr_output is None or len(pr_output) <= 0:
            print("Total Commits and PRs: " + str(git_output_service.get_commit_count(output)))
        else:
            commit_cout, pr_count = git_output_service.get_commit_count(output, pr_output=pr_output)
            print(f"Total Commits: {str(commit_cout)} Total PRs: {str(pr_count)} ")

        if check_jira and args.output_format:
            output_format = args.output_format
            jira_file_name = (f"./{author if not author == "*" else "all"}-"
                                f"{github_user if not github_user == "*" else "all"}-{datetime.now().strftime("%y-%m-%d")}-jira-issues.{output_format}")
            jira_count = jira_exporter.main(jira_url, jira_token, author, jira_file_name, start_date=since, end_date=until, output_format=output_format)
            print(f"Total JIRA Issues worked on: {str(jira_count)}")

    except Exception as e:
        print(f"Error encountered during count operation {str(e)}")


if __name__ == "__main__":
    main()
