from rsa_algo import generateKeys
private1, public1 = generateKeys()
private2, public2 = generateKeys()
  
# g and p values agreed by both Alice and Bob(basically maine public assign krdi hai).
g = public1
p = public2
print(f"Alice's public key is {g}.\n")
print(f"bob's public key is {p}.\n")
 
print(f"Agreed g value:{g}, agreed modulo:{p}\n")
 
# Alice's private key.
A = private1
print(f"Alice's private key is {A}.\n")
# Bob's private key.
B = private2
print(f"Bob's private key is {B}.\n")

# public value of Alice's to be sent over to Bob.
a = g**A % p
print(f"Alice's calculated public value is {a}, which will be sent to Bob publicly.\n")
 
# public value of Bob's to be sent over to Alice.
b = g**B % p
print(f"Bob's calculated public value is {b}, which will be sent over to Alice publicly.\n")
 
# Alice uses Bob's public value and her private value to compute the secret key.
secret_key1 = b**A % p
 
# Bob uses Alice's public value and his private value to compute the secret key.
secret_key2 = a**B % p
 
if secret_key1 == secret_key2:
    print("Secret key has been successfully derived! See below...\n")
    print(f"Bob uses Alice's public value which is {a}, and his own private value which is {B}, "
          f"the secret key is {secret_key2}.\n")
    print(f"Alice uses Bob's public value which is {b}, and her own private random value which is {A},"
          f"the secret key is {secret_key1}.")
else:
    print("Alice and Bob have different secret keys, which is wrong! Try again!")