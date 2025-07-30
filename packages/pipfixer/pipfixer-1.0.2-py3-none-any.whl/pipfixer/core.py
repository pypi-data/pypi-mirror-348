import ast
import sys
import subprocess
import importlib.util

def extract_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=file_path)

    modules = set()

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                modules.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                modules.add(n.module.split('.')[0])

    return sorted(modules)

def is_builtin_module(module_name):
    return module_name in sys.builtin_module_names

def is_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_module(module_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
    except Exception as e:
        print(f"❌ Failed to install {module_name}: {e}")

def pipfixer(file_path):
    print(f"🔍 Scanning '{file_path}' for imports...\n")
    imports = extract_imports(file_path)

    for module in imports:
        if is_builtin_module(module):
            print(f"✅ '{module}' is a built-in module. Skipping.")
        elif is_installed(module):
            print(f"✅ '{module}' is already installed.")
        else:
            print(f"📦 Installing missing module: '{module}'...")
            install_module(module)
