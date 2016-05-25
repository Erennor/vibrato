from debug import print_debug
import shelve
class Handler:
    """database controller, also handle commands"""
    def __init__(self, microInput,ls):
        print("[DEBUG] : INIT")
        self.learn = True
        self.ls = ls
        self.scripts = []
        self.links = dict()
        self.recordLabel = 42
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

    def learn_hit(self,id):
        self.recordLabel = id
        self.learn = True

    def delete_hit(self,hit):
        print_debug("deleting hit "+ str(hit))
        self.links.pop(hit)
        for i in range(0,ls['META']):
            if ls["micro" + str(i)][1] == hit:
                ls.pop("micro" + str(i))
                return
        print("[DEBUG] : hit not found on database")

    def handle_cmd(self, cmd):
        try:
            if cmd[0] == "d":
                self.delete_hit(int(cmd[2:]))
            elif cmd[0] == "c":
                self.learn_hit(int(cmd[2:]))
                # TODO : create a hit
            elif cmd[0] == "l":
                cmd_list = cmd.split(str="_")
                self.link(cmd_list[1],cmd_list[2])
        except:
            print_debug("Error parsing command " + str(cmd))
    def tell_me_more(self):
        print_debug("tell_me_more:")
        print_debug("scripts repertories:")
        for elt in scripts:
            print_debug("\t" + str(elt))
        print_debug("liaisons hit/scripts:")
        for key,elt in links.items:
            print_debug("\t" + str(key)+ " --> " + str(elt))

if __name__ == "__main__":
    """ print database ( *.db ) """
    biblio = 'new_sample.db'
    ls = shelve.open(biblio, writeback=True)
    print(ls)
    ls.close()
