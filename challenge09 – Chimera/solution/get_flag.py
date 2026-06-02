import cowsay
import art
from arc4 import ARC4

current_user = b'G0ld3n_Tr4nsmut4t10n'
ENCRYPTED_CHIMERA_FORMULA = b'r2b-\r\x9e\xf2\x1fp\x185\x82\xcf\xfc\x90\x14\xf10\xad#]\xf3\xe2\xc0L\xd0\xc1e\x0c\xea\xec\xae\x11b\xa7\x8c\xaa!\xa1\x9d\xc2\x90'

art.tprint('AUTHENTICATION SUCCESS', font='small')
print('Biometric scan MATCH. Identity confirmed as Lead Researcher.')
print('Finalizing Project Chimera...')

arc4_decipher = ARC4(current_user)
decrypted_formula = arc4_decipher.decrypt(ENCRYPTED_CHIMERA_FORMULA).decode()

cowsay.cow('I am alive! The secret formula is:\n' + decrypted_formula)
