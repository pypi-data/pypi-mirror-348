import ast

"""
每个脚本注册前，用ast静态检查脚本里用到的模块
"""
class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        self.imports.append(module.split(".")[0]) # first level
        self.generic_visit(node)

def get_import_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as fp:
        source_code = fp.read()

    ast_tree = ast.parse(source_code)
    import_collector = ImportCollector()
    import_collector.visit(ast_tree)
    return import_collector.imports

"""
对动态导入、模块udf，进行运行时检查，只需在每个interpreter最开始被执行一次
"""
import sys
from importlib.abc import MetaPathFinder

class BlockImport(MetaPathFinder):
    def __init__(self, blocked_modules):
        self.blocked_modules = set(blocked_modules)

    def find_spec(self, fullname, path, target=None):
        if fullname in self.blocked_modules:
            raise ImportError(f"Import of '{fullname}' is blocked")
        return None  # skip

def block_imports(blocked):
    sys.meta_path.insert(0, BlockImport(blocked))
