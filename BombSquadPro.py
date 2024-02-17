# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import _bainternal

if TYPE_CHECKING:
    from typing import Sequence


# ba_meta export plugin
class BSPro(ba.Plugin):
    # def mode(test) -> bool:
    #     return True
    # if _ba.env().get("build_number", 0) >= 20395:
    #     _ba.get_purchased = mode

    def mode(test) -> bool:
        return True
    if _ba.env().get("build_number", 0) >= 20884:
        _bainternal.get_purchased = mode
