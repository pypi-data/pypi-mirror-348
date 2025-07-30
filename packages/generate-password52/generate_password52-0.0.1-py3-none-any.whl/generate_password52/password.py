import random as rm

def p_a_s_s(num):
    str1 = '1234567890'
    str2 = 'qwertyuiopasdfghjklzxcvbnm'
    str3 = str2.upper()
    str4 = str1+str2+str3
    ls = list(str4)
    rm.shuffle(ls)
    psw = ''.join([rm.choice(ls) for x in range(num)])
    print(f'Password: {psw}')
