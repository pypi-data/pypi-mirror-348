from qb.compiler_functions import encrypt_strings, preprocess, multi_line_lambda, replace_keywords, better_range, \
    transform_lists, manage_pipes, decrypt_strings

def __remove_entrypoint_decorator(code):
    """
    Remove the entrypoint decorator from the code.
    """
    lines = code.split("\n")
    new_lines = []
    for line in lines:
        if line.strip().startswith("@entrypoint"):
            continue
        new_lines.append(line)
    return "\n".join(new_lines)

def __add_qb_runtime_imports(code):
    imports = [
        "from qb_runtime import *",
    ]

    # Add the imports to the beginning of the code
    code = "\n".join(imports) + "\n" + code

    return code

def compile_to_qb(code):
    encrypted = encrypt_strings(code)
    code = encrypted[0]
    encrypted_strings = encrypted[1]

    code = preprocess(code)
    code = __remove_entrypoint_decorator(code)
    code = __add_qb_runtime_imports(code)
    code = multi_line_lambda(code)
    code = replace_keywords(code)
    code = better_range(code)
    code = transform_lists(code)
    code = manage_pipes(code)

    code = decrypt_strings(code, encrypted_strings)

    return code