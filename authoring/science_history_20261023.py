"""Selected free-bank adaptations and original bilingual drafts. Never writes approvals.

Fact checking and a separate wording/distractor pass are recorded in reviews/ only
after reading each draft. Re-running this script writes drafts, not published packs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT, EVIDENCE = [], {}
LICENSE = 'https://raw.githubusercontent.com/iamsomon/questiq-content/main/imports/global-mmlu/LICENSE-APACHE-2.0.txt'
CREDITS = 'https://github.com/iamsomon/questiq-content/blob/main/credits/global_mmlu_20261023.md'


def add(cat, slug, level, ru, en, options, fr, fe, url, location, source_id=None):
    pairs = [s.split('|') for s in options.split(';')]
    assert len(pairs) == 4 and all(len(p) == 2 for p in pairs)
    qid = f'{cat}_{slug}_0001'
    sources = [url]
    if source_id:
        fr += ' Адаптация: Global-MMLU, Cohere Labs и др., Apache 2.0.'
        fe += ' Adaptation: Global-MMLU, Cohere Labs et al., Apache 2.0.'
        # The existing app opens the first source. This page includes the exact
        # source ID, changes, primary fact link, attribution and full license.
        sources = [f'{CREDITS}#{qid.replace("_", "-")}', url, LICENSE]
    q = dict(id=qid, categoryId=cat, difficulty=level, type='single_choice', revision=1,
             localizations={'ru': dict(question=ru, explanation=fr), 'en': dict(question=en, explanation=fe)},
             options=[dict(id=f'o{i}', ru=p[0], en=p[1]) for i, p in enumerate(pairs)],
             correctOptionId='o0', sources=sources, image=None)
    OUT.append(q)
    EVIDENCE[qid] = dict(url=url, location=location, claim=f'{en} Answer: {pairs[0][1]}. {fe}',
                         sourceId=source_id, authorship='Global-MMLU adaptation' if source_id else 'Original bilingual wording')


B = 'https://openstax.org/books/biology-2e/pages/'
for slug, level, ru, en, op, fr, fe, page, loc, sid in [
('chloroplast', 'easy', 'В какой органелле растительной клетки происходит фотосинтез?', 'In which plant-cell organelle does photosynthesis take place?',
 'Хлоропласт|Chloroplast;Митохондрия|Mitochondrion;Ядро|Nucleus;Аппарат Гольджи|Golgi apparatus',
 'Хлорофилл в мембранах тилакоидов поглощает свет.', 'Chlorophyll in thylakoid membranes absorbs light.', '8-1-overview-of-photosynthesis', 'Main Structures: chloroplasts and thylakoid membranes', 'miscellaneous/test/222'),
('cactus_spines', 'easy', 'Какие органы у кактуса опунции превратились в колючки?', 'Which organs became spines in the prickly pear cactus?',
 'Листья|Leaves;Корни|Roots;Лепестки|Petals;Тычинки|Stamens',
 'Такая форма уменьшает потерю воды; фотосинтез идёт в зелёных стеблях.', 'This shape reduces water loss; photosynthesis takes place in green stems.', '30-5-transport-of-water-and-solutes-in-plants', 'Figure 30.35(a): modified leaves and photosynthetic stem', None),
('coast_redwood', 'easy', 'Какой вид известен самыми высокими современными деревьями?', 'Which species is known for the tallest living trees?',
 'Секвойя вечнозелёная|Coast redwood;Секвойядендрон гигантский|Giant sequoia;Ель ситхинская|Sitka spruce;Псевдотсуга Мензиса|Douglas fir',
 'Научное название вида — Sequoia sempervirens; речь идёт о высоте, а не объёме ствола.', 'The species is Sequoia sempervirens; height is distinct from trunk volume.', '30-5-transport-of-water-and-solutes-in-plants', 'Figure 30.31: coastal redwoods, tallest trees', 'miscellaneous/test/371'),
('flytrap_leaves', 'easy', 'Какой орган венериной мухоловки образует захлопывающуюся ловушку?', 'Which organ of a Venus flytrap forms its snapping trap?',
 'Лист|Leaf;Корень|Root;Цветок|Flower;Плод|Fruit',
 'Чувствительные волоски внутри ловушки реагируют на прикосновения добычи.', 'Sensitive hairs inside the trap respond to contact with prey.', 'https://www.kew.org/read-and-watch/carnivorous-plants', 'Venus flytraps: modified trap leaves; trigger hairs; lobes of a leaf', None),
('guard_cells', 'medium', 'Какие клетки регулируют открытие и закрытие устьица листа?', 'Which cells regulate the opening and closing of a leaf stoma?',
 'Замыкающие клетки|Guard cells;Корневые волоски|Root hair cells;Ситовидные элементы|Sieve elements;Клетки пробки|Cork cells',
 'Изменяя форму, пара этих клеток регулирует газообмен и потерю водяного пара.', 'By changing shape, a pair of these cells regulates gas exchange and water-vapor loss.', '30-5-transport-of-water-and-solutes-in-plants', 'Control of Transpiration: two guard cells surrounding stomata', 'miscellaneous/test/537'),
('transpiration', 'medium', 'Как называется потеря растением воды в виде пара?', 'What is the loss of water from a plant as vapor called?',
 'Транспирация|Transpiration;Конденсация|Condensation;Ферментация|Fermentation;Кристаллизация|Crystallization',
 'Испарение воды с поверхности листьев помогает создавать тягу в ксилеме.', 'Evaporation at leaf surfaces helps create tension in the xylem.', '30-5-transport-of-water-and-solutes-in-plants', 'Movement of Water and Minerals in the Xylem: transpiration', 'miscellaneous/test/702'),
('negative_gravitropism', 'medium', 'Как называется рост побега против направления силы тяжести?', 'What is shoot growth against the direction of gravity called?',
 'Отрицательный гравитропизм|Negative gravitropism;Положительный гравитропизм|Positive gravitropism;Положительный фототропизм|Positive phototropism;Отрицательный фототропизм|Negative phototropism',
 'Реакцию на силу тяжести отличают от фототропизма — реакции на направление света.', 'The response to gravity differs from phototropism, a response to light direction.', '30-6-plant-sensory-systems-and-responses', 'Plant Responses to Gravity: upward shoot growth', 'high_school_biology/test/175'),
('ethylene', 'medium', 'Какой газообразный растительный гормон способствует созреванию плодов?', 'Which gaseous plant hormone promotes fruit ripening?',
 'Этилен|Ethylene;Ауксин|Auxin;Цитокинин|Cytokinin;Абсцизовая кислота|Abscisic acid',
 'Выделяемый одним созревающим плодом газ может ускорять созревание соседних.', 'Gas released by one ripening fruit can accelerate the ripening of nearby fruit.', '30-6-plant-sensory-systems-and-responses', 'Ethylene: volatile hormone; paper bag and neighboring fruit', None),
('phytochrome', 'hard', 'Какой растительный фоторецептор переключается между формами Pr и Pfr?', 'Which plant photoreceptor switches between Pr and Pfr forms?',
 'Фитохром|Phytochrome;Фототропин|Phototropin;Криптохром|Cryptochrome;Хлорофилл a|Chlorophyll a',
 'Эти формы различаются поглощением красного и дальнего красного света.', 'The forms differ in their absorption of red and far-red light.', '30-6-plant-sensory-systems-and-responses', 'The Phytochrome System: red/far-red photointerconvertible forms', 'high_school_biology/test/176'),
('oxygen_source', 'hard', 'Из какого вещества образуется выделяемый растением O₂ при фотосинтезе?', 'Which substance supplies the O₂ released by a plant during photosynthesis?',
 'Вода (H₂O)|Water (H₂O);Углекислый газ (CO₂)|Carbon dioxide (CO₂);Пероксид водорода (H₂O₂)|Hydrogen peroxide (H₂O₂);Угарный газ (CO)|Carbon monoxide (CO)',
 'В световых реакциях вода расщепляется; для одной молекулы O₂ нужны две молекулы воды.', 'Water is split in the light reactions; two water molecules supply one O₂ molecule.', '8-2-the-light-dependent-reactions-of-photosynthesis', 'Photosystem II: water splitting and diatomic oxygen', 'high_school_biology/test/275'),
]:
    add('plants', slug, level, ru, en, op, fr, fe, page if page.startswith('https://') else B+page, loc, sid)

K = 'https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work'
D = 'https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works'
for slug, level, ru, en, op, fr, fe, url, loc, sid in [
('iris', 'easy', 'Как называется окрашенная часть глаза, окружающая зрачок?', 'What is the colored part of the eye surrounding the pupil called?',
 'Радужная оболочка|Iris;Роговица|Cornea;Сетчатка|Retina;Хрусталик|Lens',
 'Она изменяет размер зрачка и помогает регулировать количество поступающего света.', 'It changes pupil size and helps regulate how much light enters the eye.', 'https://www.nei.nih.gov/eye-health-information/healthy-vision/how-eyes-work', 'Iris: colored part controlling pupil size', 'miscellaneous/test/314'),
('paired_kidneys', 'easy', 'Какой из этих органов в обычном строении тела человека парный?', 'Which of these organs is paired in typical human anatomy?',
 'Почка|Kidney;Печень|Liver;Желудок|Stomach;Жёлчный пузырь|Gallbladder',
 'Две почки расположены по обе стороны позвоночника и фильтруют кровь.', 'Two kidneys lie on opposite sides of the spine and filter blood.', K, 'Opening: two bean-shaped organs, one on each side of spine', 'miscellaneous/test/569'),
('bladder', 'easy', 'В каком органе моча накапливается перед выведением из организма?', 'In which organ is urine stored before leaving the body?',
 'Мочевой пузырь|Urinary bladder;Жёлчный пузырь|Gallbladder;Желудок|Stomach;Поджелудочная железа|Pancreas',
 'Из почек моча поступает туда по мочеточникам.', 'Urine reaches this organ from the kidneys through the ureters.', K, 'Opening: ureters carry urine to bladder for storage', None),
('heart_chambers', 'easy', 'Сколько камер в нормальном сердце человека?', 'How many chambers does a normal human heart have?',
 '4|4;2|2;3|3;5|5',
 'Две верхние камеры — предсердия, две нижние — желудочки.', 'The two upper chambers are atria and the two lower chambers are ventricles.', 'https://www.nhlbi.nih.gov/health/heart/anatomy', 'Heart chambers: two atria and two ventricles', None),
('alveoli', 'medium', 'Как называются крошечные воздушные мешочки лёгких, где происходит газообмен?', 'What are the tiny air sacs in the lungs where gas exchange occurs called?',
 'Альвеолы|Alveoli;Бронхи|Bronchi;Бронхиолы|Bronchioles;Капилляры|Capillaries',
 'Через их стенки кислород переходит в кровь, а углекислый газ — из крови в воздух.', 'Across their walls, oxygen enters the blood and carbon dioxide moves from blood into air.', 'https://www.nhlbi.nih.gov/health/lungs/respiratory-system', 'Air fills your lung’s air sacs; Oxygen flows into your blood', 'anatomy/test/113'),
('cochlea', 'medium', 'Какая заполненная жидкостью структура внутреннего уха имеет спиральную форму?', 'Which fluid-filled structure in the inner ear has a spiral shape?',
 'Улитка|Cochlea;Барабанная перепонка|Eardrum;Слуховая труба|Eustachian tube;Ушная раковина|Pinna',
 'В ней находятся чувствительные волосковые клетки, участвующие в восприятии звука.', 'It contains sensory hair cells that help detect sound.', 'https://www.nidcd.nih.gov/health/how-do-we-hear', 'Steps 3–4: snail-shaped cochlea, fluid and hair cells', None),
('bile_producer', 'medium', 'Какой орган вырабатывает жёлчь?', 'Which organ produces bile?',
 'Печень|Liver;Жёлчный пузырь|Gallbladder;Поджелудочная железа|Pancreas;Желудок|Stomach',
 'Жёлчный пузырь хранит её, а сама жёлчь помогает переваривать жиры.', 'The gallbladder stores it; bile helps digest fats.', D, 'How does my digestive system break food into small parts? Liver and Gallbladder', None),
('olfactory_location', 'medium', 'Где расположены чувствительные нейроны, распознающие запахи?', 'Where are the sensory neurons that detect odors located?',
 'В верхней части носовой полости|High inside the nasal cavity;В наружном слуховом проходе|In the outer ear canal;В сетчатке глаза|In the retina;В пищеводе|In the esophagus',
 'Молекулы пахучих веществ воздействуют на их рецепторы, после чего сигнал поступает в мозг.', 'Odor molecules stimulate their receptors, and signals then travel to the brain.', 'https://www.nidcd.nih.gov/health/smell-disorders', 'How does your sense of smell work? Small patch high inside nose', None),
('ileum', 'hard', 'Какой из этих отделов входит в тонкую кишку?', 'Which of these structures is part of the small intestine?',
 'Подвздошная кишка|Ileum;Слепая кишка|Cecum;Восходящая ободочная кишка|Ascending colon;Сигмовидная ободочная кишка|Sigmoid colon',
 'Это её последний отдел; перед ним располагаются двенадцатиперстная и тощая кишки.', 'It is the final section, following the duodenum and jejunum.', D, 'What is the digestive system? Three parts of small intestine versus large intestine', 'anatomy/test/120'),
('nephron', 'hard', 'Как называется структурная единица почки, в которой фильтруется кровь и образуется моча?', 'What is the kidney unit in which blood is filtered and urine is formed called?',
 'Нефрон|Nephron;Нейрон|Neuron;Альвеола|Alveolus;Остеон|Osteon',
 'Он включает почечный клубочек и каналец, где нужные вещества возвращаются в кровь.', 'It includes a glomerulus and a tubule that returns needed substances to the blood.', K, 'How do my kidneys work? Nephron includes glomerulus and tubule', None),
]:
    add('human_body', slug, level, ru, en, op, fr, fe, url, loc, sid)

M = 'https://www.metmuseum.org/essays/greek-gods-and-religious-practices'
T = 'https://historiska.se/en/explore-history/history-hub/thor-god-of-thunder/'
O = 'https://historiska.se/utforska-historien/kunskapsbank/oden-gudarnas-ledare/'
for slug, level, ru, en, op, fr, fe, url, loc, sid in [
('olympus', 'easy', 'На какой горе, согласно древнегреческим мифам, жили олимпийские боги?', 'On which mountain did the Olympian gods live according to ancient Greek myths?',
 'Олимп|Olympus;Парнас|Parnassus;Этна|Etna;Ида|Ida',
 'Это мифологический дом богов; Зевс возглавлял олимпийский пантеон.', 'This was the gods’ mythical home; Zeus headed the Olympian pantheon.', M, 'Pantheon paragraph: Mount Olympus, home of gods', 'miscellaneous/test/651'),
('poseidon', 'easy', 'Кто был богом моря в древнегреческой мифологии?', 'Who was the god of the sea in ancient Greek mythology?',
 'Посейдон|Poseidon;Арес|Ares;Гефест|Hephaistos;Аполлон|Apollo',
 'По мифам, его братья Зевс и Аид властвовали над небом и подземным миром.', 'In the myths, his brothers Zeus and Hades ruled the sky and Underworld.', M, 'Zeus paragraph: brothers Hades and Poseidon, their domains', None),
('artemis', 'easy', 'Какая древнегреческая богиня покровительствовала охоте?', 'Which ancient Greek goddess was a patron of hunting?',
 'Артемида|Artemis;Афродита|Aphrodite;Гера|Hera;Деметра|Demeter',
 'Её часто изображали с луком и колчаном; Аполлон считался её братом-близнецом.', 'She was often shown with a bow and quiver; Apollo was her twin brother.', M, 'Apollo paragraph: Artemis, hunting, bow and quiver', None),
('mjolnir', 'easy', 'Какое оружие называлось Мьёльнир в скандинавских мифах?', 'What kind of weapon was Mjölnir in Norse mythology?',
 'Молот|Hammer;Копьё|Spear;Меч|Sword;Лук|Bow',
 'Им владел Тор, сражавшийся с великанами.', 'It belonged to Thor, who fought giants.', T, 'Mjölnir – Thor’s mighty hammer', None),
('hermes', 'medium', 'Какой бог выполнял роль вестника в древнегреческих мифах?', 'Which god served as a messenger in ancient Greek myths?',
 'Гермес|Hermes;Арес|Ares;Посейдон|Poseidon;Гефест|Hephaistos',
 'Среди его атрибутов — крылатые сандалии и жезл глашатая.', 'His attributes include winged sandals and a herald’s staff.', M, 'Apollo paragraph: Hermes, winged sandals and herald’s staff', None),
('dionysos', 'medium', 'Какой древнегреческий бог связан с вином и театром?', 'Which ancient Greek god is associated with wine and theater?',
 'Дионис|Dionysos;Арес|Ares;Аид|Hades;Гермес|Hermes',
 'Его почитание связывало виноделие, празднества и театральные представления.', 'His worship connected winemaking, festivals and theatrical performances.', M, 'Other important deities: Dionysos, wine and theater', None),
('odin_ravens', 'medium', 'Какими птицами были Хугин и Мунин, спутники Одина?', 'What birds were Huginn and Muninn, Odin’s companions?',
 'Воронами|Ravens;Орлами|Eagles;Соколами|Falcons;Совами|Owls',
 'В мифах они облетали мир и сообщали Одину об увиденном.', 'In the myths, they flew around the world and reported what they saw to Odin.', O, 'Oden har flera djur: two ravens Hugin och Munin report what they saw', None),
('anubis', 'medium', 'С головой какого животного обычно изображали древнеегипетского Анубиса?', 'With the head of which animal was the ancient Egyptian Anubis commonly depicted?',
 'Шакала|Jackal;Кошки|Cat;Сокола|Falcon;Крокодила|Crocodile',
 'Он был связан с бальзамированием и охраной погребений.', 'He was associated with embalming and the protection of graves.', 'https://egyptianmuseum.org/deities-Anubis', 'Anubis: black head of a jackal; cemeteries and embalming', None),
('athena_bird', 'hard', 'Какая птица была священной для Афины в древнегреческой традиции?', 'Which bird was sacred to Athena in ancient Greek tradition?',
 'Сова|Owl;Павлин|Peacock;Голубь|Dove;Лебедь|Swan',
 'С богиней связывали также оливковое дерево, ткачество и ремёсла.', 'The goddess was also associated with the olive tree, weaving and crafts.', M, 'Wise Athena paragraph: owl, olive tree, weaving and carpentry', None),
('thoth', 'hard', 'Какой древнеегипетский бог считался покровителем писцов?', 'Which ancient Egyptian god was a patron of scribes?',
 'Тот|Thoth;Собек|Sobek;Сет|Seth;Анубис|Anubis',
 'Его изображали ибисом или павианом и связывали с письмом и знанием.', 'He was depicted as an ibis or baboon and associated with writing and knowledge.', 'https://egyptianmuseum.org/deities-thoth', 'Thoth: patron of scribes; ibis or baboon; art of writing', None),
]:
    add('mythology', slug, level, ru, en, op, fr, fe, url, loc, sid)

E = 'https://egyptianmuseumcairo.eg/historical-timeline/'
Q = 'https://whc.unesco.org/en/list/441/'
for slug, level, ru, en, op, fr, fe, url, loc, sid in [
('cuneiform', 'easy', 'Какая древняя письменность получила название от клиновидных знаков?', 'Which ancient writing system takes its name from wedge-shaped signs?',
 'Клинопись|Cuneiform;Египетские иероглифы|Egyptian hieroglyphs;Финикийское письмо|Phoenician script;Линейное письмо Б|Linear B',
 'В Месопотамии такие знаки вдавливали в мягкую глину концом тростниковой или деревянной палочки.', 'In Mesopotamia, such signs were impressed into soft clay with a reed or wooden stylus.', 'https://www.metmuseum.org/essays/the-origins-of-writing', 'Clay medium; wedge-shaped signs; Latin cuneus', 'prehistory/test/17'),
('khufu', 'easy', 'Для какого фараона была построена Великая пирамида в Гизе?', 'For which pharaoh was the Great Pyramid at Giza built?',
 'Хуфу (Хеопс)|Khufu (Cheops);Джосер|Djoser;Снофру|Snefru;Рамсес II|Ramesses II',
 'Её относят к Древнему царству и IV династии.', 'It belongs to the Old Kingdom and the Fourth Dynasty.', E, 'Old Kingdom: Snefru, founder of Fourth Dynasty; Khufu and Great Pyramid', None),
('vesuvius', 'easy', 'Какой вулкан погреб под изверженными материалами Помпеи в 79 году н. э.?', 'Which volcano buried Pompeii under volcanic material in AD 79?',
 'Везувий|Vesuvius;Этна|Etna;Стромболи|Stromboli;Вулькано|Vulcano',
 'Извержение затронуло также Геркуланум; погребённые здания сохранили свидетельства римской жизни.', 'The eruption also struck Herculaneum; buried buildings preserved evidence of Roman life.', 'https://whc.unesco.org/en/list/829/', 'Description: Vesuvius, AD 79, Pompei and Herculaneum; day/month deliberately omitted', None),
('papyrus', 'easy', 'Из чего древние египтяне делали листы папируса для письма?', 'What did ancient Egyptians use to make papyrus writing sheets?',
 'Из сердцевины стеблей растения|The pith of plant stalks;Из обработанных шкур|Prepared animal skins;Из обожжённой глины|Fired clay;Из тонких медных пластин|Thin copper plates',
 'Полоски укладывали слоями и сушили под давлением.', 'Strips were laid in layers and dried under pressure.', 'https://www.metmuseum.org/essays/papyrus-in-ancient-egypt', 'Writing surface: strips of pith from stalk, layered and dried under pressure', None),
('upper_egypt', 'medium', 'В каком направлении от Нижнего Египта располагался Верхний Египет?', 'In which direction from Lower Egypt was Upper Egypt located?',
 'К югу|South;К северу|North;К востоку|East;К западу|West',
 'Нижний Египет соответствовал области дельты Нила, Верхний — южной части долины.', 'Lower Egypt corresponded to the Nile Delta, while Upper Egypt lay in the southern valley.', E, 'Predynastic – Early Dynastic Period: Delta (Lower Egypt), south (Upper Egypt)', 'prehistory/test/212'),
('qin_emperor', 'medium', 'С погребальным комплексом какого правителя связана знаменитая Терракотовая армия?', 'The famous Terracotta Army belongs to the burial complex of which ruler?',
 'Цинь Шихуанди|Qin Shi Huang;Хань У-ди|Emperor Wu of Han;Тан Тай-цзун|Emperor Taizong of Tang;Юнлэ|Yongle Emperor',
 'Это первый император объединённой державы Цинь; объединение датируют 221 годом до н. э.', 'He was the first emperor of the unified Qin state; unification is dated to 221 BC.', Q, 'Description and criterion (vi): Qin Shi Huang, first unification in 221 BCE', None),
('parthenon_deity', 'medium', 'Какой богине был посвящён афинский Парфенон?', 'To which goddess was the Parthenon in Athens dedicated?',
 'Афине|Athena;Гере|Hera;Артемиде|Artemis;Афродите|Aphrodite',
 'В главном зале стояла созданная Фидием статуя богини из золота и слоновой кости.', 'The main chamber held Pheidias’s gold-and-ivory statue of the goddess.', 'https://www.theacropolismuseum.gr/en/exhibit-halls/parthenon-gallery', 'The Parthenon: temple of Athena Parthenos; gold-and-ivory statue by Pheidias', None),
('rosetta_scholar', 'medium', 'Кто расшифровал египетские иероглифы в 1822 году, опираясь на Розеттский камень?', 'Who deciphered Egyptian hieroglyphs in 1822 using the Rosetta Stone?',
 'Жан-Франсуа Шампольон|Jean-François Champollion;Говард Картер|Howard Carter;Генрих Шлиман|Heinrich Schliemann;Артур Эванс|Arthur Evans',
 'Камень стал ключом к чтению древнеегипетских текстов благодаря сопоставлению надписей.', 'Comparing the inscriptions on the stone provided a key to reading ancient Egyptian texts.', 'https://rosetta-stone.dh.uni-leipzig.de/rs/the-rosetta-stone/index.html', 'The Rosetta Stone: Champollion deciphered hieroglyphs in 1822', None),
('colosseum_opening', 'hard', 'В каком году н. э. Тит устроил игры по случаю открытия Колизея?', 'In which year AD did Titus hold games to mark the opening of the Colosseum?',
 '80|80;44|44;117|117;212|212',
 'Празднества по случаю открытия амфитеатра продолжались сто дней.', 'The celebrations marking the amphitheater’s opening lasted one hundred days.', 'https://colosseo.it/en/event/blood-and-the-arena/', 'Opening paragraph: Titus, June–September 80 AD, 100 days; read via direct HTTPS after web timeout', None),
('terracotta_discovery', 'hard', 'В каком году была обнаружена Терракотовая армия у мавзолея первого императора Цинь?', 'In which year was the Terracotta Army at the first Qin emperor’s mausoleum discovered?',
 '1974|1974;1922|1922;1949|1949;1987|1987',
 'Скульптуры изображают воинов, лошадей и колесницы погребального комплекса.', 'The sculptures depict warriors, horses and chariots in the burial complex.', Q, 'Description: archaeological discovery in 1974; statues, horses and chariots', None),
]:
    add('ancient_world', slug, level, ru, en, op, fr, fe, url, loc, sid)


if __name__ == '__main__':
    for cat in sorted({q['categoryId'] for q in OUT}):
        (ROOT/'drafts'/f'science_history_20261023_{cat}.json').write_text(
            json.dumps([q for q in OUT if q['categoryId'] == cat], ensure_ascii=False, indent=2)+'\n')
    (ROOT/'authoring/science_history_20261023.evidence.json').write_text(json.dumps(EVIDENCE, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(OUT)} drafts written; no approvals created.')
