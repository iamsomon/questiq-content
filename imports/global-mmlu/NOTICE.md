# Attribution and changes

Contains a transformed RU/EN subset of **Global-MMLU** by **Cohere Labs / Shivalika Singh et al. (2024)**, based on **MMLU by Dan Hendrycks et al.** The publisher releases the dataset under Apache License 2.0. No endorsement by the authors is implied.

Source: https://huggingface.co/datasets/CohereLabs/Global-MMLU

Pinned source version: `0e619dbeb34206cd48705a1a0ea7fb21cae09993`.

Changes by Questiq: selected Russian and English dev/test records; aligned records by source sample ID; converted Parquet to JSONL; preserved question, answer choices, answer labels and source annotations; added provenance, attribution, missing-game-field lists and automated risk flags. Questions and choices were not rewritten or retranslated. Other languages and the publisher's illustration are not included. No editorial or human translation approval is granted by this conversion. These files are research/adaptation inputs and are not served as game content.

Publisher citation:

```bibtex
@misc{singh2024globalmmluunderstandingaddressing,
  title={Global MMLU: Understanding and Addressing Cultural and Linguistic Biases in Multilingual Evaluation},
  author={Shivalika Singh and Angelika Romanou and Clémentine Fourrier and David I. Adelani and Jian Gang Ngui and Daniel Vila-Suero and Peerat Limkonchotiwat and Kelly Marchisio and Wei Qi Leong and Yosephine Susanto and Raymond Ng and Shayne Longpre and Wei-Yin Ko and Madeline Smith and Antoine Bosselut and Alice Oh and Andre F. T. Martins and Leshem Choshen and Daphne Ippolito and Enzo Ferrante and Marzieh Fadaee and Beyza Ermis and Sara Hooker},
  year={2024},
  eprint={2412.03304},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2412.03304}
}
```
