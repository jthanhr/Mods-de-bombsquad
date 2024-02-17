# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.actor.spaz import Spaz
from bastd.actor.bomb import Bomb

if TYPE_CHECKING:
	pass


# ba_meta export plugin
class SuperBombMod(ba.Plugin):
	def on_app_running(self) -> None:
		Spaz.oldspazinit = Spaz.__init__
		def spazinit(self, **kwargs):
			self.oldspazinit(**kwargs)
			self.blast_radius = 4
		Spaz.__init__ = spazinit

		Bomb.oldbombinit = Bomb.__init__
		def bombinit(self, **kwargs):
			self.oldbombinit(**kwargs)
			self.super_bomb_light = ba.newnode(
				'light',
				owner=self.node,
				attrs={'radius': 0.2,
					'color': (1, 0, 0),
					'intensity': 0.5
				})
			self.super_bomb_shield = ba.newnode(
				'shield',
				owner=self.node,
				attrs={
					'color': (1, 0, 0),
					'radius': 0.8
				})
			self.node.connectattr('position', self.super_bomb_light, 'position')
			self.node.connectattr('position', self.super_bomb_shield, 'position')
		Bomb.__init__ = bombinit