import numpy as np
print "lijie1"

str1 = "abc".encode('utf-8')
#str1 = ord(str1)
#str1 = "%x"%(ord(str1))
#print str1

strlen1 = 1 * 8

olddata = np.zeros( (16), dtype = np.uint32 )
#olddata[0] = str1 | 1 << strlen1
#olddata[0] = str1 | 0x80000000
#olddata[0] = 0x32800000
#olddata[0] = 0x61626380
olddata[0] = 0x80636261
olddata[15] = 0x18000000
#print "%x"%olddata[0]
#print olddata


H = np.array((0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19), dtype = np.uint32)
#print H
W = np.zeros((64), dtype = np.uint32)
M = np.array(olddata)

#print olddata
#print M

K = np.array((0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070, 0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2),dtype = np.uint32)

    
#def strlen(x):
def shr(x, n):
    return np.uint32((x & 0xFFFFFFFF) >> n)

def rotr(x, n):
    return np.uint32(shr(x, n) | (x << (32 - n)))

def CH(x,y,z):
    return np.uint32(np.uint32(x & y) ^ np.uint32((~x) & z))

def MAJ (x, y, z):
    return np.uint32(np.uint32(x & y) ^ np.uint32(x & z) ^ np.uint32(y & z))

def BSIG0(x):
    return np.uint32(rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22))

def BSIG1(x):
    return np.uint32(rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25))

def SSIG0(x):
    return np.uint32(rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3))

def SSIG1(x):
    return np.uint32(rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10))



#main
for t in range(16):
    W[t] = (M[t]&0xFF000000)>>24 | (M[t]&0x00FF0000)>>8 | (M[t]&0x0000FF00)<<8 | ((M[t]&0xFF)<<24)

for t in range(16, 64):
    W[t] = np.uint32(SSIG1(W[t-2]) + W[t-7] + SSIG0(W[t-15]) + W[t-16])

a = H[0]
b = H[1]
c = H[2]
d = H[3]
e = H[4]
f = H[5]
g = H[6]
h = H[7]



T1 = 0
T2 = 0
for t in range(64):
    T1 = np.uint32((h&0xFFFFFFFF) + (BSIG1(e)&0xFFFFFFFF) + (CH(e,f,g)&0xFFFFFFFF) + (K[t]&0xFFFFFFFF) + (W[t]&0xFFFFFFFF))
    T2 = np.uint32((BSIG0(a)&0xFFFFFFFF) + (MAJ(a,b,c)&0xFFFFFFFF))
    h = g
    g = f
    f = e
    e = np.uint32((d&0xFFFFFFFF) + (T1&0xFFFFFFFF))
    d = c
    c = b
    b = a
    a = np.uint32((T1&0xFFFFFFFF) + (T2&0xFFFFFFFF))

H[0] = np.uint32(a + H[0])
H[1] = np.uint32(b + H[1])
H[2] = np.uint32(c + H[2])
H[3] = np.uint32(d + H[3])
H[4] = np.uint32(e + H[4])
H[5] = np.uint32(f + H[5])
H[6] = np.uint32(g + H[6])
H[7] = np.uint32(h + H[7])

result = np.zeros((32), dtype = np.uint8)

for i in range(32):
    result[i] = (H[i>>2] >> 8*(3 - (i & 0x03)))&0xFF
print result


for x in range(32):
    print "%02x"%result[x],
