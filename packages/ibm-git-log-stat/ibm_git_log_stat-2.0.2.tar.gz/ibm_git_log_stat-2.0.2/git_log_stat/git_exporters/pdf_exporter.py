from collections import defaultdict
from logging import Logger
from textwrap import wrap
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from git_log_stat.git_exporters.base_exporter import BaseExporter


def generate_commit_summary_pdf(
        log: Logger,
        commit_logs: str,
        pr_logs: Optional[str] = None,
        output_pdf_path="git-activity-report.pdf",
        skip_summary=False
):
    """
    Generates PDF file with commits and summary if requested.
    :param log: logger to use for logging during pdf creation
    :param commit_logs: commit logs to be written and processed through NLP
    :param pr_logs: pull request logs to be written to pdf
    :param output_pdf_path: output pdf file path
    :param skip_summary: boolean flag to exclude summary. Default is False.
    :return: Path where pdf file is generated
    """
    grouped_commits = defaultdict(list)
    combined_messages = []

    for line in commit_logs.strip().split("\n"):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            date, author, commit_id, *message_parts = parts
            message = " | ".join(message_parts)
            grouped_commits[author].append((date, message))
            combined_messages.append(f"{author} - {message}")

    summary = None
    if not skip_summary:
        try:
            from git_log_stat.git_repo.git_nlp import init_summarizer
            summarizer = init_summarizer()
        except ImportError:
            summarizer = None

        full_text = ". ".join(combined_messages)
        if len(full_text.split()) > 1024:
            full_text = " ".join(full_text.split()[:1024])
        summary = summarizer(full_text, max_length=120, min_length=40, do_sample=False)[0]['summary_text']

    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4
    x_margin = 1 * inch
    right_margin = width - 1 * inch
    y = height - 1 * inch

    max_chars_per_line = 100  # approximate based on page width

    def draw_multiline(text, start_y, font="Helvetica", size=12, max_width_chars=100):
        c.setFont(font, size)
        for line in text.split('\n'):
            wrapped_lines = wrap(line, width=max_width_chars)
            for subline in wrapped_lines:
                if start_y < inch:
                    c.showPage()
                    start_y = height - inch
                    c.setFont(font, size)
                c.drawString(x_margin, start_y, subline)
                start_y -= 14
        return start_y

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, "Commit Summary Report")
    y -= 30

    if summary:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "📝 Natural Language Summary:")
        y -= 20
        y = draw_multiline(summary, y)
        y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, "📜 Commits by Author:")
    y -= 20

    for author, commits in grouped_commits.items():
        c.setFont("Helvetica-Bold", 13)
        y = draw_multiline(f"👤 {author}", y, font="Helvetica-Bold", size=13)

        for date, message in commits:
            is_pr = 'pull request' in message.lower() or 'merge' in message.lower()
            formatted = f"🔀 {date} | {message}" if is_pr else f"{date} | {message}"
            font_style = "Helvetica-Bold" if is_pr else "Helvetica"
            y = draw_multiline(formatted, y, font=font_style, size=11)

        y -= 10  # Gap between authors

    # Separate Page for PR Logs
    if pr_logs:
        c.showPage()
        y = height - 1 * inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "🔗 Pull Requests:")
        y -= 20

        pr_log_list = []
        if not isinstance(pr_logs, list):
            pr_log_list = pr_logs.strip().split("\n")
        else:
            pr_log_list = pr_logs

        for pr_line in pr_log_list:
            if pr_line.strip():
                y = draw_multiline(pr_line.strip(), y, font="Helvetica", size=11)

    c.save()
    log.info(f"✅ PDF saved to {output_pdf_path}")


class PdfExporter(BaseExporter):

    def export(self, output_file_name, commit_output: str | list[str], pr_output: str | list[str] = None,
               skip_summary=False):
        self.log.info("Generating PDF %s", output_file_name)
        generate_commit_summary_pdf(
            self.log,
            commit_logs=commit_output,
            pr_logs=pr_output,
            output_pdf_path=output_file_name,
            skip_summary=skip_summary
        )
