阶段 1 范围：

分析对象：
- 原始 K-Waay / Collins 2024
- core protocol without full BatchReceive
- abstract KEM / abstract split-KEM
- ProVerif symbolic model

本阶段分析性质：
- honest-run reachability
- receiver authentication
- sender/receiver agreement on sid and session key
- session key secrecy with explicit compromise exceptions

本阶段暂不分析：
- full BatchReceive
- prekey exhaustion
- receiver state reuse across multiple senders
- Tamarin state model
- CryptoVerif computational proof
- deniability equivalence
- EasyCrypt simulator proof
- Sparrow-KEM / Sym-Sparrow-KEM internal MLWE proof