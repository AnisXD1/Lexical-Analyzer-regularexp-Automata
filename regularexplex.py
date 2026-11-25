
import re
from collections import Counter

KEYWORDS = {"if", "else", "while", "int", "float"}

TOKEN_SPECIFICATION = [
    ("COMMENT",     r"//[^\n]*"),
    ("INVALID_ID",  r"\d+[A-Za-z_][A-Za-z0-9_]*"),
    ("NUMBER",      r"\d+(\.\d+)?"),
    ("IDENTIFIER",  r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OPERATOR",    r"==|!=|<=|>=|[+\-*/<>]"),
    ("ASSIGNMENT",  r"="),
    ("SEPARATOR",   r"[;,(){}]"),
    ("WHITESPACE",  r"\s+"),
    ("INVALID",     r"."),
]


def lexical_analysis(source_code):

    tokens = []
    errors = []

    pattern = "|".join(
        f"(?P<{name}>{regex})"
        for name, regex in TOKEN_SPECIFICATION
    )

    line = 1
    column = 1

    for match in re.finditer(pattern, source_code):

        token_type = match.lastgroup
        lexeme = match.group()

        start_line = line
        start_column = column

        # Ignore comments and whitespace
        if token_type not in ("COMMENT", "WHITESPACE"):

            # Invalid identifier starting with a digit
            if token_type == "INVALID_ID":

                errors.append(
                    f"Lexical error: {lexeme!r} "
                    f"at line {start_line}, column {start_column}: "
                    "An identifier cannot start with a digit."
                )

            # Invalid integer starting with zero
            elif token_type == "NUMBER":

                if "." in lexeme:
                    token_type = "REAL"

                else:
                    if len(lexeme) > 1 and lexeme[0] == "0":

                        errors.append(
                            f"Lexical error: {lexeme!r} "
                            f"at line {start_line}, column {start_column}: "
                            "An integer cannot start with zero."
                        )

                    else:
                        token_type = "INTEGER"
                        tokens.append(
                            (token_type, lexeme, start_line)
                        )

            # Identifiers and keywords
            elif token_type == "IDENTIFIER":

                if lexeme in KEYWORDS:
                    token_type = "KEYWORD"

                tokens.append(
                    (token_type, lexeme, start_line)
                )

            # Operators, assignments and separators
            elif token_type in ("OPERATOR", "ASSIGNMENT", "SEPARATOR"):

                tokens.append(
                    (token_type, lexeme, start_line)
                )

            # Invalid characters
            elif token_type == "INVALID":

                errors.append(
                    f"Lexical error: {lexeme!r} "
                    f"at line {start_line}, column {start_column}: "
                    "Invalid character."
                )

        # Update line and column positions
        if "\n" in lexeme:

            line += lexeme.count("\n")
            column = len(lexeme.rsplit("\n", 1)[-1]) + 1

        else:
            column += len(lexeme)

    # Count tokens
    statistics = Counter(token[0] for token in tokens)

    return tokens, errors, statistics


# Example input
source = """
int x = 01;
int y = 25;
int 1name = 10;
int z = 007;
float a = 2.5;
int b = 0;
"""


# Run lexical analysis
tokens, errors, statistics = lexical_analysis(source)


# Display tokens
print("TOKENS:")

for token in tokens:
    print(token)


# Display lexical errors
print("\nLEXICAL ERRORS:")

if errors:
    for error in errors:
        print(error)
else:
    print("No lexical errors.")


# Display statistics
print("\nTOKEN STATISTICS:")

print("Total tokens:", len(tokens))

for token_type, count in sorted(statistics.items()):
    print(f"{token_type}: {count}")
    