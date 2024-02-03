import random
import string

def checkShortCodeCharValidity(shortcode):
    isValid = True
    for element in shortcode:
        if(not(element.isalnum() or element == '_')):
            isValid = False
    return isValid

def generate_random_alphanumeric_or_underscore():
    # Define the pool of characters (alphanumeric + underscore)
    pool = string.ascii_letters + string.digits + '_'
    
    # Generate a random character from the pool
    random_char = random.choice(pool)
    
    return random_char

def isValidShortCode(shortcode):
    if len(shortcode) != 6:
        return False
    else:
        return checkShortCodeCharValidity(shortcode)
    

def generateRandomShortCode():
    randomCode = '' 
    for char in range(6):
        randomChar = generate_random_alphanumeric_or_underscore()
        randomCode = randomCode + randomChar
    return randomCode
