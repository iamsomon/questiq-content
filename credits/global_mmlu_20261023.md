# Global-MMLU adaptations in Questiq — 23 October 2026

14 selected questions from Global-MMLU were adapted for play. This is not an approval of the full imported bank. The remaining 26 questions in this 40-question release use original bilingual wording of independently checked facts.

Attribution: **Cohere Labs / Shivalika Singh et al., Global-MMLU (2024), based on MMLU by Dan Hendrycks et al.** No endorsement is implied. Source: https://huggingface.co/datasets/CohereLabs/Global-MMLU . Pinned version: `0e619dbeb34206cd48705a1a0ea7fb21cae09993`.

License: **Apache License 2.0**, reproduced in full below and in [LICENSE-APACHE-2.0.txt](../imports/global-mmlu/LICENSE-APACHE-2.0.txt). The original publisher citation is retained in [NOTICE](../imports/global-mmlu/NOTICE.md).

Changes by Questiq: shortened/reworded prompts, corrected Russian translations, replaced unsuitable distractors, removed ambiguous or absolute claims, mapped subjects/difficulty, added separately written RU/EN explanations and primary-source verification. No source images are included. Per-record changes and pinned normalized source hashes are in [the mapping](global_mmlu_20261023.mapping.json). Agent review only; no human/editorial or independent approval is claimed.

For older installed clients, each adapted question opens this page from its Source button. A short credit remains inside both offline explanation texts. The next app build also bundles the full notice and Apache license in its license screen.

### ancient-world-cuneiform-0001

Game ID: `ancient_world_cuneiform_0001`; source record: `prehistory/test/17`.

Какая древняя письменность получила название от клиновидных знаков? / Which ancient writing system takes its name from wedge-shaped signs?

[Primary fact source](https://www.metmuseum.org/essays/the-origins-of-writing) — Clay medium; wedge-shaped signs; Latin cuneus.

Met derives cuneiform from Latin wedge and describes reed/wood stylus signs in clay. Replaced source's disputed absolute 'earliest writing' assertion with a specific etymological fact. Hieroglyphs, Phoenician script and Linear B have different names; no mixed script/medium options.

### ancient-world-upper-egypt-0001

Game ID: `ancient_world_upper_egypt_0001`; source record: `prehistory/test/212`.

В каком направлении от Нижнего Египта располагался Верхний Египет? / In which direction from Lower Egypt was Upper Egypt located?

[Primary fact source](https://egyptianmuseumcairo.eg/historical-timeline/) — Predynastic – Early Dynastic Period: Delta (Lower Egypt), south (Upper Egypt).

Cairo museum explicitly places Lower Egypt in Delta and Upper Egypt in south. Compass distractors distinct; no inversion from English blank to misleading Russian noun fragment. Both languages ask relative location, not altitude.

### human-body-alveoli-0001

Game ID: `human_body_alveoli_0001`; source record: `anatomy/test/113`.

Как называются крошечные воздушные мешочки лёгких, где происходит газообмен? / What are the tiny air sacs in the lungs where gas exchange occurs called?

[Primary fact source](https://www.nhlbi.nih.gov/health/lungs/respiratory-system) — Air fills your lung’s air sacs; Oxygen flows into your blood.

NHLBI confirms air sacs at bronchiole ends and oxygen/CO2 exchange with surrounding capillaries. Changed original to ask for air sacs: capillaries also participate in exchange but are blood vessels, so cannot be second correct answer. Bronchi and bronchioles are tubes.

### human-body-ileum-0001

Game ID: `human_body_ileum_0001`; source record: `anatomy/test/120`.

Какой из этих отделов входит в тонкую кишку? / Which of these structures is part of the small intestine?

[Primary fact source](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) — What is the digestive system? Three parts of small intestine versus large intestine.

NIDDK lists duodenum, jejunum and ileum as small intestine, versus cecum and colon as large intestine. Ileum last section confirmed. No alternate correct structure among distractors; Russian подвздошная is distinct from подвздошная кость/ilium.

### human-body-iris-0001

Game ID: `human_body_iris_0001`; source record: `miscellaneous/test/314`.

Как называется окрашенная часть глаза, окружающая зрачок? / What is the colored part of the eye surrounding the pupil called?

[Primary fact source](https://www.nei.nih.gov/eye-health-information/healthy-vision/how-eyes-work) — Iris: colored part controlling pupil size.

NEI identifies the iris as colored tissue controlling pupil size. Cornea is transparent, retina light-sensitive tissue and lens focusing tissue; all are eye structures. Source's Russian 'ирис/ученик' and unrelated cochlea distractor are corrected.

### human-body-paired-kidneys-0001

Game ID: `human_body_paired_kidneys_0001`; source record: `miscellaneous/test/569`.

Какой из этих органов в обычном строении тела человека парный? / Which of these organs is paired in typical human anatomy?

[Primary fact source](https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work) — Opening: two bean-shaped organs, one on each side of spine.

NIDDK explicitly describes two kidneys on opposite sides of the spine. Liver, stomach and gallbladder are unpaired in typical anatomy. 'Typical/обычное строение' avoids claiming everyone has two kidneys; source's mistranslated 'пару А' removed.

### mythology-olympus-0001

Game ID: `mythology_olympus_0001`; source record: `miscellaneous/test/651`.

На какой горе, согласно древнегреческим мифам, жили олимпийские боги? / On which mountain did the Olympian gods live according to ancient Greek myths?

[Primary fact source](https://www.metmuseum.org/essays/greek-gods-and-religious-practices) — Pantheon paragraph: Mount Olympus, home of gods.

Met essay identifies Mount Olympus as mythic home and Zeus foremost. Replaced source's planet and hall options with mountains, so all options fit question class. Scope explicitly ancient Greek myth, not a factual claim that gods live there.

### plants-chloroplast-0001

Game ID: `plants_chloroplast_0001`; source record: `miscellaneous/test/222`.

В какой органелле растительной клетки происходит фотосинтез? / In which plant-cell organelle does photosynthesis take place?

[Primary fact source](https://openstax.org/books/biology-2e/pages/8-1-overview-of-photosynthesis) — Main Structures: chloroplasts and thylakoid membranes.

Chloroplast and thylakoid chlorophyll are confirmed in Biology 2e 8.1. Nucleus, mitochondrion and Golgi have other roles; none is the plant photosynthetic organelle. RU organelle terms match EN singulars.

### plants-coast-redwood-0001

Game ID: `plants_coast_redwood_0001`; source record: `miscellaneous/test/371`.

Какой вид известен самыми высокими современными деревьями? / Which species is known for the tallest living trees?

[Primary fact source](https://openstax.org/books/biology-2e/pages/30-5-transport-of-water-and-solutes-in-plants) — Figure 30.31: coastal redwoods, tallest trees.

Figure 30.31 identifies Sequoia sempervirens as the tallest tree species, not the greatest-volume giant sequoia. Douglas fir is corrected to pseudotsuga in Russian; all four options are different tree taxa. No changing individual-tree height record is asserted.

### plants-guard-cells-0001

Game ID: `plants_guard_cells_0001`; source record: `miscellaneous/test/537`.

Какие клетки регулируют открытие и закрытие устьица листа? / Which cells regulate the opening and closing of a leaf stoma?

[Primary fact source](https://openstax.org/books/biology-2e/pages/30-5-transport-of-water-and-solutes-in-plants) — Control of Transpiration: two guard cells surrounding stomata.

Transport section confirms paired guard cells open/close stomata. Replaced source's membrane/cytoplasm/cellulose with other cell types, removing its category mismatch. RU 'Камера охраны' corrected to 'Замыкающие клетки'; both questions ask regulation, not generic passage.

### plants-negative-gravitropism-0001

Game ID: `plants_negative_gravitropism_0001`; source record: `high_school_biology/test/175`.

Как называется рост побега против направления силы тяжести? / What is shoot growth against the direction of gravity called?

[Primary fact source](https://openstax.org/books/biology-2e/pages/30-6-plant-sensory-systems-and-responses) — Plant Responses to Gravity: upward shoot growth.

Gravity section explicitly distinguishes negative shoot gravitropism from positive root response. The stem's gravity direction is specified, not inferred from illumination. Phototropism answers describe another stimulus. Both languages preserve 'against gravity'.

### plants-oxygen-source-0001

Game ID: `plants_oxygen_source_0001`; source record: `high_school_biology/test/275`.

Из какого вещества образуется выделяемый растением O₂ при фотосинтезе? / Which substance supplies the O₂ released by a plant during photosynthesis?

[Primary fact source](https://openstax.org/books/biology-2e/pages/8-2-the-light-dependent-reactions-of-photosynthesis) — Photosystem II: water splitting and diatomic oxygen.

Photosystem II section confirms two H2O split for one diatomic O2. CO2 supplies carbon rather than released oxygen; H2O2 decomposition is not the specified photosynthetic source, and CO is not that substrate. Subscripts and compound names match RU/EN.

### plants-phytochrome-0001

Game ID: `plants_phytochrome_0001`; source record: `high_school_biology/test/176`.

Какой растительный фоторецептор переключается между формами Pr и Pfr? / Which plant photoreceptor switches between Pr and Pfr forms?

[Primary fact source](https://openstax.org/books/biology-2e/pages/30-6-plant-sensory-systems-and-responses) — The Phytochrome System: red/far-red photointerconvertible forms.

Red/far-red section explicitly names Pr/Pfr as phytochrome forms. Rewrote broad original flowering question to the distinctive photoreceptor forms so auxin/gibberellin involvement cannot create another answer. Phototropin, cryptochrome and chlorophyll do not have these forms.

### plants-transpiration-0001

Game ID: `plants_transpiration_0001`; source record: `miscellaneous/test/702`.

Как называется потеря растением воды в виде пара? / What is the loss of water from a plant as vapor called?

[Primary fact source](https://openstax.org/books/biology-2e/pages/30-5-transport-of-water-and-solutes-in-plants) — Movement of Water and Minerals in the Xylem: transpiration.

Xylem section defines water-vapor loss as transpiration and links evaporation to tension. Condensation is opposite phase change, fermentation a biochemical process, crystallization solid formation. RU/EN questions and explanations have equal scope.

## Full Apache License 2.0

```text

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
