from pathlib import Path
from typing import List

from git_log_stat.app_logs.logger_service import IBMLogger

log = IBMLogger("GitExportService").get_logger()


def export_git_activity_report(
        commit_logs: List[str],
        pr_logs: List[str],
        author: str,
        start_date: str,
        end_date: str,
        output_dir: str = ".",
        file_prefix: str = "git-activity-report",
        include_summary: bool = True,
        export_excel: bool = True,
        export_pdf: bool = True,
        export_docx: bool = True,
        export_pptx: bool = True,
        export_txt: bool = True,
        export_csv: bool = False,
        export_tsv: bool = False,
        export_all: bool = False
):
    log.info("Exporting git activity report")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    '''
    file_prefix = str(file_prefix) + datetime.now().strftime("-%y-%m-%d-") + author + "-" + start_date + "-to-" + end_date
    '''

    # FIXME: Dirty workaround. Needs to be aligned with exporters. Change this flag to skip_summary
    include_summary = not include_summary

    if export_excel:
        from git_log_stat.git_exporters.xls_exporter import XlsExporter
        xls_exporter = XlsExporter()
        excel_file = output_dir / f"{file_prefix}.xlsx" if export_all else file_prefix
        xls_exporter.export(excel_file, commit_logs, pr_logs, include_summary)

    if export_pdf:
        from git_log_stat.git_exporters.pdf_exporter import PdfExporter
        pdf_exporter = PdfExporter()
        pdf_file = str(output_dir / f"{file_prefix}.pdf" if export_all else file_prefix)
        pdf_exporter.export(pdf_file, commit_logs, pr_logs, include_summary)

    if export_docx:
        from git_log_stat.git_exporters.docx_exporter import DocxExporter
        docx_exporter = DocxExporter()
        docx_file = str(output_dir / f"{file_prefix}.docx" if export_all else file_prefix)
        docx_exporter.export(docx_file, commit_logs, pr_logs, include_summary)

    if export_pptx:
        from git_log_stat.git_exporters.ppt_exporter import PptExporter
        pptx_exporter = PptExporter()
        pptx_file = str(output_dir / f"{file_prefix}.pptx" if export_all else file_prefix)
        pptx_exporter.export(pptx_file, commit_logs, pr_logs, include_summary)

    if export_txt:
        from git_log_stat.git_exporters.txt_exporter import TxtExporter
        txt_exporter = TxtExporter()
        txt_file = output_dir / f"{file_prefix}.txt" if export_all else file_prefix
        txt_exporter.export(txt_file, commit_logs, pr_logs, include_summary)

    if export_csv:
        from git_log_stat.git_exporters.csv_tsv_exporter import CsvExporter
        csv_exporter = CsvExporter()
        csv_exporter.export(file_prefix, commit_logs, pr_logs, include_summary)

    if export_tsv:
        from git_log_stat.git_exporters.csv_tsv_exporter import TsvExporter
        tsv_exporter = TsvExporter()
        tsv_exporter.export(file_prefix, commit_logs, pr_logs, include_summary)

    log.info("✅ All requested exports completed.")
