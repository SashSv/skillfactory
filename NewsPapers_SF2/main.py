x = []
objects = [1, 2, 1, 2, 3]

for obj in objects:
    if len(x) == 0:
        x.append(obj)
    else:
        if obj not in objects:
            x.append(obj)


print(set(x))