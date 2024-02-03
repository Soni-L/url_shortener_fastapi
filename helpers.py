def checkShortCodeCharValidity(shortcode):
    isValid = True
    for element in shortcode:
        if(not(element.isalnum() or element == '_')):
            isValid = False
    return isValid

def isValidShortCode(shortcode):
    if len(shortcode) != 6:
        return False
    else:
        return checkShortCodeCharValidity(shortcode)
    

