# Random-Sample
Randomized Algorithm project_05

阅读文献1：random sample over join revisit， Sigmod 2018并实现相关代码:

数据： 前一部分简单的二元、三元抽样从txt中读入，后一部分改进的连接抽样使用的是自动生成的数据，可自定义连接个数、关系中元组个数、每个属性值的取值范围。

背景：连接操作往往会得到大量数据，而这些数据往往并不是全部被需要，例如求某属性的均值、个数、总和等，少数情况需要所有数据，例如求最大值或最小值。可以通过对连接结果采样来实现占用内存的减少，在不影响结果的情况下显著提高效率。
最直观的采样方法是对已经求出来的接连结果进行均匀采样，或者是等概率的放回或不放回的抽取。将结果存在数组等结构中可以很方便的进行，但如果要求在没有做完全部连接的情况下，无法进行这种抽样。且sample(R1) ꝏ sample(R2) != sample(R1ꝏR2)

1.对两个关系的连接做采样  
假设对R1(a, b)、R2(b, c)做连接操作，m是R2中b属性中出现次数最多的b值。首先从R1中均匀随机选择一个元组，再从R2的与这个元组的b值相同的元组集合中随机抽取一个元组。这个算法依赖于R2在属性b上有索引，可以不必扫描整个R2关系，只需要用过索引扫描属性值相同的元组进行抽样。计算整个b值在R2中出现的次数，即R2中属性值都等于这个b的元组数，记作d。最终以概率d/m接受这两个元组的连接输出在结果中。
这个采样方法的问题在与，如果R2中b属性中最大频率很大，那么每个元组的拒绝率很高，让关系的属性值本身对是否接受影响很大。  
2.对多个关系（通过外键）的连接做采样  
假设对多个关系做连接操作。这里对参与连接的关系有要求：首先，对于任意i < j且Ri和Rj有公共属性，那么这个属性一定是Ri的主键，Rj的外键；其次，对于任意i，都存在一个j > i，使得Ri和Rj有公共属性。这两要求即：在所有的关系中必须存在唯一一个源关系。源关系是指一个与连接结果一一对应的关系。满足这个要求的待做连接的关系集合中，对这些关系求连接结果的采样化简为对这个源关系做采样。
在代码中，R1的两个外键分别对应R2、R3的主键，这三个关系符合以上要求，可以分两次对R3进行采样先与R1连接再与R2连接得到最终结果。  
3.普适抽样框架  
按照论文中提出的算法1实现代码
