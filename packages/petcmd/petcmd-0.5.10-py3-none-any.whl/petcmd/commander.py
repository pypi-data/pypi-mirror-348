
import os
import sys
import traceback
from typing import Callable, Optional, Iterable

from petcmd.argparser import ArgParser
from petcmd.command import Command
from petcmd.exceptions import CommandException
from petcmd.interface import Interface
from petcmd.utils import validate_type_hints, shell_complete_t
from petcmd.autocompletion.zsh import ZSH_AUTOCOMPLETE_TEMPLATE

class Commander:

	def __init__(self, error_handler: Callable[[Exception], None] = None,
			compact_commands_list: bool = False,
			autocomplete_description: bool = True):
		self.error_handler = error_handler
		self.compact_commands_list = compact_commands_list
		self.autocomplete_description = autocomplete_description
		self.__commands: list[Command] = []
		self.__completion_commands = ["show-shell-completion", "setup-shell-completion",
			"remove-shell-completion", "setup-zshrc-for-completion", "help-completion"]

		@self.command("help", shell_complete={"command": lambda: sum([c.cmds for c in self.__commands], ())})
		def help_command(command: str = None):
			"""
			Show a help message or usage message when a command is specified.

			:param command: Command for which instructions for use will be displayed.
			"""
			self.__help_command(command)

		@self.command("help-completion")
		def help_completion():
			"""Show a help message for completion commands."""
			Interface.commands_list([c for c in self.__commands if c.cmds[0] in self.__completion_commands])

		@self.command("setup-shell-completion")
		def setup_shell_completion(alias: str = None):
			"""
			Set up a shell completion script for the current cli tool.
			Save it to ~/.zsh/completions/_alias.

			:param alias:   Alias for the cli tool completion.
							If not specified, the name of the current script is used.
			"""
			if alias is None:
				alias = os.path.basename(sys.argv[0])
			completions = os.path.join(os.path.expanduser("~"), ".zsh", "completions")
			os.makedirs(completions, exist_ok=True)
			with open(os.path.join(completions, f"_{alias}"), "w") as f:
				f.write(ZSH_AUTOCOMPLETE_TEMPLATE.format(alias=alias))
			print(f"Shell completion script for {alias} has been saved to {completions}. Restart terminal to load it.")

		@self.command("remove-shell-completion")
		def remove_shell_completion(alias: str = None):
			"""
			Remove a shell completion script for the current cli tool.
			Search it in ~/.zsh/completions/_alias.

			:param alias:   Alias for the cli tool completion.
							If not specified, the name of the current script is used.
			"""
			os.remove(os.path.join(os.path.expanduser("~"), ".zsh", "completions", f"_{alias}"))

		@self.command("setup-zshrc-for-completion")
		def setup_zshrc_for_completion():
			"""Fill ~/.zshrc with commands to enable shell completion for zsh with ~/.zsh/completions/* files."""
			home = os.path.expanduser("~")
			zshrc = os.path.join(home, ".zshrc")
			completions = os.path.join(home, ".zsh", "completions")
			if not os.path.exists(zshrc):
				with open(zshrc, "w") as f:
					f.write("")
			with open(zshrc, "r") as f:
				content = f.read()
			commands = [
				f"fpath=({completions} $fpath)",
				"autoload -Uz compinit",
				"compinit",
				"zstyle ':completion:*:petcmd' sort false"
			]
			with open(zshrc, "a") as f:
				if any(command not in content for command in commands):
					f.write("\n")
				for command in commands:
					if command not in content:
						f.write(f"{command}\n")

	def command(self, *cmds: str, shell_complete: shell_complete_t = None):
		def dec(func: Callable) -> Callable:
			self.add_command(cmds, func, shell_complete)
			return func
		return dec

	def add_command(self, cmds: str | Iterable[str], func: Callable, shell_complete: shell_complete_t = None):
		cmds = (cmds,) if isinstance(cmds, str) else cmds
		shell_complete = shell_complete if isinstance(shell_complete, dict) else {}
		for command in self.__commands:
			if command.match(cmds):
				raise CommandException(f"Duplicated command: {", ".join(cmds)}")
		validate_type_hints(func, shell_complete)
		self.__commands.append(Command(cmds, func, shell_complete))

	def process(self, argv: list[str] = None):
		if argv is None:
			argv = sys.argv[1:]

		if len(argv) > 0 and argv[0] == "--shell-completion":
			try:
				if len(argv) == 3:
					self.__print_commands()
				elif command := self.__find_command(argv[2]):
					ArgParser(argv[3:], command).autocomplete(int(argv[1]) - 1, self.autocomplete_description)
			except Exception: pass
			return

		command = self.__find_command(argv[0] if len(argv) > 0 else "help")
		if command is None:
			print(f"\nUnknown command '{argv[0]}'")
			self.__help_command()
			return

		try:
			args, kwargs = ArgParser(argv[1:], command).parse()
			command.func(*args, **kwargs)
		except CommandException as e:
			print("\n" + str(e))
			Interface.command_usage(command)
		except Exception as e:
			if isinstance(self.__error_handler, Callable):
				self.__error_handler(e)
			else:
				print("\n" + traceback.format_exc())

	def __find_command(self, cmd: str) -> Optional[Command]:
		for command in self.__commands:
			if command.match(cmd):
				return command

	def __print_commands(self):
		for command in self.__commands:
			for synonym in command.cmds:
				print(synonym)

	def __help_command(self, cmd: str = None):
		if cmd and (command := self.__find_command(cmd)):
			Interface.command_usage(command)
			return
		Interface.commands_list([c for c in self.__commands if c.cmds[0] not in self.__completion_commands],
			self.__compact_commands_list)
