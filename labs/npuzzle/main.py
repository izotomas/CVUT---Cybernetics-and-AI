import npuzzle

p = npuzzle.NPuzzle(3)
p.visualise()
tile = p.read_tile(1, 2)
print(tile)
p.reset()
p.visualise()
try:
    p.read_tile(3, 3)
except IndexError:
    print('index eror test passed')
