# Void — scored at the wrong token position

Computed on the correct published data, but every metric read `logits[:, -1, :]`.
TransformerLens right-pads a batch with <|endoftext|>, and IOI prompts run 15 to 20 tokens
padded to 21, so for most examples that position held padding rather than the final token
of the prompt.

The symptom was visible and went unremarked for a full run: IOI's logit difference came out
at 0.4963 where Wang et al. report 3.56, and IOI accuracy sat at 0.585 on a task GPT-2 small
does perfectly. Indexing each example's own final token gives 3.8795 and 1.000.

Affects E1, E1c, E3, E4, E5. E2a is unaffected because it scores every position.

Kept as a record. Do not cite, do not reason from.
