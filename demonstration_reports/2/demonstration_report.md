```
(B1b) Full Details: Serializers
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Serializer                   ┃ Encod. Ok ? ┃ Σ Encoded   ┃ Σ Encoded     ┃ Decod. Ok ? ┃ Σ Decoded   ┃ Reversibility ?  ┃ Σ memory     ┃
┃                              ┃ (Max=29)    ┃ Time        ┃ Str. Length   ┃ (Max=29)    ┃ Time        ┃ (Max=29)         ┃              ┃
┃                              ┃             ┃ (seconds)   ┃ (characters)  ┃             ┃ (seconds)   ┃                  ┃              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Iaswn                        │ 29          │ 0.000464    │ 9460          │ 29          │ 0.000510    │ 29 (100.00%)     │ 0 byte       │
│                              │ (100.00%)   │             │               │ (100.00%)   │             │                  │              │
│ json                         │ 29          │ 0.000240    │ 9483          │ 29          │ 0.000210    │ 29 (100.00%)     │ 0 byte       │
│                              │ (100.00%)   │             │               │ (100.00%)   │             │                  │              │
│ marshal                      │ 29          │ 0.000052    │ 9399          │ 29          │ 0.000045    │ 29 (100.00%)     │ 0 byte       │
│                              │ (100.00%)   │             │               │ (100.00%)   │             │                  │              │
│ pickle                       │ 29          │ 0.000078    │ 9637          │ 29          │ 0.000063    │ 29 (100.00%)     │ 0 byte       │
│                              │ (100.00%)   │             │               │ (100.00%)   │             │                  │              │
└──────────────────────────────┴─────────────┴─────────────┴───────────────┴─────────────┴─────────────┴──────────────────┴──────────────┘

(C1a) Conclusion: Data Objects Handled by the Serializer(s)

Iaswn: According to the tests carried out on all data, Iaswn can handle 29 data objects among 29 (100.00%), namely bool/false, bool/true, demonstration_dataobj, dict(keys/str), dict(keys/str+subdicts), 
float, int, int_-0xffff, int_-0xffffffff, int_-0xffffffffffffffff, int_-0xffffffffffffffffffffffffffffffff, int_-1, int_0, int_0xffff, int_0xffffffff, int_0xffffffffffffffff, 
int_0xffffffffffffffffffffffffffffffff, int_1, io.string(empty), list, list(+sublists), list(empty), metaclass, none, str, str(empty), str(long), str(non ascii characters) and time(time.time) .
json: According to the tests carried out on all data, json can handle 29 data objects among 29 (100.00%), namely bool/false, bool/true, demonstration_dataobj, dict(keys/str), dict(keys/str+subdicts), float, 
int, int_-0xffff, int_-0xffffffff, int_-0xffffffffffffffff, int_-0xffffffffffffffffffffffffffffffff, int_-1, int_0, int_0xffff, int_0xffffffff, int_0xffffffffffffffff, int_0xffffffffffffffffffffffffffffffff,
int_1, io.string(empty), list, list(+sublists), list(empty), metaclass, none, str, str(empty), str(long), str(non ascii characters) and time(time.time) .
marshal: According to the tests carried out on all data, marshal can handle 29 data objects among 29 (100.00%), namely bool/false, bool/true, demonstration_dataobj, dict(keys/str), dict(keys/str+subdicts), 
float, int, int_-0xffff, int_-0xffffffff, int_-0xffffffffffffffff, int_-0xffffffffffffffffffffffffffffffff, int_-1, int_0, int_0xffff, int_0xffffffff, int_0xffffffffffffffff, 
int_0xffffffffffffffffffffffffffffffff, int_1, io.string(empty), list, list(+sublists), list(empty), metaclass, none, str, str(empty), str(long), str(non ascii characters) and time(time.time) .
pickle: According to the tests carried out on all data, pickle can handle 29 data objects among 29 (100.00%), namely bool/false, bool/true, demonstration_dataobj, dict(keys/str), dict(keys/str+subdicts), 
float, int, int_-0xffff, int_-0xffffffff, int_-0xffffffffffffffff, int_-0xffffffffffffffffffffffffffffffff, int_-1, int_0, int_0xffff, int_0xffffffff, int_0xffffffffffffffff, 
int_0xffffffffffffffffffffffffffffffff, int_1, io.string(empty), list, list(+sublists), list(empty), metaclass, none, str, str(empty), str(long), str(non ascii characters) and time(time.time) .

(C1b) Conclusion: Data Objects NOT Handled by the Serializer(s)

Iaswn: According to the tests carried out on all data, there's no data object among the 29 used data objects that serializer Iaswn can't handle (0%).
json: According to the tests carried out on all data, there's no data object among the 29 used data objects that serializer json can't handle (0%).
marshal: According to the tests carried out on all data, there's no data object among the 29 used data objects that serializer marshal can't handle (0%).
pickle: According to the tests carried out on all data, there's no data object among the 29 used data objects that serializer pickle can't handle (0%).

(C2a) Conclusion: Serializers (Not Sorted)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Serializer                ┃ Σ Encoded Str.   ┃ Σ Encod.+Decod.  ┃ Reversibility    ┃ Memory       ┃
┃                           ┃ Length           ┃ Time (seconds)   ┃ (Coverage Rate)  ┃              ┃
┃                           ┃ (characters)     ┃                  ┃ (Max=29)         ┃              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ -                         │ -                │ -                │ -                │              │
│ Iaswn                     │ 9460             │ 0.000974         │ 29 (100.00%)     │ 0 byte       │
│ json                      │ 9483             │ 0.000450         │ 29 (100.00%)     │ 0 byte       │
│ marshal                   │ 9399             │ 0.000097         │ 29 (100.00%)     │ 0 byte       │
│ pickle                    │ 9637             │ 0.000141         │ 29 (100.00%)     │ 0 byte       │
└───────────────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────┘

(C2b) Conclusion: Overall Score Based on 4 Comparisons Points (Σ Encoded Str. Length/Σ Encod.+Decod. Time/Coverage Rate/Σ memory)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Serializer                ┃ Overall Score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ -                         │ -             │
│ Iaswn                     │ 12            │
│ json                      │ 10            │
│ marshal                   │ 12            │
│ pickle                    │ 6             │
└───────────────────────────┴───────────────┘

(C2c) Conclusion
According to the tests carried out on all data, marshal is the quickest to encode/decode, marshal produces the shortest strings, all serializers are equal when it comes to data coverage and all serializers 
are equal when it comes to memory consumption. Iaswn and marshal are ranked #1 among 4 serializers, according to the overall scores (¹).
On the contrary, Iaswn is the slowest to encode/decode, pickle produces the longest strings, all serializers are equal when it comes to data coverage and all serializers are equal when it comes to memory 
consumption. pickle is ranked #4 among 4 serializers, according to the overall scores (¹).

- notes -
[¹] a rank based on 4 comparisons points: Σ encoded str./Σ encod.+decod. time/Coverage Rate/Σ memory

```

![Slowness](report1.png)

![Memory Usage](report2.png)

![Encoded String Length](report3.png)

![Coverage data (Reversibility)](report4.png)

