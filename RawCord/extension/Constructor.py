from .Functionals import InvalidArguments

class Embed:
    def __init__(self,title=None,description=None,colour=None):
        if title==None and description==None:
            raise InvalidArguments("<title> and <description> cannot be empty")
            return
            self.title = title
        self.description = description
        self.colour = colour
        self.raw = {"title":title,"description":description,"color":colour}

    def add_field(self,name=None,value=None,inline=True):
        if name==None and value==None:
            raise InvalidArguments("<name> and <value> cannot be empty")
            return
        elif type(name)!=str and type(value)!=str:
            raise InvalidArguments("<name> and <value> have to be type <str>")
            return
        elif type(inline) != bool:
            raise InvalidArguments(f"<inline> must be type <bool> not type <{type(inline)}>")
            return
        if "fields" not in self.raw:
            self.raw["fields"] = []
        self.raw["fields"].append({"name":name,"value":value,"inline":inline})
