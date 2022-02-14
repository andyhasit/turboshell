from turboshell import ts


{
    "js": {
         "exclude": ["node_modules", "dist"],
         "extensions": ["js", "ts", "jsx", "tsx"]
    },
    "py": {
         "exclude": ["venv"],
         "extensions": ["py"]
    }
}

def generate():
        
    for ext in ["js", "py"]:
        ts.alias(f"grep.{ext}", f"grep -ir $1 --include=\*.{ext}")


if ts.collecting:
    generate()