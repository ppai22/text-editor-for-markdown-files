import cx_Freeze


base = None

executables = [cx_Freeze.Executable('markdown_editor.py', base=base)]

cx_Freeze.setup(
    name='WriteMD',
    version='0.1',
    description='A text editor built using Python and tkinter for editing Markdown files',
    executables=executables
)
