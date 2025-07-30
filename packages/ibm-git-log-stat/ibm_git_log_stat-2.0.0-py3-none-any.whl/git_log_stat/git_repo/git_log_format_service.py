from git_log_stat.app_logs.logger_service import IBMLogger


class GitLogFormatService:

    def __init__(self):
        self.log = IBMLogger("GitLogFormatService").get_logger()

    def default_git_log_format(self):
        self.log.debug("using default log format")
        return "format:%h %ad | %s"

    def get_log_format(self, **kwargs):
        format_str = "format:"
        self.log.debug("processing format args")
        for key, val in kwargs.items():
            self.log.debug("Processing arg: %s with value %s", key, val)
            format_str = format_str + " " + val
        return format_str

    def get_log_format_detailed(self):
        arg_map = {"date": "%ad", "sep-2": "|", "name": "%an", "sep-3": "|", "git-commit": "%h", "sep-1": "|",
                   "ref-name": "%s"}
        return self.get_log_format(**arg_map)
