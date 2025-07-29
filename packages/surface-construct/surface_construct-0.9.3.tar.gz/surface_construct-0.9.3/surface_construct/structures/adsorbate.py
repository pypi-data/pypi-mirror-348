import numpy as np
from ase import Atoms

class Adsorbate:
    """
    吸附分子的类，包含质心，内坐标，主轴
    """
    def __init__(self, atoms, **kwargs):
        # TODO：加上半径的参数，计算分子半径
        self.atoms = atoms
        self.internal_coords = dict()
        self.kwargs = kwargs
        self._rads = 0.76 # 默认是碳原子的共价半径

    @property
    def com(self):
        return self.atoms.center_of_mass()

    @property
    def principal_axis(self):
        # 分子主轴向量
        evals, evecs = self.atoms.get_moments_of_inertia(vectors=True)
        return evecs[np.argmin(np.abs(evals))]

    @property
    def rads(self):
        # 分子的半径，sg_obj 构造时作为参考
        # TODO: 计算分子半径
        return self._rads

    @rads.setter
    def rads(self, value):
        self._rads = value

    @property
    def natoms(self):
        return len(self.atoms)

