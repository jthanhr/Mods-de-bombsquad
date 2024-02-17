# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba

if TYPE_CHECKING:
    pass


# ba_meta export plugin
class DisableVFXPlugin(ba.Plugin):
    def emitfx(position: Sequence[float],
               velocity: Optional[Sequence[float]] = None,
               count: int = 10,
               scale: float = 1.0,
               spread: float = 1.0,
               chunk_type: str = 'rock',
               emit_type: str = 'chunks',
               tendril_type: str = 'smoke') -> None:
        return None
    ba.emitfx = emitfx
