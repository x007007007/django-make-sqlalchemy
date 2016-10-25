import warnings
from UserList import UserList


class Stem(object):
    def get_lines(self):
        warnings.warn("please implement", NotImplemented)

    def __str__(self):
        return "\n".join(self.get_lines())


class BlankLine(Stem):
    def __init__(self, line):
        self.line = line

    def get_lines(self):
        for _ in range(self.line):
            yield ""


class Stems(Stem, UserList):
    def __init__(self, *args):
        self.data = args

    def get_lines(self):
        for stem in self.data:
            if isinstance(stem, Stem):
                for s in stem.get_lines():
                    yield s
            else:
                yield stem


class Operator(Stem):
    pass


class Parentheses(Operator):
    def __init__(self, start=None, body=None, end=None):
        self.start = start
        self.body = body
        self.end = end

    def get_lines(self):
        if isinstance(self.start, Stem):
            start = list(self.start.get_lines())
            for s in start[:-1]:
                yield s
            temp = start[-1]
        elif self.start is None:
            temp = ""
        else:
            temp = self.start
        if isinstance(self.body, Stem):
            for l in Block(temp, self.body, sep="(").get_lines():
                yield l
            yield ")"
        elif self.body is None:
            temp += "()"
        else:
            temp = "{temp}({body})".format(temp=temp, body=self.body)
        if isinstance(self.end, Stem):
            end = list(self.end.get_lines())
            yield "{}{}".format(temp, end[0])


class Comment(Operator):
    def __init__(self, comment, start=None):
        if start is None:
            self.start = ""
        else:
            self.start = start
        self.comment = comment

    def get_lines(self):
        if self.start == "":
            temp = "# "
        elif isinstance(self.start, Stem):
            start = list(self.start.get_lines())
            for y in start[:-1]: yield y
            temp = "{}  # ".format(start[-1])
        else:
            temp = "{}  # ".format(self.start)

        if isinstance(self.comment, Stem):
            for l in  self.comment.get_lines():
                yield "# {}".format(l)
        else:
            yield "{}{}".format(temp, self.comment)


class Block(Stem):
    def __init__(self, head, body, indent=4, sep=":"):
        self.head = head
        self.body = body
        self.sep = sep
        self.indent = " " * indent

    def get_lines(self):
        if isinstance(self.head, Stem):
            heads = list(self.head)
            for head in heads[:-1]: yield head
            if heads:
                yield "{}{}".format(heads[-1], sep)
        else:
            yield self.head

        if isinstance(self.body, Stem):
            for b in self.body.get_lines():
                yield "{}{}".format(self.indent, b)
        else:
            yield "{}{}".format(self.indent, self.body)


class ClassStem(Block):
    def __init__(self, name, exp, stem):
        self.name = name
        self.exp = exp
        self.stem = stem

    def get_lines(self):
        yield 1


class VarName(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Bind(Operator):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_lines(self):
        yield "{names} = {values}".format(
            names=",".join(self.kwargs.keys()),
            values=",".join(str(i) for i in self.kwargs.values())
        )


if __name__ == "__main__":
    print(Stems(
        Bind(a=1, c=3),
        Bind(d=VarName("a")),
        BlankLine(2),
        Block("class hello world", Stems(
            Comment("test ", start=Bind(xxc=VarName("d")))
        ))
    ))