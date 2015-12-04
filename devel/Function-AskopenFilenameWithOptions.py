    ----------------------------------------------------------------------
    def open_file(self):
        """
        Open a file, read it line-by-line and print out each line
        """
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = '/home'
        options['parent'] = self.root
        options['title'] = "Open a file"

        with tkFileDialog.askopenfile(mode='r', **options) as f_handle:
            for line in f_handle:
                print line
