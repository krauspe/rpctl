import ScrolledText
import sys
import tkFileDialog
import Tkinter

import subprocess as sub

# Script using /opt/dfs/rpctl/binsim/admin_simulate.s to test/develop output from external command
# outside main app (rpctl)

########################################################################
class RedirectText(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl

    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        self.output.insert(Tkinter.END, string)


########################################################################
class MyApp(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Redirect")
        self.frame = Tkinter.Frame(parent)
        self.frame.pack()

        self.text = ScrolledText.ScrolledText(self.frame)
        self.text.pack()

        # redirect stdout
        self.stdoutOrig = sys.stdout
        self.redir = RedirectText(self.text)
        sys.stdout = self.redir

        # btn = Tkinter.Button(self.frame, text="Open file", command=self.open_file)
        btn = Tkinter.Button(self.frame, text="Open file", command=self.runShell)
        btn.pack()

    #----------------------------------------------------------------------
    # def open_file(self):
    #     """
    #     Open a file, read it line-by-line and print out each line to
    #     the text control widget
    #     """
    #     options = {}
    #     options['defaultextension'] = '.txt'
    #     options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    #     options['initialdir'] = '/home'
    #     options['parent'] = self.root
    #     options['title'] = "Open a file"
    #
    #     with tkFileDialog.askopenfile(mode='r', **options) as f_handle:
    #         for line in f_handle:
    #             print line

    def runShell(self):
            # http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
            #cmd = "cat /etc/HOSTNAME"
            #cmd = "/opt/dfs/tsctl2/bin/admin_get_status_list.sh"
            #print "Running on:\n"
            cmd = "/opt/dfs/rpctl/binsim/admin_simulate.sh"
            opt = ""
            cmd  += "; echo ; echo Done."
            #cmd = "ls -la"

            if opt == "fake":
                print "  running shell command:(FAKE !)"
                print "\n  %s\n" % cmd
            else:
                print "  running shell command:"
                print "\n  %s\n" % cmd

                # p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
                # output, errors = p.communicate()
                # return output, errors

                #p = sub.Popen(cmd, shell=True, stderr=sub.PIPE)

                #self.update_idletasks()

                self.p = sub.Popen(cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
                while True:
                    out = self.p.stdout.read(1)
                    if out == '' and self.p.poll() != None:
                        break
                    if out != '':
                        # self.text += out
                        self.redir.write(out)
                        self.stdoutOrig.write(out)
                while True:
                    err = self.p.stderr.read(1)
                    if err == '' and self.p.poll() != None:
                        break
                    if err != '':
                        # self.err_text += err
                        self.redir.write(err)
                        self.stdoutOrig.write(err)


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("800x600")
    app = MyApp(root)
    root.mainloop()