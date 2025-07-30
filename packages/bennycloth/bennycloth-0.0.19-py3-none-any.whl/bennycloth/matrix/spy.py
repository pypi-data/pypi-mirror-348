import numpy as np
import openseespy.opensees as ops

def Spy():
    Neqn = ops.systemSize()

    if Neqn < 1:
        print('Number of equations is zero')
        return [[],0];

    SpyMatrix = np.identity(Neqn)

    for e in ops.getEleTags():
        dofs = []
        for nd in ops.eleNodes(e):
            dofs += ops.nodeDOFs(nd)

        for idof in dofs:
            if idof < 0:
                continue
            for jdof in dofs:
                if jdof < 0:
                    continue
                SpyMatrix[idof,jdof] = 1.0

    bw = 0
    for i in range(Neqn):
        bwi = 0
        for j in range(i,Neqn):
            kij = SpyMatrix[i,j]
            if kij != 0.0:
                bwi = j-i+1
        if bwi > bw:
            bw = bwi

    #plt.spy(SpyMatrix,markersize=.05)
    return [SpyMatrix,bw]


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import openseespy.opensees as ops

    N = 50
    ops.wipe()
    ops.model('basic','-ndm',1,'-ndf',1)

    ops.node(0,0); ops.fix(0,1)

    ops.uniaxialMaterial('Elastic',1,1.0)
    for i in range(1,N+1):
        ops.node(i,0)
        ops.element('zeroLength',i,i-1,i,'-mat',1,'-dir',1)

    ops.analysis('Static','-noWarnings')
    ops.analyze(1)

    SpyMatrix,bw = Spy()

    plt.spy(SpyMatrix)
    plt.title(f'Bandwidth = {bw}')
    plt.tight_layout()
    plt.show()
