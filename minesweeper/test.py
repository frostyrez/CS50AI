# def main():
#     result = surr(0)
#     print(result)
#     print(type(result))

# def surr(cell):
#     ret1 = [cell,1]
#     ret2 = [cell,2]
#     return [ret1,ret2]

# main()
# cell = [1,1]
# width = 2
# height = 2

# if cell[0] == 0:
#     rangei = [0,1]
# elif cell[0] == width-1:
#     rangei = [-1,0]
# else:
#     rangei = [-1,1]

# if cell[1] == 0:
#     rangej = [0,1]
# elif cell[1] == height-1:
#     rangej = [-1,0]
# else:
#     rangej = [-1,1]

# surrcells = set()
# for i in rangei:
#     for j in rangej:
#         surrcells.add([i,j])
# surrcells.remove([0,0])
# print(surrcells)

test = set()
test.add((0,1))
test.add((1,2))
test.add((2,3))

test2 = set()
test2.add((3,4))
test2.add((2,3))

test3 = set(test.intersection(test2))

print(type(test3))