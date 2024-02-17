# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.ui import popup
from bastd.actor.spaz import Spaz

if TYPE_CHECKING:
	from typing import Any


class CustomLang:
	lang = ba.app.lang.language
	if lang == 'Spanish':
		title = 'Eliminación Épica'
		time = 'Tiempo Épico'
		enable = 'Habilitar'
		slowest = 'Más Lento'
		slow = 'Lento'
		normal = 'Normal'
		fast = 'Rápido'
		faster = 'Más Rápido'
	else:
		title = 'Epic Elimination'
		time = 'Epic Time'
		enable = 'Enable'
		slowest = 'Slowest'
		slow = 'Slow'
		normal = 'Normal'
		fast = 'Fast'
		faster = 'Faster'


class EpicEliminationPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = ba.app.ui.uiscale
		self._transitioning_out = False
		self._width = 400
		self._height = 220
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			position=(0.0, 0.0),
			size=(self._width, self._height),
			scale=2.4 if uiscale is ba.UIScale.SMALL else 1.2,
			bg_color=bg_color)

		self._cancel_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(25, self._height - 40),
			size=(50, 50),
			scale=0.58,
			label='',
			color=bg_color,
			on_activate_call=self._on_cancel_press,
			autoselect=True,
			icon=ba.gettexture('crossOut'),
			iconscale=1.2)
		ba.containerwidget(edit=self.root_widget,
						   cancel_button=self._cancel_button)

		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height - 27),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=0.8,
			text=CustomLang.title,
			maxwidth=self._width * 0.7,
			color=ba.app.ui.title_color)

		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.265, self._height * 0.295 + 60),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=CustomLang.time,
			maxwidth=150,
			color=(0.8, 0.8, 0.8, 1.0))

		popup.PopupMenu(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height * 0.18 + 60),
			width=150,
			scale=2.8 if uiscale is ba.UIScale.SMALL else 1.3,
			choices=['slowest', 'slow', 'normal', 'fast', 'faster'],
			choices_display=[
				ba.Lstr(value=CustomLang.slowest),
				ba.Lstr(value=CustomLang.slow),
				ba.Lstr(value=CustomLang.normal),
				ba.Lstr(value=CustomLang.fast),
				ba.Lstr(value=CustomLang.faster),
			],
			current_choice=ba.app.config['Epic Elimination']['time'],
			on_value_change_call=self._set_time,
		)

		ba.checkboxwidget(
			parent=self.root_widget,
			position=(self._width * 0.28, self._height * 0.18),
			size=(self._width * 0.48, 50),
			autoselect=True,
			maxwidth=self._width * 0.3,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=ba.app.config['Epic Elimination']['enable'],
			text=CustomLang.enable,
			on_value_change_call=self.change_enable,
		)

	def _set_time(self, val: str) -> None:
		cfg = ba.app.config
		cfg['Epic Elimination']['time'] = val
		cfg.apply_and_commit()

	def change_enable(self, val: bool) -> None:
		cfg = ba.app.config
		cfg['Epic Elimination']['enable'] = val
		cfg.apply_and_commit()

	def _on_cancel_press(self) -> None:
		self._transition_out()

	def _transition_out(self) -> None:
		if not self._transitioning_out:
			self._transitioning_out = True
			ba.containerwidget(edit=self.root_widget, transition='out_scale')

	def on_popup_cancel(self) -> None:
		ba.playsound(ba.getsound('swish'))
		self._transition_out()


# ba_meta export plugin
class EpicEliminationPlugin(ba.Plugin):
	def on_app_running(self) -> None:
		if not 'Epic Elimination' in ba.app.config:
			epic_elimination_list = {
				'enable': True,
				'time': 'normal',
			}
			ba.app.config['Epic Elimination'] = epic_elimination_list
			ba.app.config.apply_and_commit()
		Spaz.oldhandlemessage = Spaz.handlemessage
		def handlemessage(self, msg: Any) -> Any:
			if isinstance(msg, ba.DieMessage):
				self.oldhandlemessage(msg)
				if not self.node:
					return
				if ba.app.config['Epic Elimination']['enable']:
					glb = ba.getactivity().globalsnode
					def normal():
						glb.slow_motion = False
					glb.slow_motion = True
					cfgtime = ba.app.config['Epic Elimination']['time']
					if cfgtime == 'slowest':
						time = 1.0
					elif cfgtime == 'slow':
						time = 0.8
					elif cfgtime == 'normal':
						time = 0.6
					elif cfgtime == 'fast':
						time = 0.4
					else:
						time = 0.2
					ba.timer(time, normal)
			else:
				self.oldhandlemessage(msg)
		Spaz.handlemessage = handlemessage

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		EpicEliminationPopup()
