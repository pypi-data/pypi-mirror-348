class EnvironmentValidator:
    def __init__(self):
        self._checks = []

    def add_check(self, name, check_fn):
        self._checks.append((name, check_fn))

    def run_all(self):
        results = {}
        for name, fn in self._checks:
            try:
                results[name] = fn()
            except Exception:
                results[name] = False
        return results
