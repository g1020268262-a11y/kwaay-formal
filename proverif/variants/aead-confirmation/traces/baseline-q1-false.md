1. A 发出合法消息 m = (ctL, ctE, ctS)

2. 攻击者从 m 中保留 ctS

3. 攻击者自己重新构造 ctL' 和 ctE'

4. 攻击者拼出 m' = (ctL', ctE', ctS)

5. 攻击者把 m' 发给 B

6. B 根据 m' 计算 sid' 和 k'

7. baseline 中 B 直接 RecvDone(B,A,sid',k')

8. 但 A 没有 SendDone(A,B,sid',k')