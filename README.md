# c-repl

Minimal C REPL prompt, written in Python and Bash. The main focus is _extreme minimalism_; how much mileage can we get only using a handful of Python and Bash scripts? It turns out that, when it comes to the interactive C prompt, you can sort of do it. Your computer will suffer a lot from unnecessary and repetitive computations, but at least _you_ can do your job.

## Requirements

 - Clang (any version, maybe)

## How to Use

Run `c-repl` and enter C statements. `-h` for help.

```
$ ./c-repl
```

Optionally, initialize header lookup cache for automatic non-C-library header inclusion. **This may take some time.**

```
$ ./assets/find-header cache
```


## Summary 

 - Every statement goes to `int main()` by default.
 - A function definition can be started by typing a function prototype.
    - Functions will be _global_: no local function definition.
    - When defining a function, every statement will be added to the it (not in `main`).
    - Previous duplicate functions will be commented out.
 - New program output will be printed after every new statement.
    - If a new program output is not prepended with the previous one, the entire new output will be printed.
 - Missing headers will be handled on the best-effort basis.
    - Compiler-suggested headers will be automatically included.
    - If not, users have to choose what to include among the suggestions by `find-header`. 
    - Users can manually type `#include` to include headers.
 - All proprocessor directives will be prepended at the beginning.
 - If a new statement generates an error (either at compile time or at runtime), the statement will be commented out and the error message will be added above as additional comments.


## FAQ

 - Does it work?
    - Yes, it works.
