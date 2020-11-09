def skid(id1, id2):
    id1 = int(id1)
    id2 = int(id2)
    if id1 < id2:
        kid = str(id1) + str(id2)
    else:
        kid = kid = str(id2) + str(id1)
    kid = int(kid)
    return kid


def pk(privateuser2, publicuser1, publicuser2):
    g = publicuser1
    p = publicuser2
    # print(f"Alice's public key is {g}.\n")
    # print(f"bob's public key is {p}.\n")
    # print(f"Agreed g value:{g}, agreed modulo:{p}\n")
    A = privateuser2
    # print(f"Alice's private key is {A}.\n")
    a = g ** A % p
    # print(f"Alice's calculated public value is {a}, which will be sent to Bob publicly.\n")
    return a


def secret(privateuser1, publicuser2, psharedkeyuser2):
    b = psharedkeyuser2
    A = privateuser1
    p = publicuser2
    sk = b ** A % p
    return sk
