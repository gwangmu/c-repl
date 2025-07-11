#!/usr/bin/python

import os
import re
import sys

INDENT = "  "

class EnumType():
    def __init__(self, name="?"):
        self.name = name
        self.children = []

    def get(self):
        ret = ["enum {} {{".format(self.name)]
        for child in self.children:
            ret += ["{}{},".format(INDENT, child)]
        ret += ["}"]
        return ret

    def fields(self):
        return self.children

class RecordType():
    def __init__(self, kind="?", name="?"):
        self.kind = kind 
        self.name = name
        self.children = []

    def get(self):
        ret = ["{} {}{{".format(self.kind, self.name + " " if self.name else "")]
        for child in self.children:
            ret += [INDENT + s for s in child.get()]
        ret += ["}"]
        return ret

    def fields(self):
        return [c.fields() for c in self.children]

class GenericType():
    def __init__(self, name="?"):
        self.name = name

    def get(self):
        return [self.name]

    def fields(self):
        return self.name

class RecordField():
    def __init__(self, type=None, name="?"):
        self.type = type
        self.name = name

    def get(self):
        ret = self.type.get()
        ret[-1] += " {};".format(self.name)
        return ret

    def fields(self):
        if (isinstance(self.type, RecordType)):
            return { self.name: self.type.fields() }
        else:
            return self.name

def parse_record(lines, start_idx=0, target_name=None, nest_prefix="| ", rec_ctx={}):
    cur_record = None 

    idx = start_idx 
    while (idx < len(lines)):
        cur_line = lines[idx]
        if (not cur_record):
            re_rec_decl = re.search("RecordDecl .* (struct|union) ([a-zA-Z0-9_]*) ?definition", cur_line)
            if (re_rec_decl):
                rec_kind = re_rec_decl.group(1)
                rec_name = re_rec_decl.group(2)
                if (target_name == None or target_name == "{} {}".format(rec_kind, rec_name)): 
                    cur_record = RecordType(rec_kind, rec_name)
                    if (not rec_name):
                        re_lineno = re.search("<line:([0-9:]+),", cur_line)
                        if (re_lineno):
                            cur_record.name = "@unnamed_at_{}@".format(re_lineno.group(1))
                            rec_ctx[re_lineno.group(1)] = cur_record
                    else:
                        rec_ctx["{} {}".format(rec_kind, rec_name)] = cur_record
        else:
            if (not cur_line.startswith(nest_prefix)): 
                break
            re_field_decl = re.search("FieldDecl .* ([a-zA-Z0-9_]+) '([^']+)'", cur_line)
            if (re_field_decl):
                field_name = re_field_decl.group(1)
                field_type = re_field_decl.group(2)
                if ("(unnamed " in field_type):
                    re_lineno = re.search("at [^:]*:([0-9:]*)", field_type)
                    if (re_lineno and re_lineno.group(1) in rec_ctx.keys()):
                        field_type_obj = rec_ctx[re_lineno.group(1)]
                elif (field_type in rec_ctx.keys()):
                    field_type_obj = rec_ctx[field_type]
                elif ("struct " in field_type or "union " in field_type):
                    new_rec_type, _ = parse_record(lines, start_idx=0, target_name=field_type, nest_prefix="| ", rec_ctx=rec_ctx)
                    rec_ctx[field_type] = new_rec_type
                    field_type_obj = new_rec_type
                else:
                    field_type_obj = GenericType(field_type)
                cur_record.children += [RecordField(field_type_obj, field_name)]
            elif ("RecordDecl" in cur_line):
                child_rec, next_idx = parse_record(lines, start_idx=idx, nest_prefix="| " + nest_prefix, rec_ctx=rec_ctx)
                assert(child_rec)
                idx = next_idx
        idx += 1

    return cur_record, idx-1

def parse_enum(lines, target_name):
    cur_enum = None
    nest_prefix = ""
    target_name_name = target_name.removeprefix("enum ")

    for line in lines:
        if (not cur_enum):
            if (re.match("[| -]*EnumDecl .* {}".format(target_name_name), line)):
                cur_enum = EnumType(target_name_name)
                re_prefix = re.search("^([| ]*)", line)
                assert(re_prefix)
                nest_prefix = re_prefix.group(1) + " "
        else:
            if (not line.startswith(nest_prefix)): break
            re_enum_const = re.search("EnumConstantDecl .* ([a-zA-Z_][a-zA-Z0-9_]*) '", line)
            if (re_enum_const):
                cur_enum.children += [re_enum_const.group(1)]

    return cur_enum

def find_typedef_type(lines, target_name):
    typedef_sig = "{} '".format(target_name)
    for line in lines:
        if ("TypedefDecl" in line):
            if (typedef_sig in line):
                re_real_name = re.search("'(struct|union|enum) ([A-Za-z0-9_]+)", line)
                if (re_real_name):
                    return "{} {}".format(re_real_name.group(1), re_real_name.group(2))
    return target_name

def main():
    filename = sys.argv[1]
    target_name = sys.argv[2]

    with open(filename, 'r') as f:
        ast_lines = f.readlines()

    target_name = find_typedef_type(ast_lines, target_name)
    if (target_name.startswith("struct ") or target_name.startswith("union ")):
        rec = parse_record(ast_lines, target_name=target_name)[0]
    elif (target_name.startswith("enum ")):
        rec = parse_enum(ast_lines, target_name=target_name)
    else:
        rec = None

    if (rec):
        for rec_line in rec.get():
            print(rec_line)
        print(rec.fields())

if __name__ == "__main__":
    main()
