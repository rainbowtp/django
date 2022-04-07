from Crypto.Cipher import AES

key = '1000000000000000'.encode('utf-8')
# data = b'hello from other side'
data = 'asd'.encode('utf-8')

N = b'\x94\x87\x90\xcd"\xaa\x04\xe9\xf1\xe3\xd2\x81\xe7J%\x1c'

e_cipher = AES.new(key, AES.MODE_EAX, N)
 
e_data = e_cipher.encrypt(data)

e_data = b'pF\xa8'
d_cipher = AES.new(key, AES.MODE_EAX, N)
d_data = d_cipher.decrypt(e_data)

print(key)

print("Encryption was: ", e_data, type(e_data))
print("Original Message was: ", d_data,d_data.decode('utf-8'))
# print(e_cipher.nonce)
# print(e_data.decode('utf-8'))
# print(e_data.decode('utf-8').encode('utf-8'))




# from Crypto.Hash import MD5
# h = MD5.new()
# h.update(b'Hello')
# print (h.hexdigest())

# h = MD5.new()
# h.update(b'Hello')
# print (h.hexdigest())
