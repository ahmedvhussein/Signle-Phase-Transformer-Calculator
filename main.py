# -*- coding: utf-8 -*-
import sys
import math
from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
	QLineEdit, QPushButton, QTabWidget, QFormLayout, QMessageBox,
	QHBoxLayout, QGroupBox, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt


class InputPage(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		# Main vertical layout
		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(5, 5, 5, 5)
		main_layout.setSpacing(5)

		# Header (centered)
		head = QLabel('SINGLE PHASE TRANSFORMER CALCULATOR')
		head_font = QFont()
		head_font.setPointSize(10)
		head_font.setBold(True)
		head.setFont(head_font)
		head.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(head)

		# Subtitle
		sub = QLabel('Provide all given values to obtain transformer characteristics')
		sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(sub)

		# Note in smaller red font
		note = QLabel("*Note: only step-down voltage permitted")
		note_font = QFont()
		note_font.setPointSize(9)
		note.setFont(note_font)
		note.setStyleSheet('color: red;')
		note.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(note)

		# Horizontal section: left inputs, right image placeholder
		hbox = QHBoxLayout()

		# Left: grouped input fields
		left_group = QGroupBox()
		left_layout = QVBoxLayout()

		# Basic inputs form
		form = QFormLayout()
		form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
		form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		form.setHorizontalSpacing(5)
		form.setVerticalSpacing(3)
		self.power_rating = QLineEdit()
		self.primary_voltage = QLineEdit()
		self.secondary_voltage = QLineEdit()
		form.addRow('Power Rating, S (VA):', self.power_rating)
		form.addRow('Primary Voltage, V1 (V):', self.primary_voltage)
		form.addRow('Secondary Voltage, V2 (V):', self.secondary_voltage)
		# Power factor and phase angle displays (computed from short-circuit test)
		self.pf_display = QLabel('')
		self.pf_display.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 4px;')
		self.pf_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
		form.addRow('Power Factor, cos(θ):', self.pf_display)
		self.phase_display = QLabel('')
		self.phase_display.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 4px;')
		self.phase_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
		form.addRow('Phase Angle, θ (°):', self.phase_display)
		# Open circuit test group
		open_group = QGroupBox('Open Circuit Test')
		open_form = QFormLayout()
		open_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
		open_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		open_form.setHorizontalSpacing(5)
		open_form.setVerticalSpacing(3)
		self.voc = QLineEdit()
		self.ioc = QLineEdit()
		self.poc = QLineEdit()
		open_form.addRow('Voltage, Voc (V):', self.voc)
		open_form.addRow('Current, Ioc (A):', self.ioc)
		open_form.addRow('Power, Poc (W):', self.poc)
		open_group.setLayout(open_form)

		# Short circuit test group
		short_group = QGroupBox('Short Circuit Test')
		short_form = QFormLayout()
		short_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
		short_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		short_form.setHorizontalSpacing(5)
		short_form.setVerticalSpacing(3)
		self.vsc = QLineEdit()
		self.isc = QLineEdit()
		self.psc = QLineEdit()
		short_form.addRow('Voltage, Vsc (V):', self.vsc)
		short_form.addRow('Current, Isc (A):', self.isc)
		short_form.addRow('Power, Psc (W):', self.psc)
		short_group.setLayout(short_form)

		left_layout.addLayout(form)
		left_layout.addWidget(open_group)
		left_layout.addWidget(short_group)

		# Transformer ratio (computed, display-only)
		self.ratio_display = QLabel('')
		# Make it look like a disabled text field (gray background)
		self.ratio_display.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 4px;')
		self.ratio_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.ratio_display.setMinimumWidth(150)
		ratio_h = QHBoxLayout()
		ratio_label = QLabel('Turns of Ratio, a = N1/N2:')
		ratio_label.setMinimumWidth(200)
		ratio_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		ratio_h.addWidget(ratio_label)
		ratio_h.addWidget(self.ratio_display)
		ratio_h.addStretch()
		left_layout.addLayout(ratio_h)
		left_group.setLayout(left_layout)
		hbox.addWidget(left_group, 2)

		# Right: image
		right_group = QGroupBox()
		right_layout = QVBoxLayout()
		self.image_label = QLabel()
		pixmap = QPixmap('img1.jpeg')
		if not pixmap.isNull():
			scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			self.image_label.setPixmap(scaled_pixmap)
		else:
			self.image_label.setText('Image not found')
		self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.image_label.setStyleSheet('border: 1px solid #ccc;')
		self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		right_layout.addWidget(self.image_label)
		right_group.setLayout(right_layout)
		hbox.addWidget(right_group, 1)

		main_layout.addLayout(hbox)

		# Calculate button
		calc_btn = QPushButton('Calculate')
		calc_btn.clicked.connect(self.calculate)
		calc_btn.setFixedWidth(120)
		calc_btn.setStyleSheet('font-weight: bold;')
		# center button
		btn_box = QHBoxLayout()
		btn_box.addStretch()
		btn_box.addWidget(calc_btn)
		btn_box.addStretch()
		main_layout.addLayout(btn_box)

		self.setLayout(main_layout)

	def calculate(self):
		"""Main calculation method that validates inputs and computes all transformer parameters."""
		print("\n=== CALCULATE BUTTON CLICKED ===")
		# Validate and parse all input fields
		try:
			power = float(self.power_rating.text())
			print(f"Power: {power}")
			print(f"Power: {power}")
			vp = float(self.primary_voltage.text())
			print(f"Primary Voltage: {vp}")
			vs = float(self.secondary_voltage.text())
			voc = float(self.voc.text())
			ioc = float(self.ioc.text())
			poc = float(self.poc.text())
			vsc = float(self.vsc.text())
			isc = float(self.isc.text())
			psc = float(self.psc.text())
		except ValueError:
			QMessageBox.warning(self, 'Input Error', 'Please ensure all fields are numeric and not empty.')
			return

		# Validate step-down configuration
		if vs > vp:
			QMessageBox.warning(self, 'Configuration Error', 'Only step-down transformers are permitted (Vs ≤ Vp).')
			return

		# Calculate transformer turns ratio: a = N1/N2 = Vp/Vs
		if vs == 0:
			QMessageBox.warning(self, 'Calculation Error', 'Secondary voltage cannot be zero.')
			return
		turns_ratio = vp / vs
		
		# Display transformer turns ratio
		self.ratio_display.setText(f"{turns_ratio:.2f}")

		# SHORT-CIRCUIT TEST: Compute series impedance parameters
		# Power factor: PF_sc = P_sc / (V_sc * I_sc)
		if vsc * isc == 0:
			QMessageBox.warning(self, 'Calculation Error', 'Vsc and Isc must be non-zero to compute power factor.')
			return
		pf_sc = psc / (vsc * isc)
		pf_sc_clamped = max(-1.0, min(1.0, pf_sc))
		theta_sc_rad = math.acos(pf_sc_clamped)
		theta_sc_deg = math.degrees(theta_sc_rad)
		
		# Update power factor and phase angle displays
		self.pf_display.setText(f"{pf_sc:.2f}")
		self.phase_display.setText(f"{theta_sc_deg:.2f}")

		a_squared = turns_ratio ** 2

		# |Z_eq| = V_sc / I_sc
		z_eq_mag = vsc / isc
		
		# R_eq = P_sc / I_sc^2
		r_eq = psc / (isc ** 2)
		
		# X_eq = sqrt(|Z_eq|^2 - R_eq^2)
		x_eq_sq = z_eq_mag ** 2 - r_eq ** 2
		if x_eq_sq < 0:
			QMessageBox.warning(self, 'Calculation Warning', 
							   'Inconsistent impedance values detected. Setting X_eq to zero.')
			x_eq = 0.0
		else:
			x_eq = math.sqrt(x_eq_sq)

		# Z_eq in polar form
		z_eq_polar = f"{z_eq_mag:.2f} ∠ {theta_sc_deg:.2f}°"

		# OPEN-CIRCUIT TEST: Compute excitation branch parameters
		# Y_Ï• magnitude: |Y_Ï•| = I_oc / V_oc
		if voc == 0:
			QMessageBox.warning(self, 'Calculation Error', 'Voc cannot be zero.')
			return
		y_phi_mag = a_squared * ioc / voc
		
		# Power factor (open-circuit): PF_oc = P_oc / (V_oc * I_oc)
		if voc * ioc == 0:
			QMessageBox.warning(self, 'Calculation Error', 'Voc and Ioc must be non-zero.')
			return
		pf_oc = poc / (voc * ioc)
		pf_oc_clamped = max(-1.0, min(1.0, pf_oc))
		theta_oc_rad = math.acos(pf_oc_clamped)
		theta_oc_deg = math.degrees(theta_oc_rad)

		# G_φ = |Y_φ| * cos(θ_oc)
		g_phi = abs(y_phi_mag) * math.cos(-theta_oc_rad)
		
		# B_Ï• = |Y_Ï•| * sin(θ_oc)
		b_phi = y_phi_mag * math.sin(-theta_oc_rad)
		
		# R_c = 1 / G_Ï•
		r_c = (a_squared **2) * (1.0 / g_phi) if g_phi > 1e-12 else None
		
		# X_m = 1 / |B_Ï•|
		x_m = (a_squared **2) * (1.0 / abs(b_phi)) if abs(b_phi) > 1e-12 else None

		# Format Z_Ï• as rectangular form
		z_phi_rect = None
		if r_c is not None and x_m is not None:
			z_phi_rect = f"{r_c:.2f} + j{x_m:.2f} Ω"

		# REFERRED PARAMETERS: Calculate secondary-side values using turns ratio
		# Z_eq2 = Z_eq1 / a^2 (impedances divide by a² when referred to secondary)
		
		z_eq_mag_sec = z_eq_mag / a_squared
		r_eq_sec = r_eq / a_squared
		x_eq_sec = x_eq / a_squared
		z_eq_polar_sec = f"{z_eq_mag_sec:.4f} ∠ {theta_sc_deg:.4f}°"

		# Y_φ2, G_φ2, B_φ2 (admittances multiply by a² when referred to secondary)
		y_phi_mag_sec = y_phi_mag / a_squared
		g_phi_sec = g_phi / a_squared
		b_phi_sec = b_phi / a_squared
		
		# R_c2, X_m2 (impedances divide by a² when referred to secondary)
		r_c_sec = (r_c / a_squared) if r_c is not None else None
		x_m_sec = (x_m / a_squared) if x_m is not None else None
		z_phi_rect_sec = None
		if r_c_sec is not None and x_m_sec is not None:
			z_phi_rect_sec = f"{r_c_sec:.4f} + j{x_m_sec:.4f} Ω"

		# Update all tabs with calculated values
		self._update_tabs(
			# Primary side parameters
			z_eq_polar, r_eq, x_eq, y_phi_mag, theta_oc_deg, g_phi, b_phi, r_c, x_m, z_phi_rect,
			# Secondary side parameters
			z_eq_polar_sec, r_eq_sec, x_eq_sec, y_phi_mag_sec, g_phi_sec, b_phi_sec, r_c_sec, x_m_sec, z_phi_rect_sec,
			# Common parameters
			power, vs, vp, turns_ratio
		)
		
		# Show success message
		print("Calculation completed successfully!")
		QMessageBox.information(self, 'Success', 'Calculations completed! Check all tabs for results.')

	def _update_tabs(self, z_eq_polar, r_eq, x_eq, y_phi_mag, theta_oc_deg, g_phi, b_phi, r_c, x_m, z_phi_rect,
					 z_eq_polar_sec, r_eq_sec, x_eq_sec, y_phi_mag_sec, g_phi_sec, b_phi_sec, r_c_sec, x_m_sec, z_phi_rect_sec,
					 power, vs, vp, turns_ratio):
		"""Update Impedances, Voltage Regulation, and Efficiency tabs with computed values."""
		# Find parent tab widget
		parent = self.parent()
		while parent is not None and not isinstance(parent, QTabWidget):
			parent = parent.parent()
		if parent is None:
			return

		# Iterate through all tabs and update relevant pages
		for i in range(parent.count()):
			tab_name = parent.tabText(i).lower()
			page = parent.widget(i)

			# UPDATE IMPEDANCES PAGE
			if tab_name.startswith('imped'):
				try:
					# Primary side values
					page.primary_values['Zeq'].setText(z_eq_polar)
					page.primary_values['Req'].setText(f"{r_eq:.4f} Ω")
					page.primary_values['Xeq'].setText(f"{x_eq:.4f} jΩ")
					page.primary_values['Yφ'].setText(f"{y_phi_mag:.4f} ∠ -{theta_oc_deg:.4f}°")
					page.primary_values['Gφ'].setText(f"{g_phi:.4f} S")
					page.primary_values['Bφ'].setText(f"{b_phi:.4f} S")
					page.primary_values['Zφ'].setText(z_phi_rect if z_phi_rect else '')
					page.primary_values['Rc'].setText(f"{r_c:.4f} Ω" if r_c is not None else '')
					page.primary_values['Xₘ'].setText(f"{x_m:.4f} Ω" if x_m is not None else '')

					# Secondary side values (referred to secondary)
					page.secondary_values['Zeq'].setText(z_eq_polar_sec)
					page.secondary_values['Req'].setText(f"{r_eq_sec:.4f} Ω")
					page.secondary_values['Xeq'].setText(f"{x_eq_sec:.4f} jΩ")
					page.secondary_values['Yφ'].setText(f"{y_phi_mag_sec:.4f} ∠ -{theta_oc_deg:.4f}°")
					page.secondary_values['Gφ'].setText(f"{g_phi_sec:.4f} S")
					page.secondary_values['Bφ'].setText(f"{b_phi_sec:.4f} S")
					page.secondary_values['Zφ'].setText(z_phi_rect_sec if z_phi_rect_sec else '')
					page.secondary_values['Rc'].setText(f"{r_c_sec:.4f} Ω" if r_c_sec is not None else '')
					page.secondary_values['Xₘ'].setText(f"{x_m_sec:.4f} Ω" if x_m_sec is not None else '')
				except Exception as e:
					print(f"Error updating impedances page: {e}")
					import traceback
					traceback.print_exc()

			# UPDATE VOLTAGE REGULATION PAGE
			elif tab_name.startswith('volt'):
				try:
					# Calculate rated secondary current: I2 = S / V2
					i2_rated = power / vs if vs != 0 else None
					if i2_rated is None:
						continue
					page.i2_rated.setText(f"{i2_rated:.4f} A")

					# No-load secondary voltage: V2,nl = a * V1 = Vs (rated)
					v2_nl = vs
					page.v2_nl.setText(f"{v2_nl:.4f} V")
					
					# Use secondary-side impedance for voltage drop calculations
					z_eq_complex = complex(r_eq_sec, x_eq_sec)
					v2_nl_phasor = complex(v2_nl, 0)

					# UNITY POWER FACTOR (pf = 1.0)
					i2_unity = complex(i2_rated, 0)
					v2_fl_phasor = v2_nl_phasor - z_eq_complex * i2_unity
					v2_fl_mag = abs(v2_fl_phasor)
					page.v2_fl.setText(f"{v2_fl_mag:.4f} V")

					# Voltage regulation: VR = (V_nl - V_fl) / V_fl * 100%
					if v2_fl_mag != 0:
						vr_pct = (v2_nl - v2_fl_mag) / v2_fl_mag * 100.0
						page.vr.setText(f"{vr_pct:.4f} %")
					else:
						page.vr.setText('')

					# 0.8 PF LAGGING (current lags voltage by θ)
					phi_08 = math.acos(0.8)
					i2_lag = i2_rated * complex(math.cos(-phi_08), math.sin(-phi_08))
					v2_fl_lag_phasor = v2_nl_phasor - z_eq_complex * i2_lag
					v2_fl_lag_mag = abs(v2_fl_lag_phasor)
					if v2_fl_lag_mag != 0:
						vr_lag_pct = (v2_nl - v2_fl_lag_mag) / v2_fl_lag_mag * 100.0
						page.vr_08_lag.setText(f"{vr_lag_pct:.4f} %")
					else:
						page.vr_08_lag.setText('')

					# 0.8 PF LEADING (current leads voltage by θ)
					i2_lead = i2_rated * complex(math.cos(phi_08), math.sin(phi_08))
					v2_fl_lead_phasor = v2_nl_phasor - z_eq_complex * i2_lead
					v2_fl_lead_mag = abs(v2_fl_lead_phasor)
					if v2_fl_lead_mag != 0:
						vr_lead_pct = (v2_nl - v2_fl_lead_mag) / v2_fl_lead_mag * 100.0
						page.vr_08_lead.setText(f"{vr_lead_pct:.4f} %")
					else:
						page.vr_08_lead.setText('')
				except Exception as e:
					print(f"Error updating voltage regulation page: {e}")
					import traceback
					traceback.print_exc()			# UPDATE EFFICIENCY PAGE
			elif tab_name.startswith('effi'):
				try:
					# Calculate rated secondary current
					i2_rated = power / vs if vs != 0 else None
					if i2_rated is None or r_eq_sec is None or r_c is None:
						continue

					# Use secondary-side impedance for accurate calculations
					z_eq_complex = complex(r_eq_sec, x_eq_sec)
					v2_nl_phasor = complex(vs, 0)
					i2_unity = complex(i2_rated, 0)
					v2_fl_phasor = v2_nl_phasor - z_eq_complex * i2_unity
					v2_fl_mag = abs(v2_fl_phasor)

					# Copper loss: P_cu = I2^2 * R_eq (on secondary side)
					p_cu = (i2_rated ** 2) * r_eq_sec

					# Core loss: P_core = V2,nl^2 / R_c (using primary-side R_c and primary voltage)
					# For accurate core loss, use primary voltage referred value
					p_core = (v2_nl ** 2) / r_c_sec if r_c_sec is not None else None

					# Output power: P_out = V2,fl * I2 * cos(θ) (assuming unity pf)
					p_out = v2_fl_mag * i2_rated * 1.0

					# Input power: P_in = P_out + P_cu + P_core
					if p_core is not None:
						p_in = p_out + p_cu + p_core
					else:
						p_in = None

					# Efficiency: Î· = (P_out / P_in) * 100%
					eta_pct = (p_out / p_in * 100.0) if (p_in is not None and p_in != 0) else None

					# Update display fields
					page.pin.setText(f"{p_in:.4f} W" if p_in is not None else '')
					page.pout.setText(f"{p_out:.4f} W")
					page.pcu.setText(f"{p_cu:.4f} W")
					page.pcore.setText(f"{p_core:.4f} W" if p_core is not None else '')
					page.eta.setText(f"{eta_pct:.4f} %" if eta_pct is not None else '')
				except Exception as e:
					print(f"Error updating efficiency page: {e}")
					import traceback
					traceback.print_exc()

class ImpedancesPage(QWidget):
	"""Page displaying transformer impedance parameters referred to primary and secondary."""
	def __init__(self, parent=None):
		super().__init__(parent)
		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(5, 5, 5, 5)
		main_layout.setSpacing(5)

		# Parameter names to display
		param_names = ['Zeq', 'Req', 'Xeq', 'Yφ', 'Gφ', 'Bφ', 'Zφ', 'Rc', 'Xₘ']

	# PRIMARY SIDE SECTION
		primary_group = QGroupBox('Referred to Primary')
		primary_h = QHBoxLayout()

		# Left: Grid layout for parameter labels and values (vertical)
		primary_grid = QGridLayout()
		primary_grid.setHorizontalSpacing(5)
		primary_grid.setVerticalSpacing(3)
		self.primary_values = {}
		
		for idx, param_name in enumerate(param_names):
			row = idx
			col = 0
			
			label = QLabel(param_name + ':')
			label.setMinimumWidth(50)
			label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
			
			value_display = QLabel('')
			value_display.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 2px;')
			value_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
			value_display.setMinimumWidth(180)
			value_display.setMaximumHeight(22)
			
			self.primary_values[param_name] = value_display
			primary_grid.addWidget(label, row, col)
			primary_grid.addWidget(value_display, row, col + 1)
		
		primary_h.addLayout(primary_grid)
		primary_h.addStretch()

		# Right: Image
		primary_img = QLabel()
		pixmap = QPixmap('img2.jpeg')
		if not pixmap.isNull():
			scaled_pixmap = pixmap.scaled(320, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			primary_img.setPixmap(scaled_pixmap)
		else:
			primary_img.setText('Image not found')
		primary_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
		primary_img.setStyleSheet('border: 1px solid #ccc; background-color: #fafafa;')
		primary_img.setMinimumHeight(120)
		primary_h.addWidget(primary_img, 1)

		primary_group.setLayout(primary_h)
		main_layout.addWidget(primary_group)

		# SECONDARY SIDE SECTION
		secondary_group = QGroupBox('Referred to Secondary')
		secondary_h = QHBoxLayout()

		# Left: Image
		secondary_img = QLabel()
		pixmap = QPixmap('img3.jpeg')
		if not pixmap.isNull():
			scaled_pixmap = pixmap.scaled(320, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			secondary_img.setPixmap(scaled_pixmap)
		else:
			secondary_img.setText('Image not found')
		secondary_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
		secondary_img.setStyleSheet('border: 1px solid #ccc; background-color: #fafafa;')
		secondary_img.setMinimumHeight(120)
		secondary_h.addWidget(secondary_img, 1)

		# Right: Grid layout for parameter labels and values (vertical)
		secondary_grid = QGridLayout()
		secondary_grid.setHorizontalSpacing(5)
		secondary_grid.setVerticalSpacing(3)
		self.secondary_values = {}
		
		for idx, param_name in enumerate(param_names):
			row = idx
			col = 0
			
			label = QLabel(param_name + ':')
			label.setMinimumWidth(50)
			label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
			
			value_display = QLabel('')
			value_display.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 2px;')
			value_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
			value_display.setMinimumWidth(180)
			value_display.setMaximumHeight(22)
			
			self.secondary_values[param_name] = value_display
			secondary_grid.addWidget(label, row, col)
			secondary_grid.addWidget(value_display, row, col + 1)
		
		secondary_h.addStretch()
		secondary_h.addLayout(secondary_grid)

		secondary_group.setLayout(secondary_h)
		main_layout.addWidget(secondary_group)

		self.setLayout(main_layout)

class VoltageRegulationPage(QWidget):
	"""Page displaying voltage regulation calculations at different power factors."""
	def __init__(self, parent=None):
		super().__init__(parent)
		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(5, 30, 5, 5)
		main_layout.setSpacing(5)

		# Title
		title = QLabel('Voltage Regulation Analysis')
		title_font = QFont()
		title_font.setPointSize(14)
		title_font.setBold(True)
		title.setFont(title_font)
		title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(title)
		main_layout.addSpacing(30)

		# Output fields form
		form_widget = QWidget()
		form = QFormLayout()
		form.setContentsMargins(5, 5, 5, 5)
		form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
		form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		form.setHorizontalSpacing(5)
		form.setVerticalSpacing(8)

		# Create output labels with consistent styling
		self.i2_rated = self._create_output_label()
		form.addRow('Rated Secondary Current, I₂,rated (A):', self.i2_rated)

		self.v2_fl = self._create_output_label()
		form.addRow('Full Load Secondary Voltage, V₂,ꜰʟ (V):', self.v2_fl)

		self.v2_nl = self._create_output_label()
		form.addRow('No Load Secondary Voltage, V₂,ɴʟ (V):', self.v2_nl)

		self.vr = self._create_output_label()
		form.addRow('Voltage Regulation, VR (%):', self.vr)

		self.vr_08_lag = self._create_output_label()
		form.addRow('VR at 0.8 PF Lagging (%):', self.vr_08_lag)

		self.vr_08_lead = self._create_output_label()
		form.addRow('VR at 0.8 PF Leading (%):', self.vr_08_lead)

		form_widget.setLayout(form)
		main_layout.addWidget(form_widget)

		# Image below the form
		photo = QLabel()
		pixmap = QPixmap('img4.jpeg')
		if not pixmap.isNull():
			scaled_pixmap = pixmap.scaled(320, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			photo.setPixmap(scaled_pixmap)
		else:
			photo.setText('Image not found')
		photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
		photo.setStyleSheet('border: 1px solid #ccc; background-color: #fafafa; padding: 5px;')
		main_layout.addWidget(photo)
		main_layout.addStretch()
		self.setLayout(main_layout)

	def _create_output_label(self):
		"""Helper method to create consistently styled output labels."""
		label = QLabel('')
		label.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 6px;')
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setMinimumWidth(250)
		return label


class EfficiencyPage(QWidget):
	"""Page displaying transformer efficiency and loss calculations."""
	def __init__(self, parent=None):
		super().__init__(parent)
		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(5, 30, 5, 5)
		main_layout.setSpacing(5)

		# Title
		title = QLabel('Efficiency and Losses')
		title_font = QFont()
		title_font.setPointSize(14)
		title_font.setBold(True)
		title.setFont(title_font)
		title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		main_layout.addWidget(title)
		main_layout.addSpacing(30)

		# Output fields form
		form_widget = QWidget()
		form = QFormLayout()
		form.setContentsMargins(5, 5, 5, 5)
		form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
		form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		form.setHorizontalSpacing(5)
		form.setVerticalSpacing(8)

		# Create output labels with consistent styling
		self.pin = self._create_output_label()
		form.addRow('Input Power, Pin (W):', self.pin)

		self.pout = self._create_output_label()
		form.addRow('Output Power, Pout (W):', self.pout)

		self.pcu = self._create_output_label()
		form.addRow('Copper Loss, Pcu (W):', self.pcu)

		self.pcore = self._create_output_label()
		form.addRow('Core Loss, Pcore (W):', self.pcore)

		self.eta = self._create_output_label()
		form.addRow('Efficiency, η (%):', self.eta)

		form_widget.setLayout(form)
		main_layout.addWidget(form_widget)

		# Image below the form
		photo = QLabel()
		pixmap = QPixmap('img5.jpeg')
		if not pixmap.isNull():
			scaled_pixmap = pixmap.scaled(320, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			photo.setPixmap(scaled_pixmap)
		else:
			photo.setText('Image not found')
		photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
		photo.setStyleSheet('border: 1px solid #ccc; background-color: #fafafa; padding: 5px;')
		main_layout.addWidget(photo)
		main_layout.addStretch()
		self.setLayout(main_layout)

	def _create_output_label(self):
		"""Helper method to create consistently styled output labels."""
		label = QLabel('')
		label.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 6px;')
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setMinimumWidth(250)
		return label


class InfoPage(QWidget):
	"""Info page displaying course and student information."""
	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QVBoxLayout()
		layout.setContentsMargins(10, 120, 10, 10)
		layout.setSpacing(5)
		
		# Main header
		header = QLabel('EEE-3003 - Electromechanical Energy Conversion')
		header.setAlignment(Qt.AlignmentFlag.AlignCenter)
		header_font = QFont()
		header_font.setPointSize(16)
		header_font.setBold(True)
		header.setFont(header_font)
		
		layout.addWidget(header)
		layout.addSpacing(80)
		
		# Group Members header
		group_header = QLabel('Group Members')
		group_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
		group_header_font = QFont()
		group_header_font.setPointSize(11)
		group_header_font.setBold(True)
		group_header.setFont(group_header_font)
		layout.addWidget(group_header)
		
		# First student name
		student1 = QLabel('220702705 - Ahmed Mahmoud Elsayed Hussein')
		student1.setAlignment(Qt.AlignmentFlag.AlignCenter)
		student1_font = QFont()
		student1_font.setPointSize(10)
		student1.setFont(student1_font)
		
		# Second student name
		student2 = QLabel('220702084 - Gökdeniz Günde')
		student2.setAlignment(Qt.AlignmentFlag.AlignCenter)
		student2_font = QFont()
		student2_font.setPointSize(10)
		student2.setFont(student2_font)
		
		layout.addWidget(student1)
		layout.addWidget(student2)
		layout.addSpacing(40)
		
		# Lecturers header
		lecturers_header = QLabel('Name of Lecturers')
		lecturers_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
		lecturers_header_font = QFont()
		lecturers_header_font.setPointSize(11)
		lecturers_header_font.setBold(True)
		lecturers_header.setFont(lecturers_header_font)
		
		# First lecturer
		lecturer1 = QLabel('Doç. Dr. Akın Taşcıkaraoğlu')
		lecturer1.setAlignment(Qt.AlignmentFlag.AlignCenter)
		lecturer1_font = QFont()
		lecturer1_font.setPointSize(10)
		lecturer1.setFont(lecturer1_font)
		
		# Second lecturer
		lecturer2 = QLabel('Arş. Gör. Ali Can Erüst')
		lecturer2.setAlignment(Qt.AlignmentFlag.AlignCenter)
		lecturer2_font = QFont()
		lecturer2_font.setPointSize(10)
		lecturer2.setFont(lecturer2_font)
		
		layout.addWidget(lecturers_header)
		layout.addWidget(lecturer1)
		layout.addWidget(lecturer2)
		layout.addStretch()
		
		self.setLayout(layout)


class MainWindow(QMainWindow):
	"""Main application window with tabbed interface for transformer calculations."""
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Single Phase Transformer Calculator')
		
		# Set light mode colors explicitly
		self.setStyleSheet("""
			QMainWindow {
				background-color: white;
			}
			QWidget {
				background-color: white;
				color: black;
			}
			QTabWidget::pane {
				background-color: white;
				border: 1px solid #ccc;
			}
			QTabBar::tab {
				background-color: #e0e0e0;
				color: black;
				padding: 8px 16px;
				border: 1px solid #ccc;
			}
			QTabBar::tab:selected {
				background-color: white;
				border-bottom-color: white;
			}
			QLineEdit {
				background-color: white;
				color: black;
				border: 1px solid #ccc;
				padding: 4px;
			}
			QPushButton {
				background-color: #0078d4;
				color: white;
				border: none;
				padding: 8px 16px;
				border-radius: 4px;
			}
			QPushButton:hover {
				background-color: #106ebe;
			}
			QGroupBox {
				background-color: white;
				color: black;
				border: 1px solid #ccc;
				margin-top: 10px;
				padding-top: 10px;
			}
			QGroupBox::title {
				color: black;
			}
		""")
		
		# Create tab widget
		tabs = QTabWidget()
		tabs.addTab(InputPage(), 'Input')
		tabs.addTab(ImpedancesPage(), 'Impedances')
		tabs.addTab(VoltageRegulationPage(), 'Voltage Regulation')
		tabs.addTab(EfficiencyPage(), 'Efficiency')
		tabs.addTab(InfoPage(), 'Info')
		
		self.setCentralWidget(tabs)


def main():
	"""Application entry point."""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.resize(750, 550)
	window.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()


