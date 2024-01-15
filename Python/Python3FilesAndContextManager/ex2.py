def read_n_lines(path, n):
    with open(path, 'r') as file:
        lines = []
        for i in range(n):
            line = file.readline()
            if not line:
                break
            lines.append(line.rstrip('\n'))
        return lines
