
import glob
import os
from mirascope import BaseMessageParam, Messages
import tree_sitter_rust as tsrust
from tree_sitter import Language, Parser

from cache import cache_fn
from model import dynLLM


# class DocAgent:
#     def __init__(self, path: str):
#         self.source = glob.glob(os.path.join(path, "**.rs"))        
#         self.context = []
#         if os.path.exists(os.path.join(path, "README.md")):
#             self.context.append(Messages.User(self.summary_gen(os.path.join(path, "README.md")).content))

@cache_fn(".cargo-aidoc")
def _summary_gen(context: list[BaseMessageParam], content: str, path: str) -> str:
    while True:
        content = dynLLM(
            Messages.System(
                "You are a documentation generator for Rust code."
                f"Please summarize the file `{path}` given by the user. The file describes a functionality of a Rust module. "
                "The file content will be given to you later, together with the context of that file. "
                "Please provide a system message describing the context of this module for other AI models. "
                "Your prompt should start with **'You are currently navigating within ...'**, and then describe the content. "
            ),
            *context,
            Messages.User(content),
        ).content
        if content.startswith("You are currently navigating within"):
            return content

def summary_gen(context: list[BaseMessageParam], path: str) -> BaseMessageParam | None:
    if os.path.isfile(path):
        with open(path, "r") as f:
            return Messages.System(_summary_gen(context, f.read(), path))
    else:
        files = ["README.md", "main.rs", "lib.rs", "mod.rs"]
        l = [os.path.join(path, file) for file in files if os.path.exists(os.path.join(path, file))]
        if len(l) >= 1:
            with open(l[0], "r") as f:
                return Messages.System(_summary_gen(context, f.read(), l[0]))
        else:
            return None
        

@cache_fn(".cargo-aidoc")
def _docgen(context: str, code: str, indent: str = "") -> str:
    while True:
        resp = dynLLM(
            Messages.System(
                "You are a documentation generator for Rust code. \n"
                "You are given a Rust code snippet and you need to generate a documentation for it. \n"
                "We will also provide context about the code for you. \n"
                "Please provide result in pure markdown text based on the following guidelines. \n"
                "\n"
                "* Do not generate examples. Do not add titles/headers. \n"
                "* Simply provide the markded text describe the functionity of the item. \n"
                "* Do not explain basic Rust concept like the function is `pub` or `u8`. Assume user knows Rust. \n"
                "* **Do not mention the name of this Rust item and its type**. Assume function name and types are available to the user. \n"
                "* **No implementation details**. Simply explain the interface. \n"
                "* Provide your response in 1–2 paragraphs. Begin with a one-sentence summary of the code snippet. Include a second paragraph explaining the functionality in detail, but omit it for simple code. \n"
                "    * For functions, start with a verb and describe the functionality. \n"
                "    * For structs, enums and unions, start the documentation with a noun phrase summarizing this type, and then elaborate the details. \n"
            ),
            *context,
            Messages.User(
                "Now please generate documentation for the following code snippet:\n"
                f"```rust\n{code}\n```\n"
            ),
        ).content
        if "//" not in resp and "# " not in resp:
            break
    
    if resp.split("\n")[0].count(". ") > 1:
        resp = resp.split("\n")[0].replace(". ", ". \n", 1) + "\n" + "\n".join(resp.split("\n")[1:])
    resp = resp.replace(". ", ". \n")
    return f"{indent}/// " + resp.replace("\n", f"\n{indent}/// ")


RUST_LANGUAGE = Language(tsrust.language())

def docgen(crate_path, path: str, item_types: list[str]) -> dict[int, str]:
    crate_path = os.path.abspath(os.path.normpath(crate_path))
    path = os.path.abspath(os.path.normpath(path))
    
    mod = path
    modules = []
    while mod != crate_path:
        mod = os.path.dirname(mod)
        modules.append(mod)

    modules.reverse()

    context = []
    for mod in modules:
        if msg := summary_gen(context, mod):
            context.append(msg)
        
    parser = Parser(RUST_LANGUAGE)
    comments = dict()
    with open(path, "rb") as f:
        file_content = f.read()
        tree = parser.parse(file_content)
        file_context = Messages.System(
            "You are looking at a Rust file shown as follows:\n"
            f"```rust\n{file_content.decode()}\n```\n"
        )
        already_commented = False
        for child in tree.root_node.children:
            if child.type == "line_comment" and child.text.decode().strip().startswith("///"):
                already_commented = True
            if child.type == "impl_item":
                for child2 in child.child_by_field_name("body").children:
                    if child2.type == 'line_comment' and child2.text.decode().strip().startswith("///"):
                        already_commented = True
                    if child2.type in item_types:
                        if already_commented:
                            already_commented = False
                            continue

                        code = (
                            f"\n\nimpl {child.child_by_field_name('type').text.decode()} {{\n"
                            f"    {child2.text.decode()}\n"
                            "}\n"
                        )
                        comments |= { child2.start_point.row : _docgen(context + [file_context], code, indent="    ") + "\n" }
            elif child.type in item_types:
                if already_commented:
                    already_commented = False
                    continue
                comments |= { child.start_point.row : _docgen(context + [file_context], child.text.decode()) + "\n" }
    return comments
