
import fractions

def check_if_entry_value_is_legal(value):
				val = value.get()
				try:
					fractions.Fraction(val)
				except:
					value.set("0.0")
				value.set("{:.1f}".format(float(val)))
				return val

def check_if_entry_value_is_legal_realtime(value):
				try:
					fractions.Fraction(value.get())
				except:
					return 0
				return value.get()


def get_correction_factor_from_wavelength(wavelength):
	return (-0.000000000001354119*wavelength**6 + 0.000000004416176*wavelength**5 -0.00000596327*wavelength**4 +
		0.004269544*wavelength**3 - 1.710567*wavelength**2 + 364.3159*wavelength - 32208.6)
