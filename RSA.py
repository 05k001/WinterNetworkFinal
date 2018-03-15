#Python RSA

import random
import pdb

'''
Euclid's algorithm for Gcd. 

'''

def gcd(a,b):
	while b != 0:
		a, b = b, a % b
	return a


def multiplicative_inverse(e, phi):

#Global Vars for the MI function

	d = 0
	x1 = 0
	x2 = 1
	y1 = 1

	temp_phi = phi


	while e > 0:

		temp1 = temp_phi/e
		temp2 = temp_phi - temp1 * e
		temp_phi = e
		e = temp2

		x = x2 - temp1 * x1
		y = d - temp1 * y1


		x2 = x1
		x1 = x
		d = y1
		y1 = y


		if temp_phi == 1:
			return d + phi

# Writitng a Prime Number checker


def is_prime(num):

	if num == 2:
		return True

	if num < 2 or num % 2 == 0:
		return False

	for n in xrange(3, int(num**0.5)+2, 2):
		if num % n == 0:
			return False

	return True


def generate_keypair(p, q):
	if not (is_prime(p) and is_prime(q)):
		raise ValueError('Gotta use primes bro')
	elif p == q:
		raise ValueError('Cant use the same numbers....jeeze')


	# Woah now we can find N (n = pq)

	n = p * q

	# Lets get phi....(The toitent of n)

	phi = (p-1) * (q-1)


	# Now we can find and e that is coprime of phi(n)

	e = random.randrange(1,phi)

	#Euclid's to verify


	g = gcd(e,phi)
	while g != 1:
		e = random.randrange(1,phi)
		g = gcd(e,phi)

	#Extended Algorithm for Private Key Gens

	d = multiplicative_inverse(e, phi)

	#Return Public  and private keys

	return ((e,n), (d,n))

def encrypt(pk,plaintext):
	#Unpack the Key

	key, n = pk

	#Convert each letter to Plaintext 

	cipher = [(ord(char) ** key) % n for char in plaintext]

	return cipher

def decrypt(pk, ciphertext):

	#Unpack Key into components

	key, n = pk

	#Generate the Plaintxt into the keyspace.

	plain = [chr((char ** key ) % n ) for char in ciphertext]

	#Return the array of the bute stream

	return ''.join(plain)



if __name__ == '__main__':

	# This should work perfecly right?

	print "RSA Program YAY!"

	p = int(raw_input("Enter a prime number (17, 19, 23, 42....etc): "))

	q = int(raw_input("Enter another prime number...but like...different: "))

	print "IMA GENERATING A KEYPAIR....."

	public, private = generate_keypair(p,q)

	print "Your public key is: ", public, " and your private key is: ", private

	message = raw_input("Enter a message: ")

	encrypted_msg = encrypt(private, message)

	print "\nEncrypted Message is: \n\n"

	print ''.join(map(lambda x : str(x), encrypted_msg))

	print "Now decrypting message ........\n\n"

	# pdb.set_trace()



	print ''.join(map(lambda x : str(x), (decrypt(public, encrypted_msg))))








