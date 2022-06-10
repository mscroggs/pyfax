with open(".coveralls_output") as f:
    cov = int(f.read().split("TOTAL")[-1].split("%")[0].split(" ")[-1])
    print(f"Coverage is {cov}%")
    assert cov >= 80
