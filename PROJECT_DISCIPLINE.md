# PaperRoute 项目纪律

本文件是 PaperRoute 的最高级项目约束。代码、文档、数据整理、结果、
判断、反馈和版本更新均不得偏离本文件。

## 1. 首要目标

PaperRoute 的目标不是无限完善一个 workflow，也不是展示软件工程能力。

> 首要目标是帮助初学者从一篇锚点文献出发，完成一项科学上可信、
> 逻辑上严谨、技术上可执行，并最终能够形成论文稿件的研究。

workflow、代码和审查机制都是服务论文产出的工具，不是最终目的。

## 2. 从模仿开始，但不做简单复制

面向初学者，从高质量文献中借鉴问题结构、证据链、分析方法和代码实现，
可以降低学习成本和错误风险。但模仿必须经过以下转换：

1. 审计锚点文献的科学问题、证据结构、优点、缺口和不可复现部分；
2. 明确保留、替换、扩展和删除的内容；
3. 对候选方向进行创新性与可行性审计；
4. 使用适合新问题和新数据的统计设计；
5. 清楚区分精确复现、独立重建、概念改编和敏感性分析；
6. 对所有替代、推断和后验调整进行显式记录和人工审查。

不得通过替换名称、癌种、细胞或基因后直接重复原文叙事来制造创新。

## 3. 初学者导向与创新强度校准

PaperRoute 同时服务于学习和论文产出，但必须分别评价学习价值与发表价值。
锚点文献的质量、期刊层级或影响力不自动决定新项目的目标层级。学习一篇
高水平文献，不等于必须把初学者项目推荐为同层级或更高层级的研究。

方向选择遵守两条边界：

- **创新下限**：不能只用替换癌种、细胞、基因或名称这一事实证明创新；必须说明相对
  最近邻文献新增了什么认识、为什么有价值，以及哪项决定性证据能够证明；
- **雄心上限**：主张深度和研究复杂度不得超过可获得数据、可靠代码、
  验证条件、时间、算力、实验资源和项目成员当前能力能够支撑的范围。

G0 不以改动数量判断创新或风险。疾病、核心对象、中心关系、主要结局和证据结构可以
保留，也可以同时修复、替换、扩展或删除。每项改变必须记录科学理由、贡献、所需证据、
代码或方法 donor、相互作用风险和停止条件。允许多轴改编，但不允许用复杂度掩盖缺乏
明确问题。

候选方向必须分别评价科学有效性、可行性、新颖性、科学价值、实施负担、学习价值和
锚点复用；这些是彼此独立的维度，不得压缩成单一“雄心层级”或不透明总分。硬伤修复
默认恢复可信度而不自动构成创新；若要把修复作为方法学贡献，必须单独证明其可推广性
和最近邻空缺。

“最小充分”约束的是对中心结论无必要的工作量，不是与锚点的表面距离。多轴替换可以是
合理的最小充分方案，单轴改变也可能实质上改变稿件类型。AI 必须同时呈现互有取舍的
合格候选，说明学习收益、论文贡献、成本、失败风险和停止条件，由项目负责人选择。

## 4. 四项核心质量标准

所有研究方向、主张、数据、方法和结果必须同时接受四项审查：

- **创新性**：相对最近邻文献，新增了什么问题、证据、机制、边界或方法价值；
- **可行性**：数据、metadata、代码、计算资源、时间和验证条件是否足够；
- **科学性**：设计、统计单位、对照、因果边界和生物学解释是否成立；
- **逻辑严谨性**：主张、证据、方法、结果和结论是否形成可审计的推理链。

代码可运行不能替代科学正确；结果显著不能替代逻辑成立。

## 5. 论文导向的范围控制

任何新增工作都必须至少属于以下一种理由：

- 支持或检验一个稿件主张；
- 填补证据链缺口；
- 修复可能改变结论的正确性风险；
- 满足结果可复现的最低要求；
- 回应必要的人工或同行审查问题。

每个工作项必须写明：

1. 关联的方向、主张、模块或决定；
2. 预期形成的稿件内容，例如 Figure、Table、Methods、Results 或 Limitation；
3. 最小充分交付物；
4. 明确的停止条件。

不能说明稿件价值和停止条件的优化，不进入当前范围。

## 6. 最小充分工程

PaperRoute 只建设足以保证下列目标的工程能力：

- 信息和判断可追溯；
- 分析可以稳定运行；
- 关键错误能够被测试发现；
- 结果能够追溯到输入、参数和运行版本；
- 用户能够审查高影响决定；
- 稿件结果能够被重新生成。

在达到这些要求后，不因“还可以更优雅、更通用或更自动化”继续扩展。
通用化只有在当前稿件需要，或已被至少两个真实项目证明重复需要时，才进入优先范围。

## 7. 结果可以改变方向，但不能制造后验故事

结果可能要求继续、细化、改道或停止。任何 `refine`、`reroute` 或 `stop`
必须：

1. 先保存原计划和原结果；
2. 建立 Change Request；
3. 说明对稿件贡献和结论边界的影响；
4. 计算受影响的下游主张、模块和结果；
5. 对高影响变化重新进行人工审查；
6. 建立新版本，而不是覆盖已审查版本；
7. 将结果驱动的新分析标为探索性，直到获得独立验证。

不允许为了获得阳性结果而不断更换分组、阈值、基因集、队列或终点。

## 8. 阴性、矛盾和不可行也是有效判断

项目目标是形成可信论文，而不是保证原假设成立。

- 阴性结果可以界定机制边界；
- 队列间矛盾可以形成异质性问题；
- 数据不足可以降低 claim ceiling；
- 致命混杂可以否决方向；
- 缺少干预数据时不得用更多观察性分析冒充因果证据。

若现有条件不足以形成科学上可信的稿件，应及时改道或停止，而不是通过
无穷优化延长项目。

## 9. 人机分工

AI 负责信息采集、结构化整理、候选方案、代码实现、测试、差异识别和
影响分析。用户负责审查研究方向、高风险替代、结论边界和最终稿件判断。

AI 的建议默认是 `proposed`，不是自动批准。重要决定必须进入结构化
Decision/Review 记录，不能只存在于聊天上下文。

## 10. 完成定义

PaperRoute 项目的完成，不以 workflow 功能数量衡量，而以是否交付以下内容衡量：

- 明确且经审查的创新问题；
- 可执行且通过验证的分析；
- 足以支持主张的证据链；
- 清楚标注的限制、阴性和不可验证部分；
- 可追溯的 source tables、figures、methods 和 run manifests；
- 一份结构完整、结论不过度的稿件草案。

一旦这些内容达到预定质量，项目应进入稿件完善和投稿准备，而不是继续
无边界优化 workflow。

---

## Authoritative English summary

PaperRoute exists to help a beginner-led project produce a scientifically
defensible manuscript through audited imitation and justified adaptation.
Anchor-paper prestige, learning value, and target-manuscript ambition are
separate judgments. A candidate may retain, repair, replace, extend, or drop
one or multiple scientific components. Change count is not a novelty metric.
Every change requires a scientific rationale, contribution role, evidence and
donor plan, and risk statement. Scientific validity, feasibility, novelty,
scientific value, implementation burden, learning value, and anchor reuse are
audited independently and reviewed as explicit trade-offs.
Software and workflow optimization are subordinate to manuscript value.
Every work item must link to a manuscript claim, evidence gap, correctness
risk, reproducibility requirement, or review requirement; it must also define
an expected manuscript output and a stopping condition. Result-driven changes
must be versioned, reviewed, and protected against hindsight bias.
