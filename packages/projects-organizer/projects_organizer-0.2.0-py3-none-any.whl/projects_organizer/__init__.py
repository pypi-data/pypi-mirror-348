from pathlib import Path
from typing_extensions import Annotated
from datetime import datetime
import ast
import typer
from rich.console import Console
import frontmatter
import jsonschema
import yaml

__version__ = "0.2.0"

app = typer.Typer(pretty_exceptions_enable=False)
state = {}
err_console = Console(stderr=True)

MD_FILE_DEFAULT = "index.md"

projects = {}

def init():
    md_files = []
    for file in state['base_dir'].glob("*"):
        if file.is_dir():
            full_path = file.resolve() / MD_FILE_DEFAULT
            if not full_path.exists() or not full_path.is_file():
                raise RuntimeError(f"Missing {MD_FILE_DEFAULT} in {file}")
            md_files.append(full_path)
    md_files = sorted(md_files)

    for file in md_files:
        with open(file, "r") as f:
            metadata, content = frontmatter.parse(f.read())
            title = metadata["title"]
            if title in projects:
                raise RuntimeError(f"Duplicate project title: {title} in {projects[title]['file']} and {file}")
            projects[title] = {
                'file': file,
                'metadata': metadata,
                'content': content,
            }

def parse_filter(filter: str):
    parsed = ast.parse(filter, mode="eval")
    #print(ast.dump(parsed, indent=4))

    if not isinstance(parsed, ast.Expression):
        raise RuntimeError(f"Invalid filter: {filter}")

    if not isinstance(parsed.body, ast.BoolOp) and not isinstance(parsed.body, ast.UnaryOp) and not isinstance(parsed.body, ast.Name):
        if not isinstance(parsed.body, ast.Compare):
            raise RuntimeError(f"Invalid filter: {filter}")

        final = ast.BoolOp(
            op=ast.And(),
            values=[parsed.body, ast.Constant(value=True)]
        )
        parsed.body = ast.copy_location(final, parsed.body)
        ast.fix_missing_locations(parsed)

    #print(f"comparison: {ast.dump(parsed, indent=4)}")
    compiled = compile(parsed, filename="<ast>", mode="eval")

    variables = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Name):
            variables.add(node.id)
    #print(f"variables: {variables}")

    #check_code = []
    #for v in variables:
    #    check_code.append(f'if "{v}" not in locals():\n  {v} = False')
    #check_code = '\n'.join(check_code)
    #print(check_code)
    #check_expr = ast.parse(check_code, mode='eval')
    #ast.fix_missing_locations(check_expr)
    #print(check_expr)

    return compiled, variables


@app.command()
def list(highlighted: Annotated[bool, typer.Option("--highlighted", "-h", help="Show only highlighted projects")] = False,
         archived: Annotated[bool, typer.Option("--archived", "-a", help="Show only archived projects")] = False,
         draft: Annotated[bool, typer.Option("--draft", "-d", help="Show only draft projects")] = False,
         filter: Annotated[str, typer.Option("--filter", "-f", help="Filter by element")] = None):
    for p in projects.values():
        if state["verbose"]:
            print(f"Processing {p['file']}")

        if highlighted and not p['metadata'].get('highlight', False):
            continue

        if archived and not p['metadata'].get('archived', False):
            continue

        if draft and not p['metadata'].get('draft', False):
            continue

        if filter is not None:
            compiled, variables = parse_filter(filter)
            context = {}
            for v in variables:
                if v == "datetime":
                    context[v] = datetime
                    continue
                if v not in p['metadata']:
                    context[v] = False
                    #raise RuntimeError(f"Variable {v} not found in {p['file']}")
                else:
                    context[v] = p['metadata'][v]
            result = eval(compiled, {}, context)
            if not result:
                continue
        
        print(f"- {p['metadata']['title']}")

@app.command()
def show(name: str):
    selected = []
    for p in projects.values():
        if name.lower() in p['metadata']['title'].lower():
            selected.append(p['metadata']['title'])

    if len(selected) == 0:
        raise RuntimeError(f"Project {name} not found.")

    found = None
    for s in selected:
        if name.lower() == s.lower():
            found = s

    if len(selected) > 1:
        if found is None:
            print(f"Multiple projects found: {', '.join([p for p in selected])}")
            return
    else:
        found = selected[0]

    if state["verbose"]:
        print(f"Project found: {projects[found]['file']}")
    print(projects[found]['metadata'])

@app.command()
def validate(schema: str,
             stop_on_error: Annotated[bool, typer.Option("--stop-on-error", "-s", help="Stop on first error")] = False):
    with open(schema, "r") as f:
        sc = yaml.safe_load(f.read())
    invalid = {}
    for p in projects.values():
        try:
            jsonschema.validate(p['metadata'], sc)
        except jsonschema.exceptions.ValidationError as e:
            invalid[p['metadata']['title']] = e
    if len(invalid) == 0:
        print("All projects are valid.")
    else:
        if stop_on_error:
            title, error = next(iter(invalid.items()))
            print(f"error for project {title}")
            print(error)
            pass
        else:
            for title, error in invalid.items():
                print(f"- {title}: {error}")
        raise typer.Exit(code=1)

@app.callback()
def main_options(verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
                 base_dir: Annotated[Path, typer.Option("--base_dir", "-d")] = Path(".")):
    state["verbose"] = verbose
    state["base_dir"] = base_dir
    init()

def main() -> None:
    try:
        app()
    except RuntimeError as e:
        err_console.print(f"[red]error[/red]: {e}")

if __name__ == "__main__":
    main()
