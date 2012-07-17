# import bpy

filename = 'siggraphSpacecraft70.igs'
file_in_mem = open(filename)

def makeDiv(input):
	return input.center(80, '-')

# strips newlines while appending to lines list.
lines = []
for line in file_in_mem:
	lines.append(line[:-1])


for line in lines[:10]:
	print(line)
	







