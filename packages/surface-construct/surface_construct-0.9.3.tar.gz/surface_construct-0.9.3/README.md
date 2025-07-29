# 催化剂表面位点和反应分子构象综合采样

催化剂构效关系是建立表面位点结构和反应过程势能面的关联关系，这依赖对表面上各种可能位点的充分分析和采样，找到这些位点对关键反应步骤的影响情况。从催化剂的角度看，研究的目标是从表面上存在的位点中找到表面最适合反应的位点，即使反应势能面最低的位点；从反应的角度看，研究目标是对于一系列反应通道，找到反应势能面上的卡点，找到能够突破卡点的催化环境。

本软件同时进行表面位点的构建、采样、计算、分析，和反应过程的分析采样，即过渡态和分子构象，由此可以实现分子在表面反应的全过程采样。其中的技术关键是采样的效率，我们针对性地使用综合使用了多样化的采样策略，保证表面各类型位点和关键位点的充分采样。



<img src="docs/birds_view.png" alt="表面位点全局分析" style="zoom:50%;" />



## 程序流程图  Program Workflow



![flowchart](docs/modules-计算流程.jpg)

## 重要的概念 Glossary

* 表面格点 Grid：以范德华或者共价键长等值面进行离散化得到，表现为 (xi, yi, zi) 三维坐标。

  ![Ru Grid](docs/Ru0001_grid.jpg)

* 表面向量 Vector：用来表征格点局部化学环境的向量表示方法，表现形式为 N 维的向量。

  * 本方法中我们使用正则化的距离向量表达，其中距离是与N个最近邻原子之间的距离。
  * 正则化是为了保证不同化学环境格点的区分度尽量大。我们这里使用距离的倒数作为正则化方法，即距离越远对化学环境的描述贡献越小。
  * 为了减小计算量，在进行向量操作之前要对向量进行降维。降维的标准是保证保留尽可能多的信息，默认信息丢失不超过 5%。

* 向量化 Vectorization:  将格点转化为向量的过程

  * 当前我们使用多点定位 Multilateration 进行向量化

    <img src="docs/multilateration.jpg" alt="multilateration" style="zoom:50%;" />

* 分层采样 Stratified sampling。根据“相似结构具有相似性质”的原理采样分层采样的策略对表面位点进行采样，降低计算量。

  ![stratified sampling](docs/stratified_sampling.jpg)

* 表面分子结构采样。表面的分子自由度分解为表面位点+分子姿态+分子內自由度。针对它们采用不同的采样策略。

  <img src="docs/adsorption_structure.jpg" alt="adsorption structure" style="zoom:50%;" />

## 安装 Installation

`pip install -U surface-construct`

## 使用方法 Tutorial

参考例子 CuO_Cu_interface_LASP

### [其他 ASE 优化算法](https://wiki.fysik.dtu.dk/ase/ase/optimize.html)

* BFGS, BFGSLineSearch, LBFGS, LBFGSLineSearch
* GPMin
* MDMin
* FIRE

各种优化算法的对比，参考[链接](https://wiki.fysik.dtu.dk/gpaw/devel/ase_optimize/ase_optimize.html)

**使用方法**

修改 `surface_reaction_sample.py` 其中的一行 

```
from ase.optimize import BFGS
```

改为

```
from ase.optimize import XXX as BFGS
```

注意：目前这只是权宜之计，后面会把相应的设置加入到 `parameter.py`

### Gaussian Process Regression 方法

高斯过程回归 GPR 的优点：

* 不仅可以返回回归函数，可以给出拟合的置信度。根据置信度，可以进行进一步差点，迭代进行可以系统地降低整个拟合误差。
* 可以灵活地选择 kernel 函数来适用于不同的场景。

GPR 最重要的参数是kernel的选择。根据格点向量的特点，我们使用添加噪音的 (RBF) (aka Gassian kernel, Squared Exponetial Kernel) kernel 函数：
$$
k(x_i,x_j)=\sigma^2 \exp(-{d(x_i,x_j)^2\over 2l^2}) + {noise\_level}
$$


其中 $l$ 代表 length scale, $\sigma ^2$ 是 output variance。 使用 scikit-learn 中的类进行构造，
$$
\text{Kernel = ConstantKernel}\times \text{RBF} + \text{WhiteKernel}
$$
其中 ConstantKernel 代表 output variance  $\sigma^2$, 因为 scikit-learn 内置的 RBF kernel 不包含这一项，WhiteKernel 将 noise_level 考虑进去，RBF 是 Radial Basis Function kernel。

**重要的参数**

* RBF kernel
  * Length Scale $l$：determines the length of the 'wiggles' in your function.  In general, you won't be able to extrapolate more than ℓ units away from your data. [^Duvenaud] 
  
    参考 [^BASC] 文献，此处我们设置实空间的 $l_{grid}=1 \text{\AA}$ ，变化范围[0.5, 2.0]，转化为向量空间的长度[^向量空间转化]。根据实际情况，我们使用非对称 anisotropic 的 RBF。
* Constant kernel

  * GPR 在训练之前将 y 数值进行正则化，因而此处设置为 1.0，且训练过程中不变化。

* White kernel

  * noise level 是一个经验的参数。根据 DFT 吸附和过渡态的常见误差的量级为 0.1 eV，将此数值绝对值定为 0.1。设置时需要根据 y 正则化的系数进行缩放。在拟合过程中，keep fixed。

* GPR

  * $\alpha$：参数用于防止过拟合，根据经验设置为 $10^{-5}$。 
  * n_restarts_optimizer：9，经验选择。
  * 其他数值使用默认值。


## 路线图 Roadmap

* v 0.4.1: 单原子和双原子分子表面吸附
* v 0.4.2: 双原子过渡态计算，扫描 phi 角度
* v 0.5: 多种表面采样方法
* v 0.6: 新的高效表面格点构造，支持表面和团簇
* v 0.7: 新的 grid_sample 方法，包含 Hull.vertices VIP 位点。 
* v 0.8: 孔材料体系格点构造
* v 0.9: 重新梳理软件的模块，优化软件使用逻辑
  * v 0.9.2: debug 支持三斜晶系的表面格点化

**TODO**

* 表面位点数据库
* 多原子体系（内坐标受限体系）
* 完善用户界面、例子、教程


## Reference

[^Duvenaud]: [The Kernel Cookbook: Advice on Covariance functions](https://www.cs.toronto.edu/~duvenaud/)]
[^BASC]: Shane Carr, Roman Garnett, Cynthia LoBASC: Applying Bayesian Optimization to the Search for Global Minima on Potential Energy Surfaces.
[^向量空间转化]: 计算实空间和向量空间的相邻格点距离的映射系数，根据此系数将实空间的距离转化为向量空间距离。

