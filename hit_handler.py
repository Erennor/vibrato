from debug import print_debug
from subprocess import call
import shelve
class Handler:
    """database controller, also handle commands"""
    def __init__(self, microInput,ls):
        print("[DEBUG] : INIT")
        self.learn = False
        self.ls = ls
        self.links = dict()
        self.recordLabel = 42
        self.microInput = microInput

    def handle_hit(self, hit):
        print("[DEBUG] : handle HIT")
        print("hit=" + str(hit))
        if self.ls['links'].has_key(hit):
            script = self.ls['links'][hit]
            self.execute(script)

    def link(self, hit, script):
        print("[DEBUG] : link")
        self.ls['links'][hit] = script

    def execute(self,script):
        print("[DEBUG] : execute")
        # La ligne de code la plus sale que j'ai jamais ecrite je dois avouer
        call(["python2.7", "onAction/"+script+".py"])


    def learn_hit(self,id):
        self.recordLabel = id
        self.learn = True

    def delete_hit(self,hit):
        print_debug("deleting hit "+ str(hit))
        try:
            index = self.ls['labels'].index(hit)
            self.ls['samples'].pop(index)
            self.ls['labels'].pop(index)
        except Exception, e:
            print("[DEBUG] : hit not found on database")
        else:
            pass
        finally:
            try:
                self.ls['links'].pop(hit)
            except:
                pass

    def handle_cmd(self, cmd):
        print("[DEBUG] : handle_cmd " + cmd)
        try:
            if cmd[0] == "d":
                self.delete_hit(int(cmd[2:]))
            elif cmd[0] == "c":
                self.learn_hit(int(cmd[2:]))
            elif cmd[0] == "l":
                print_debug("Link called on " + cmd)
                cmd_list = cmd.split("_")
                print(cmd_list)
                print_debug("Link called on " )
                self.link(int(cmd_list[1]),cmd_list[2])
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
