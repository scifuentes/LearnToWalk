


class ContextPrint():
    def __init__(self):
        self.context=[]
    def push(self, context):
        self.context.append(context)
    def pop(self):
        self.context=self.context[:-1]
    def cprint(self, *prints):
        print self.context, ', '.join([str(p) for p in prints])
