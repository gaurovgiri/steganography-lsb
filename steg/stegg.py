import cv2
from cryptography.fernet import Fernet

class stegg:

    def __init__(self) -> None:
        try:
            with open('secret.txt', 'r') as f:
                key = f.readline()
                self.cipher = Fernet(str.encode(key))
        except BaseException:
            with open('secret.txt', 'w') as f:
                key = Fernet.generate_key()
                f.write(key.decode())
                self.cipher = Fernet(key)

    def stegencode(self, image_input_path, msg, image_output_path):
        img = cv2.imread(image_input_path)
        text = self.cipher.encrypt(str.encode(msg))
        text_length = len(text)
        if (text_length * 8) > (img.shape[0] * img.shape[1]):
            print("Need Image of Bigger size") #Create an exception for this
            exit(-1)

        text_length_bits = iter(format(text_length, 'b').zfill(8))
        text_byte = iter([format(char, 'b').zfill(8)] for char in text)

        # Storing Length of the message:
        try:
            for i in range(1,5):
                for j in range(1,3):
                    current_bit = next(text_length_bits)
                    image_byte = list(format(img[-i][-j][0], 'b').zfill(8))
                    image_byte.pop()
                    image_byte.append(current_bit)
                    image_byte = int(''.join(image_byte), 2)
                    img[-i][-j][0] = image_byte
        except BaseException:
            print("Error Occurred!")

        # Storing the message to the image:
        try:
            for i in range(text_length):
                current_byte = next(text_byte)[0]
                for j in range(8):
                    bytes_to_be_used = list(format(img[i][j][0], 'b').zfill(8))
                    bytes_to_be_used.pop()
                    bytes_to_be_used.append(current_byte[j])
                    bytes_to_be_used = int(''.join(bytes_to_be_used), 2)
                    img[i][j][0] = bytes_to_be_used

            cv2.imwrite(image_output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            print("Encoded Successfully!")

        except StopIteration:
            print("Error Occurred")

    def stegdecode(self, image_path):
        image = cv2.imread(image_path)

        # Extracting the length of the message:
        try:
            msg_len = []
            for i in range(1,5):
                for j in range(1,3):
                    len_bytes = list(format(image[-i][-j][0], 'b').zfill(8))
                    msg_len.append(len_bytes[-1])
            msg_len = int(''.join(msg_len), 2)
            print(msg_len)
        except BaseException:
            print("Error Occurred during Extraction of Message Length")

        # Extracting the message from the image:
        try:
            msg = []
            for i in range(msg_len):
                data = []
                for j in range(8):
                    required_bytes = list(format(image[i][j][0], 'b').zfill(8))
                    data.append(required_bytes[-1])
                msg.append(int(''.join(data), 2))

            message = ''.join([chr(char) for char in msg])

            decoded_message = self.cipher.decrypt(str.encode(message))

            print(decoded_message.decode())

        except Exception:
            print("Error Occured During Decoding!")


stegging = stegg()
