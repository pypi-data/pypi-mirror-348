from logging import Logger

import pandas as pd

from git_log_stat.git_exporters.base_exporter import BaseExporter


def generate_xls(log: Logger, output_file: str, commit_output: str | list[str], pr_output: str | list[str] = None,
                 skip_summary: bool = False):
    try:
        # Normalize input
        if isinstance(commit_output, list):
            commit_output = "\n".join(commit_output)
        if isinstance(pr_output, list):
            pr_output = "\n".join(pr_output)

        # Prepare commit data
        commit_data = []
        commit_messages = []

        for line in commit_output.strip().splitlines():
            parts = [part.strip() for part in line.split("|", 3)]
            if len(parts) == 4:
                date, author, commit_hash, message = parts
                commit_data.append({
                    "Date": date,
                    "Author": author,
                    "Commit": commit_hash,
                    "Message": message
                })
                commit_messages.append(f"{author} - {message}")

        # Optional summary
        summary_text = ""
        if not skip_summary and commit_messages:
            try:
                from git_log_stat.git_repo.git_nlp import init_summarizer
                summarizer = init_summarizer()
                full_text = ". ".join(commit_messages)
                full_text = " ".join(full_text.split()[:1024])
                summary_text = summarizer(full_text, max_length=120, min_length=40, do_sample=False)[0]['summary_text']
            except ImportError:
                log.warning("⚠️ Summarizer module not found. Skipping summary.")
            except Exception as e:
                log.warning(f"⚠️ Summarization failed: {e}")

        # Begin writing to Excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            if summary_text:
                pd.DataFrame({"Summary": [summary_text]}).to_excel(writer, sheet_name="Summary", index=False)

            # Write commit data
            df_commits = pd.DataFrame(commit_data)
            df_commits.to_excel(writer, sheet_name="Commits", index=False)

            # Write PR data (if provided)
            if pr_output:
                pr_lines = [line.strip() for line in pr_output.strip().splitlines() if line.strip()]
                pr_df = pd.DataFrame(pr_lines, columns=["Pull Request Info"])
                pr_df.to_excel(writer, sheet_name="Pull Requests", index=False)

        log.info(f"✅ Excel file written to: {output_file}")

    except Exception as e:
        log.error(f"❌ Failed to write Excel file: {e}", exc_info=True)


class XlsExporter(BaseExporter):

    def export(self, output_file_name, commit_output, pr_output=None, skip_summary=False):
        self.log.info("Generating Excel file: %s", output_file_name)
        generate_xls(
            log=self.log,
            output_file=output_file_name,
            commit_output=commit_output,
            pr_output=pr_output,
            skip_summary=skip_summary
        )
