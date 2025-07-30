"""
pybrv - Python Business Rule Validator
Main module that provides the core functionality and interface.
"""
from .rule_manager import RuleManager, DatabricksPybrvEtlmeta

# Singleton instance of the rule manager
rule_manager = RuleManager()

def help():
    """Display help information about pybrv."""
    print("pybrv is the Python-based business rule validator.")
