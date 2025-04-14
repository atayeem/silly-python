from ctypes import CDLL

lib = CDLL('libc.so.6')
toupper = lib.toupper
tolower = lib.tolower

def evenOrOdd(n):
  # Odd:  False
  # Even: True
  return not bool(n % 2)

def formatName(n):
  if len(n) == 0:
      print("\033[31;1mNo name entered!\033[0")
      exit()
  out = ""
  
  out += chr(toupper(ord(n[0])))
    
  for i in range(1, len(n)):
    out += chr(tolower(ord(n[i])))
    
  return out


num = input("Please enter a number\n")
if num == '':
    print("\033[31;1mNo number entered!\033[0m")
    exit()
    
try:
    num = int(num)
except ValueError:
    print("\033[31;1mInvalid number!\033[0m")
    exit()
print(num, "is" + " not" * evenOrOdd(num), "odd")
    
print()

name = input("Please enter a name\n")
print(formatName(name))
