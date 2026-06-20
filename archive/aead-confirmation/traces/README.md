# traces 目录

本目录用于保存和解释 ProVerif 给出的 trace 或反例。

建议文件：

  baseline-q1-false.md
  aead-q1-blocked.md

baseline-q1-false.md 用于解释原始 core 中攻击者如何让接收方接受 unpartnered session。

aead-q1-blocked.md 用于解释加入 AEAD confirmation 后，攻击者为什么无法通过 aead_verify。
