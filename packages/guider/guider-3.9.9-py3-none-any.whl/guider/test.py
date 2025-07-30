import time

s = "hello_world!!!"

# rstrip() 성능 테스트
start = time.perf_counter()
for _ in range(10**8):
    s.rstrip("!")
end = time.perf_counter()
print(f"rstrip: {end - start:.6f} sec")

# removesuffix() 성능 테스트
start = time.perf_counter()
for _ in range(10**8):
    s.removesuffix("!!!")
end = time.perf_counter()
print(f"removesuffix: {end - start:.6f} sec")
