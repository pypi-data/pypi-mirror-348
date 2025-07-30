from pathlib import Path

from git_log_stat.app_logs.logger_service import IBMLogger
from git_log_stat.git_exporters.base_exporter import BaseExporter
from git_log_stat.git_repo.git_export_service import export_git_activity_report

class GitOutputService:

    def __init__(self):
        self.log = IBMLogger("GitOutputService").get_logger()

    def generate_output_file(self, output_format, output_file_name,
                             commit_output, author, start_date, end_date,
                             pr_output=None, include_summary=True, output_dir: str|Path="."):
        match output_format:
            case "all":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                   author=author, output_dir=output_dir, file_prefix=output_file_name,
                                   start_date=start_date, end_date=end_date, include_summary=include_summary,
                                   export_excel=True, export_csv=False, export_pdf=True,
                                   export_tsv=False, export_txt=True, export_docx=True, export_pptx=True, export_all=True)
            case "txt":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                           author=author, output_dir=output_dir, file_prefix=output_file_name,
                                           start_date=start_date, end_date=end_date, include_summary=include_summary,
                                           export_excel=False, export_csv=False, export_pdf=False,
                                           export_tsv=False, export_txt=True, export_docx=False, export_pptx=False)
            case "pdf":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                           author=author, output_dir=output_dir, file_prefix=output_file_name,
                                           start_date=start_date, end_date=end_date, include_summary=include_summary,
                                           export_excel=False, export_csv=False, export_pdf=True,
                                           export_tsv=False, export_txt=False, export_docx=False, export_pptx=False)
            case "xls":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                           author=author, output_dir=output_dir, file_prefix=output_file_name,
                                           start_date=start_date, end_date=end_date, include_summary=include_summary,
                                           export_excel=True, export_csv=False, export_pdf=False,
                                           export_tsv=False, export_txt=False, export_docx=False, export_pptx=False)
            case "csv":
                self.log.info("CSV not implemented yet")
            case "tsv":
                self.log.info("TSV not implemented yet")
            case "docx":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                           author=author, output_dir=output_dir, file_prefix=output_file_name,
                                           start_date=start_date, end_date=end_date, include_summary=include_summary,
                                           export_excel=False, export_csv=False, export_pdf=False,
                                           export_tsv=False, export_txt=False, export_docx=True, export_pptx=False)
            case "ppt":
                export_git_activity_report(commit_logs=commit_output, pr_logs=pr_output,
                                           author=author, output_dir=output_dir, file_prefix=output_file_name,
                                           start_date=start_date, end_date=end_date, include_summary=include_summary,
                                           export_excel=False, export_csv=False, export_pdf=False,
                                           export_tsv=False, export_txt=False, export_docx=False, export_pptx=True)

    def get_commit_count(self, output, pr_output=None):
        self.log.info("Getting counts for commits and PRs")
        return BaseExporter.export_count(commit_output=output, pr_output=pr_output)



