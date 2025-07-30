from git_log_stat.git_exporters.base_exporter import BaseExporter
from git_log_stat.git_exporters.file_exporter import generate_file


class TsvExporter(BaseExporter):

    def export(self, output_file_name, commit_output, pr_output=None, skip_summary=False):
        self.log.info("Generating TSV file: %s", output_file_name)
        generate_file(
            log=self.log,
            output_file=output_file_name,
            commit_output=commit_output,
            pr_output=pr_output,
            skip_summary=skip_summary
        )

class CsvExporter(BaseExporter):

    def export(self, output_file_name, commit_output, pr_output=None, skip_summary=False):
        self.log.info("Generating CSV file: %s", output_file_name)
        generate_file(
            log=self.log,
            output_file=output_file_name,
            commit_output=commit_output,
            pr_output=pr_output,
            skip_summary=skip_summary
        )
