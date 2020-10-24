def message():
    return('Enter a message: ')

def message_for_the_key():
    return('Enter a key between 1 and 25 : ')

print('''
'e' to encode a string
'd' to decode a string
'd+' to decode a string (extension)
'q' to quit
''')

command = input('Command to run : ')

# ---------------- Encoding ------------------ #

if command == 'e' or command == 'E':
    #Verify the message is in lower case and the key is an integer between 1 and 25
    message = input(message()).lower()
    while True:
        try:
            key = int(input(message_for_the_key()))
            if key < 1 or key > 25:
                key = int(input(message_for_the_key()))
            elif key > 0 and key < 26:
                break
        except:
            continue
            
    ALPHABET='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    index = 0
    n = 0
    final_word = ''
    
    #For each letter find the position in the alphabet and find the corresponding letter with the shift value
    #The corresponding letter is stored and displayed as a final encoded word
    while index < len(message):
        try:
            message_finder = ALPHABET.index(message[n])
        except:
            message_finder = message[n]
                
        try:
            letter_message_finder = ALPHABET[message_finder]
        except:
            letter_message_finder = message[n]

        try:
            key_finder = ALPHABET.index(ALPHABET[message_finder + key])
        except:
            key_finder = message[n]
            
        try:
            letter_key_finder = ALPHABET[key_finder]
        except:
            letter_key_finder = message[n]

        n += 1
        index += 1

        final_word = final_word + letter_key_finder

    print('Final word =', final_word)


# ---------------- Decoding ------------------ #

elif command == 'd' or command == 'D':
    #Verify the message is in lower case and the key is an integer between 1 and 25
    message = input(message()).lower()
    while True:
        try:
            key = int(input(message_for_the_key()))
            if key < 1 or key > 25:
                key = int(input(message_for_the_key()))
            elif key > 0 and key < 26:
                break
        except:
            continue
        
    ALPHABET='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    index = 0
    n = 0
    final_word = ''

    #For each letter find the position in the alphabet and find the corresponding letter minus the shift value
    #The corresponding letter is stored and displayed as a final decoded word
    while index < len(message):         
        try:
            message_finder = ALPHABET.index(message[n])
        except:
            message_finder = message[n]
                
        try:
            letter_message_finder = ALPHABET[message_finder]
        except:
            letter_message_finder = message[n]

        try:
            key_finder = ALPHABET.index(ALPHABET[message_finder - key])
        except:
            key_finder = message[n]
            
        try:
            letter_key_finder = ALPHABET[key_finder]
        except:
            letter_key_finder = message[n]

        n += 1
        index += 1
        final_word = final_word + letter_key_finder

    print('Encoded string : ', message)
    print('Decoded string : ', final_word)


# ---------------- Decoding (extension) ------------------ #

elif command == 'd+' or command == 'D+':
    
    message = input(message()).lower()
    plain_text = input('Enter plain-text : ')
    ALPHABET='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    final_word = ''
    word = ''
    index = 1
    b = 0

    #apply to each character of the message of shift value of b to decode the message
    #Same code as the decoding part but with a b beggining at 1 and finishing at 26
    while b < 27 and plain_text not in final_word:
        for letter in message:
            try:
                letter_finder = ALPHABET.index(letter[0])
            except:
                letter_finder = letter[0]

            try:
                second_letter_finder = ALPHABET[letter_finder - (b)]
            except:
                second_letter_finder = letter[0]
                
            final_word = final_word + second_letter_finder
            
        b += 1
        final_word = final_word + second_letter_finder

    #When the plain text appear in the final decoded message
    #The b value allowing the previous message to be decoded is stored
    #The previous decoding algorithm is used with the new b
    if plain_text in final_word:
        c = b-1
        index = 0
        n = 0
        key = c
        final_word = ''
        #Previous decoding algorithm
        while index < len(message):         
            try:
                message_finder = ALPHABET.index(message[n])
            except:
                message_finder = message[n]
                    
            try:
                letter_message_finder = ALPHABET[message_finder]
            except:
                letter_message_finder = message[n]

            try:
                key_finder = ALPHABET.index(ALPHABET[message_finder - key])
            except:
                key_finder = message[n]
                
            try:
                letter_key_finder = ALPHABET[key_finder]
            except:
                letter_key_finder = message[n]

            n += 1
            index += 1
            final_word = final_word + letter_key_finder

        print('Encoded string : ', message)
        print('Decoded string : ', final_word)

# ---------------- End of the program ------------------ #

elif command == 'q' or command == 'Q':
    print()
    print('----- End of the program -----')
    print()

#REFERENCES:
#Every classes of Programming Principles 1 at the University of Westminster - Semester 1 - London, UK (2018-2019)
