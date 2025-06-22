import cmd

class REPLoop(cmd.Cmd):
    intro = "Fancy intro v0.1.1"
    prompt = ">>> "

    def precmd(self, line):
        line_strip = line
        if (line_strip[0:1] == '%'):
            self.prompt = "{} >>> ".format(line_strip)
        return line

    def default(self, line):
        print(line)

repl = REPLoop()
repl.cmdloop()
