# Transformer Equations Reference

This file collects the short-circuit, open-circuit, referred-parameter, voltage-regulation and efficiency equations used by the app. Use these exact formulas when you ask me to compute specific quantities.

---

## 1) Short-Circuit (Series) Parameters

- Power factor (short-circuit):

  PF_sc = cos(θ) = P_sc / (V_sc * I_sc)

- Phase angle:

  θ = arccos(PF_sc)

- Equivalent impedance magnitude:

  |Z_eq| = V_sc / I_sc

- Equivalent impedance (polar form):

  Z_eq = |Z_eq| ∠ θ

- Equivalent resistance:

  R_eq = P_sc / I_sc^2

- Equivalent reactance:

  X_eq = sqrt(|Z_eq|^2 - R_eq^2)

  (X_eq is the same as X_leq)

- Equivalent impedance (rectangular form):

  Z_eq = R_eq + j X_eq

> Units: |Z_eq|, R_eq, X_eq are in ohms (Ω).

---

## 2) Open-Circuit (Excitation Branch) Parameters

- Power factor (open-circuit):

  PF_oc = cos(θ) = P_oc / (V_oc * I_oc)

- Phase angle:

  θ = arccos(PF_oc)

- Excitation admittance (phasor):

  Y_ϕ = (I_oc / V_oc) ∠ (−θ)

- Conductance:

  G_ϕ = |Y_ϕ| cos(θ)

- Susceptance:

  B_ϕ = |Y_ϕ| sin(θ)

- Admittance (rectangular):

  Y_ϕ = G_ϕ − j B_ϕ

- Core-loss resistance:

  R_c = 1 / G_ϕ

- Magnetizing reactance:

  X_m = 1 / |B_ϕ|

- Excitation impedance:

  Z_ϕ = R_c + j X_m

---

## 3) Referred Parameters

- Excitation impedance referred to primary:

  Z_ϕ1 = a^2 · Z_ϕ2

  (where a = N1 / N2 is the turns ratio)

- Series impedance referred to secondary (relationship using turns ratio):

  Z_eq2 = Z_eq1 / a^2

  (equivalently Z_eq1 = a^2 · Z_eq2)

---

## 4) Voltage Regulation Equations

- Voltage regulation (percent):

  VR = (V_nl − V_fl) / V_fl × 100%

- Full-load seconday voltage:

  V_2,fl = V_1

- No-load secondary voltage:

  V_2,nl = a · V_1

- Phasor voltage equation (referred forms):

  a·V_1 = V_2 + R_eq·I_2 + j X_eq·I_2

- Full-load secondary current magnitude (from rated apparent power S):

  |I_2| = S_rated / V_2,rated

- Unity power factor assumption (if used):

  I_2 = |I_2| ∠ 0°

- Phasor magnitude and angle (generic):

  |a·V_1| = sqrt((Re)^2 + (Im)^2)

  θ = atan2(Im, Re)

---

## 5) Efficiency and Losses

- Copper loss (at load current I_2):

  P_cu = I_2^2 · R_eq

- Core loss (excitation branch):

  P_core = V_2,nl^2 / R_c

- Output power:

  P_out = P_2 = V_2 · I_2 · cos(θ)

- Input power:

  P_in = P_out + P_cu + P_core

- Efficiency (percentage):

  η = (P_out / P_in) × 100%

---

## Notes

- All phasor angles are in radians for internal calculations, but degrees may be used for display.
- Units are important: voltages (V), currents (A), powers (W), impedances (Ω), admittances (S).
- If you want, I can also add a JSON or YAML version of these formulas to make programmatic retrieval easier.

---

*File created to serve as the canonical source of the equations used by the GUI.*
