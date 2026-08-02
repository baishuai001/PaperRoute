# WORK-001 / G0 方向审计评审包

> **状态更新（2026-08-02）**：本文件保存第一次 G0 推荐，现已因方向模型缺陷被标记为
> `challenged`，不再代表当前主推荐。新评审必须使用根目录
> `docs/g0-decision-standard.md`、`registry/direction_changes.tsv` 和
> `registry/direction_assessments.tsv`。本文件仅作为回归审计证据。

审计快照日期：2026-08-01

决策状态：proposed；等待项目所有者人工审查。

当前 gate：G0_DIRECTION

## 结论先行

建议主方向为 **DIR-002**：

> **跨队列审计 CRC/CRLM 已发表髓系状态的可迁移性与情境边界**

建议备选方向为 **DIR-003**：

> **外部验证 CRC 转移中“恶性相关”与“肝脏生态位相关”的免疫程序**

两条路线均不把锚点期刊层级自动转化为新稿件目标。DIR-002 是面向初学者的
bounded_adaptation：只改变一个核心问题——从“再发现一个 SPP1+TAM 机制”
转为“已发表髓系状态中，哪些能在独立患者队列中成立，哪些只在特定队列、组织或定义下成立”。
DIR-003 是更高负担的 evidence_extension，只作为备选，不作为默认升级路线。

这不是保守到没有创新。它把创新放在一个当前拥挤领域仍未被可靠解决的问题上：
论文不断产生 SPP1+、MRC1+CCL18+、脂质/溶酶体、抗原呈递、应激和其他命名状态，
但不同研究是否在描述同一程序、组织效应是否能跨患者和跨队列迁移、细胞级显著性是否能在
患者级成立，仍缺少预先登记、重叠审计和 meta-analytic 的系统回答。

## 1. 为什么不建议继续原叙事

截至本次快照，直接的 SPP1+TAM—CRLM—免疫抑制空间已高度饱和：

- [Qi 等，FAP+ fibroblast–SPP1+ macrophage](https://doi.org/10.1038/s41467-022-29366-6)
  已建立 CRC 空间互作框架；
- [Bill 等，CXCL9:SPP1 polarity](https://doi.org/10.1126/science.ade2292)
  已把它提升为跨癌种巨噬细胞连续轴；
- [Trehan 等](https://doi.org/10.1038/s41467-025-59529-0)和
  [Ding 等](https://doi.org/10.1136/jitc-2025-012330)
  已连接肝转移、肿瘤特异 T 细胞耗竭/应激及 SPP1-CD44；
- [Chang 等](https://doi.org/10.1186/s12967-026-07978-6)已报道
  mCAF–SPP1 macrophage–T-cell 空间生态位；
- [Bellomo 等](https://doi.org/10.1126/sciadv.aed1296)已报道
  THBS1–SPP1 单核-巨噬细胞轴、肿瘤边缘/核心免疫分区和结局；
- [2026 Cancer Cell CRC 中性粒细胞图谱](https://doi.org/10.1016/j.ccell.2025.12.003)
  又使“把 TAM 换成中性粒细胞”这种表面替换失去新颖性。

因此，下列标题即使分析能运行，也不构成足够的新方向：

- “SPP1+TAM 在 CRLM 中富集并提示差预后”；
- “某个新受体/配体与 SPP1+TAM 互作”但只有 CellChat 推断；
- “把 TAM 换成中性粒细胞”；
- “把 SPP1 换成另一个 marker”；
- “把范围扩成泛癌”但没有新 estimand；
- “SPP1+TAM 与 CAF/T 细胞共定位”但没有超出现有文献的空间检验。

## 2. 主方向 DIR-002

### 2.1 核心问题

> 当多个 CRLM 研究使用不同 marker、signature、聚类分辨率和数据集命名髓系状态时，
> 哪些状态在独立患者队列中具有可重复的组织关联，哪些只在特定队列、处理史、空间区域
> 或状态定义下成立？

SPP1+TAM 是锚点、阳性对照和测量案例，不是预先保证胜出的主角。分析应预先冻结一个有限的
已发表状态 panel，而不是在所有基因中不断寻找最显著的新 cluster。

### 2.2 暂定主张

建议将稿件的可检验主张写成：

> 已发表 CRLM 髓系状态具有可检验且不相等的跨队列可迁移性；在保持患者/样本为推断单位后，
> 跨队列效应和异质性能够区分广泛可重复的组织相关程序、情境特异程序和证据不足的命名。

这个表述允许三种合法结果：

1. 某些状态方向一致且可空间验证；
2. 某些状态只在特定组织、治疗或技术条件下成立；
3. 某些流行标签在患者级分析后不再成立。

阴性和矛盾不是失败；如果设计预先冻结，它们正是该方向的贡献。

### 2.3 论文解决的问题

该路线解决的不是“有没有 SPP1 表达”，而是四个更基础的问题：

1. **命名问题**：不同论文的同名/异名 macrophage cluster 是否对应同一多基因程序；
2. **统计问题**：细胞级显著性在患者或独立样本级是否仍然成立；
3. **迁移问题**：发现队列中的状态能否映射到非重叠队列；
4. **边界问题**：组织、治疗、平台、取材位置或状态定义何时改变结论。

### 2.4 预期证据链与稿件骨架

| 稿件模块 | 主要产出 | 它支持什么 | 它不能支持什么 |
|---|---|---|---|
| Figure 1：来源与重叠图 | 数据集—论文—患者/样本 provenance 图；纳入排除表 | 独立性、可审计性和适用范围 | 生物学机制 |
| Figure 2：状态对应关系 | 冻结的已发表 signature panel；离散 cluster 与连续程序的对应/不对应 | 状态定义是否可迁移 | 轨迹或谱系 |
| Figure 3：患者级跨队列效应 | 每队列效应量、置信区间、异质性和 leave-one-study-out | 哪些组织关联可重复 | 因果作用 |
| Figure 4：空间正交验证 | 至少一个非重叠空间/成像队列的定位或邻域检验 | 组织区域和空间关联 | ligand-receptor 机制 |
| Supplement：稳健性 | marker-only 与 module、注释、QC、处理史和阈值敏感性 | 结论边界和失效模式 | 用后验调参制造阳性 |

如果最终只得到一个 UMAP、几个 violin plot 和 CellChat 圆图，这条路线没有达到创新下限。

### 2.5 第一轮数据可行性

已确认的候选资源包括：

- [GSE164522](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164522)：
  101 个 CD45+ 样本，覆盖血液、淋巴结、原发 CRC、CRLM 和邻近组织；
- [GSE225857](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857)：
  6 名患者、27 个样本，含单细胞和有限空间数据；所有患者均有术前治疗；
- [Bellomo Zenodo](https://doi.org/10.5281/zenodo.15322885)：
  6 名患者、74,804 个免疫细胞，含正常肝、肿瘤边缘和核心，以及 mass cytometry；
- [NMP CELLxGENE collection](https://cellxgene.cziscience.com/collections/be679cb1-35f0-46c9-9a2d-30691862a54a)：
  6 名供体、75,104 个细胞，可用于状态持续性或外部验证；
- [CRC atlas CELLxGENE collection](https://cellxgene.cziscience.com/collections/3a844375-60ea-474b-adf1-98e76928baee)：
  当前公开对象含 3,790,266 个细胞和 588 名供体，可作为参考图谱和研究级元数据入口。

这些数字不能直接相加作为“验证样本量”。CRC atlas 汇集了许多原始研究，可能包含上述队列；
G1 必须建立底层 study、GEO accession、患者和样本重叠图，真正独立的研究才进入 meta-analysis。

### 2.6 代码策略

不能选择“最像论文的脚本”作为唯一基础。建议分四层：

1. **工程骨架**：
   [icbi-lab/crc-atlas](https://github.com/icbi-lab/crc-atlas) 提供 Nextflow、
   环境、容器、预计算结果和清楚的上下游拆分，是目前审计到的最佳工程 donor。
   但其完整发布资源约 159 GB，精确 atlas build 使用 A100 80 GB；当前服务器为 24 GB 显存，
   因此只复用预计算对象、下游模式和工程约束，不重跑完整 atlas。
2. **统计实现**：优先采用有维护文档的正式包，例如
   [muscat](https://bioconductor.org/packages/release/bioc/html/muscat.html)，
   最终方法由 G2 的 estimand、count 类型、配对结构和重复数决定。
3. **论文方法碎片**：LianLab、Qi、LPC、TASrev2 和 Bellomo 脚本只用于还原作者意图、
   marker、图形和参数线索；硬编码路径、交互选择和未锁定依赖必须被替换。
4. **PaperRoute 项目代码**：用配置驱动的 dataset adapter、状态 panel、患者级统计模块、
   测试和 run manifest 把前三层连接起来；所有替代和偏离均登记来源。

这满足用户提出的原则：好思路可以从同类文献补足处理细节，但最终正确性不能由“论文代码存在”
自动背书；论文片段、正式方法实现和本项目验证承担不同职责。

### 2.7 创新下限、雄心上限与稿件定位

创新下限：

- 至少三个真正独立且含患者/样本 ID 的队列；
- 至少两个队列可估计同一个主要组织对比；
- 至少一个非重叠空间或成像队列；
- 预先冻结状态 panel、主要 estimand 和异质性分析；
- 至少得到一个可验证的新边界、矛盾解释或跨队列证据排序；
- 不能只重复“SPP1 高、预后差”。

雄心上限：

- 只主张关联、可迁移性、异质性和空间定位；
- 不主张驱动肝转移、单核细胞分化方向、真实细胞通讯或治疗协同；
- 不把 bulk signature 当成巨噬细胞特异丰度；
- 不承诺 CNS 或与锚点同层级期刊。

如果满足上述条件，这是一条有机会形成领域型方法/资源/再分析稿件的受控路线；
如果不满足，应降级为学习复现或停止，而不是增加更多图来伪装完整论文。

## 3. 备选方向 DIR-003

### 3.1 核心问题

> CRC 原发灶和肝转移中的免疫状态，哪些更随“恶性肿瘤身份”迁移，哪些更随“肝脏生态位”重塑？

该问题受到 GSE164522 的 M-type/N-type 框架启发，但新稿件必须做非重叠队列的外部验证，
而不是重新绘制原论文。

### 3.2 为什么是备选而不是主线

优点：

- 问题比单一 marker 更接近“跨尺度肿瘤免疫生态”的核心；
- 即使 SPP1 状态本身不稳定，仍可得到不同细胞谱系的生态边界；
- 可以利用 CRC atlas 的参考映射和多个组织来源。

风险：

- 需要在多细胞谱系和多队列之间统一状态，工作量显著增加；
- 组织、研究、处理史、建库平台往往同时变化，可能无法统计分离；
- 真正具有原发灶、肝转移和邻近肝的外部配对队列数量有限；
- 很容易从受控问题滑向无边界“做一个大图谱”。

致命停止条件：

- 找不到至少两个非重叠的外部匹配队列；
- 肿瘤身份和器官来源与 study/batch 完全共线；
- 参考映射只能重现 GSE164522 的原标签，不能产生外部可检验贡献。

主张上限仍然是“程序更接近恶性相关或生态位相关”，不是细胞来源、真实迁移路径或因果塑形。

## 4. 暂不推荐的条件路线

DIR-004（dMMR CRC 新辅助 PD-1 后的巨噬细胞程序重塑）具有学习价值，但目前只有
[GSE205506](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE205506)
这一关键单细胞来源：19 名患者、处理组混合 anti-PD-1 与 anti-PD-1+celecoxib，
配对和非 pCR 数量有限，尚未确认独立 CRC ICI 单细胞验证队列。

因此它只能保留为 hold_conditional。没有独立验证时，最多形成探索性结果，
不应包装为预测 biomarker 或治疗机制稿件。

DIR-005（锚点近似重建）应保留为训练任务，但不能单独满足“产出新文献”的首要目标。

完整比较及致命否决项见
[g0_direction_matrix.tsv](g0_direction_matrix.tsv)。

## 5. G1 的最小充分范围

若项目所有者批准 DIR-002，G1 只做足以决定能否进入统计设计的工作：

1. 建立 paper–accession–sample–patient–treatment–modality manifest；
2. 明确底层研究重叠，冻结 discovery、validation 和 spatial-validation 角色；
3. 检查每队列是否有 counts、patient ID、sample ID、tissue、treatment 和可追溯注释；
4. 统计每个患者/样本的髓系细胞可用量，不先运行全套下游分析；
5. 冻结候选状态 panel 的文献来源、基因列表和转移规则；
6. 用小规模 smoke subset 证明对象能够读取、metadata 能够映射；
7. 形成 go / narrow / stop 决策。

G1 不下载或重建完整 4.27M 细胞 atlas，不为“以后可能有用”而收集所有 CRC 数据，
也不在看到效应方向后更换主要状态 panel。

## 6. 需要项目所有者审查的决策

请对以下内容明确批准、要求修改或拒绝：

1. 是否批准 DIR-002 为主方向；
2. 是否批准 DIR-003 为备选方向；
3. 是否接受 DIR-002 的创新下限与关联性 claim ceiling；
4. 是否同意 DIR-004 仅保留为条件路线、DIR-005 仅作为训练任务；
5. 是否允许进入上述“最小充分 G1”，而不是直接开始全量下载和分析。

在人工审查前：

- DECISION-001 保持 proposed；
- REVIEW-001 保持 pending；
- WORK-001 保持 in_progress；
- PROJECT.json.active_direction_id 保持审计伞方向 DIR-001；
- 不启动 WORK-002 的正式分析实现。

## 7. 审计覆盖与不确定性

本次快照核查了锚点 PDF/补充材料、PubMed/PMC、GEO、CELLxGENE、GitHub 和 Zenodo，
重点覆盖 2022–2026 年的直接近邻、公共数据和代码。它是方向决策所需的定向审计，
不是注册式系统综述；新发表论文、预印本转正、数据撤回或代码更新均可重新打开 G0。

证据逐项记录见
[g0_evidence_snapshot.tsv](g0_evidence_snapshot.tsv)，锚点研究语法和不可复现边界见
[g0_anchor_grammar.md](g0_anchor_grammar.md)。
