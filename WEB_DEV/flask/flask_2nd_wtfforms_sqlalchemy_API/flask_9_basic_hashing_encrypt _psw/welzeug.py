from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash('psw')

print(hashed)

check_psw = check_password_hash(hashed, 'psw')
check_psw_2 = check_password_hash(hashed, 'psw_2')

print(check_psw)
print(check_psw_2)
