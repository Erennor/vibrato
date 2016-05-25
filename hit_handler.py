from machineLearning import ls


class Handler:
    def __init__(self, microInput):
        print("[DEBUG] : INIT")
        self.scripts = []
        self.links = dict()
        self.microInput = microInput

    def handle_hit(self, hit):
        print("[DEBUG] : handle HIT")
        print("hit=" + str(hit))
        script = self.links.get(hit)

    def link(self, hit, script):
        print("[DEBUG] : link")
        self.links[hit] = script

    def execute(self,script):
        print("[DEBUG] : execute")

    def delete_hit(self,hit):
        print("[DEBUG] : delete HIT")
        self.links.pop(hit)
        for i in range(0,ls['META']):
            if ls["micro" + str(i)][1] == hit:
                ls.pop("micro" + str(i))
                return
        print("[DEBUG] : hit not found on database")

    def handle_cmd(self, cmd):
        print("[DEBUG] : handle cmd")
        cmd_list = cmd.split(cmd)
        if cmd_list[0] == "del":
            self.delete_hit(cmd_list[1])
        if cmd_list[0] == "learn":
            global learn
            learn = True
        else:
            print(cmd)
