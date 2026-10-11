# Stage 6 独立论文源码

这是本轮审核后的 latex-v2 构建输入快照，含6张表、2幅冻结TikZ图、3个编号与4个未编号展示公式及8条参考文献。main.pdf与当前latex-v2/main.pdf逐字节一致，共12页。

在本目录使用 TeX Live/XeLaTeX：

```
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

不依赖外部仓库路径。冻结图源没有改动。构建输入的SHA-256见SOURCE_MANIFEST.json。本目录用于独立交付，后续修改应明确以哪份源码为权威，避免双份编辑。

Word及WPS导出的7页预览位于../word-final/K-Waay-AROCMAG-submission-stage6.docx和同名-stage6-preview.pdf。研究贡献审计与验收报告位于../notes/。本轮没有新运行Tamarin，也没有完成MathType或Microsoft Word验收。
