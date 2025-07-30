# IBM Git Log Stat [![PyPI Downloads](https://static.pepy.tech/badge/ibm-git-log-stat)](https://pepy.tech/projects/ibm-git-log-stat)

A lightweight CLI tool to track your **git commits** and **GitHub pull requests** within a date range, across multiple
repositories.

## 🔧 Installation

```bash
pip install ibm-git-log-stat
```

## Usage

```bash
export GITHUB_TOKEN="provide_your_github_token_here"
export JIRA_TOKEN="provide_jira_token_if_you_want_to_check_jira"
ibm-git-log-stat \
  --base-dir ~/projects \
  --author "you@example.com" or "*" \
  --github-user "yourgithubusername" or "*" \
  --start-date 2025-04-01 \
  --end-date 2025-04-30 \
  --output-format xls,txt,pdf,docx,ppt,all \
  --check-pr (remove the argument if u want to disable PR)
  --use-nlp (remove the argument if u want to disable NLP)
  --check-jira (remove the argument if u do not want to check JIRA)
  --github-url (override default github url which is specific to IBM employees)
  --jira_url (override default jira url which is specific to IBM employees)

Remember using NLP for the first time can be very slow depending on the
internet speed. It downloads the model for summarization and can take time.
In case it is slow, it is advisable to disable NLP.

If you are not sure of the author and github username specify '*'
Please note JIRA cannot be checked when author is *. Author needs to be a valid email
address if JIRA issues are to be fetched. 

Arguments can also be set using environment variables:

BASE_DIR
AUTHOR
GITHUB_USER
START_DATE
END_DATE
OUTPUT_FORMAT
CHECK_JIRA
USE_NLP
GITHUB_URL
JIRA_URL

Just export before running if you dont want to specify everytime in parameter
```

## Output Formats

If you want to generate all supported formats then specify in param `--output-format all`

### DOCX, PDF, PPT
Contains a summary of work done with commits grouped by author per page.

Note: Summary is created using NLP and LLM Models. 
For the first time this operation will be slow as the model has to be downloaded locally. 
Depending on internet speed, the maximum time is spent in downloading model.
Either have a good connection to download faster or disable NLP and summary feature.

### TXT, XLS, CSV, TSV
Contains the git commit output in tabular form.

Date | Author  | Commit Hash | Message
---  |---------|-------------| ---
2025-04-29 | Faizan Fordkar | wehfbdhd | Implemented FIXMEs.

Made with ❤️ from India

## Change Log

### v0.1.1
First Release
Get git commits and PRs in console as a CLI tool

### v1.0.2
Public Beta Release
Export Functionality in DOCX, PPTX, XLSX, PDF, TXT, CSV, TSV
NLP Summarization

### v2.0.0
JIRA reports. 
Issues touched by user (email used in git commit search). 
Custom Github and JIRA URLs

### v2.0.1
JIRA reports bug fix where report was generated in all format irrespective
of output format specified.

### v2.0.2
JIRA token bug fix where it was allowing no token with check jira flag.

## Roadmap

### v3.0.0
Customise Reports
Web Portal