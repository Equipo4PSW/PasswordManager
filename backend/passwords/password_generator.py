import random
   
def generate_pasword(size:int,a:bool,A:bool,n:bool,symbols:str="!@$%^*&-_+#=:;,.?/"):
    minus = "abcdefghijklmnopqrstuvwxyz"
    mayus = minus.upper()
    nums = "0123456789"
    
    base = ""
    if(a):
        base += minus
    if(A):
        base +=  mayus
    if(n):
        base += nums
    base += symbols
    
    has_lowercase = not a
    has_uppercase = not A
    has_digit = not n
    
    if len(symbols) == 0:
        while(has_lowercase!=a and has_uppercase!=A and has_digit!=n):
            sample = random.sample(base,size)
            password = "".join(sample)
            has_lowercase = any(char.islower() for char in password)
            has_uppercase = any(char.isupper() for char in password)
            has_digit = any(char.isdigit() for char in password)
    
    else:
        has_special = False
        while(has_lowercase!=a and has_uppercase!=A and has_digit!=n and not has_special):
            sample = random.sample(base,size)
            password = "".join(sample)
            has_lowercase = any(char.islower() for char in password)
            has_uppercase = any(char.isupper() for char in password)
            has_digit = any(char.isdigit() for char in password)
            has_special = any(char in symbols for char in password)
    
    
    return password


#Example
'''
for _ in range(100):
    print(generate_pasword(15,True,True,True))
'''