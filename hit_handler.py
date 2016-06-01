from debug import print_debug
from subprocess import call
import shelve
from openhab import *
class Handler:
    """database controller, also handle commands"""
    def __init__(self, microInput,ls):
        print("[DEBUG] : INIT")
        self.learn = False
        self.ls = ls
        self.recordLabel = 42
        self.microInput = microInput
        self.openHab = OpenHab()

    def handle_hit(self, hitId):
        print_debug("handle hit " + hitId)
        # openhab.post_command(scriptListener,hitId)
        self.openHab.post_command("scriptListener",hitId)
        # TODO : send hit data back to openHab

    def learn_hit(self,hitId):
        self.recordLabel = hitId
        self.learn = True

    def delete_hit(self,hitId):
        print_debug("deleting hit "+ hitId)
        try:
            index = self.ls['labels'].index(hitId)
            self.ls['samples'].pop(index)
            self.ls['labels'].pop(index)
        except Exception, e:
            print("[DEBUG] : hit not found on database")

    def handle_cmd(self, cmd):
        print("[DEBUG] : handle_cmd " + cmd)
        try:
            if cmd[0] == "d":
                self.delete_hit(cmd[2:])
            elif cmd[0] == "c":
                self.learn_hit(cmd[2:])
        except:
            print_debug("Error parsing command " + str(cmd))

if __name__ == "__main__":
    """ print database ( *.db ) """
    biblio = 'new_sample.db'
    ls = shelve.open(biblio, writeback=True)
    print(ls)
    ls.close()
