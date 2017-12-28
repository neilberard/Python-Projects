import pymel.core as pymel
import timeit
start_time = timeit.default_timer()

print  9**3

def is_prime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n%f == 0: return False
    if n%(f+2) == 0: return False
    f +=6
  return True

prime_numbers = []

for i in range(10000):
    prime = is_prime(i)
    if prime:
        prime_numbers.append(i)


elapsed = timeit.default_timer() - start_time

print elapsed, "duration"
print prime_numbers