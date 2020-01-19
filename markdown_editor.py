import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class Menubar:

    def __init__(self, parent):
        # Font specs
        font_specs = None

        # Defining the menu bar
        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        # File Menu
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label='New...', accelerator='Ctrl+N', command=parent.new_file)
        file_dropdown.add_command(label='Open...', accelerator='Ctrl+O', command=parent.open_file)
        file_dropdown.add_command(label='Append...', accelerator='Ctrl+Shift+A',command=parent.append_to_file)
        file_dropdown.add_command(label='Save', accelerator='Ctrl+S', command=parent.save)
        file_dropdown.add_command(label='Save As...', accelerator='Ctrl+Shift+S', command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit', command=parent.exit_file)

        # Format menu
        format_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Heading sub menu
        heading_menu = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Emphasis sub menu
        emphasis_menu = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Code-block sub menu
        code_block_menu = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Sub-menu to add language syntax
        code_lang = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Sub-menu to add Lists
        lists_menu = tk.Menu(menubar, font=font_specs, tearoff=0)
        sub_lists_menu = tk.Menu(menubar, font=font_specs, tearoff=0)
        # Add Help menu
        help_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)

        # Adding the File and Format menus on the menu bar
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='Format', menu=format_dropdown)
        menubar.add_cascade(label='Help', menu=help_dropdown)

        # Adding Heading sub-menus to Format
        format_dropdown.add_cascade(label='Heading', menu=heading_menu)
        heading_menu.add_command(label='H1', command=parent.heading_1)
        heading_menu.add_command(label='H2', command=parent.heading_2)
        heading_menu.add_command(label='H3', command=parent.heading_3)
        heading_menu.add_command(label='H4', command=parent.heading_4)
        heading_menu.add_command(label='H5', command=parent.heading_5)
        heading_menu.add_command(label='H6', command=parent.heading_6)

        # Adding Emphasis sub-menus to Format
        format_dropdown.add_cascade(label='Emphasis', menu=emphasis_menu)
        emphasis_menu.add_command(label='Bold', accelerator='Ctrl+B', command=parent.make_bold)
        emphasis_menu.add_command(label='Italicize', accelerator='Ctrl+I', command=parent.italicize)
        # Adding Quotes sub-menu to Format
        format_dropdown.add_cascade(label='Quotes', command=parent.add_quotes)

        # Add a seperator
        format_dropdown.add_separator()

        # Adding Hyperlink sub-menu to Format
        format_dropdown.add_cascade(label='Hyperlink', command=parent.hyperlink)

        # Adding Code blocks sub-menus to Format
        format_dropdown.add_cascade(label='Code', menu=code_block_menu)
        code_block_menu.add_command(label='In-line Code', command=parent.code_inline)
        code_block_menu.add_cascade(label='Code Block', menu=code_lang)

        # Adding language syntaxing to code-blocks
        code_lang.add_command(label='No Syntax', command=parent.code_block_no_syntax)
        code_lang.add_command(label='Python', command=parent.code_block_py)
        code_lang.add_command(label='Javascript', command=parent.code_block_js)

        # Add a seperator
        format_dropdown.add_separator()

        # Adding Lists sub-menus to Format
        format_dropdown.add_cascade(label='Lists', menu=lists_menu)
        lists_menu.add_command(label='Numbered', command=parent.numbered_lists)
        lists_menu.add_command(label='Bullets', command=parent.bulleted_lists)
        lists_menu.add_cascade(label='Sub-Lists', menu=sub_lists_menu)
        sub_lists_menu.add_command(label='Numbered', command=parent.numbered_sub_lists)
        sub_lists_menu.add_command(label='Bullets', command=parent.bulleted_sub_lists)

        # Add table sub-menu
        format_dropdown.add_command(label='Add Table', command=parent.fetch_row_columns)

        # Add About sub-menu
        help_dropdown.add_command(label='About', command=parent.show_about)



class Notepad:

    def __init__(self, master):
        master.title('Untitled - WriteMD')
        master.geometry('1200x700')

        font_specs = ('ubuntu mono', 14)

        self.master = master
        self.filename = None

        self.textArea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textArea.yview)
        self.textArea.configure(yscrollcommand=self.scroll.set)
        self.textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.shortcut_keys()

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + ' - Notepad+++')
        else:
            self.master.title('Untitled - Notepad+++')

    def new_file(self, *args):
        self.textArea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title('Untitled - Notepad+++')

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'),
                       ('Text Files', '*.txt'),
                       ('Python Files', '*.py'),
                       ('Markdown Documents', '*.md')]
        )
        if self.filename:
            self.textArea.delete(1.0, tk.END+'-1c')
            with open(self.filename, 'r+') as f:
                self.textArea.insert(1.0, f.read())
            self.set_window_title(self.filename)

    def append_to_file(self, *args):
        text = '\n' + self.textArea.get('1.0', tk.END+'-1c')
        self.filename = filedialog.askopenfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'),
                       ('Text Files', '*.txt'),
                       ('Python Files', '*.py'),
                       ('Markdown Documents', '*.md')]
        )
        if self.filename:
            with open(self.filename, 'a+') as f:
                f.write('\n' + text + '\n')

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textArea.get(1.0, tk.END+'-1c')
                with open(self.filename, 'w+') as f:
                    f.write(textarea_content)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile='Untitled.txt',
                defaultextension='.txt',
                filetypes=[('All Files', '*.*'),
                           ('Text Files', '*.txt'),
                           ('Python Files', '*.py'),
                           ('Markdown Documents', '*.md')]
            )
            textarea_content = self.textArea.get(1.0, tk.END+'-1c')
            with open(new_file, 'w+') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
        except Exception as e:
            print(e)

    def exit_file(self):
        self.master.destroy()

    def heading_1(self):
        self.textArea.insert(tk.SEL_FIRST, '# ')

    def heading_2(self):
        self.textArea.insert(tk.SEL_FIRST, '## ')

    def heading_3(self):
        self.textArea.insert(tk.SEL_FIRST, '### ')

    def heading_4(self):
        self.textArea.insert(tk.SEL_FIRST, '#### ')

    def heading_5(self):
        self.textArea.insert(tk.SEL_FIRST, '##### ')

    def heading_6(self):
        self.textArea.insert(tk.SEL_FIRST, '###### ')

    def make_bold(self, *args):
        self.textArea.insert(tk.SEL_FIRST, '__')
        self.textArea.insert(tk.SEL_LAST, '__')
        self.textArea.tag_add('bold', tk.SEL_FIRST, tk.SEL_LAST)
        self.textArea.tag_config('bold', foreground='red')

    def italicize(self, *args):
        self.textArea.insert(tk.SEL_FIRST, '_')
        self.textArea.insert(tk.SEL_LAST, '_')

    def add_quotes(self, *args):
        li = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST).split('\n')
        li = ['> ' + str(item) for item in li]
        numbered_text = '\n'.join(li)
        self.textArea.insert(tk.SEL_FIRST, numbered_text)
        self.textArea.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def hyperlink(self, *args):
        try:
            text = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            messagebox.showinfo('Selection Error', 'No text selected!')
        else:
            self.input_box = tk.Tk()
            self.input_box.title('Hyperlink')
            self.input_box.geometry('400x100')
            self.label = tk.Label(self.input_box, justify=tk.CENTER, padx=5, text='Add Hyperlink').pack()
            self.input_box.resizable(width=False, height=False)
            font_specs = ('ubuntu mono', 14)
            self.entry = tk.Entry(self.input_box, bd=3, font=font_specs)
            self.entry.config(width=350)
            self.entry.pack(padx=5, pady=5)
            self.button = tk.Button(self.input_box, text='OK', command=self.add_url)
            self.button.config(width=10)
            self.button.pack(side=tk.RIGHT, padx=60, pady=5)
            self.button_cancel = tk.Button(self.input_box, text='Cancel', command=self.input_box.destroy)
            self.button_cancel.config(width=10)
            self.button_cancel.pack(side=tk.RIGHT, padx=60, pady=5)
            self.input_box.mainloop()

    def add_url(self):
        url = self.entry.get()
        self.input_box.destroy()
        self.textArea.insert(tk.SEL_FIRST, '[')
        self.textArea.insert(tk.SEL_LAST, '](' + url + ')')

    def code_block_no_syntax(self):
        self.textArea.insert(tk.SEL_FIRST, '```\n')
        self.textArea.insert(tk.SEL_LAST, '\n```')

    def code_block_py(self):
        self.textArea.insert(tk.SEL_FIRST, '```python\n')
        self.textArea.insert(tk.SEL_LAST, '\n```')

    def code_block_js(self):
        self.textArea.insert(tk.SEL_FIRST, '```javascript\n')
        self.textArea.insert(tk.SEL_LAST, '\n```')

    def code_inline(self):
        self.textArea.insert(tk.SEL_FIRST, '`')
        self.textArea.insert(tk.SEL_LAST, '`')

    def fetch_row_columns(self):
        self.input_box = tk.Tk()
        self.input_box.title('Add Table')
        self.input_box.geometry('200x155')
        self.input_box.resizable(width=False, height=False)
        font_specs = ('ubuntu mono', 14)
        self.row_label = tk.Label(self.input_box, justify=tk.CENTER, padx=5, text='Rows').pack()
        self.entry_row = tk.Entry(self.input_box, bd=3, font=font_specs)
        self.entry_row.config(width=5)
        self.entry_row.pack()
        self.col_label = tk.Label(self.input_box, justify=tk.CENTER, padx=5, text='Columns').pack()
        self.entry_col = tk.Entry(self.input_box, bd=3, font=font_specs)
        self.entry_col.config(width=5)
        self.entry_col.pack()
        tk.Label(self.input_box, justify=tk.CENTER, text='').pack()
        self.button = tk.Button(self.input_box, text='OK', command=self.add_table)
        self.button.config(width=10)
        self.button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.button_cancel = tk.Button(self.input_box, text='Cancel', command=self.input_box.destroy)
        self.button_cancel.config(width=10)
        self.button_cancel.pack(side=tk.RIGHT, padx=10, pady=5)
        self.input_box.mainloop()

    def add_table(self):
        rows = int(self.entry_row.get())
        columns = int(self.entry_col.get())
        self.input_box.destroy()
        header_row = '|'.join([' Header ' for i in range(columns)])
        seperator = '|'.join(['-----' for i in range(columns)])
        main_row_template = '|'.join([' Cell ' for i in range(columns)])
        main_rows = '\n'.join([main_row_template for i in range(rows)])
        table = '\n'.join([header_row, seperator, main_rows]) + '\n'
        self.textArea.insert(tk.INSERT, table)

    def numbered_lists(self):
        li = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST).split('\n')
        li = [str(li.index(item)+1) + '.' + ' ' + str(item) for item in li]
        numbered_text = '\n'.join(li)
        self.textArea.insert(tk.SEL_FIRST, numbered_text)
        self.textArea.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def bulleted_lists(self):
        li = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST).split('\n')
        li = ['- ' + str(item) for item in li]
        numbered_text = '\n'.join(li)
        self.textArea.insert(tk.SEL_FIRST, numbered_text)
        self.textArea.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def numbered_sub_lists(self):
        li = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST).split('\n')
        li = ['  ' + str(li.index(item)+1) + '.' + ' ' + str(item) for item in li]
        numbered_text = '\n'.join(li)
        self.textArea.insert(tk.SEL_FIRST, numbered_text)
        self.textArea.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def bulleted_sub_lists(self):
        li = self.textArea.get(tk.SEL_FIRST, tk.SEL_LAST).split('\n')
        li = ['  - ' + str(item) for item in li]
        numbered_text = '\n'.join(li)
        self.textArea.insert(tk.SEL_FIRST, numbered_text)
        self.textArea.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def show_about(self):
        about_text = 'This is a text editor built using Python and tkinter for updating markdown files.\n\nVersion: 1.0'
        messagebox.showinfo('About', about_text)

    def shortcut_keys(self):
        self.textArea.bind('<Control-n>', self.new_file)
        self.textArea.bind('<Control-o>', self.open_file)
        self.textArea.bind('<Control-A>', self.append_to_file)
        self.textArea.bind('<Control-s>', self.save)
        self.textArea.bind('<Control-S>', self.save_as)
        self.textArea.bind('<Control-b>', self.make_bold)
        self.textArea.bind('<Control-i>', self.italicize)
        self.textArea.bind('<Control-q>', self.add_quotes)
        self.textArea.bind('<Control-h>', self.hyperlink)


if __name__ == '__main__':
    master = tk.Tk()
    notepad = Notepad(master)
    master.mainloop()
