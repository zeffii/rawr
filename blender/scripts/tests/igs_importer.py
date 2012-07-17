# import bpy

filename = 'siggraphSpacecraft70.igs'
file_in_mem = open(filename)

file_structure = []

counter = 0
situa = True

def makeDiv(input):
	return input.center(80, '-')


# section 1
print(makeDiv('header'))
while(situa):
	current_line = file_in_mem.readline()
	if current_line[0] is not ' ':
		current_line = current_line.replace('\n','')
		print(current_line)
	counter += 1

	if counter > 3:
		situa = False

# section 2
print(makeDiv('declarations'))
print(file_in_mem.readline())