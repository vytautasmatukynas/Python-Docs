# number types
x = 15        # Integer: Represents a whole number without decimal points
y = 21.12245  # Float: Represents a decimal number with floating-point precision
z = -87.7e10   # Float in scientific notation: Represents -87.7 multiplied by 10 raised to the power of 10
w = 5j        # Complex number: Represents a number with both a real and an imaginary part
print(type(x))
print(type(y))
print(type(z))
print(type(w))

# Basic arithmetic operations
# Addition
sum_result = 10 + 5
# Subtraction
difference_result = 10 - 5
# Multiplication
product_result = 10 * 5
# Division (floating-point)
quotient_result = 10 / 5
# Division (floor division, returns integer quotient)
floor_division_result = 10 // 5
# Modulus (remainder)
remainder_result = 10 % 5
# Exponentiation
exponentiation_result = 10 ** 2  # 10 raised to the power of 2
# Augmented assignment
x = 10
x += 5  # Equivalent to x = x + 5
x -= 3  # Equivalent to x = x - 3
x *= 2  # Equivalent to x = x * 2
x /= 4  # Equivalent to x = x / 4
x **= 3  # Equivalent to x = x ** 3
x //= 2  # Equivalent to x = x // 2
x %= 7  # Equivalent to x = x % 7
# Using built-in math functions
x = -15
y = 21.12245
z = 87.7
w = -5
# Floor division with positive and negative numbers
floor_pos = 10 // 3  # Result: 3
floor_neg = -10 // 3  # Result: -4 (towards negative infinity)
# Modulus with positive and negative numbers
mod_pos = 10 % 3  # Result: 1
mod_neg = -10 % 3  # Result: 2 (sign follows dividend)
# Compare
greater_than = 10 > 5
less_than = 5 < 10
equal_to = 10 == 10
not_equal = 5 != 10
greater_equal = 10 >= 5
less_equal = 5 <= 10

# Absolute value
abs_x = abs(x)
print("Absolute value of x:", abs_x)
# Minimum value
min_val = min(x, y, z, w)
print("Minimum value:", min_val)
# Maximum value
max_val = max(x, y, z, w)
print("Maximum value:", max_val)
# Rounding numbers
rounded_y = round(y, 2)
print("Rounded y:", rounded_y)
# Converting to integer
int_z = int(z)
print("Integer value of z:", int_z)
# Power function
power_result = pow(y, 3)
print("y raised to the power of 3:", power_result)


import math

# Trigonometric functions
angle_rad = math.radians(45)
sin_result = math.sin(angle_rad)
cos_result = math.cos(angle_rad)
tan_result = math.tan(angle_rad)
print("sin:", sin_result)
print("cos:", cos_result)
print("tan:", tan_result)

# Exponential and logarithmic functions
exp_result = math.exp(2)
log_result = math.log(10)       # Natural logarithm (base e)
log10_result = math.log10(100)  # Base 10 logarithm
log2_result = math.log2(8)      # Base 2 logarithm
print("exp:", exp_result)
print("log:", log_result)
print("log10:", log10_result)
print("log2:", log2_result)

# Rounding and remainder functions
ceil_result = math.ceil(7.3)
floor_result = math.floor(7.7)
trunc_result = math.trunc(9.87)
fmod_result = math.fmod(10.5, 3.2)
modf_result = math.modf(12.75)
print("ceil:", ceil_result)
print("floor:", floor_result)
print("trunc:", trunc_result)
print("fmod:", fmod_result)
print("modf:", modf_result)

# Constants
pi_value = math.pi
e_value = math.e
inf_positive = math.inf
inf_negative = -math.inf
nan_value = math.nan
print("pi:", pi_value)
print("e:", e_value)
print("inf_positive:", inf_positive)
print("inf_negative:", inf_negative)
print("nan:", nan_value)

# Angular conversion
angle_deg = math.degrees(math.pi)      # Convert radians to degrees
angle_rad_back = math.radians(angle_deg)  # Convert degrees back to radians
print("angle_deg:", angle_deg)
print("angle_rad_back:", angle_rad_back)

# Absolute value
abs_value = math.fabs(-10.5)
print("abs_value:", abs_value)

# Factorial
factorial_result = math.factorial(5)
print("factorial:", factorial_result)

# Greatest common divisor (GCD) and least common multiple (LCM)
gcd_result = math.gcd(15, 20)
lcm_result = math.lcm(15, 20)  # Available in Python 3.9+
print("gcd:", gcd_result)
print("lcm:", lcm_result)

# Exponential minus 1 and logarithm plus 1
expm1_result = math.expm1(1)
log1p_result = math.log1p(1)
print("expm1:", expm1_result)
print("log1p:", log1p_result)

# Inverse hyperbolic functions
acosh_result = math.acosh(2)
asinh_result = math.asinh(3)
atanh_result = math.atanh(0.5)
print("acosh:", acosh_result)
print("asinh:", asinh_result)
print("atanh:", atanh_result)


