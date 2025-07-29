import abc
from dataclasses import dataclass

import hikari


@dataclass(kw_only=True)
class Choice:
	display_name: str
	value: str

	description: str | None = None
	emoji: hikari.Emoji | None = None


@dataclass(kw_only=True)
class Setting(abc.ABC):
	name: str

	display_name: str
	emoji: hikari.Emoji | None = None

	choices: tuple[Choice]
	"""When empty, a text input will be used."""

	def default(self) -> str:
		raise NotImplementedError

	def set(self, value: str) -> None:
		raise NotImplementedError

	def get(self) -> str:
		raise NotImplementedError
