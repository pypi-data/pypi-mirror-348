"""
Find file by name recursively from a starting directory.

Args:
    nome_arquivo (str): File name to search for.
    pasta_base (str, optional): Directory to start search. Defaults to current working dir.
    retornar_todos (bool): If True, returns a list of all matches. If False, returns first match.

Returns:
    str or List[str]: Full path(s) to the file(s).

Raises:
    FileNotFoundError: If no matching file is found.
"""
