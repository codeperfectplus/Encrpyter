""" Python script to encrpyt/decrypt files using Fernet encryption algorithm


    Usage:
        python script.py -t encrypt -i <file/directory>
        python script.py -t decrypt -i <file/directory>

    Example:
        python script.py -t encrypt -i test.txt
        python script.py -t decrypt -i test.txt.encrypted
        python script.py -t encrypt -i test_dir
        python script.py -t decrypt -i test_dir

    Note:
        1. If you are encrypting a directory, all the files in the directory will be encrypted
        2. If you are decrypting a directory, all the files in the directory will be decrypted


 """
from cryptography.fernet import Fernet
import os
import argparse
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_or_read_key():  
    key = Fernet.generate_key()
    if not os.path.exists('filekey.key'):
        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)

        return key
    else:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()

        return key


fernet = Fernet(generate_or_read_key())


# todo: add option to encrypt/decrypt based on file extension  (eg: encrypt all .txt files in a directory)
def encrypt_file(input_dir, filename, file_extension=None):

    if filename.endswith('.encrypted'):
        return 

    if file_extension is not None:
        if not filename.endswith(file_extension):
            return

    output_file_path = os.path.join(input_dir, filename + ".encrypted")
    with open(os.path.join(input_dir, filename), 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(output_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    os.remove(os.path.join(input_dir, filename))


def decrypt_file(input_dir, filename):
    if filename.endswith(".encrypted"):
        output_file_path = os.path.join(input_dir, filename.replace(".encrypted", ""))
        with open(os.path.join(input_dir, filename), 'rb') as file:
            original = file.read()

        decrypted = fernet.decrypt(original)

        with open(output_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        os.remove(os.path.join(input_dir, filename))



def parser():
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt files")
    parser.add_argument("-t", "--type", help="encrypt or decrypt")
    parser.add_argument("-i", "--input", help="input file or directory")
    args = parser.parse_args()

    return args


def main():
    opt = parser()

    input_dir = opt.input
    action_type = opt.type

    # check if file/directory exists in source directory action type is encrypt/decrypt

    if not os.path.exists(input_dir):
        print("Input file/directory does not exist")
        return
    
    if action_type != "encrypt" and action_type != "decrypt":
        print("Action type should be encrypt or decrypt")
        return


    if action_type == "encrypt":
        if os.path.isfile(input_dir):
            print("Encrypting file: " + input_dir)
            encrypt_file(os.path.dirname(input_dir), os.path.basename(input_dir))
        else:
            print("Encrypting directory: " + input_dir)
            for filename in os.listdir(input_dir):
                encrypt_file(input_dir, filename)

    elif action_type == "decrypt":
        if os.path.isfile(input_dir):
            print("Decrypting file: " + input_dir)
            decrypt_file(os.path.dirname(input_dir), os.path.basename(input_dir))
        else:
            print("Decrypting directory: " + input_dir)
            for filename in os.listdir(input_dir):
                decrypt_file(input_dir, filename)


if __name__ == "__main__":
    main()