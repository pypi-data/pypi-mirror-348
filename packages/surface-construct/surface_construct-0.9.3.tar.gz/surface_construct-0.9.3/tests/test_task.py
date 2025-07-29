import os
import shutil
from random import randint

import ase.io
import pytest
from lasp_ase.lasp import Lasp
from surface_construct import SurfaceGrid
from surface_construct.structures import AdsGridCombiner
from surface_construct.structures.adsorbate import Adsorbate
from surface_construct.tasks import SurfaceSiteSampleTask
from ase.optimize import LBFGS, BFGS


class TestSurfaceSiteSampling:
    """
    Simple Ru 0001 suface
    """
    def setup_method(self):
        self.task_dir = '%x' % randint(16**3, 16**4 - 1)
        if not os.path.exists(self.task_dir):
            os.makedirs(self.task_dir)
        os.chdir(self.task_dir)

    def teardown_method(self):
        os.chdir("../")
 #       if os.path.exists(self.task_dir):
 #           shutil.rmtree(self.task_dir)

    def test_job1(self):
        """
        C atom on Ru(0001) surface
        :return:
        """
        shutil.copyfile('../atoms_files/RuCHO_lasp.in', 'lasp.in')
        shutil.copyfile('../atoms_files/RuCHO_pf2.pot', 'RuCHO.pot')
        atoms = ase.io.read('../atoms_files/ru_0001_POSCAR')
        atoms.calc = Lasp()
        ads_atoms = ase.Atoms('C',[[0.,0.,0.]])
        ads_obj = Adsorbate(ads_atoms)
        sg_obj = SurfaceGrid(atoms)
        ads_grid_comb = AdsGridCombiner(sg_obj, ads_obj)
        sampler =[
            {
                'size': 3,  # 采样大小
                'surface': "InitialSGSampler",  # 表面采样方法
            },  # 第一步采样
            {
                'size': 5,  # 采样大小
                'surface': ("MaxDiversitySGSampler", "MinEnergySGSampler", "MaxSigmaSGSampler"),  # 表面采样方法
                'weight': (0.1, 0.45, 0.45),  # 表面采样方法的权重
            }  # 第二步采样
        ]
        task_obj = SurfaceSiteSampleTask(combiner=ads_grid_comb, sampler=sampler, optimizer=BFGS)
        task_obj.run()
        print('Done')

    def test_job2(self):
        """
        H atom on CuO/Cu surface
        :return:
        """
        shutil.copyfile('../atoms_files/CuCHO_lasp.in', 'lasp.in')
        shutil.copyfile('../atoms_files/CuCHO.pot', 'CuCHO.pot')
        atoms = ase.io.read('../atoms_files/CuOx-Cu100-CONTCAR')
        atoms.calc = Lasp()
        ads_atoms = ase.Atoms('H',[[0.,0.,0.]])
        ads_obj = Adsorbate(ads_atoms)
        sg_obj = SurfaceGrid(atoms)
        ads_grid_comb = AdsGridCombiner(sg_obj, ads_obj)
        sampler =[
            {
                'surface': "KeyPointSGSampler",  # 表面采样方法
            },  # 第一步采样
            {
                'size': 3,  # 采样大小
                'surface': ("MaxDiversitySGSampler", "MinEnergySGSampler", "MaxSigmaSGSampler"),  # 表面采样方法
                'weight': (0.4, 0.3, 0.3),  # 表面采样方法的权重
            }  # 第二步采样
        ]
        task_obj = SurfaceSiteSampleTask(combiner=ads_grid_comb, sampler=sampler, optimizer=LBFGS)
        task_obj.run()
        print('Done')