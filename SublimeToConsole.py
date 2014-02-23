import sublime, sublime_plugin, subprocess

settings = {}

class SublimeToConsoleCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global settings
    settings = sublime.load_settings('SublimeToConsole.sublime-settings')
    prog = settings.get('program')

    line = self.get_current_file_name_and_line_number()
    command = "bundle exec rspec " + line
    print("Executing in " + prog + ": '" + command + "'")
    SublimeToConsoleCommand.send(prog, command)

  def get_current_file_name_and_line_number(self):
    return self.get_current_file_name() + ':' + str(self.get_current_line_number())

  def get_current_file_name(self):
    return self.view.file_name()

  def get_current_line_number(self):
    char_under_cursor = self.view.sel()[0].begin()
    line_number = self.view.rowcol(char_under_cursor)[0] + 1
    return line_number

  @staticmethod
  def send(prog, command):
    
    # Terminal.app
    if prog == "Terminal.app":
      subprocess.call(['osascript', '-e',
        'tell app "Terminal" to do script "' + command + '" in window 1'])

    # iTerm
    if prog == "iTerm":
      subprocess.call(['osascript', '-e', 'tell app "iTerm"',
        '-e', 'set mysession to current session of current terminal',
        '-e', 'tell mysession to write text "' + command + '"',
        '-e', 'end tell'])