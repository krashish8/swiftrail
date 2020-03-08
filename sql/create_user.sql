INSERT INTO users VALUES (1, 'ashish@gmail.com', 'ashish', AES_ENCRYPT('Password123', 'secret'), 'Ashish', 'Kumar', 'm', '2000-01-01', 'India', '6205144592', 'C.V. Raman Hostel');
SELECT AES_DECRYPT(password, 'secret') AS password FROM users;
