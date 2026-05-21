# ProVerif Model Plan for K-Waay Core

## Scope

- Model: original K-Waay core without full BatchReceive.
- Tool: ProVerif symbolic model.
- Goal: first runnable model for reachability, authentication, agreement, and session key secrecy.
- Out of scope: full BatchReceive, Tamarin state model, CryptoVerif proof, deniability,
  Sparrow-KEM internals.

## 1. ProVerif Types

Suggested first-pass types and their protocol-map sources:

| Type | Protocol-map ID | Purpose |
|---|---|---|
| agent | ID-A01, ID-A02 | Protocol participants Pi and Pj. |
| sig_sk | LT-01 | Long-term signature secret key ssk. |
| sig_pk | LT-02 | Long-term signature public key spk. |
| kem_sk | LT-03 | Long-term KEM secret key ksk. |
| kem_pk | LT-04 | Long-term KEM public key kpk. |
| pk_tuple | LT-02, LT-04 | Long-term public key tuple pk = (spk, kpk). |
| skem_sender_sk | SP-01 | Sender split-KEM secret state from KeyGenA_sKEM. |
| skem_sender_pk | SP-02 | Sender split-KEM public prekey. |
| skem_receiver_sk | RP-01 | Receiver split-KEM secret state from KeyGenB_sKEM. |
| skem_receiver_pk | RP-02 | Receiver split-KEM public prekey. |
| ekem_sk | RP-03 | Receiver ephemeral KEM secret key. |
| ekem_pk | RP-04 | Receiver ephemeral KEM public key. |
| kem_ct | CT-01 | Long-term KEM ciphertext ct_l. |
| ekem_ct | CT-02 | Ephemeral KEM ciphertext ct_k. |
| skem_ct | CT-03 | Split-KEM ciphertext ct_s. |
| shared_secret | SS-01, SS-02, SS-03 | K_l, K_k, and K_s. |
| sid_t | DV-01 | Session identifier sid. |
| session_key | DV-02 | KDF output session key. |
| signature | SP-03, RP-05 | Signature value sigma_i. |
| prekey_payload | SP-02, RP-02, RP-04 | Signed payload for prekey bundles. |
| sender_prekey_bundle | SP-03 | Sender bundle representing (sender_skem_pk, bottom, sigma). |
| receiver_prekey_bundle | RP-05 | Receiver bundle representing (receiver_skem_pk, receiver_ekem_pk, sigma). |
| message_tuple | INF-02 | Message m = (ct_l, ct_k, ct_s). |
| randomness | CT-01, CT-02, CT-03 | Encapsulation randomness. |
| bool | SP-03, RP-05 | Verification result, if explicit bool modeling is used. |

`bottom` is abstracted by `payload_sender(...)` and `sender_prekey(...)`, so the first
model does not need a separate bottom term unless later required.

## Modeling Conventions

- Repeated type names in a function declaration are argument types, not variable names.
- For example, `kdf(shared_secret, shared_secret, shared_secret, sid_t)` has three
  distinct shared-secret arguments:
  - `K_l` from long-term KEM
  - `K_k` from ephemeral KEM
  - `K_s` from split-KEM
- The order of KDF arguments is fixed: `KDF(K_l, K_k, K_s, sid)`.
- Similarly, `sid(agent, agent, pk_tuple, pk_tuple, sender_prekey_bundle,
  receiver_prekey_bundle, message_tuple)` has distinct ordered arguments:
  - sender identity
  - receiver identity
  - sender long-term public key tuple
  - receiver long-term public key tuple
  - sender prekey bundle
  - receiver prekey bundle
  - message tuple
- The order matters and follows Figure 7.

## 2. Constructors and Destructors

This section is a modeling sketch, not complete ProVerif code.

### Signature

- `fun spk(sig_sk): sig_pk.`
- `fun payload_sender(skem_sender_pk): prekey_payload.`
- `fun payload_receiver(skem_receiver_pk, ekem_pk): prekey_payload.`
- `fun sign(sig_sk, prekey_payload): signature.`
- `reduc forall ssk: sig_sk, p: prekey_payload;`
  `verify(spk(ssk), p, sign(ssk, p)) = true.`
- `verify` is a destructor introduced by the reduc rule; do not also declare it as a
  separate fun in the `.pv` file.
- Sender role signs `payload_sender(sender_skem_pk)`, corresponding to Figure 7
  `ekpki = bottom`.
- Receiver role signs `payload_receiver(receiver_skem_pk, receiver_ekem_pk)`.
- Do not mix tuple-argument signing with payload-argument signing in the first model.

### Long-term KEM

- `fun kpk(kem_sk): kem_pk.`
- `fun lkem_enc(kem_pk, randomness): kem_ct.`
- `fun lkem_ss(kem_pk, randomness): shared_secret.`
- `reduc forall ksk: kem_sk, r: randomness;`
  `lkem_dec(ksk, lkem_enc(kpk(ksk), r)) = lkem_ss(kpk(ksk), r).`
- The decapsulation functions are destructors introduced by reduc rules; do not also
  declare them separately as fun symbols in the `.pv` file.
- Models CT-01 and SS-01.

### Ephemeral KEM

- `fun ekpk(ekem_sk): ekem_pk.`
- `fun ekem_enc(ekem_pk, randomness): ekem_ct.`
- `fun ekem_ss(ekem_pk, randomness): shared_secret.`
- `reduc forall eksk: ekem_sk, r: randomness;`
  `ekem_dec(eksk, ekem_enc(ekpk(eksk), r)) = ekem_ss(ekpk(eksk), r).`
- The decapsulation functions are destructors introduced by reduc rules; do not also
  declare them separately as fun symbols in the `.pv` file.
- Models CT-02 and SS-02.

### Split-KEM

- `fun pk_skem_sender(skem_sender_sk): skem_sender_pk.`
- `fun pk_skem_receiver(skem_receiver_sk): skem_receiver_pk.`
- `fun skem_enc(skem_sender_sk, skem_receiver_pk, randomness): skem_ct.`
- `fun skem_ss(skem_sender_sk, skem_receiver_pk, randomness): shared_secret.`
- `reduc forall sender_sk: skem_sender_sk,`
  `receiver_sk: skem_receiver_sk,`
  `r: randomness;`
  `skem_dec(receiver_sk,`
  `pk_skem_sender(sender_sk),`
  `skem_enc(sender_sk, pk_skem_receiver(receiver_sk), r))`
  `= skem_ss(sender_sk, pk_skem_receiver(receiver_sk), r).`
- The decapsulation functions are destructors introduced by reduc rules; do not also
  declare them separately as fun symbols in the `.pv` file.
- The sender public key used by the receiver must match `pk_skem_sender(sender_sk)`.
- This first model abstracts split-KEM correctness, not the full split-KEM security game.
- Models CT-03 and SS-03 with sender/receiver role separation.

### Prekey Bundle

- `fun sender_prekey(skem_sender_pk, signature): sender_prekey_bundle.`
- `fun receiver_prekey(skem_receiver_pk, ekem_pk, signature): receiver_prekey_bundle.`
- `sender_prekey` represents `(sender_skem_pk, bottom, sigma)`.
- `receiver_prekey` represents `(receiver_skem_pk, receiver_ekem_pk, sigma)`.
- The first model keeps sender and receiver prekey bundle types separate to avoid role
  confusion.
- If field extraction is needed later, add destructors or pattern matching for
  sender/receiver bundle fields.

### Message Tuple

- `fun msg(kem_ct, ekem_ct, skem_ct): message_tuple.`
- Represents Figure 7 `m = (ct_l, ct_k, ct_s)`.
- Message tuple enters sid directly.
- Receive context additionally carries sender public key and sender prekey.

### SID

- `fun pk(sig_pk, kem_pk): pk_tuple.`
- `fun sid(agent, agent, pk_tuple, pk_tuple, sender_prekey_bundle, receiver_prekey_bundle,`
  `message_tuple): sid_t.`
- Parameter positions:

```text
sid(
  sender_id,
  receiver_id,
  sender_pk,
  receiver_pk,
  sender_prekey,
  receiver_prekey,
  message
)
```

- The two agent arguments are not the same variable; the first is sender identity and the
  second is receiver identity.
- The two `pk_tuple` arguments are not the same variable; the first is `sender_pk` and the
  second is `receiver_pk`.
- The `sender_prekey_bundle` and `receiver_prekey_bundle` arguments are role-separated.
- Send order follows Figure 7: `sid(Pi, Pj, pki, pkj, preki, prekj, m)`.
- Receive reconstructs the same logical sid using local receiver/sender naming.
- `pk = (spk, kpk)`, so both long-term public keys enter sid through pk.

### KDF

- `fun kdf(shared_secret, shared_secret, shared_secret, sid_t): session_key.`
- Although `shared_secret` appears three times, these are three distinct arguments, not the
  same variable.
- Argument 1 = `K_l` from long-term KEM.
- Argument 2 = `K_k` from ephemeral KEM.
- Argument 3 = `K_s` from split-KEM.
- Argument 4 = `sid`.
- The order is fixed: `KDF(K_l, K_k, K_s, sid)`.
- The session key is KDF output, not KDF input.
- In the first model, keep one `shared_secret` type but use different constructors for the
  three sources:
  - `lkem_ss(...)`
  - `ekem_ss(...)`
  - `skem_ss(...)`

## 3. Events

- `event InitSender(agent).`
  Marks that an agent initialized sender split-KEM prekey state.
- `event InitReceiver(agent).`
  Marks that an agent initialized receiver split-KEM and ephemeral KEM state.
- `event SendDone(agent, agent, sid_t, session_key).`
  Marks that sender A completed Send to receiver B with sid and session key.
- `event RecvDone(agent, agent, sid_t, session_key).`
  Marks that receiver B accepted a session with sender A.
- `event SenderPrekeyVerified(agent, agent, sender_prekey_bundle).`
  Marks that receiver B verified sender A's signed sender prekey bundle.
- `event ReceiverPrekeyVerified(agent, agent, receiver_prekey_bundle).`
  Marks that sender A verified receiver B's signed receiver prekey bundle.
- `event CompromiseSigSk(agent).`
  Records adversarial exposure of an agent's long-term signature secret key.
- `event CompromiseKemSk(agent).`
  Records adversarial exposure of an agent's long-term KEM secret key.
- `event CompromiseSenderSkemState(agent).`
  Records exposure of sender split-KEM secret state.
- `event CompromiseReceiverSkemState(agent).`
  Records exposure of receiver split-KEM secret state.
- `event CompromiseReceiverEkemState(agent).`
  Records exposure of receiver ephemeral KEM secret state.

## 4. First Queries

Q0 Reachability:
There exists an honest execution where SendDone and RecvDone occur with the same sid and
session key.

Q1 Receiver authentication:
If B accepts a session with A, then A previously sent a matching session.
Expected correspondence shape:
`RecvDone(B, A, sid, k) ==> SendDone(A, B, sid, k)`.

Q2 Session key secrecy:
If B accepts and no disallowed compromise happened before the session, the adversary
should not learn the session key.
The first version may start without compromise exceptions; compromise events will be added
after the honest core model runs.

Q3 Agreement:
A and B agree on sid, which binds identities, public keys, prekey bundles, and ciphertext
tuple.

## 5. Processes

### KeyGenSetup

1. Generate or declare agents A and B.
2. Generate long-term signature secret keys `ssk_A`, `ssk_B`.
3. Derive signature public keys `spk_A`, `spk_B`.
4. Generate long-term KEM secret keys `ksk_A`, `ksk_B`.
5. Derive KEM public keys `kpk_A`, `kpk_B`.
6. Publish public keys as `pk_A = pk(spk_A, kpk_A)` and `pk_B = pk(spk_B, kpk_B)`.
7. Keep long-term secret keys private unless a compromise process exposes them.

### InitSender(A)

1. Generate sender split-KEM secret state with `KeyGenA_sKEM`.
2. Derive sender split-KEM public key `espki` with `pk_skem_sender`.
3. Set sender ephemeral KEM public key field `ekpki` to bottom.
4. Build `payload_sender(espki)` and sign it using A's long-term signature secret key.
5. Build sender prekey bundle `(espki, bottom, sigma_i)` as a `sender_prekey_bundle`.
6. Publish the sender prekey bundle.
7. Emit `InitSender(A)`.

### InitReceiver(B)

1. Generate receiver split-KEM secret state with `KeyGenB_sKEM`.
2. Derive receiver split-KEM public key `espki` with `pk_skem_receiver`.
3. Generate receiver ephemeral KEM secret key.
4. Derive receiver ephemeral KEM public key `ekpki`.
5. Build `payload_receiver(espki, ekpki)` and sign it using B's long-term signature key.
6. Build receiver prekey bundle `(espki, ekpki, sigma_i)` as a
   `receiver_prekey_bundle`.
7. Publish the receiver prekey bundle and emit `InitReceiver(B)`.

### Send(A,B)

1. Read B's long-term public key and receiver prekey bundle.
2. Verify B's prekey signature over `payload_receiver(espki, ekpki)` and emit
   `ReceiverPrekeyVerified(A, B, receiver_prekey_B)`.
3. Encapsulate to B's long-term KEM public key to get `ct_l` and `K_l`.
4. Encapsulate to B's receiver ephemeral KEM public key to get `ct_k` and `K_k`.
5. Run sender split-KEM operation to get `ct_s` and `K_s`.
6. Build `m = (ct_l, ct_k, ct_s)` and `sid` using `sender_prekey_A` and
   `receiver_prekey_B`.
7. Derive `session_key = KDF(K_l, K_k, K_s, sid)` and emit `SendDone`.

### Receive(B,A)

For the first ProVerif model, Receive(B,A) abstracts BatchReceive with a single input
item. Full BatchReceive and receiver-side prekey reuse are deferred.

1. Receive message tuple `m` with sender public key and sender prekey context.
2. Verify A's sender prekey signature over `payload_sender(espki)` and emit
   `SenderPrekeyVerified(B, A, sender_prekey_A)`.
3. Decapsulate `ct_l` using B's long-term KEM secret key to recover `K_l`.
4. Decapsulate `ct_k` using B's receiver ephemeral KEM secret key to recover `K_k`.
5. Run receiver split-KEM operation using B's receiver state and A's sender public key.
6. Reconstruct `sid` using `sender_prekey_A` and `receiver_prekey_B`.
7. Derive `session_key = KDF(K_l, K_k, K_s, sid)` and emit `RecvDone`.

## 6. Deliberately Deferred

- full BatchReceive
- receiver-side prekey reuse
- expose oracle exact freshness predicates
- deniability equivalence
- computational proof
- Sparrow-KEM internals
