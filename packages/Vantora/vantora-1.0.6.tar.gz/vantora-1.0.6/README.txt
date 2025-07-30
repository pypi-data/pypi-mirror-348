###############
Team Nexia
###############

UltraUtils is a powerful and highly trusted Python library crafted specifically for developers and cybersecurity professionals who require advanced, secure, and flexible cryptographic tools.

The library includes a comprehensive suite of encryption algorithms such as XOR, Caesar, Vigenère, and many more. It supports multi-layer encryption, custom cryptographic schemes, and obfuscation techniques that go beyond conventional standards — ensuring the highest levels of data protection.

UltraUtils is engineered with a strong emphasis on security, performance, and modularity, making it ideal for building secure applications, protecting sensitive data, and performing sophisticated cryptographic operations.

Key features:

Advanced encryption algorithms and custom methods.

Multi-stage and hybrid encryption capabilities.

Designed with extensibility for real-world applications.

Lightweight, well-documented, and actively maintained.


Whether you're developing secure software, analyzing data privacy, or building encrypted communication systems, UltraUtils offers the reliability and strength required for mission-critical cryptographic tasks.

#### **1. Basic Arithmetic Operations**
- **`add(x, y)`**
  - **Purpose**: Adds two numbers.
  - **Usage**: `result = UltraUtils.add(5, 3)`

- **`subtract(x, y)`**
  - **Purpose**: Subtracts the second number from the first.
  - **Usage**: `result = UltraUtils.subtract(5, 3)`

#### **2. Text Encryption and Decryption**
- **`encrypt_text(text, key=5)`**
  - **Purpose**: Encrypts text using a simple shift (Caesar cipher).
  - **Usage**: `encrypted = UltraUtils.encrypt_text("Hello", 5)`

- **`decrypt_text(text, key=5)`**
  - **Purpose**: Decrypts text encrypted with `encrypt_text`.
  - **Usage**: `decrypted = UltraUtils.decrypt_text(encrypted, 5)`

#### **3. Number Encryption and Decryption**
- **`encrypt_number(num)`**
  - **Purpose**: Encrypts a number by shifting its digits.
  - **Usage**: `encrypted_num = UltraUtils.encrypt_number(1234)`

- **`decrypt_number(num)`**
  - **Purpose**: Decrypts a number encrypted with `encrypt_number`.
  - **Usage**: `decrypted_num = UltraUtils.decrypt_number(encrypted_num)`

#### **4. Byte Encryption and Decryption**
- **`encrypt_bytes(source)`**
  - **Purpose**: Encrypts a string into a list of bytes.
  - **Usage**: `encrypted_bytes = UltraUtils.encrypt_bytes("Hello")`

- **`decrypt_bytes(data)`**
  - **Purpose**: Decrypts a list of bytes back into a string.
  - **Usage**: `decrypted_string = UltraUtils.decrypt_bytes(encrypted_bytes)`

#### **5. Reinforcement**
- **`reinforce(data)`**
  - **Purpose**: Reinforces data using Base64 and SHA-256.
  - **Usage**: `reinforced_data = UltraUtils.reinforce("data")`

#### **6. Base64 Encoding and Decoding**
- **`defTest.b64encode(text)`**
  - **Purpose**: Encodes text in a custom Base64 format.
  - **Usage**: `encoded = UltraUtils.defTest.b64encode("Hello")`

- **`defTest.b64decode(data)`**
  - **Purpose**: Decodes custom Base64 encoded data.
  - **Usage**: `decoded = UltraUtils.defTest.b64decode(encoded)`

#### **7. Alien Encryption**
- **`alien_encrypt(text)`**
  - **Purpose**: Encrypts text using a custom algorithm and Base85 encoding.
  - **Usage**: `alien_encrypted = UltraUtils.alien_encrypt("Hello")`

- **`alien_decrypt(text)`**
  - **Purpose**: Decrypts text encrypted with `alien_encrypt`.
  - **Usage**: `alien_decrypted = UltraUtils.alien_decrypt(alien_encrypted)`

#### **8. XOR Encryption**
- **`xor_encrypt(text, key)`**
  - **Purpose**: Encrypts text using XOR with a key.
  - **Usage**: `xor_encrypted = UltraUtils.xor_encrypt("Hello", "key")`

- **`xor_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `xor_encrypt`.
  - **Usage**: `xor_decrypted = UltraUtils.xor_decrypt(xor_encrypted, "key")`

#### **9. Caesar Cipher**
- **`caesar_encrypt(text, shift)`**
  - **Purpose**: Encrypts text using a Caesar cipher with a specified shift.
  - **Usage**: `caesar_encrypted = UltraUtils.caesar_encrypt("Hello", 3)`

- **`caesar_decrypt(text, shift)`**
  - **Purpose**: Decrypts text encrypted with `caesar_encrypt`.
  - **Usage**: `caesar_decrypted = UltraUtils.caesar_decrypt(caesar_encrypted, 3)`

#### **10. Vigenère Cipher**
- **`vigenere_encrypt(plaintext, key)`**
  - **Purpose**: Encrypts text using the Vigenère cipher.
  - **Usage**: `vigenere_encrypted = UltraUtils.vigenere_encrypt("Hello", "key")`

- **`vigenere_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `vigenere_encrypt`.
  - **Usage**: `vigenere_decrypted = UltraUtils.vigenere_decrypt(vigenere_encrypted, "key")`

#### **11. Hashing Functions**
- **`hash_md5(data)`**
  - **Purpose**: Returns the MD5 hash of the data.
  - **Usage**: `md5_hash = UltraUtils.hash_md5("data")`

- **`hash_sha1(data)`**
  - **Purpose**: Returns the SHA-1 hash of the data.
  - **Usage**: `sha1_hash = UltraUtils.hash_sha1("data")`

- **`hash_sha512(data)`**
  - **Purpose**: Returns the SHA-512 hash of the data.
  - **Usage**: `sha512_hash = UltraUtils.hash_sha512("data")`

- **`hash_blake2b(data)`**
  - **Purpose**: Returns the BLAKE2b hash of the data.
  - **Usage**: `blake2b_hash = UltraUtils.hash_blake2b("data")`

#### **12. Custom Base64 Encryption**
- **`custom_base64_encrypt(text)`**
  - **Purpose**: Encrypts text using a custom Base64 method.
  - **Usage**: `custom_encrypted = UltraUtils.custom_base64_encrypt("Hello")`

- **`custom_base64_decrypt(text)`**
  - **Purpose**: Decrypts text encrypted with `custom_base64_encrypt`.
  - **Usage**: `custom_decrypted = UltraUtils.custom_base64_decrypt(custom_encrypted)`

#### **13. Digit Rotation**
- **`rotate_digits_encrypt(num)`**
  - **Purpose**: Encrypts a number by rotating its digits.
  - **Usage**: `rotated_encrypted = UltraUtils.rotate_digits_encrypt(1234)`

- **`rotate_digits_decrypt(num)`**
  - **Purpose**: Decrypts a number rotated by `rotate_digits_encrypt`.
  - **Usage**: `rotated_decrypted = UltraUtils.rotate_digits_decrypt(rotated_encrypted)`

#### **14. Feistel Network**
- **`feistel_encrypt(text, rounds=4, key=0xAB)`**
  - **Purpose**: Encrypts text using a Feistel network.
  - **Usage**: `feistel_encrypted = UltraUtils.feistel_encrypt("Hello")`

- **`feistel_decrypt(ciphertext, rounds=4, key=0xAB)`**
  - **Purpose**: Decrypts text encrypted with `feistel_encrypt`.
  - **Usage**: `feistel_decrypted = UltraUtils.feistel_decrypt(feistel_encrypted)`

#### **15. Multi-Stage Encryption**
- **`multi_stage_encrypt(text, key)`**
  - **Purpose**: Encrypts text using multiple methods.
  - **Usage**: `multi_stage_encrypted = UltraUtils.multi_stage_encrypt("Hello", "key")`

- **`multi_stage_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `multi_stage_encrypt`.
  - **Usage**: `multi_stage_decrypted = UltraUtils.multi_stage_decrypt(multi_stage_encrypted, "key")`

#### **16. Ultra Unique Encryption**
- **`ultra_unique_encrypt(text, key)`**
  - **Purpose**: Encrypts text using a unique method based on a key.
  - **Usage**: `unique_encrypted = UltraUtils.ultra_unique_encrypt("Hello", "key")`

- **`ultra_unique_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `ultra_unique_encrypt`.
  - **Usage**: `unique_decrypted = UltraUtils.ultra_unique_decrypt(unique_encrypted, "key")`

#### **17. Polyalphabetic Progressive Encryption**
- **`polyalphabetic_progressive_encrypt(text, key)`**
  - **Purpose**: Encrypts text using a progressive polyalphabetic method.
  - **Usage**: `progressive_encrypted = UltraUtils.polyalphabetic_progressive_encrypt("Hello", "key")`

- **`polyalphabetic_progressive_decrypt(text, key)`**
  - **Purpose**: Decrypts text encrypted with `polyalphabetic_progressive_encrypt`.
  - **Usage**: `progressive_decrypted = UltraUtils.polyalphabetic_progressive_decrypt(progressive_encrypted, "key")`

#### **18. Bit Permutation Encryption**
- **`bit_permutation_encrypt(text, key)`**
  - **Purpose**: Encrypts text using bit permutation based on a key.
  - **Usage**: `bit_permuted_encrypted = UltraUtils.bit_permutation_encrypt("Hello", "key")`

- **`bit_permutation_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `bit_permutation_encrypt`.
  - **Usage**: `bit_permuted_decrypted = UltraUtils.bit_permutation_decrypt(bit_permuted_encrypted, "key")`

#### **19. Hybrid Advanced Encryption**
- **`hybrid_advanced_encrypt(text, key)`**
  - **Purpose**: Encrypts text using a hybrid method.
  - **Usage**: `hybrid_encrypted = UltraUtils.hybrid_advanced_encrypt("Hello", "key")`

- **`hybrid_advanced_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `hybrid_advanced_encrypt`.
  - **Usage**: `hybrid_decrypted = UltraUtils.hybrid_advanced_decrypt(hybrid_encrypted, "key")`

#### **20. Alpha-Numeric Encryption**
- **`alpha_numeric_encrypt(num, key='K3Y')`**
  - **Purpose**: Encrypts a number into an alphanumeric string.
  - **Usage**: `alpha_numeric_encrypted = UltraUtils.alpha_numeric_encrypt(1234)`

- **`alpha_numeric_decrypt(enc_str, key='K3Y')`**
  - **Purpose**: Decrypts an alphanumeric string back into a number.
  - **Usage**: `alpha_numeric_decrypted = UltraUtils.alpha_numeric_decrypt(alpha_numeric_encrypted)`

#### **21. Ultra Hyper Encryption**
- **`ultra_hyper_encrypt(text, key)`**
  - **Purpose**: Encrypts text using a complex method.
  - **Usage**: `hyper_encrypted = UltraUtils.ultra_hyper_encrypt("Hello", "key")`

- **`ultra_hyper_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `ultra_hyper_encrypt`.
  - **Usage**: `hyper_decrypted = UltraUtils.ultra_hyper_decrypt(hyper_encrypted, "key")`

#### **22. Sequential Custom Encryption**
- **`sequential_custom_encrypt(text, key)`**
  - **Purpose**: Encrypts text using a sequential custom method.
  - **Usage**: `sequential_encrypted = UltraUtils.sequential_custom_encrypt("Hello", "key")`

- **`sequential_custom_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `sequential_custom_encrypt`.
  - **Usage**: `sequential_decrypted = UltraUtils.sequential_custom_decrypt(sequential_encrypted, "key")`

#### **23. Dynamic Positional Encryption**
- **`dynamic_positional_encrypt(text, key)`**
  - **Purpose**: Encrypts text using dynamic positional methods.
  - **Usage**: `dynamic_encrypted = UltraUtils.dynamic_positional_encrypt("Hello", "key")`

- **`dynamic_positional_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts text encrypted with `dynamic_positional_encrypt`.
  - **Usage**: `dynamic_decrypted = UltraUtils.dynamic_positional_decrypt(dynamic_encrypted, "key")`

#### **24. Complex Text Number Encryption**
- **`complex_text_number_encrypt(text, key)`**
  - **Purpose**: Encrypts text into a complex number format.
  - **Usage**: `complex_encrypted = UltraUtils.complex_text_number_encrypt("Hello", "key")`

- **`complex_text_number_decrypt(ciphertext, key)`**
  - **Purpose**: Decrypts complex number format back into text.
  - **Usage**: `complex_decrypted = UltraUtils.complex_text_number_decrypt(complex_encrypted, "key")`

### **defTest**
- **`defTest.b64encode(text)`**
  - **Purpose**: Encodes text in a custom Base64 format with a random pattern.
  - **Usage**: `encoded = UltraUtils.defTest.b64encode("Hello")`

- **`defTest.b64decode(data)`**
  - **Purpose**: Decodes custom Base64 encoded data.
  - **Usage**: `decoded = UltraUtils.defTest.b64decode(encoded)`

### **EncNew Encrypt File**
- **`EncNew()`**
  - **Purpose**: Encrypts the file with the strongest encryption methods. 
  - **Usage**: EncNew('File.py')
### **upload_and_run**
- **`upload_and_run`**
  - **Purpose**: Run Python bots forever 
  - **Usage**: upload_and_run('Bot.py')

### **1. `def dump(obj, file, protocol=None, buffer_callback=None)`**
- **Purpose**: Serializes an object and writes it to a file using the specified protocol.
- **Parameters**:
  - `obj`: The object to be serialized.
  - `file`: A file-like object where the serialized data will be written.
  - `protocol`: The protocol version to use for serialization (default is `pickle.HIGHEST_PROTOCOL`).
  - `buffer_callback`: Optional callback for handling buffer data.
- **Usage**:
  ```python
  with open('data.pkl', 'wb') as f:
      dump(my_object, f)
  ```

### **2. `def dumps(obj, protocol=None, buffer_callback=None)`**
- **Purpose**: Serializes an object and returns it as a byte string.
- **Parameters**:
  - `obj`: The object to be serialized.
  - `protocol`: The protocol version to use for serialization (default is `pickle.HIGHEST_PROTOCOL`).
  - `buffer_callback`: Optional callback for handling buffer data.
- **Usage**:
  ```python
  serialized_data = dumps(my_object)
  ```

### **3. `def load(file)`**
- **Purpose**: Deserializes an object from a file.
- **Parameters**:
  - `file`: A file-like object containing the serialized data.
- **Usage**:
  ```python
  with open('data.pkl', 'rb') as f:
      my_object = load(f)
  ```

### **4. `def loads(data)`**
- **Purpose**: Deserializes an object from a byte string.
- **Parameters**:
  - `data`: A byte string containing the serialized data.
- **Usage**:
  ```python
  my_object = loads(serialized_data)
  ```

### **Example Usage**
Here’s a complete example demonstrating how to use these methods:

```python
import pickle

# Example object to serialize
my_object = {'key': 'value', 'number': 42}

# Serialize and save to a file
with open('data.pkl', 'wb') as f:
    dump(my_object, f)

# Serialize to a byte string
serialized_data = dumps(my_object)

# Deserialize from the file
with open('data.pkl', 'rb') as f:
    loaded_object = load(f)

# Deserialize from the byte string
loaded_from_bytes = loads(serialized_data)

# Check results
print(loaded_object)        # Output: {'key': 'value', 'number': 42}
print(loaded_from_bytes)    # Output: {'key': 'value', 'number': 42}
```
- The `dump` and `dumps` methods are used for serialization, while `load` and `loads` are used for deserialization.
- These methods allow you to easily save and retrieve Python objects, making it convenient for data persistence and transfer.
################
Made By In Iraq ~ Team Nexia
################
`Thank You`
`Create By Team Nexia`