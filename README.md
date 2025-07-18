# c-repl

Minimal interactive C prompt. The main focus: how much mileage can we get with only a handful of Python and Bash scripts? When it comes to the interactive C prompt, you can go quite far. Your computer will probably suffer a lot from unnecessary and repetitive computations, but at least _you_ can do your job.

## Requirements

Installing them from the OS package repository should be enough.

 - Clang (non-ancient)
 - Python (3.0.0+)

Optionally, if your default shell is not Bash, you may want to install it too.

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
 - A _global_ function definition can be started by entering a function header with `{` at the end.
    - Then, every new statement will be added to it (not to `main`) until it's ended.
    - Similarly, a block can be opened by typing the block header with `{` at the end.
    - Enter `}` to end a function (or exit the current block in general).
    - Duplicate function definition will be rejected.
 - New program output will be printed after every new statement.
    - If a new program output is not prepended with the previous one, the entire new output will be printed.
 - Missing headers will be handled on a best-effort basis.
    - Compiler-suggested headers will be automatically included.
    - If not, users have to choose what to include among the suggestions by `find-header`. 
    - Users can manually type `#include` to include headers.
 - The pre-existing C code could be included with the `-i` option.

### Value Printing

The return value of expressions (e.g., variables) can be printed. Type `%print <expr>` (`<expr>` being your expression), and it'll print the value (if `<expr>` is executable) and its type (if it's identifiable). For example,

```
>>> const char *s = "Hello";
>>> %print s
s = (const char *) "Hello"
```

You can specify **print hints** in the parentheses next to `%print` to control the print result. Available hints:

 - `ptr`: print the pointer address.
 - `len=<len>`: print an array with a length `<len>`. `<len>` can be a number or a variable name.

For example, the following snippet prints the above string `s` as a `unsigned char` array of length `6`.

```
>>> %print(len=6) (unsigned char *)s
(unsigned char *)s = [ 72, 101, 108, 108, 111, 0 ]
```

### Including Pre-written C Snippet

A pre-written C snippet (e.g., functions or struct/enum definitions) can be included at startup with the `-i` option.

```
$ cat foo.c
#include <stdio.h>
void foo() {
    printf("Hello\n");
}

$ c-repl -i foo.c
C-REPL 0.1.5 (main, 17 Jul 2025 09:24:08) [Ubuntu Clang 18.1.3 (1ubuntu1)] on linux
Type "help" for more information.
>>> foo();
Hello
```

## When to Use

### Manual Unit Testing

You could use `c-repl` to unit-test a function. This is the usage that I'm mainly using it for. For example, suppose you should write a function that swaps `#` to `/` in a URI string, but only when it is used as a demarcator (e.g., between a domain name and a path-like identifier). Assuming you wrote a function `fix_sharp_to_slash_delim` for this, you could create a test wrapper function `test` and include both of them before starting up `c-repl`. Then you could use `%print` to check the return value of `test`.

```
$ cat fix-uri.c 
#include <string.h>

static void fix_sharp_to_slash_delim(char *s) {
    char *ptr_sharp = strchr(s, '#');
    char *ptr_slash = strchr(s, '/');

    if (ptr_sharp && (!ptr_slash || ptr_sharp < ptr_slash)) 
        *ptr_sharp = '/';

    return;
}

static char *test(const char *s) {
    char *ss = strdup(s);
    fix_sharp_to_slash_delim(ss);
    return ss;
}

$ c-repl -i fix-uri.c 
C-REPL 0.1.5 (main, 17 Jul 2025 09:24:08) [Ubuntu Clang 18.1.3 (1ubuntu1)] on linux
Type "help" for more information.
>>> %print test("aa.bb.cc#aa/bb")
test("aa.bb.cc#aa/bb") = "aa.bb.cc/aa/bb"
>>> %print test("aa.bb.cc/aa/bb")
test("aa.bb.cc/aa/bb") = "aa.bb.cc/aa/bb"
>>> %print test("aa.bb.cc/aa#aa/bb")
test("aa.bb.cc/aa#aa/bb") = "aa.bb.cc/aa#aa/bb"
>>> %print test("aa.bb.cc")
test("aa.bb.cc") = "aa.bb.cc"
```

## FAQ

 - Does it work?
    - Yes, it works.
