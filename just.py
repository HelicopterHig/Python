import os

print ("Great Python")
print ("Hello Programmer")
name = input("Name: ")

print(name, ", Welcome,")

answer = input(" Have you work? (Y/N)")

if answer == 'Y':
	print("OK, let's go!")
	print("I can:")
	print(" [1] - list files")
	print(" [2] - list information about the sysytem")
	do = int(input("Enter the number:"))

	if do == 1:
		print(os.listdir())
	elif do == 2:
		pass
	else:
		pass

elif answer =='N':
	print("Goodbye!")
else:
	print("Unknown number")
