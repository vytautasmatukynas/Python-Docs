from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

password = 'psw'

# encrypt psw
hashed = bcrypt.generate_password_hash(password)

print(hashed)

# check if psw is correct
check = bcrypt.check_password_hash(hashed, 'worng psw')
check_2 = bcrypt.check_password_hash(hashed, 'psw')

print(check)
print(check_2)

