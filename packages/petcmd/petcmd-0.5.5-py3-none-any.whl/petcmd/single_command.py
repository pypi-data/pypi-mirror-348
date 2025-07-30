
import sys
import traceback
from typing import Callable

from petcmd.argparser import ArgParser
from petcmd.command import Command
from petcmd.exceptions import CommandException
from petcmd.interface import Interface
from petcmd.utils import validate_type_hints, shell_complete_t

class SingleCommand:

	def __init__(self, error_handler: Callable[[Exception], None] = None):
		self.__error_handler = error_handler
		self.__command = None

	def use(self, shell_complete: shell_complete_t = None):
		shell_complete = shell_complete if isinstance(shell_complete, dict) else {}
		def dec(func: Callable) -> Callable:
			if self.__command is not None:
				raise CommandException("You can't use more than one command with SingleCommand")
			validate_type_hints(func, shell_complete)
			self.__command = Command(("__main__",), func, shell_complete)
			return func
		return dec

	def process(self, argv: list[str] = None):
		if argv is None:
			argv = sys.argv[1:]

		if len(argv) == 1 and argv[0] in ("--help", "-help", "-h", "--h"):
			Interface.command_usage(self.__command)
			return
		elif len(argv) > 0 and argv[0] == "--shell-completion":
			try: ArgParser(argv[2:], self.__command).autocomplete(int(argv[1]))
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
