# c-repl

Minimal interactive C prompt. The main focus: how much mileage can we get with only a handful of Python and Bash scripts? When it comes to the interactive C prompt, you can go quite far. Your computer will probably suffer a lot from unnecessary and repetitive computations, but at least _you_ can do your job.

## Requirements

Installing them from the OS package repository should be enough.

 - Clang (non-ancient)
 - Python (3.0.0+)

## How to Use

Run `c-repl` and enter C statements. `-h` for help.

```
$ ./c-repl
```

Optionally, initialize the header lookup cache for automatic non-C-library header inclusion. **This may take some time.**

```
$ ./assets/find-header cache
```


## How Does It Work

### Basics

 - Every statement goes to `int main()` by default.
    - If a new statement generates an error, the statement and the error message will be added as a comment.
    - All preprocessor directives will be prepended at the beginning.
 - A function definition can be started by typing a function prototype.
    - Then, every new statement will be added to it (not in `main`) until it's ended.
    - Similarly, a block can be opened by typing the block header (with `{` at the end).
    - Functions will be _global_: no local function definition.
    - Type `}` to end a function (or a block).
    - Duplicate function definition will be rejected.
 - New program output will be printed after every new statement.
    - If a new program output is not prepended with the previous one, the entire new output will be printed.
 - Missing headers will be handled on a best-effort basis.
    - Compiler-suggested headers will be automatically included.
    - If not, users have to choose what to include among the suggestions by `find-header`. 
    - Users can manually type `#include` to include headers.
 - The pre-existing C code could be included with the `-i` option.

### Value Printing

The return value of expressions (e.g., variables) can be printed. Type `%print <expr>` (`<expr>` being your expression), and it'll print the value (if `<expr>` is reachable from the execution point of view) and its type (if it's identifiable). For example,

```
>>> const char *s = "Hello";
>>> %print s
s = (const char*) "Hello"
```

You can specify **print hints** in the parentheses next to `%print` to control the print result. Available hints:

 - `ptr`: print the pointer address.
 - `len=<len>`: print an array with a length `<len>`. `<len>` can be a number or a variable name.

## FAQ

 - Does it work?
    - Yes, it works.
