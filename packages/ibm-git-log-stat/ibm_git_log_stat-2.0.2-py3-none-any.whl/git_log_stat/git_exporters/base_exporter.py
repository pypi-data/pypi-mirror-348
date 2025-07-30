from abc import ABC, abstractmethod

from git_log_stat.app_logs.logger_service import IBMLogger


class BaseExporter(ABC):

    def __init__(self):
        self.log = IBMLogger("GitExporter").get_logger()

    @abstractmethod
    def export(self, output_file_name, commit_output, pr_output=None):
        """
        Export method to be implemented by each type of exporter.
        :param output_file_name: output file name to be used
        :param commit_output: commit logs to be exported
        :param pr_output: pr logs to be exported. Optional.
        :return: Path where file is exported successfully.
        """
        pass

    @staticmethod
    def export_count(commit_output: str | list, pr_output: str | list =None):
        c_count = 0
        p_count = 0
        if pr_output:
            c_count = len(commit_output) if isinstance(commit_output, list) else len(commit_output.split("\n"))
            p_count =  len(pr_output) if isinstance(pr_output, list) else len(pr_output.split("\n"))
            return c_count, p_count
        else:
            c_count = len(commit_output) if isinstance(commit_output, list) else len(commit_output.split("\n"))
            return c_count