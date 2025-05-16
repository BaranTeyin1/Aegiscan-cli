import ast

class SASTEngine:
    def __init__(self, rules):
        self.rules = rules
        self.results = []

    def run(self, code: str, filename: str = "<string>"):
        tree = ast.parse(code, filename)
        self._visit(tree)
        return self.results

    def _visit(self, node):
        for child in ast.walk(node):
            for rule in self.rules:
                match = rule.get("matches", [])[0]
                if match["node_type"] == type(child).__name__:
                    func = getattr(child, "func", None)
                    # Debug satırı
                    # print(f"DEBUG: Found node {type(child).__name__} with func {getattr(func, 'id', None)}")
                    if isinstance(func, ast.Name) and func.id == match["func_name"]:
                        self.results.append({
                            "filename": "test_code.py",
                            "line": child.lineno,
                            "rule_id": rule["id"],
                            "message": rule["description"],
                            "severity": rule["severity"]
                        })
