src = open("tokens.txt", "r")
tokens = src.read().splitlines()
src.close()
dst = open("tokens.py", "w")

dst.write("# Generated from tokens.txt\n\n")

for token in tokens:
    if token == '':
        dst.write("\n")
        continue
    dst.write(f"{token} = '{token}'\n")

dst.write("\n")

dst.write("tokens = {\n")

for token in tokens:
    if token == '':
        dst.write("\n")
        continue
    dst.write(f"    {token},\n")

dst.write("}\n")

dst.close()