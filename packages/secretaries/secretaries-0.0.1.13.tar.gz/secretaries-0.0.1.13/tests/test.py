import sys

from secretaries import secretary as s

meh = s.run("Bo Lund vill bo i Lund",
      ambiguous = "bo lund".split())

print(meh)

sys.exit(0)
