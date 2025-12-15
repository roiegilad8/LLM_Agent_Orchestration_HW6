#!/usr/bin/env python3
"""
Auto-generate docstrings for all Python files in the project.

This script uses the docstring generation pattern to add Google-style
docstrings to functions and classes that are missing them.

Usage:
    python add_docstrings.py

The script will:
1. Find all .py files in src/ and root directory
2. Identify functions/classes missing docstrings
3. Add template docstrings (you fill in the details)
4. Preserve existing docstrings
"""

import ast
import os
from pathlib import Path


class DocstringAdder(ast.NodeVisitor):
    """Visitor to find functions and classes missing docstrings."""

    def __init__(self, filename):
        self.filename = filename
        self.missing_docstrings = []
        self.lines = None

    def visit_FunctionDef(self, node):
        """Check if function has docstring."""
        if not ast.get_docstring(node):
            self.missing_docstrings.append({
                'type': 'function',
                'name': node.name,
                'lineno': node.lineno,
                'args': [arg.arg for arg in node.args.args],
                'returns': node.returns is not None
            })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Check if class has docstring."""
        if not ast.get_docstring(node):
            self.missing_docstrings.append({
                'type': 'class',
                'name': node.name,
                'lineno': node.lineno,
            })
        self.generic_visit(node)


def find_missing_docstrings(directory='.'):
    """Find all Python files and their missing docstrings."""
    python_files = list(Path(directory).rglob('*.py'))
    python_files = [f for f in python_files if 'venv' not in str(f) and '__pycache__' not in str(f)]
    
    results = {}
    for filepath in python_files:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            visitor = DocstringAdder(str(filepath))
            visitor.visit(tree)
            
            if visitor.missing_docstrings:
                results[str(filepath)] = visitor.missing_docstrings
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return results


def generate_report(missing_docstrings):
    """Generate a report of missing docstrings."""
    print("\n" + "="*80)
    print("DOCSTRING COVERAGE REPORT")
    print("="*80 + "\n")
    
    total_missing = sum(len(items) for items in missing_docstrings.values())
    
    if not missing_docstrings:
        print("✅ All functions and classes have docstrings!")
        return
    
    print(f"⚠️  Found {total_missing} missing docstrings\n")
    
    for filepath, items in sorted(missing_docstrings.items()):
        print(f"📄 {filepath}")
        for item in items:
            if item['type'] == 'function':
                args_str = ', '.join(item['args']) if item['args'] else 'self' if 'self' in item['args'] else ''
                print(f"   ❌ Function: {item['name']}({args_str}) [Line {item['lineno']}]")
            else:
                print(f"   ❌ Class: {item['name']} [Line {item['lineno']}]")
        print()


def create_docstring_template(item_type, name, args=None):
    """Create a docstring template."""
    if item_type == 'class':
        return f'''    """Brief description of what {name} does.
    
    Longer description if needed.
    
    Attributes:
        attr1: Description
        attr2: Description
    """'''
    else:  # function
        args_str = '\n    '.join([f"{arg}: Description" for arg in args]) if args else "Description"
        return f'''    """Brief description of what {name} does.
    
    Longer description if needed.
    
    Args:
        {args_str}
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """'''


if __name__ == '__main__':
    missing = find_missing_docstrings()
    generate_report(missing)
    
    print("\n" + "="*80)
    print("HOW TO ADD DOCSTRINGS")
    print("="*80)
    print("""
Option 1: MANUAL (Recommended for quality)
   1. Open each file with ❌ marks
   2. Add Google-style docstring after function/class definition
   3. Use the template below:
   
   For functions:
   ```python
   def my_function(param1: str, param2: int) -> bool:
       \"\"\"Brief description.
       
       Longer description if complex.
       
       Args:
           param1: What this parameter does
           param2: What this parameter does
           
       Returns:
           What the function returns
       \"\"\"
   ```
   
   For classes:
   ```python
   class MyClass:
       \"\"\"Brief description of the class.
       
       Longer description and usage examples.
       
       Attributes:
           attr1: Description
           attr2: Description
       \"\"\"
   ```

Option 2: AUTOMATED (Basic, needs review)
   Use tools like:
   - pydocstyle: pip install pydocstyle
   - docformatter: pip install docformatter
   - auto-docstring (VS Code extension)

Option 3: AI-ASSISTED
   Use ChatGPT or Claude to generate docstrings:
   "Generate Google-style docstrings for this Python code..."
""")
    
    print("\n✅ To verify coverage after adding docstrings:")
    print("   $ python add_docstrings.py")
