# c-repl

Minimal C REPL prompt, written in Python and Bash.

## Requirements

 - Clang (any version)

## How to Use

 1. (one-time) Initialize header lookup cache. **This may take some time.**

```
$ ./find-header cache
```

 2. Run `c-repl` and enter C statements.

```
$ ./c-repl    # -o <code_path>, if you'd like to get the code.
```

## Summary 

 - Every statement goes to `int main()` by default.
 - A function definition can be started by typing a function prototype.
    - Functions will be _global_: no local function definition.
    - When defining a function, every statement will be added to the it (not in `main`).
    - Previous duplicate functions will be commented out.
 - New program output will be printed after every new statement.
    - If the new program output is not prepended with the previous one, the entire new output will be printed.
 - Missing headers will be handled on the best-effort basis.
    - Compiler-suggested headers will be automatically included.
    - If not, users have to choose what to include among the suggestions by `find-header`. 
    - Users can manually type `#include` to include headers.
 - All proprocessor directives will be prepended at the beginning.
 - If the new statement generates an error (either at compile time or at runtime), the statement will be commented out and the error message will be added above as additional comments.
