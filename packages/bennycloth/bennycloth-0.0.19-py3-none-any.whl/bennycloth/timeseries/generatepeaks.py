def GeneratePeaks(values,tensionOnly=False,compressionOnly=False):
    N = len(values)
    if N < 1:
        return []
    
    t = [0]
    f = [0]

    for i in range(N):
        a = values[i]

        if not compressionOnly:
            t.append(t[-1]+a)
            f.append(a)
            t.append(t[-1]+a)
            f.append(0)
        if not tensionOnly:
            t.append(t[-1]+a)
            f.append(-a)
            t.append(t[-1]+a)
            f.append(0)

    return t,f

if __name__ == '__main__':
    t,f = GeneratePeaks([1,2],compressionOnly=True)
    print(t)
    print(f)
