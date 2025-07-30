class LogGenerator:
    def __init__(self, template_path=None):
        self._template_path = template_path

    def collect_changes(self, from_ref, to_ref):
        return [
            "Fix: resolve issue with build step",
            "Add: new deployment script",
            "Update: dependency versions"
        ]

    def format_log(self, entries):
        return "\n".join(f"- {entry}" for entry in entries)

    def write_log(self, path, content):
        with open(path, "w") as f:
            f.write(content)
