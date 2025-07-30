from collections import defaultdict

from transformers import pipeline

from git_log_stat.app_logs.logger_service import IBMLogger

log = IBMLogger("GitNlpService").get_logger()


def parse_commits(commit_lines):
    parsed = []
    for line in commit_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) == 4:
            parsed.append({'date': parts[0], 'author': parts[1], 'hash': parts[2], 'message': parts[3]})
    return parsed


def init_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_by_author(parsed_commits):
    summarizer = init_summarizer()
    author_msgs = defaultdict(list)
    for commit in parsed_commits:
        author_msgs[commit['author']].append(commit['message'])

    author_summaries = {}
    for author, messages in author_msgs.items():
        joined = " ".join(messages)
        if len(joined.split()) > 30:  # BART's min_length requirement
            summary = summarizer(joined, max_length=80, min_length=30, do_sample=False)[0]['summary_text']
        else:
            summary = "Too few commits for summarization. Messages: " + "; ".join(messages)
        author_summaries[author] = summary
    return author_summaries


def generate_natural_summary(commit_lines):
    summarizer = init_summarizer()
    # Combine all commit messages with authors
    combined_messages = []
    for line in commit_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            date, author, *message_parts = parts
            message = " | ".join(message_parts)
            combined_messages.append(f"{author} - {message}")

    # Prepare input for the model
    text = ". ".join(combined_messages)

    # Optional: Truncate if too long
    if len(text.split()) > 1024:
        text = " ".join(text.split()[:1024])

    # Generate summary
    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]['summary_text']
