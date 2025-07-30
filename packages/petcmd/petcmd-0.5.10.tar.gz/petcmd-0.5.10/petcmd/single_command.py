import os
import sys
import traceback
from typing import Callable

from petcmd.argparser import ArgParser
from petcmd.autocompletion.zsh import ZSH_AUTOCOMPLETE_TEMPLATE
from petcmd.command import Command
from petcmd.exceptions import CommandException
from petcmd.interface import Interface
from petcmd.utils import validate_type_hints, shell_complete_t

class SingleCommand:

	def __init__(self, error_handler: Callable[[Exception], None] = None, autocomplete_description: bool = True):
		self.error_handler = error_handler
		self.autocomplete_description = autocomplete_description
		self.__command = None

	def use(self, shell_complete: shell_complete_t = None):
		def dec(func: Callable) -> Callable:
			self.register_command(func, shell_complete)
			return func
		return dec

	def register_command(self, func: Callable, shell_complete: shell_complete_t = None):
		shell_complete = shell_complete if isinstance(shell_complete, dict) else {}
		if self.__command is not None:
			raise CommandException("You can't use more than one command with SingleCommand")
		validate_type_hints(func, shell_complete)
		self.__command = Command(("__main__",), func, shell_complete)

	def process(self, argv: list[str] = None):
		if argv is None:
			argv = sys.argv[1:]

		if len(argv) == 1 and argv[0] in ("--help", "-help", "-h", "--h"):
			Interface.command_usage(self.__command)
			return
		elif len(argv) >= 1 and argv[0] == "--setup-shell-completion":
			alias = os.path.basename(sys.argv[0]) if len(argv) == 1 else argv[1]
			completions = os.path.join(os.path.expanduser("~"), ".zsh", "completions")
			os.makedirs(completions, exist_ok=True)
			with open(os.path.join(completions, f"_{alias}"), "w") as f:
				f.write(ZSH_AUTOCOMPLETE_TEMPLATE.format(alias=alias))
			print(f"Shell completion script for {alias} has been saved to {completions}. Restart terminal to load it.")
			return
		elif len(argv) >= 1 and argv[0] == "--remove-shell-completion":
			alias = os.path.basename(sys.argv[0]) if len(argv) == 1 else argv[1]
			os.remove(os.path.join(os.path.expanduser("~"), ".zsh", "completions", f"_{alias}"))
			return
		elif len(argv) >= 1 and argv[0] == "--setup-zshrc-for-completion":
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
			return
		elif len(argv) >= 1 and argv[0] == "--shell-completion":
			try: ArgParser(argv[2:], self.__command).autocomplete(int(argv[1]), self.autocomplete_description)
			except Exception: pass
			return

		try:
			args, kwargs = ArgParser(argv, self.__command).parse()
			self.__command.func(*args, **kwargs)
		except CommandException as e:
			print("\n" + str(e))
			Interface.command_usage(self.__command)
		except Exception as e:
			if isinstance(self.__error_handler, Callable):
				self.__error_handler(e)
			else:
				print("\n" + traceback.format_exc())
