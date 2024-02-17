# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from bastd.actor.spaz import Spaz
from bastd.ui.popup import PopupWindow

if TYPE_CHECKING:
	from typing import Any, Sequence


lang = ba.app.lang.language
if lang == 'Spanish':
	title_text = 'Tipo de Salud'
	percentage = 'Porcentaje'
	number = 'Número'
	default = 'Por defecto'
else:
	title_text = 'Health Type'
	percentage = 'Percentage'
	number = 'Number'
	default = 'Default'


class NewHealthPopup(PopupWindow):

	def __init__(self):
		uiscale = ba.app.ui.uiscale
		self._transitioning_out = False
		self._width = 420
		self._height = 310
		bg_color = (0.5, 0.4, 0.6)
		scale = (2.2 if uiscale is ba.UIScale.SMALL
			else 1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)

		# creates our _root_widget
		PopupWindow.__init__(self,
							 position=(0.0, 0.0),
							 size=(self._width, self._height),
							 scale=scale,
							 bg_color=bg_color)

		cancel_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(25, self._height - 40),
			size=(50, 50),
			scale=0.75,
			label='',
			color=bg_color,
			on_activate_call=self.cancel,
			autoselect=True,
			icon=ba.gettexture('crossOut'),
			iconscale=1.2)
		ba.containerwidget(edit=self.root_widget,
						   cancel_button=cancel_button)

		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.49, self._height - 25),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=0.9,
			text=title_text,
			color=(1.0, 1.0, 0.0),
			maxwidth=self._width * 0.7)

		posy = 60
		spacing = 75
		self._number_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(self._width * 0.05, self._height * 0.4 + posy),
			size=(380, 75),
			label='',
			on_activate_call=ba.Call(self.change, 'number'),
			autoselect=True)
		self._number_text = ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.23, self._height * 0.522 + posy),
			size=(0, 0),
			h_align='left',
			v_align='center',
			scale=1.0,
			text=number + ' -> 1000',
			color=(1.0, 1.0, 1.0),
			maxwidth=self._width * 0.6)
		self._number_on = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.2, 1.0, 0.2),
			texture=ba.gettexture('circleShadow'))
		self._number_off = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.0, 0.0, 0.0),
			texture=ba.gettexture('circleShadow'))

		posy -= spacing
		self._percentage_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(self._width * 0.05, self._height * 0.4 + posy),
			size=(380, 75),
			label='',
			on_activate_call=ba.Call(self.change, 'percentage'),
			autoselect=True)
		self._percentage_text = ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.23, self._height * 0.522 + posy),
			size=(0, 0),
			h_align='left',
			v_align='center',
			scale=1.0,
			text=percentage + ' -> 100%',
			color=(1.0, 1.0, 1.0),
			maxwidth=self._width * 0.6)
		self._percentage_on = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.2, 1.0, 0.2),
			texture=ba.gettexture('circleShadow'))
		self._percentage_off = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.0, 0.0, 0.0),
			texture=ba.gettexture('circleShadow'))

		posy -= spacing
		self._default_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(self._width * 0.05, self._height * 0.4 + posy),
			size=(380, 75),
			label='',
			on_activate_call=ba.Call(self.change, 'default'),
			autoselect=True)
		self._default_text = ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.23, self._height * 0.522 + posy),
			size=(0, 0),
			h_align='left',
			v_align='center',
			scale=1.0,
			text=default + ' -> []',
			color=(1.0, 1.0, 1.0),
			maxwidth=self._width * 0.6)
		self._default_on = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.2, 1.0, 0.2),
			texture=ba.gettexture('circleShadow'))
		self._default_off = ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.1, self._height * 0.455 + posy),
			size=(40, 40),
			color=(0.0, 0.0, 0.0),
			texture=ba.gettexture('circleShadow'))

		self._update()

	def _update(self) -> None:
		type = ba.app.config['Health Type']
		if type == 'number':
			ba.imagewidget(edit=self._number_on, opacity=1.0)
			ba.imagewidget(edit=self._number_off, opacity=0.0)
			ba.imagewidget(edit=self._percentage_on, opacity=0.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.3)
			ba.imagewidget(edit=self._default_on, opacity=0.0)
			ba.imagewidget(edit=self._default_off, opacity=0.3)
		elif type == 'percentage':
			ba.imagewidget(edit=self._number_on, opacity=0.0)
			ba.imagewidget(edit=self._number_off, opacity=0.3)
			ba.imagewidget(edit=self._percentage_on, opacity=1.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.0)
			ba.imagewidget(edit=self._default_on, opacity=0.0)
			ba.imagewidget(edit=self._default_off, opacity=0.3)
		elif type == 'default':
			ba.imagewidget(edit=self._number_on, opacity=0.0)
			ba.imagewidget(edit=self._number_off, opacity=0.3)
			ba.imagewidget(edit=self._percentage_on, opacity=0.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.3)
			ba.imagewidget(edit=self._default_on, opacity=1.0)
			ba.imagewidget(edit=self._default_off, opacity=0.0)

	def change(self, type: str) -> None:
		if type == 'number':
			ba.imagewidget(edit=self._number_on, opacity=1.0)
			ba.imagewidget(edit=self._number_off, opacity=0.0)
			ba.imagewidget(edit=self._percentage_on, opacity=0.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.3)
			ba.imagewidget(edit=self._default_on, opacity=0.0)
			ba.imagewidget(edit=self._default_off, opacity=0.3)
		elif type == 'percentage':
			ba.imagewidget(edit=self._number_on, opacity=0.0)
			ba.imagewidget(edit=self._number_off, opacity=0.3)
			ba.imagewidget(edit=self._percentage_on, opacity=1.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.0)
			ba.imagewidget(edit=self._default_on, opacity=0.0)
			ba.imagewidget(edit=self._default_off, opacity=0.3)
		elif type == 'default':
			ba.imagewidget(edit=self._number_on, opacity=0.0)
			ba.imagewidget(edit=self._number_off, opacity=0.3)
			ba.imagewidget(edit=self._percentage_on, opacity=0.0)
			ba.imagewidget(edit=self._percentage_off, opacity=0.3)
			ba.imagewidget(edit=self._default_on, opacity=1.0)
			ba.imagewidget(edit=self._default_off, opacity=0.0)
		ba.app.config['Health Type'] = type
		ba.app.config.apply_and_commit()

	def cancel(self) -> None:
		ba.containerwidget(edit=self.root_widget, transition='out_scale')


# ba_meta export plugin
class NewHealthPlugin(ba.Plugin):

	Spaz._old_health_init = Spaz.__init__
	def __health_init__(self,
				 color: Sequence[float] = (1.0, 1.0, 1.0),
				 highlight: Sequence[float] = (0.5, 0.5, 0.5),
				 character: str = 'Spaz',
				 source_player: ba.Player = None,
				 start_invincible: bool = True,
				 can_accept_powerups: bool = True,
				 powerups_expire: bool = False,
				 demo_mode: bool = False):
		self._old_health_init(color,highlight,character,source_player,
					   start_invincible,can_accept_powerups,
					   powerups_expire,demo_mode)
		self.hp: ba.Node = None
		if ba.app.config['Health Type'] in ['number','percentage']:
			hp = ba.newnode('math',
							owner=self.node,
							attrs={
								'input1': (
									0, 1.16, 0) if self.source_player else (
									0, 0.85, 0),
								'operation': 'add'
							})
			self.node.connectattr('torso_position', hp, 'input2')
			self.hp = ba.newnode('text',
								 owner=self.node,
								 attrs={
									'text': '',
									'in_world': True,
									'shadow': 1.0,
									'flatness': 1.0,
									'scale': 0.012,
									'h_align': 'center',
								 })
			hp.connectattr('output', self.hp, 'position')
			ba.animate(self.hp, 'scale', {
				0.0: 0.0,
				0.2: 0.0,
				0.6: 0.022,
				0.8: 0.016})

			def update():
				if self.shield:
					hptext = int(self.shield_hitpoints)
				else:
					hptext = int(self.hitpoints)
				if hptext >= self.hitpoints_max*0.75:
					color = (0.2, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.50:
					color = (1.0, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.25:
					color = (1.0, 0.5, 0.2)
				else:
					color = (1.0, 0.2, 0.2)
				if ba.app.config['Health Type'] == 'number':
					self.hp.text = str(hptext)
				elif ba.app.config['Health Type'] == 'percentage':
					if self.shield:
						hptext = int(self.shield_hitpoints * 100 / (
							self.shield_hitpoints_max))
					else:
						hptext = int(self.hitpoints * 100 / self.hitpoints_max)
					self.hp.text = str(hptext) + '%'
				self.hp.color = (0.2, 1.0, 0.8) if self.shield else color
			ba.timer(0.05, update)


	Spaz.oldhealthequip_shields = Spaz.equip_shields
	def healthequip_shields(self, decay: bool = False) -> None:
		self.oldhealthequip_shields(decay)
		if ba.app.config['Health Type'] in ['number','percentage']:
			def update():
				if self.shield:
					hptext = int(self.shield_hitpoints)
				else:
					hptext = int(self.hitpoints)
				if hptext >= self.hitpoints_max*0.75:
					color = (0.2, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.50:
					color = (1.0, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.25:
					color = (1.0, 0.5, 0.2)
				else:
					color = (1.0, 0.2, 0.2)
				if ba.app.config['Health Type'] == 'number':
					self.hp.text = str(hptext)
				elif ba.app.config['Health Type'] == 'percentage':
					if self.shield:
						hptext = int(self.shield_hitpoints * 100 / (
							self.shield_hitpoints_max))
					else:
						hptext = int(self.hitpoints * 100 / self.hitpoints_max)
					self.hp.text = str(hptext) + '%'
				self.hp.color = (0.2, 1.0, 0.8) if self.shield else color
			ba.timer(0.05, update)


	Spaz.oldhealthshield_decay = Spaz.shield_decay
	def healthshield_decay(self) -> None:
		self.oldhealthshield_decay()
		if ba.app.config['Health Type'] in ['number','percentage']:
			if not self.hp:
				return
			if self.shield:
				hptext = int(self.shield_hitpoints)
			else:
				hptext = int(self.hitpoints)
			if hptext >= self.hitpoints_max*0.75:
				color = (0.2, 1.0, 0.2)
			elif hptext >= self.hitpoints_max*0.50:
				color = (1.0, 1.0, 0.2)
			elif hptext >= self.hitpoints_max*0.25:
				color = (1.0, 0.5, 0.2)
			else:
				color = (1.0, 0.2, 0.2)
			if ba.app.config['Health Type'] == 'number':
				self.hp.text = str(hptext)
			elif ba.app.config['Health Type'] == 'percentage':
				if self.shield:
					hptext = int(self.shield_hitpoints * 100 / (
						self.shield_hitpoints_max))
				else:
					hptext = int(self.hitpoints * 100 / self.hitpoints_max)
				self.hp.text = str(hptext) + '%'
			self.hp.color = (0.2, 1.0, 0.8) if self.shield else color


	Spaz.oldhealthhandlemessage = Spaz.handlemessage
	def healthhandlemessage(self, msg: Any) -> Any:
		if isinstance(msg, ba.HitMessage):
			if not self.node:
				return None
			self.oldhealthhandlemessage(msg)
			if ba.app.config['Health Type'] in ['number','percentage']:
				if not self.hp:
					return
				if self.shield:
					hptext = int(self.shield_hitpoints)
				else:
					hptext = int(self.hitpoints)
				if hptext >= self.hitpoints_max*0.75:
					color = (0.2, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.50:
					color = (1.0, 1.0, 0.2)
				elif hptext >= self.hitpoints_max*0.25:
					color = (1.0, 0.5, 0.2)
				else:
					color = (1.0, 0.2, 0.2)
				if ba.app.config['Health Type'] == 'number':
					self.hp.text = str(hptext)
				elif ba.app.config['Health Type'] == 'percentage':
					if self.shield:
						hptext = int(self.shield_hitpoints * 100 / (
							self.shield_hitpoints_max))
					else:
						hptext = int(self.hitpoints * 100 / self.hitpoints_max)
					self.hp.text = str(hptext) + '%'
				self.hp.color = (0.2, 1.0, 0.8) if self.shield else color
		else:
			return self.oldhealthhandlemessage(msg)

	Spaz.__init__ = __health_init__
	Spaz.equip_shields = healthequip_shields
	Spaz.shield_decay = healthshield_decay
	Spaz.handlemessage = healthhandlemessage

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		NewHealthPopup()

	if 'Health Type' in ba.app.config:
		old_config = ba.app.config['Health Type']
		if not isinstance(old_config, str):
			ba.app.config['Health Type'] = 'percentage'
			ba.app.config.apply_and_commit()
	else:
		ba.app.config['Health Type'] = 'percentage'
		ba.app.config.apply_and_commit()
