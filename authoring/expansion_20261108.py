"""Original bilingual draft batch. This script NEVER grants editorial approval."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT, EVIDENCE = [], {}
SOURCES = {}

def source(key, url):
    SOURCES[key] = url

def rows(category, text):
    for line in text.strip().splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        slug, level, prompt, options, explanation, src, location = line.split('§')
        ru, en = prompt.split('~'); fr, fe = explanation.split('~')
        pairs = [v.split('~') for v in options.split(';')]
        assert len(pairs)==4 and all(len(v)==2 for v in pairs), slug
        q = {'id':f'{category}_nov08_{slug}', 'categoryId':category,
             'difficulty':{'E':'easy','M':'medium','H':'hard'}[level],
             'type':'single_choice','revision':1,
             'localizations':{'ru':{'question':ru,'explanation':fr},'en':{'question':en,'explanation':fe}},
             'options':[{'id':f'o{i}','ru':v[0],'en':v[1]} for i,v in enumerate(pairs)],
             'correctOptionId':'o0','sources':[SOURCES[src]],'image':None}
        OUT.append(q)
        EVIDENCE[q['id']]={'url':SOURCES[src],'location':location,'claim':fe,'sourceKey':src}

source('pillars','https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/unit-one/the-five-pillars-of-islam')
source('mosque','https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/unit-one/the-mosque')
source('quran','https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/unit-one/the-quran')
source('hijra','https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/unit-one/the-prophet-muhammad-and-the-origins-of-islam')
rows('islam','''
shahada§E§Как называется исламское свидетельство веры?~What is the Islamic declaration of faith called?§Шахада~Shahada;Закят~Zakat;Хадж~Hajj;Саум~Sawm§Шахада утверждает веру в единого Бога и пророческую миссию Мухаммада.~The shahada affirms belief in one God and Muhammad's prophethood.§pillars§Profession of Faith
ramadan§E§В какой месяц исламского календаря соблюдают обязательный пост?~During which Islamic month is the obligatory fast observed?§Рамадан~Ramadan;Шавваль~Shawwal;Мухаррам~Muharram;Сафар~Safar§Рамадан — девятый месяц исламского календаря.~Ramadan is the ninth month of the Islamic calendar.§pillars§Fasting
hajj§E§В какой город совершают хадж?~To which city is the Hajj pilgrimage made?§Мекка~Mecca;Каир~Cairo;Дамаск~Damascus;Стамбул~Istanbul§В центре паломничества находится Кааба в Заповедной мечети.~The pilgrimage centres on the Kaaba in the Sacred Mosque.§pillars§Pilgrimage
zakat§E§С чем связан закят в исламе?~What does zakat concern in Islam?§Обязательная помощь нуждающимся~Obligatory almsgiving;Начало нового месяца~The start of a new month;Призыв к молитве~The call to prayer;Направление молитвы~The direction of prayer§Закят связывает религиозную практику с поддержкой членов общины.~Zakat connects religious practice with support for members of the community.§pillars§Alms
quran§E§Как называется священная книга ислама?~What is the holy book of Islam called?§Коран~Qur'an;Тора~Torah;Трипитака~Tripitaka;Авеста~Avesta§Мусульмане считают Коран откровением, переданным пророку Мухаммаду.~Muslims regard the Qur'an as revelation conveyed to the Prophet Muhammad.§quran§Opening paragraphs
mosque§E§Как называется мусульманский молитвенный дом?~What is a Muslim house of worship called?§Мечеть~Mosque;Синагога~Synagogue;Собор~Cathedral;Гурдвара~Gurdwara§Арабское слово «масджид» связано с земным поклоном.~The Arabic word masjid refers to a place of prostration.§mosque§Opening paragraph
salat§E§Как в исламской традиции называется установленная молитва?~What is the prescribed ritual prayer called in Islamic tradition?§Салят~Salat;Хадж~Hajj;Закят~Zakat;Саум~Sawm§Молитва входит в число пяти столпов ислама.~Prayer is one of the five pillars of Islam.§pillars§Prayer
imam§E§Кто обычно руководит совместной молитвой в мечети?~Who usually leads congregational prayer in a mosque?§Имам~Imam;Муэдзин~Muezzin;Каллиграф~Calligrapher;Архитектор~Architect§Имам ведёт молящихся; призыв к молитве — другая функция.~The imam leads the congregation; issuing the call to prayer is a different role.§pillars§Prayer
qibla§M§Как называется направление, в котором мусульмане молятся?~What is the direction Muslims face in prayer called?§Кибла~Qibla;Минбар~Minbar;Сахн~Sahn;Минарет~Minaret§Кибла направлена к Каабе в Мекке.~The qibla points toward the Kaaba in Mecca.§mosque§Essential Architectural Elements
mihrab§M§Какая ниша в мечети указывает направление молитвы?~Which niche in a mosque indicates the direction of prayer?§Михраб~Mihrab;Минбар~Minbar;Минарет~Minaret;Сахн~Sahn§Михраб устраивают в стене, обращённой к Мекке.~The mihrab is set into the wall facing Mecca.§mosque§Mihrab
minbar§M§С какого сооружения в мечети произносят проповедь?~From which structure in a mosque is a sermon delivered?§Минбар~Minbar;Михраб~Mihrab;Минарет~Minaret;Фонтан~Fountain§Минбар — возвышение, часто выполненное в виде лестницы.~The minbar is a raised pulpit, often shaped like a staircase.§mosque§Minbar
minaret§M§Какая башня традиционно связана с призывом к молитве?~Which tower is traditionally associated with the call to prayer?§Минарет~Minaret;Пагода~Pagoda;Колокольня~Bell tower;Донжон~Keep§Минарет расположен при мечети и служит заметным архитектурным ориентиром.~A minaret stands at or beside a mosque as a prominent architectural marker.§mosque§Minaret
sawm§M§Как называется пост среди пяти столпов ислама?~Which term names fasting among the five pillars of Islam?§Саум~Sawm;Шахада~Shahada;Закят~Zakat;Хадж~Hajj§В Рамадан пост соблюдают в светлое время суток.~During Ramadan, fasting takes place during daylight hours.§pillars§Fasting
friday§M§Какой день особенно связан с еженедельной общей молитвой в мечети?~Which day is especially associated with weekly congregational mosque prayer?§Пятница~Friday;Понедельник~Monday;Среда~Wednesday;Воскресенье~Sunday§Пятничная полуденная молитва сопровождается проповедью.~Friday's midday congregational prayer includes a sermon.§pillars§Prayer paragraph
five§M§Сколько ежедневных молитв указано среди пяти столпов ислама?~How many daily prayers are described among the five pillars of Islam?§Пять~Five;Три~Three;Семь~Seven;Девять~Nine§Время молитв связано с разными частями дня, от рассвета до ночи.~Prayer times mark different parts of the day, from dawn to night.§pillars§Prayer
hijra§M§В какой город Мухаммад и его последователи переселились из Мекки в 622 году?~To which city did Muhammad and his followers migrate from Mecca in 622?§Медина~Medina;Багдад~Baghdad;Кордова~Cordoba;Каир~Cairo§Это переселение называют хиджрой; с ним связано начало исламского летоисчисления.~This migration is called the Hijra and marks the starting point of the Islamic era.§hijra§Migration to Medina
sahn§H§Что означает «сахн» в архитектуре мечети?~What does sahn mean in mosque architecture?§Внутренний двор~Courtyard;Молитвенная ниша~Prayer niche;Кафедра проповедника~Sermon pulpit;Высокая башня~Tall tower§В таком дворе нередко находится фонтан для ритуального омовения.~Such courtyards often contain a fountain for ritual washing.§mosque§Sahn and fountain
surah§H§Как называют отдельную главу Корана?~What is a chapter of the Qur'an called?§Сура~Surah;Аят~Ayah;Хадис~Hadith;Минбар~Minbar§Суры разделены на аяты — отдельные стихи текста.~Surahs are divided into ayahs, the individual verses of the text.§quran§Organization into chapters and verses
hadith§H§Как называют сообщения о словах и поступках пророка Мухаммада?~What are reports of the Prophet Muhammad's sayings and actions called?§Хадисы~Hadith;Суры~Surahs;Минареты~Minarets;Михрабы~Mihrabs§Хадисы относятся к передаче пророческой традиции и отличаются от текста Корана.~Hadith transmit prophetic tradition and are distinct from the Qur'an itself.§hijra§Opening discussion of hadith and sunna
safa§H§Между какими холмами совершают один из обрядов паломничества в Мекке?~Between which hills is one of the Mecca pilgrimage rites performed?§Сафа и Марва~Safa and Marwa;Синай и Фавор~Sinai and Tabor;Сион и Мориа~Zion and Moriah;Палатин и Капитолий~Palatine and Capitoline§Обряд связан с преданием об Исмаиле и его матери.~The rite recalls the tradition concerning Ishmael and his mother.§pillars§Pilgrimage rituals
''')
source('buddha','https://www.metmuseum.org/essays/buddhism-and-buddhist-art')
source('mudra','https://www.metmuseum.org/essays/recognizing-the-gods')
source('buddhasites','https://whc.unesco.org/en/list/666/')
source('borobudur','https://whc.unesco.org/en/list/592/')
source('lumbini','https://whc.unesco.org/en/list/666/')
source('bodhgaya','https://whc.unesco.org/en/list/1056/')
source('sanchi','https://whc.unesco.org/en/list/524/')
rows('buddhism','''
siddhartha§E§Какое имя носил исторический Будда до просветления?~What name did the historical Buddha bear before enlightenment?§Сиддхартха~Siddhartha;Конфуций~Confucius;Махавира~Mahavira;Лао-цзы~Laozi§В буддийской традиции Сиддхартха отказался от дворцовой жизни ради духовного поиска.~In Buddhist tradition, Siddhartha left palace life to pursue a spiritual quest.§buddha§Siddhartha's life
meaning§E§Что означает титул «Будда»?~What does the title Buddha mean?§Пробуждённый~Awakened One;Великий царь~Great King;Хранитель огня~Keeper of Fire;Небесный воин~Heavenly Warrior§Титул связан с достижением просветления, а не с царской должностью.~The title refers to enlightenment rather than a royal office.§buddha§Enlightened One
bodhi§E§Под каким деревом, согласно буддийской традиции, Будда достиг просветления?~Under which tree did the Buddha attain enlightenment in Buddhist tradition?§Дерево бодхи~Bodhi tree;Олива~Olive tree;Кедр~Cedar;Баобаб~Baobab§Место просветления почитается в Бодх-Гае.~The place of enlightenment is venerated at Bodh Gaya.§bodhgaya§Brief synthesis
stupa§E§Как называется буддийское сооружение, традиционно хранящее реликвии?~What is a Buddhist monument traditionally containing relics called?§Ступа~Stupa;Минарет~Minaret;Баптистерий~Baptistery;Зиккурат~Ziggurat§Ступы стали важными центрами паломничества и монастырских комплексов.~Stupas became important centres of pilgrimage and monastic complexes.§buddha§Relics and stupas
meditation§E§Какая практика изображена у Будды, сидящего со сложенными на коленях ладонями?~Which practice is shown by a Buddha seated with palms together in the lap?§Медитация~Meditation;Стрельба из лука~Archery;Ткачество~Weaving;Игра на флейте~Flute playing§Такое положение рук называют дхьяна-мудрой.~This hand position is called the dhyana mudra.§mudra§Dhyana mudra
middle§E§Как называют путь Будды, отвергающий и роскошь, и крайнее самоистязание?~What is the Buddha's path rejecting both luxury and extreme self-mortification called?§Срединный путь~Middle Path;Царский путь~Royal Path;Северный путь~Northern Path;Морской путь~Sea Route§Согласно традиции, Будда отказался от бесплодной суровой аскезы.~According to tradition, the Buddha abandoned severe asceticism as unproductive.§buddha§Middle Path
borobudur§E§В какой современной стране находится буддийский храмовый комплекс Боробудур?~In which modern country is the Buddhist temple complex Borobudur?§Индонезия~Indonesia;Индия~India;Непал~Nepal;Китай~China§Комплекс расположен в центральной части острова Ява.~The complex stands in central Java.§borobudur§Brief synthesis
lumbini§E§С какой современной страной связано место рождения Будды в Лумбини?~Which modern country contains Lumbini, the traditional birthplace of the Buddha?§Непал~Nepal;Шри-Ланка~Sri Lanka;Таиланд~Thailand;Япония~Japan§Лумбини — место буддийского паломничества в южном Непале.~Lumbini is a Buddhist pilgrimage site in southern Nepal.§lumbini§Brief synthesis
karma§M§С чем буддийская традиция связывает карму?~What does Buddhist tradition associate karma with?§Поступки и их последствия~Actions and their consequences;Фазы Луны~Phases of the Moon;Высота гор~Mountain height;Цвет одежды~Clothing colour§В учении о перерождении поступки влияют на будущую жизнь.~In teachings on rebirth, deeds influence a future life.§buddha§Karma and rebirth
nirvana§M§Как называют освобождение от круговорота перерождений в буддизме?~What is release from the cycle of rebirth called in Buddhism?§Нирвана~Nirvana;Мудра~Mudra;Мандала~Mandala;Джатака~Jataka§Нирвана обозначает духовную цель, а не название храма или жеста.~Nirvana names a spiritual goal, rather than a temple or a gesture.§buddha§Nirvana
jataka§M§О чём рассказывают джатаки?~What do Jataka tales recount?§О прежних жизнях Будды~The Buddha's previous lives;О военных походах Цезаря~Caesar's military campaigns;О созвездиях зодиака~The zodiac constellations;О родословной фараонов~The pharaohs' genealogy§Эти истории использовались в буддийском искусстве и наставлении.~These stories were used in Buddhist art and teaching.§buddha§Narrative reliefs and jatakas
maitreya§M§Какого Будду в буддийской традиции связывают с будущим?~Which Buddha is associated with the future in Buddhist tradition?§Майтрея~Maitreya;Шакьямуни~Shakyamuni;Амитабха~Amitabha;Вайрочана~Vairocana§Майтрею изображают как будущего Будду, а также как бодхисаттву.~Maitreya is portrayed as a future Buddha and also as a bodhisattva.§buddha§Maitreya
mudra§M§Как называют символическое положение рук в буддийском искусстве?~What is a symbolic hand position in Buddhist art called?§Мудра~Mudra;Сутра~Sutra;Ступа~Stupa;Джатака~Jataka§Разные мудры передают медитацию, наставление или защиту.~Different mudras convey meditation, teaching or protection.§mudra§Hand gestures
silk§M§По какому историческому торговому пути буддизм распространялся в Китай?~Along which historic trade route did Buddhism spread to China?§Шёлковый путь~Silk Road;Янтарный путь~Amber Road;Путь из варяг в греки~Varangian Route;Королевская дорога инков~Inca Royal Road§Паломники и торговцы переносили тексты и художественные образы через Центральную Азию.~Pilgrims and traders carried texts and artistic images through Central Asia.§buddha§Gupta images and Silk Road
sanchi§M§Какой индийский памятник известен большой буддийской ступой?~Which Indian site is known for its Great Buddhist Stupa?§Санчи~Sanchi;Кносс~Knossos;Персеполь~Persepolis;Помпеи~Pompeii§Санчи хранит сооружения, связанные с длительной историей буддийского искусства.~Sanchi preserves monuments spanning a long history of Buddhist art.§sanchi§Brief synthesis
bodhgaya§M§С каким событием буддийская традиция связывает Бодх-Гаю?~Which event is associated with Bodh Gaya in Buddhist tradition?§Просветление Будды~The Buddha's enlightenment;Рождение Будды~The Buddha's birth;Рождение Конфуция~The birth of Confucius;Основание Рима~The founding of Rome§Храм Махабодхи отмечает место, связанное с этим событием.~The Mahabodhi Temple marks the place associated with this event.§bodhgaya§Brief synthesis
aniconic§H§Как в раннем буддийском искусстве могли обозначать присутствие Будды без человеческой фигуры?~How could early Buddhist art indicate the Buddha without a human figure?§Отпечатками стоп~Footprints;Римским орлом~A Roman eagle;Трезубцем Посейдона~Poseidon's trident;Лавровым венком Цезаря~Caesar's laurel wreath§Использовались также пустое сиденье и пространство под зонтом.~An empty seat and the space beneath a parasol were also used.§buddha§Early non-human representations
circumambulation§H§Какое ритуальное действие выполняют вокруг ступы?~Which ritual action is performed around a stupa?§Обход по кругу~Circumambulation;Подъём на вершину~Climbing to the top;Прыжок через огонь~Jumping over fire;Погружение в воду~Immersion in water§Вокруг ступы предусматривается путь для ритуального обхода.~A path around a stupa allows ritual circumambulation.§buddha§Stupa railings
avalokiteshvara§H§С каким качеством в буддийском искусстве связан бодхисаттва Авалокитешвара?~Which quality is associated with the bodhisattva Avalokiteshvara in Buddhist art?§Сострадание~Compassion;Военная власть~Military power;Морская торговля~Maritime trade;Земледелие~Agriculture§В коллекции Метрополитен-музея он назван бодхисаттвой бесконечного сострадания.~The Met's collection identifies him as the Bodhisattva of Infinite Compassion.§buddha§Avalokiteshvara object caption
lotus§H§Как называется распространённая поза медитации со скрещёнными ногами?~What is the common cross-legged meditation posture called?§Поза лотоса~Lotus posture;Поза орла~Eagle posture;Поза лодки~Boat posture;Поза дерева~Tree posture§В искусствоведческой терминологии эту позу называют падмасаной.~In art-historical terminology this posture is called padmasana.§mudra§Padmasana
''')

source('christ','https://www.metmuseum.org/essays/life-of-jesus-of-nazareth')
source('christintro','https://pluralism.org/introduction-to-christianity')
rows('christianity','''
gospels§E§Сколько канонических Евангелий входит в Новый Завет?~How many canonical Gospels are in the New Testament?§Четыре~Four;Два~Two;Шесть~Six;Двенадцать~Twelve§Это Евангелия от Матфея, Марка, Луки и Иоанна.~They are the Gospels of Matthew, Mark, Luke and John.§christ§Opening paragraph on the Gospels
nativity§E§Какое событие отмечает христианское Рождество?~Which event does Christian Christmas celebrate?§Рождение Иисуса~The birth of Jesus;Крещение Иисуса~The baptism of Jesus;Воскресение Иисуса~The resurrection of Jesus;Вознесение Иисуса~The ascension of Jesus§В евангельском повествовании рождение Иисуса связано с Вифлеемом.~The Gospel narrative places Jesus' birth in Bethlehem.§christ§Nativity
mary§E§Как зовут мать Иисуса в христианской традиции?~What is the name of Jesus' mother in Christian tradition?§Мария~Mary;Елизавета~Elizabeth;Марфа~Martha;Руфь~Ruth§Её образ занимает важное место в христианском искусстве.~Her image occupies an important place in Christian art.§christ§Mary and Joseph
john§E§Кто крестил Иисуса, согласно Евангелиям?~Who baptised Jesus according to the Gospels?§Иоанн Креститель~John the Baptist;Апостол Пётр~The apostle Peter;Моисей~Moses;Пророк Илия~The prophet Elijah§Евангельское повествование связывает крещение с рекой Иордан.~The Gospel account associates the baptism with the River Jordan.§christ§Baptism of Jesus
easter§E§Какое событие является центральным для христианской Пасхи?~Which event is central to Christian Easter?§Воскресение Иисуса~The resurrection of Jesus;Рождение Иисуса~The birth of Jesus;Благовещение~The Annunciation;Вход в Иерусалим~The entry into Jerusalem§Пасхальное празднование связано с евангельскими рассказами о пустой гробнице.~The Easter celebration is linked to the Gospel accounts of the empty tomb.§christ§Resurrection
apostles§E§Сколько ближайших учеников входило в первоначальный круг апостолов Иисуса?~How many disciples belonged to the original circle of Jesus' apostles?§Двенадцать~Twelve;Четыре~Four;Семь~Seven;Сорок~Forty§Их называют учениками и апостолами в рассказах о служении Иисуса.~They are called disciples and apostles in accounts of Jesus' ministry.§christ§Twelve disciples
cross§E§С каким евангельским событием связан крест как христианский символ?~Which Gospel event is associated with the cross as a Christian symbol?§Распятие~The Crucifixion;Благовещение~The Annunciation;Крещение~The Baptism;Преображение~The Transfiguration§Распятие относится к повествованию о Страстях Христовых.~The Crucifixion forms part of the account of Christ's Passion.§christ§Passion and Crucifixion
bethlehem§E§В каком городе родился Иисус, согласно евангельской традиции?~In which town was Jesus born according to Gospel tradition?§Вифлеем~Bethlehem;Назарет~Nazareth;Капернаум~Capernaum;Кесария~Caesarea§Традиция связывает детство Иисуса также с Назаретом.~The tradition also associates Jesus' childhood with Nazareth.§christ§Nativity and return to Nazareth
annunciation§M§Как называют весть архангела Гавриила Марии о рождении Иисуса?~What is Gabriel's announcement to Mary of Jesus' birth called?§Благовещение~The Annunciation;Преображение~The Transfiguration;Вознесение~The Ascension;Пятидесятница~Pentecost§Этот сюжет часто изображали на алтарных картинах.~This scene was often represented in altarpieces.§christ§Annunciation
supper§M§Как называют последнюю трапезу Иисуса с учениками перед арестом?~What is Jesus' final meal with his disciples before his arrest called?§Тайная вечеря~The Last Supper;Благовещение~The Annunciation;Богоявление~The Epiphany;Сретение~The Presentation§В евангельском повествовании она происходит в Иерусалиме.~In the Gospel narrative it takes place in Jerusalem.§christ§Passion and Last Supper
jordan§M§На какой реке, согласно Евангелиям, крестили Иисуса?~In which river was Jesus baptised according to the Gospels?§Иордан~Jordan;Нил~Nile;Евфрат~Euphrates;Тибр~Tiber§Река входит в географию евангельского рассказа о начале его служения.~The river belongs to the geography of the Gospel account of the start of his ministry.§christ§Baptism
parables§M§Как называют короткие поучительные истории, которыми Иисус часто передавал учение?~What are the short instructive stories Jesus often used in his teaching called?§Притчи~Parables;Эпитафии~Epitaphs;Летописи~Chronicles;Генеалогии~Genealogies§Такие рассказы объясняют идеи через понятные образы и ситуации.~Such stories explain ideas through familiar images and situations.§christ§Teachings delivered in parables
gethsemane§M§Как называется сад, где Иисус молился перед арестом?~What is the garden where Jesus prayed before his arrest called?§Гефсимания~Gethsemane;Эдем~Eden;Вавилон~Babylon;Синай~Sinai§Этот эпизод относится к повествованию о Страстях.~This episode belongs to the Passion narrative.§christ§Agony in the Garden
jerusalem§M§В какой город Иисус входит перед событиями Страстной недели?~Which city does Jesus enter before the events of Holy Week?§Иерусалим~Jerusalem;Антиохия~Antioch;Александрия~Alexandria;Рим~Rome§Евангелия связывают этот вход с паломничеством на праздник Пасхи.~The Gospels connect the entry with a Passover pilgrimage.§christ§Entry into Jerusalem
ascension§M§Какое событие в христианской традиции означает восхождение Иисуса на небо?~What is Jesus' rising to heaven called in Christian tradition?§Вознесение~Ascension;Преображение~Transfiguration;Сретение~Presentation;Благовещение~Annunciation§В церковном повествовании это событие следует после Воскресения.~In the church narrative this event follows the Resurrection.§christ§Ascension
pentecost§M§С каким событием связан христианский праздник Пятидесятницы?~Which event is associated with Christian Pentecost?§Сошествие Святого Духа на учеников~The Holy Spirit descending on the disciples;Рождение Иисуса~Jesus' birth;Крещение Иисуса~Jesus' baptism;Перепись Августа~Augustus' census§Рассказ об этом событии содержится в Деяниях апостолов.~The event is recounted in the Acts of the Apostles.§christ§Final paragraph on Shavuot and Holy Spirit
christ_title§H§Что означает греческое слово «Христос»?~What does the Greek word Christos mean?§Помазанник~Anointed one;Учитель письма~Writing teacher;Путешественник~Traveller;Каменщик~Stonemason§Это титул, соответствующий еврейскому слову «мессия».~It is a title corresponding to the Hebrew word Messiah.§christ§Meaning of Christ
transfiguration§H§С кем Иисус беседует в евангельском рассказе о Преображении?~With whom does Jesus speak in the Gospel account of the Transfiguration?§С Моисеем и Илиёй~Moses and Elijah;С Августом и Тиберием~Augustus and Tiberius;С Каином и Авелем~Cain and Abel;С Иродом и Пилатом~Herod and Pilate§Сцену наблюдают Пётр, Иаков и Иоанн.~Peter, James and John witness the scene.§christ§Transfiguration
emmaus§H§С каким событием связан сюжет «Путь в Эммаус»?~Which event is associated with the Road to Emmaus scene?§Явление воскресшего Иисуса ученикам~The risen Jesus appearing to disciples;Бегство Святого семейства в Египет~The Holy Family's flight into Egypt;Крещение Иисуса в Иордане~Jesus' baptism in the Jordan;Рождение Иоанна Крестителя~The birth of John the Baptist§Этот сюжет относится к рассказам о событиях после Воскресения.~This scene belongs to accounts of events after the Resurrection.§christ§Journey to Emmaus
visitation§H§Кого посещает Мария в христианском сюжете «Встреча Марии и Елизаветы»?~Whom does Mary visit in the Christian scene called the Visitation?§Елизавету~Elizabeth;Марфу~Martha;Руфь~Ruth;Сарру~Sarah§Елизавета в этом повествовании ожидает рождения Иоанна Крестителя.~Elizabeth is expecting the birth of John the Baptist in this narrative.§christ§Visitation
''')
source('judaism','https://pluralism.org/introduction-to-judaism')
source('hindu','https://pluralism.org/introduction-to-hinduism')
source('sikh','https://pluralism.org/introduction-to-sikhism')
source('jain','https://pluralism.org/introduction-to-jainism')
source('shinto','https://pluralism.org/introduction-to-shinto')
source('zoroastrian','https://pluralism.org/introduction-to-zoroastrianism')
rows('world_religions','''
synagogue§E§Как называется еврейский молитвенный дом?~What is a Jewish house of worship called?§Синагога~Synagogue;Мечеть~Mosque;Гурдвара~Gurdwara;Пагода~Pagoda§Синагога служит также местом учёбы и собраний общины.~A synagogue also serves as a place for learning and community gatherings.§judaism§Synagogue and community
rabbi§E§Как называют учителя и знатока религиозного закона в иудаизме?~What is a teacher and scholar of religious law in Judaism called?§Раввин~Rabbi;Имам~Imam;Гуру~Guru;Лама~Lama§Раввинская традиция связана с изучением и толкованием Торы.~The rabbinic tradition is associated with studying and interpreting the Torah.§judaism§Rabbinic tradition
torah§E§Какой текст занимает центральное место в иудаизме?~Which text has a central place in Judaism?§Тора~Torah;Коран~Qur'an;Авеста~Avesta;Веды~Vedas§В узком смысле Тора обозначает Пятикнижие Моисея.~In its narrower sense, Torah denotes the Five Books of Moses.§judaism§Torah
nanak§E§Кто считается первым гуру сикхской традиции?~Who is regarded as the first Guru of the Sikh tradition?§Гуру Нанак~Guru Nanak;Махавира~Mahavira;Конфуций~Confucius;Заратустра~Zarathustra§Сикхская традиция возникла в Пенджабе.~The Sikh tradition arose in the Punjab.§sikh§Guru Nanak
vedas§E§С какой религиозной традицией связаны Веды?~With which religious tradition are the Vedas associated?§Индуизм~Hinduism;Иудаизм~Judaism;Сикхизм~Sikhism;Христианство~Christianity§Веды относятся к древнейшему слою священных текстов индуизма.~The Vedas belong to the oldest layer of Hindu sacred texts.§hindu§Vedas
sabbath§E§Как называется еженедельный день покоя в иудаизме?~What is the weekly day of rest in Judaism called?§Шаббат~Shabbat;Навруз~Nowruz;Дивали~Diwali;Весак~Vesak§Его соблюдение связано с освящением времени и общинной жизнью.~Its observance connects sacred time with community life.§judaism§Shabbat
ahimsa§E§Какое понятие особенно важно для джайнского принципа ненасилия?~Which term is especially important to Jain nonviolence?§Ахимса~Ahimsa;Хиджра~Hijra;Шахада~Shahada;Хадж~Hajj§Ахимса означает стремление не причинять вред живым существам.~Ahimsa means striving not to harm living beings.§jain§Nonviolence
shinto_japan§E§С какой страной исторически связан синтоизм?~With which country is Shinto historically associated?§Япония~Japan;Египет~Egypt;Мексика~Mexico;Норвегия~Norway§Синтоистская традиция связана с почитанием ками и святилищами.~The Shinto tradition is associated with reverence for kami and with shrines.§shinto§Japanese tradition
gurdwara§M§Как называется сикхское место богослужения?~What is a Sikh place of worship called?§Гурдвара~Gurdwara;Синагога~Synagogue;Минарет~Minaret;Баптистерий~Baptistery§В гурдваре центральное место занимает Гуру Грантх Сахиб.~The Guru Granth Sahib occupies the central place in a gurdwara.§sikh§Gurdwara
granth§M§Как называется священное писание, почитаемое сикхами как вечный Гуру?~Which Sikh scripture is revered as the eternal Guru?§Гуру Грантх Сахиб~Guru Granth Sahib;Трипитака~Tripitaka;Талмуд~Talmud;Авеста~Avesta§После линии человеческих гуру духовный авторитет связан с этим писанием.~After the line of human Gurus, spiritual authority is associated with this scripture.§sikh§Guru Granth Sahib
langar§M§Что означает сикхская практика лангара?~What does the Sikh practice of langar involve?§Общая бесплатная трапеза~A free communal meal;Одинокое паломничество~A solitary pilgrimage;Пост весь год~Fasting all year;Запрет совместной еды~A ban on eating together§Лангар подчёркивает равенство людей независимо от происхождения.~Langar emphasises people's equality regardless of background.§sikh§Langar
puja§M§Как называют акт почитания божества в индуистской практике?~What is an act of worship of a deity in Hindu practice called?§Пуджа~Puja;Шаббат~Shabbat;Закят~Zakat;Хадж~Hajj§Пуджу могут совершать дома или в храме.~Puja may be performed at home or in a temple.§hindu§Worship and puja
kami§M§Как в синтоистской традиции называют почитаемые священные силы или присутствия?~What are the revered sacred powers or presences in Shinto called?§Ками~Kami;Апостолы~Apostles;Тиртханкары~Tirthankaras;Раввины~Rabbis§Ками могут быть связаны с природными местами и предками.~Kami may be associated with natural places and ancestors.§shinto§Kami
zoroaster§M§С именем какого учителя связана зороастрийская традиция?~Which teacher is associated with the Zoroastrian tradition?§Заратустра~Zarathustra;Нанак~Nanak;Лао-цзы~Laozi;Махавира~Mahavira§Другое распространённое имя Заратустры — Зороастр.~Another familiar form of Zarathustra's name is Zoroaster.§zoroastrian§Zarathustra
avesta§M§Как называется собрание священных текстов зороастризма?~What is the collection of Zoroastrian sacred texts called?§Авеста~Avesta;Талмуд~Talmud;Веды~Vedas;Трипитака~Tripitaka§Древнейшие гимны в этой традиции известны как Гаты.~The oldest hymns in this tradition are known as the Gathas.§zoroastrian§Avesta and Gathas
monotheism§M§Как называется вера в единого Бога?~What is belief in one God called?§Монотеизм~Monotheism;Политеизм~Polytheism;Анимизм~Animism;Дуализм~Dualism§Иудаизм, христианство и ислам обычно относят к монотеистическим традициям.~Judaism, Christianity and Islam are commonly classified as monotheistic traditions.§judaism§One God and covenant
mahavira§H§Какой учитель считается двадцать четвёртым тиртханкарой в джайнизме?~Which teacher is regarded as the twenty-fourth Tirthankara in Jainism?§Махавира~Mahavira;Будда~Buddha;Гуру Нанак~Guru Nanak;Заратустра~Zarathustra§Тиртханкары — духовные учителя джайнской традиции.~Tirthankaras are spiritual teachers in the Jain tradition.§jain§Mahavira
upanishads§H§С какой традицией связаны философские тексты Упанишад?~With which tradition are the philosophical texts called the Upanishads associated?§Индуизм~Hinduism;Сикхизм~Sikhism;Христианство~Christianity;Синтоизм~Shinto§Упанишады обсуждают, в частности, природу личности и высшей реальности.~The Upanishads discuss, among other things, the nature of self and ultimate reality.§hindu§Upanishads
khalsa§H§Как называется сикхская община посвящённых, учреждённая Гуру Гобиндом Сингхом в 1699 году?~What is the initiated Sikh community established by Guru Gobind Singh in 1699 called?§Хальса~Khalsa;Сангха~Sangha;Умма~Ummah;Синод~Synod§Создание Хальсы стало важным событием в истории сикхской общины.~The establishment of the Khalsa was a major event in Sikh community history.§sikh§Khalsa
covenant§H§Какое понятие описывает особые отношения между Богом и народом Израиля в иудаизме?~Which concept describes the relationship between God and the people of Israel in Judaism?§Завет~Covenant;Карма~Karma;Нирвана~Nirvana;Мудра~Mudra§Завет связывает религиозное предание с обязательствами общины.~The covenant connects religious tradition with obligations of the community.§judaism§Covenant
''')

source('sleepstages','https://www.nhlbi.nih.gov/health/sleep/stages-of-sleep')
source('sleepwhy','https://www.nhlbi.nih.gov/health/sleep/why-sleep-important')
source('hands','https://www.cdc.gov/clean-hands/about/index.html')
source('nutrition','https://www.fda.gov/food/nutrition-facts-label/how-understand-and-use-nutrition-facts-label')
source('immune','https://www.who.int/news-room/feature-stories/detail/how-do-vaccines-work')
rows('health','''
calorie§E§Что выражает калорийность пищи?~What does the calorie content of food express?§Количество энергии~Amount of energy;Объём воды~Volume of water;Степень кислотности~Degree of acidity;Температуру хранения~Storage temperature§Калории на этикетке описывают энергию, получаемую из указанного количества пищи.~Calories on a food label describe the energy supplied by the stated quantity of food.§nutrition§Calories
soap§E§Что вместе с проточной водой используют при обычном мытье рук?~What is used with running water for ordinary handwashing?§Мыло~Soap;Растительное масло~Vegetable oil;Сахар~Sugar;Сухую муку~Dry flour§Намыливание помогает удалять загрязнения с разных участков рук.~Lathering helps remove contamination from different parts of the hands.§hands§How it works
hygiene§E§Как мытьё рук влияет на распространение микробов?~How does handwashing affect the spread of germs?§Помогает уменьшить распространение~Helps reduce transmission;Гарантирует отсутствие всех болезней~Guarantees freedom from every disease;Заменяет сон~Replaces sleep;Создаёт микробы на коже~Creates germs on skin§Загрязнённые руки могут переносить микробы на пищу и поверхности.~Contaminated hands can carry germs to food and surfaces.§hands§Why it's important
sleepmemory§E§Какой процесс поддерживает полноценный сон?~Which process is supported by adequate sleep?§Обучение и запоминание~Learning and memory;Только рост волос~Only hair growth;Только изменение цвета глаз~Only eye-colour changes;Только рост ногтей~Only nail growth§Во сне мозг поддерживает функции, необходимые для обучения.~During sleep the brain supports functions needed for learning.§sleepwhy§Learning and memory
antibody§E§Как называют белки иммунной системы, распознающие определённые антигены?~What are immune-system proteins that recognise particular antigens called?§Антитела~Antibodies;Гормоны роста~Growth hormones;Пищевые волокна~Dietary fibres;Желчные кислоты~Bile acids§Антитела относятся к специфическому иммунному ответу.~Antibodies form part of a specific immune response.§immune§Antibodies
sleeprem§E§С чем связано сокращение REM в названии фазы сна?~What does REM refer to in a sleep-phase name?§Быстрые движения глаз~Rapid eye movements;Скорость дыхания при беге~Breathing rate while running;Температура кожи~Skin temperature;Частота сердцебиения стоя~Standing heart rate§Во время этой фазы движения глаз регистрируют при исследовании сна.~Eye movements during this phase are recorded in sleep studies.§sleepstages§Two phases of sleep
added§E§Какие сахара на пищевой этикетке называют добавленными?~Which sugars on a food label are called added sugars?§Внесённые при приготовлении или обработке~Those introduced during preparation or processing;Только естественный сахар цельного фрукта~Only sugar naturally in whole fruit;Все углеводы продукта~All carbohydrates in a product;Все минеральные вещества~All minerals§Общее количество сахаров включает как природные, так и добавленные.~Total sugars include both naturally occurring and added sugars.§nutrition§Total Sugars versus Added Sugars
portion§E§Что означает размер порции на пищевой этикетке?~What does serving size on a food label mean?§Количество продукта для приведённых значений~The food quantity used for the listed values;Обязательное количество для каждого человека~An amount mandatory for everyone;Вес упаковки с тарой~Package weight including the container;Максимальный срок хранения~Maximum shelf life§Значения энергии и нутриентов нужно соотносить с указанной порцией.~Energy and nutrient values must be related to the stated serving size.§nutrition§Serving Information
fibre§M§К какой группе веществ относят пищевые волокна на этикетке FDA?~Under which nutrient group does the FDA label list dietary fibre?§Углеводы~Carbohydrates;Белки~Proteins;Жиры~Fats;Минеральные вещества~Minerals§Волокна указывают отдельно внутри общего количества углеводов.~Fibre is listed separately within total carbohydrate.§nutrition§Example label
sodium§M§Какой химический элемент обозначает английское слово sodium на пищевой этикетке?~Which chemical element does sodium on a food label name?§Натрий~Sodium;Кальций~Calcium;Железо~Iron;Калий~Potassium§Натрий на этикетке — это элемент, а не название всех солей продукта.~Sodium on a label names an element, not every salt in the food.§nutrition§Nutrients and sodium
nonrem§M§Сколько стадий сна без быстрых движений глаз описывает NIH?~How many stages of non-REM sleep does NIH describe?§Три~Three;Две~Two;Пять~Five;Семь~Seven§Их различают по измеряемой активности мозга.~They are distinguished by measured brain activity.§sleepstages§Non-REM sleep
deep§M§Какую стадию сна без быстрых движений глаз называют глубоким сном?~Which non-REM stage is called deep sleep?§Третью~Stage three;Первую~Stage one;Только пробуждение~Waking only;Любую дневную активность~Any daytime activity§Она также называется медленноволновым сном.~It is also called slow-wave sleep.§sleepstages§Stage 3
cycles§M§Как обычно чередуются REM и non-REM в течение ночи?~How do REM and non-REM normally occur during a night?§Образуют повторяющиеся циклы~They form recurring cycles;REM бывает только перед засыпанием~REM occurs only before falling asleep;Non-REM бывает только после пробуждения~Non-REM occurs only after waking;Всегда идут строго по одной фазе за ночь~There is exactly one of each per night§За ночь человек обычно проходит несколько циклов сна.~A person normally passes through several sleep cycles in a night.§sleepstages§Opening paragraph
antigen§M§Как называют часть возбудителя, которую распознаёт иммунная система?~What is a part of a pathogen recognised by the immune system called?§Антиген~Antigen;Калория~Calorie;Фермент пищеварения~Digestive enzyme;Пищевое волокно~Dietary fibre§Разные антигены могут вызывать разные специфические иммунные ответы.~Different antigens can trigger different specific immune responses.§immune§Antigens and antibodies
vaccine§M§Что помогает сформировать вакцинация?~What does vaccination help establish?§Иммунную память~Immune memory;Группу крови~Blood group;Новый набор хромосом~A new chromosome set;Цвет радужки~Iris colour§Повторное распознавание знакомого антигена может происходить быстрее.~A familiar antigen can be recognised more quickly on a later encounter.§immune§How vaccines help
remsignals§M§Что, кроме движений глаз, регистрируют для различения стадий сна?~Besides eye movements, what is recorded to distinguish sleep stages?§Активность мозга~Brain activity;Длину волос~Hair length;Размер обуви~Shoe size;Цвет зубов~Tooth colour§Стадии сна определяют по физиологическим измерениям, а не по внешнему виду человека.~Sleep stages are defined by physiological measurements rather than appearance.§sleepstages§Sleep studies
percentdv§H§Что показывает %DV на пищевой этикетке FDA?~What does %DV on an FDA food label show?§Долю установленной суточной величины нутриента~The fraction of a nutrient's established Daily Value;Процент воды в упаковке~The percentage of water in the package;Вероятность аллергии~The probability of allergy;Процент усвоения пищи~The percentage of food absorbed§Это ориентир для сравнения продуктов, а не персональный медицинский расчёт.~It is a reference for comparing foods, not a personalised medical calculation.§nutrition§The Percent Daily Value
totalsugar§H§Входит ли добавленный сахар в значение Total Sugars на этикетке FDA?~Are added sugars included in Total Sugars on an FDA label?§Да, это часть общего количества~Yes, they are part of the total;Нет, значения всегда складывают~No, the two values must always be added;Только если продукт жидкий~Only for liquid foods;Только если упаковка стеклянная~Only in glass packaging§Добавленные сахара — подмножество общего количества сахаров.~Added sugars are a subset of total sugars.§nutrition§Total versus Added Sugars
memorycells§H§Что иммунная система может сохранить после знакомства с антигеном?~What can the immune system retain after encountering an antigen?§Клетки памяти~Memory cells;Запас кислорода в желудке~Oxygen stored in the stomach;Новые кости~New bones;Замену всех клеток тела~Replacement of every body cell§Эти клетки помогают ответить на повторную встречу с возбудителем.~These cells help respond to a later encounter with the pathogen.§immune§Immunological memory
pathogen§H§Как называют организм или агент, способный вызывать заболевание?~What is an organism or agent capable of causing disease called?§Патоген~Pathogen;Нутриент~Nutrient;Пигмент~Pigment;Электролит~Electrolyte§К возбудителям относятся, например, некоторые бактерии и вирусы.~Pathogens include, for example, some bacteria and viruses.§immune§Body's natural response
''')
source('evparts','https://afdc.energy.gov/vehicles/how-do-all-electric-cars-work')
source('evtypes','https://www.nhtsa.gov/vehicle-safety/electric-and-hybrid-vehicles')
source('hybrid','https://afdc.energy.gov/vehicles/how-do-hybrid-electric-cars-work')
source('carhistory','https://www.mercedes-benz.com/en/art-and-culture/museum/mercedes-benz-museum/')
source('airbags','https://www.nhtsa.gov/vehicle-safety/air-bags')
source('tires','https://www.nhtsa.gov/vehicle-safety/tires')
rows('cars','''
traction§E§Что приводит колёса полностью электрического автомобиля в движение?~What drives the wheels of an all-electric car?§Тяговый электромотор~Electric traction motor;Топливный бак~Fuel tank;Глушитель~Muffler;Радиоантенна~Radio aerial§Электромотор получает энергию от тяговой батареи.~The motor receives energy from the traction battery.§evparts§Electric traction motor
battery§E§Где электромобиль хранит основную энергию для движения?~Where does an electric car store its main driving energy?§В тяговой батарее~In the traction battery;В глушителе~In the muffler;В тормозном диске~In the brake disc;В бачке омывателя~In the washer tank§Тяговая батарея отличается по назначению от небольшой вспомогательной.~The traction battery has a different role from the smaller auxiliary battery.§evparts§Traction battery pack
hybrid§E§Какие два типа двигателей объединяет обычный гибридный автомобиль?~Which two engine types does a conventional hybrid car combine?§ДВС и электромотор~Combustion engine and electric motor;Паровую машину и турбину~Steam engine and turbine;Два реактивных двигателя~Two jet engines;Только два дизеля~Only two diesel engines§Гибрид сочетает топливо и электрическую тягу.~A hybrid combines fuel use with electric drive.§hybrid§Opening explanation
chargeport§E§Для чего электромобилю нужен зарядный разъём?~What is an electric car's charge port for?§Подключение к внешнему электропитанию~Connection to an external electricity supply;Долив моторного масла~Adding engine oil;Выпуск выхлопных газов~Releasing exhaust gases;Подача воздуха в шины~Inflating tyres§Через разъём энергия поступает в систему зарядки батареи.~Energy enters the battery charging system through the port.§evparts§Charge port
phev§E§Что отличает подключаемый гибрид PHEV от обычного HEV?~What distinguishes a PHEV from a conventional HEV?§Возможность зарядки от внешней сети~It can be charged from an external supply;Полное отсутствие батареи~It has no battery at all;Обязательная паровая тяга~It must use steam propulsion;Отсутствие колёс~It has no wheels§У PHEV есть также двигатель внутреннего сгорания.~A PHEV also has an internal combustion engine.§evtypes§PHEVs
exhaust§E§Чего нет у полностью электрического автомобиля при движении только на батарее?~What does an all-electric battery car not produce from a tailpipe while driving?§Выхлопных газов~Exhaust gases;Звука от шин~Tyre noise;Тепла от систем~Heat from its systems;Сопротивления воздуха~Air resistance§Отсутствие выхлопа не означает отсутствия воздействия производства энергии и автомобиля.~No tailpipe exhaust does not mean energy and vehicle production have no environmental impact.§evparts§Opening description
regen§E§Что делает рекуперативное торможение?~What does regenerative braking do?§Возвращает часть энергии в батарею~Returns some energy to the battery;Постоянно нагревает топливный бак~Continuously heats the fuel tank;Удваивает диаметр колёс~Doubles the wheel diameter;Производит бензин из воздуха~Makes petrol from air§При замедлении мотор может работать как генератор.~While slowing, the motor can act as a generator.§evtypes§Regenerative braking
airbag§E§Какую систему безопасности дополняет подушка безопасности?~Which safety system does an air bag supplement?§Ремень безопасности~Seat belt;Кондиционер~Air conditioning;Аудиосистему~Audio system;Стеклоомыватель~Windscreen washer§Подушки рассчитаны на совместную работу с ремнями.~Air bags are designed to work together with seat belts.§airbags§Air bags are supplemental protection
auxbattery§M§Что обычно питает вспомогательная батарея электромобиля?~What does an electric car's auxiliary battery normally supply?§Вспомогательные электрические устройства~Electrical accessories;Бензиновый топливный бак~A petrol fuel tank;Дорожное покрытие~The road surface;Внешнюю электростанцию~An external power station§Вспомогательная и тяговая батареи выполняют разные задачи.~The auxiliary and traction batteries perform different tasks.§evparts§Battery all-electric auxiliary
dcdc§M§Что делает преобразователь DC/DC в электромобиле?~What does the DC/DC converter in an electric car do?§Понижает постоянное напряжение для вспомогательных систем~Reduces DC voltage for auxiliary systems;Преобразует воду в бензин~Turns water into petrol;Измеряет скорость ветра~Measures wind speed;Изменяет давление шин~Changes tyre pressure§Он также помогает заряжать низковольтную вспомогательную батарею.~It also helps recharge the low-voltage auxiliary battery.§evparts§DC/DC converter
onboard§M§Какое устройство электромобиля преобразует переменный ток сети в постоянный для батареи?~Which onboard device converts grid AC into DC for an electric car's battery?§Бортовое зарядное устройство~Onboard charger;Рулевой механизм~Steering gear;Тормозной суппорт~Brake caliper;Дифференциал~Differential§Бортовое устройство обрабатывает энергию при зарядке от источника переменного тока.~The onboard unit processes electricity during AC charging.§evparts§Onboard charger
thermal§M§Какую задачу решает тепловая система электромобиля?~What does an electric car's thermal system do?§Поддерживает подходящую температуру компонентов~Maintains suitable component temperatures;Меняет форму дороги~Changes the road's shape;Создаёт радиосигнал~Creates a radio signal;Окрашивает кузов~Paints the body§Охлаждение требуется батарее, электромотору и силовой электронике.~The battery, motor and power electronics require cooling.§evparts§Thermal system
controller§M§Какую функцию выполняет контроллер силовой электроники электромобиля?~What is a function of an electric car's power electronics controller?§Управление потоком энергии и работой мотора~Managing energy flow and motor operation;Изготовление шин~Manufacturing tyres;Очистка стёкол вручную~Cleaning windows by hand;Хранение дорожных карт на бумаге~Storing paper road maps§Контроллер регулирует скорость и крутящий момент тягового мотора.~The controller regulates the traction motor's speed and torque.§evparts§Power electronics controller
transmission§M§Что передаёт механическую энергию электромотора колёсам?~What transfers an electric motor's mechanical power to the wheels?§Трансмиссия~Transmission;Радиаторная решётка~Grille;Воздушный фильтр салона~Cabin air filter;Зарядный разъём~Charge port§Устройство трансмиссии зависит от конкретной конструкции автомобиля.~Transmission design depends on the particular vehicle.§evparts§Transmission
hevcharge§M§Как обычный гибрид HEV пополняет тяговую батарею без подключения к розетке?~How does a conventional HEV recharge without plugging into a socket?§Работой двигателя и рекуперацией~Through the engine and regenerative braking;Только заменой всей батареи~Only by replacing the whole battery;Только солнечным светом на кузове~Only by sunlight on the body;Только давлением в шинах~Only through tyre pressure§Обычный HEV не имеет внешнюю зарядку как обязательный способ пополнения энергии.~A conventional HEV does not rely on external plug-in charging.§hybrid§Opening explanation
bev§M§Что означает BEV в автомобильной терминологии?~What does BEV stand for in vehicle terminology?§Батарейный электромобиль~Battery electric vehicle;Автомобиль только на биодизеле~Biodiesel-only vehicle;Любой бронированный автомобиль~Any armoured vehicle;Автобус с паровым двигателем~Steam-powered bus§BEV отличают от подключаемых и обычных гибридов.~BEVs are distinguished from plug-in and conventional hybrids.§evparts§Opening description
cooling§H§Какое утверждение о полностью электрическом автомобиле верно?~Which statement about an all-electric car is correct?§У него может быть жидкостная система охлаждения~It may have a liquid cooling system;У него обязательно есть выхлопной коллектор~It must have an exhaust manifold;Ему обязательно нужен бензиновый бак~It must have a petrol tank;Его мотор не выделяет тепла~Its motor produces no heat§Тепловая система охлаждает электрические компоненты, даже когда нет ДВС.~The thermal system cools electrical components even when there is no combustion engine.§evparts§Thermal system
motor_generator§H§Какое устройство может выполнять и тяговую, и генераторную функцию в электромобиле?~Which device can provide both drive and generation functions in an electric car?§Мотор-генератор~Motor-generator;Бачок омывателя~Washer tank;Рулевая рейка~Steering rack;Глушитель~Muffler§При рекуперации поток преобразования энергии меняет направление.~During regeneration, the direction of energy conversion reverses.§evparts§Electric traction motor
charger_monitor§H§Какие параметры батареи контролирует бортовое зарядное устройство?~Which battery parameters does an onboard charger monitor?§Напряжение, ток и температуру~Voltage, current and temperature;Только цвет корпуса~Only the casing colour;Только марку шин~Only the tyre brand;Только громкость радио~Only radio volume§Контроль параметров важен для процесса зарядки.~Monitoring these parameters matters to the charging process.§evparts§Onboard charger
fuelparts§H§Какой узел жидкотопливной системы не требуется типичному BEV?~Which liquid-fuel component is unnecessary in a typical BEV?§Топливный насос~Fuel pump;Ремень безопасности~Seat belt;Ступица колеса~Wheel hub;Стеклоочиститель~Windscreen wiper§У полностью электрической машины нет обычной бензиновой топливной системы.~An all-electric car has no conventional petrol fuel system.§evparts§Opening description
''')

# Explicitly selected primary source records; no approval is written here.
NOBEL_TECH = [
('marconi',13,1909,'physics','радиотелеграфия','wireless telegraphy','Радиосвязь позволяет передавать сообщения без проводной линии.','Radio communication transmits messages without a wired connection.'),
('dalen',17,1912,'physics','автоматические газовые регуляторы маяков','automatic gas regulators for lighthouses','Разработка связана с автоматизацией световых сигналов маяков и буёв.','The development automated light signals for lighthouses and buoys.'),
('wilson',34,1927,'physics','камера для наблюдения следов частиц','a chamber for observing particle tracks','В методе Вильсона следы заряженных частиц становятся видимыми благодаря конденсации пара.','In Wilson\'s method, condensation of vapour makes charged-particle tracks visible.'),
('lawrence',47,1939,'physics','циклотрон','cyclotron','Циклотрон — устройство для ускорения заряженных частиц.','A cyclotron is a device for accelerating charged particles.'),
('bardeen',66,1956,'physics','транзистор','transistor','Эта работа связана с полупроводниковой электроникой.','This work concerns semiconductor electronics.'),
('glaser',74,1960,'physics','пузырьковая камера','bubble chamber','Пузырьковая камера позволяет исследовать следы частиц в жидкости.','A bubble chamber allows particle tracks in a liquid to be studied.'),
('townes',81,1964,'physics','мазерно-лазерные генераторы и усилители','maser-laser oscillators and amplifiers','Премия была связана с фундаментальными работами по квантовой электронике.','The prize recognised fundamental work in quantum electronics.'),
('gabor',93,1971,'physics','голография','holography','Голографический метод связан с записью и восстановлением волнового фронта.','The holographic method concerns recording and reconstructing a wavefront.'),
('hounsfield',418,1979,'medicine','компьютерная томография','computer-assisted tomography','Метод относится к получению изображений внутренних структур тела.','The method produces images of internal body structures.'),
('ruska',127,1986,'physics','электронный микроскоп','electron microscope','В электронной микроскопии изображение получают с помощью электронов.','Electron microscopy uses electrons to form images.'),
('binnig',128,1986,'physics','сканирующий туннельный микроскоп','scanning tunnelling microscope','Эта работа отлична от разработки первого электронного микроскопа, отмеченной в том же году.','This work differs from the first electron microscope, also recognised that year.'),
('paul',137,1989,'physics','метод ионных ловушек','ion-trap technique','Ловушки позволяют удерживать заряженные частицы для исследования.','Traps allow charged particles to be confined for study.'),
('kilby',728,2000,'physics','интегральная схема','integrated circuit','Интегральная схема объединяет электронные компоненты в одном устройстве.','An integrated circuit combines electronic components in one device.'),
('lauterbur',764,2003,'medicine','магнитно-резонансная томография','magnetic resonance imaging','Работа Лотербура была отмечена вместе с исследованиями Питера Мэнсфилда.','Lauterbur\'s work was recognised alongside Peter Mansfield\'s research.'),
('kao',838,2009,'physics','оптоволоконная связь','fibre-optic communication','Работа связана с передачей света по волокнам для связи.','The work concerns transmitting light through fibres for communication.'),
('boyle',839,2009,'physics','ПЗС-датчик изображения','CCD image sensor','ПЗС-датчик — полупроводниковое устройство для регистрации изображения.','A CCD sensor is a semiconductor device for recording images.'),
('akam',906,2014,'physics','эффективный синий светодиод','efficient blue light-emitting diode','Синие светодиоды сделали возможными яркие энергоэффективные белые источники света.','Blue LEDs enabled bright, energy-efficient white light sources.'),
('ashkin',960,2018,'physics','оптический пинцет','optical tweezers','Эту технологию отмечали за её применение к биологическим системам.','This technology was recognised for its applications to biological systems.'),
('strickland',962,2018,'physics','метод получения сверхкоротких интенсивных световых импульсов','a method for intense ultrashort optical pulses','Стрикленд разделила эту часть премии с Жераром Муру.','Strickland shared this part of the prize with Gérard Mourou.'),
('yoshino',978,2019,'chemistry','литийионные аккумуляторы','lithium-ion batteries','Ёсино разделил премию с Джоном Гуденафом и Стэнли Уиттингемом.','Yoshino shared the prize with John Goodenough and Stanley Whittingham.'),
]
NOBEL_NAMES = [
('marconi','Гульельмо Маркони'),('dalen','Густав Дален'),('wilson','Чарльз Вильсон'),('lawrence','Эрнест Лоуренс'),('bardeen','Джон Бардин'),('glaser','Дональд Глейзер'),('townes','Чарльз Таунс'),('gabor','Деннис Габор'),('hounsfield','Годфри Хаунсфилд'),('ruska','Эрнст Руска'),('binnig','Герд Бинниг'),('paul','Вольфганг Пауль'),('kilby','Джек Килби'),('lauterbur','Пол Лотербур'),('kao','Чарльз Као'),('boyle','Уиллард Бойл'),('akam','Исаму Акасаки'),('ashkin','Артур Эшкин'),('strickland','Донна Стрикленд'),('yoshino','Акира Ёсино')]
NOBEL_CULTURE = [
(937,'Боб Дилан','США','USA','Дулут','Duluth'),
(583,'Рабиндранат Тагор','Индия','India','Калькутта','Calcutta'),
(659,'Габриэль Гарсиа Маркес','Колумбия','Colombia','Аракатака','Aracataca'),
(625,'Эрнест Хемингуэй','США','USA','Оук-Парк','Oak Park'),
(624,'Уинстон Черчилль','Великобритания','United Kingdom','Вудсток','Woodstock'),
(628,'Альбер Камю','Алжир','Algeria','Мондови','Mondovi'),
(637,'Жан-Поль Сартр','Франция','France','Париж','Paris'),
(634,'Джон Стейнбек','США','USA','Салинас','Salinas'),
(620,'Уильям Фолкнер','США','USA','Нью-Олбани','New Albany'),
(629,'Борис Пастернак','Россия','Russia','Москва','Moscow'),
(643,'Сэмюэл Беккет','Ирландия','Ireland','Дублин','Dublin'),
(619,'Томас Стернз Элиот','США','USA','Сент-Луис','St. Louis'),
(644,'Александр Солженицын','Россия','Russia','Кисловодск','Kislovodsk'),
(663,'Воле Шойинка','Нигерия','Nigeria','Абеокута','Abeokuta'),
(667,'Октавио Пас','Мексика','Mexico','Мехико','Mexico City'),
(670,'Тони Моррисон','США','USA','Лорейн','Lorain'),
(577,'Редьярд Киплинг','Индия','India','Бомбей','Bombay'),
(615,'Габриэла Мистраль','Чили','Chile','Викунья','Vicuña'),
(669,'Дерек Уолкотт','Сент-Люсия','Saint Lucia','Кастри','Castries'),
(673,'Вислава Шимборская','Польша','Poland','Бнин','Bnin')]

def nobel_drafts(cache):
    import html
    people={int(p['id']):p for p in json.loads((cache/'nobel-laureates.json').read_text())['laureates']}
    names=dict(NOBEL_NAMES)
    for i,(slug,pid,year,category,ru,en,fr,fe) in enumerate(NOBEL_TECH):
        person=people[pid]
        award=next(p for p in person['prizes'] if p['year']==str(year) and p['category']==category)
        name=html.unescape(person.get('firstname','')+' '+person.get('surname','')).strip()
        key='nobel_'+str(pid); source(key,f'https://api.nobelprize.org/v1/laureate.json?id={pid}')
        # Same broad class: actual technologies, not joke distractors. Avoid
        # closely overlapping microscope/optical device alternatives.
        distractors=[r for r in NOBEL_TECH if r[0]!=slug and r[4]!=ru]
        choices=[(ru[0].upper()+ru[1:],en[0].upper()+en[1:])]
        for j in (4,9,14):
            r=distractors[(i+j)%len(distractors)]
            choices.append((r[4][0].upper()+r[4][1:],r[5][0].upper()+r[5][1:]))
        level='E' if i<8 else 'M' if i<16 else 'H'
        rows('inventions','§'.join([slug,level,f'Лауреат Нобелевской премии {year} года — {names[slug]}. С какой технологией связана награда?~Which technology is associated with {name}’s {year} Nobel Prize?', ';'.join(a+'~'+b for a,b in choices),fr+'~'+fe,key,f'laureate id={pid}; prizes year={year}, category={category}; motivation']))
        EVIDENCE[OUT[-1]['id']]['sourceRecord']={'id':pid,'name':name,'award':award}
    countries=[('США','USA'),('Индия','India'),('Франция','France'),('Колумбия','Colombia'),('Мексика','Mexico'),('Нигерия','Nigeria'),('Великобритания','United Kingdom'),('Япония','Japan'),('Польша','Poland'),('Алжир','Algeria'),('Чили','Chile'),('Ирландия','Ireland'),('Россия','Russia'),('Сент-Люсия','Saint Lucia')]
    for i,(pid,ru,countryru,countryen,cityru,cityen) in enumerate(NOBEL_CULTURE):
        person=people[pid]; name=html.unescape(person.get('firstname','')+' '+person.get('surname','')).strip()
        code={'USA':'US','India':'IN','Colombia':'CO','United Kingdom':'GB','Algeria':'DZ','France':'FR','Russia':'RU','Ireland':'IE','Nigeria':'NG','Mexico':'MX','Chile':'CL','Saint Lucia':'LC','Poland':'PL'}[countryen]
        assert person['bornCountryCode']==code, (ru,person)
        assert cityen.casefold() in person['bornCity'].casefold(), (ru,person)
        key='nobel_'+str(pid); source(key,f'https://api.nobelprize.org/v1/laureate.json?id={pid}')
        # Explicit labels reviewed against the source projection, not inferred
        # from nationality; question asks location in present-day borders.
        distractors=[r for r in countries if r[1]!=countryen]
        opts=[(countryru,countryen)]+[distractors[(i+j)%len(distractors)] for j in (0,4,8)]
        level='E' if i<8 else 'M' if i<16 else 'H'
        rows('celebrities','§'.join([f'birth_{pid}',level,f'На территории какой современной страны родился Нобелевский лауреат {ru}?~In which present-day country was Nobel laureate {name} born?', ';'.join(a+'~'+b for a,b in opts),f'Место рождения в записи Нобелевского фонда — {cityru}.~The Nobel Foundation record lists the birthplace as {cityen}.',key,f'laureate id={pid}; bornCity and bornCountryCode']))
        EVIDENCE[OUT[-1]['id']]['sourceRecord']={k:person.get(k) for k in ('id','firstname','surname','bornCity','bornCountry','bornCountryCode')}

NOBEL_FIGURES = [
(26,'Альберт Эйнштейн','1921','physics','закон фотоэлектрического эффекта','the law of the photoelectric effect'),
(1,'Вильгельм Рентген','1901','physics','открытие рентгеновских лучей','the discovery of X-rays'),
(6,'Мария Кюри','1911','chemistry','открытие радия и полония','the discovery of radium and polonium'),
(555,'Нельсон Мандела','1993','peace','мирное прекращение апартеида','the peaceful ending of apartheid'),
(524,'Мартин Лютер Кинг','1964','peace','ненасильственная борьба за гражданские права','nonviolent work for civil rights'),
(914,'Малала Юсуфзай','2014','peace','защита права детей на образование','defending children\'s right to education'),
(339,'Александр Флеминг','1945','medicine','открытие пенициллина','the discovery of penicillin'),
(296,'Иван Павлов','1904','medicine','физиология пищеварения','the physiology of digestion'),
(23,'Макс Планк','1918','physics','открытие квантов энергии','the discovery of energy quanta'),
(27,'Нильс Бор','1922','physics','строение атомов и их излучение','atomic structure and radiation'),
(4,'Анри Беккерель','1903','physics','открытие спонтанной радиоактивности','the discovery of spontaneous radioactivity'),
(167,'Эрнест Резерфорд','1908','chemistry','распад элементов и химия радиоактивных веществ','element disintegration and the chemistry of radioactive substances'),
(41,'Джеймс Чедвик','1935','physics','открытие нейтрона','the discovery of the neutron'),
(297,'Роберт Кох','1905','medicine','исследования туберкулёза','research on tuberculosis'),
(552,'Михаил Горбачёв','1990','peace','изменения отношений между Востоком и Западом','changes in East-West relations'),
(468,'Берта фон Зутнер','1905','peace','противодействие войне','opposition to war'),
(230,'Дороти Ходжкин','1964','chemistry','рентгеноструктурное исследование биохимических веществ','using X-rays to determine structures of biochemical substances'),
(719,'Амартия Сен','1998','economics','экономика благосостояния','welfare economics'),
(870,'Лейма Гбови','2011','peace','участие женщин в миротворчестве','women\'s participation in peace-building'),
(546,'Десмонд Туту','1984','peace','ненасильственная борьба против апартеида','nonviolent opposition to apartheid'),
]
NOBEL_EVENTS=[
(525,'ЮНИСЕФ','1965','содействие солидарности стран и уменьшению неравенства','promoting international solidarity and reducing inequalities'),
(994,'Всемирная продовольственная программа','2020','борьба с голодом','combating hunger'),
(568,'Врачи без границ','1999','гуманитарная помощь на разных континентах','humanitarian work on several continents'),
(537,'Международная амнистия','1977','уважение прав человека во всём мире','worldwide respect for human rights'),
(482,'Международный комитет Красного Креста','1917','помощь раненым и военнопленным','care for wounded soldiers and prisoners of war'),
(515,'Управление Верховного комиссара ООН по делам беженцев','1954','защита и помощь беженцам','protection and assistance for refugees'),
(748,'Организация Объединённых Наций','2001','содействие более мирному и организованному миру','promoting a more organised and peaceful world'),
(881,'Европейский союз','2012','мир, примирение, демократия и права человека в Европе','peace, reconciliation, democracy and human rights in Europe'),
(527,'Международная организация труда','1969','международные нормы условий труда','international standards for working conditions'),
(893,'Организация по запрещению химического оружия','2013','усилия по уничтожению химического оружия','efforts to eliminate chemical weapons'),
(564,'Международная кампания по запрещению наземных мин','1997','запрет и обезвреживание противопехотных мин','banning and clearing anti-personnel mines'),
(797,'Международное агентство по атомной энергии','2005','мирное и безопасное использование ядерной энергии','peaceful and safe use of nuclear energy'),
(818,'Межправительственная группа экспертов по изменению климата','2007','распространение знаний об изменении климата из-за деятельности человека','spreading knowledge of human-caused climate change'),
(948,'Международная кампания за ликвидацию ядерного оружия','2017','договорный запрет ядерного оружия','a treaty-based prohibition of nuclear weapons'),
(547,'Врачи мира за предотвращение ядерной войны','1985','информирование о катастрофических последствиях ядерной войны','informing people about catastrophic consequences of nuclear war'),
(561,'Пагуошское движение учёных','1995','сокращение роли ядерного оружия','reducing the role of nuclear weapons'),
(467,'Институт международного права','1904','развитие мирных отношений через международное право','developing peaceful relations through international law'),
(477,'Международное бюро мира','1910','сотрудничество национальных обществ мира','cooperation among national peace societies'),
(503,'Нансеновская организация по делам беженцев','1938','продолжение помощи беженцам Европы','continuing aid to refugees in Europe'),
(550,'Миротворческие силы ООН','1988','предотвращение вооружённых столкновений и создание условий для переговоров','preventing armed clashes and creating conditions for negotiations'),
]

def nobel_history(cache):
    import html
    people={int(p['id']):p for p in json.loads((cache/'nobel-laureates.json').read_text())['laureates']}
    for i,(pid,ru,year,category,focusru,focusen) in enumerate(NOBEL_FIGURES):
        person=people[pid]; award=next(p for p in person['prizes'] if p['year']==year and p['category']==category)
        name=html.unescape(person.get('firstname','')+' '+person.get('surname','')).strip()
        choices=[(ru,name)]
        others=[p for p in NOBEL_FIGURES if p[0]!=pid and not any(a['year']==year and a['category']==category for a in people[p[0]]['prizes'])]
        for j in (0,5,10):
            r=others[(i+j)%len(others)]; other=people[r[0]]
            choices.append((r[1],html.unescape(other.get('firstname','')+' '+other.get('surname','')).strip()))
        key='nobel_'+str(pid); source(key,f'https://api.nobelprize.org/v1/laureate.json?id={pid}')
        rows('historical_figures','§'.join([f'award_{pid}','E' if i<8 else 'M' if i<16 else 'H',f'Кого из перечисленных отметила Нобелевская премия {year} года за работу по теме «{focusru}»?~Which of these laureates was recognised in {year} for {focusen}?',';'.join(a+'~'+b for a,b in choices),f'В официальной записи премии {year} года указана именно эта работа.~The official {year} prize record identifies this contribution.',key,f'laureate id={pid}; prizes year={year}, category={category}; motivation']))
        EVIDENCE[OUT[-1]['id']]['sourceRecord']={'id':pid,'name':name,'award':award}
    # Every selected event concerns a different organisation or recipient.
    for i,(pid,ru,year,focusru,focusen) in enumerate(NOBEL_EVENTS):
        person=people[pid]; award=next(p for p in person['prizes'] if p['year']==year and p['category']=='peace')
        name=html.unescape(person.get('firstname','')+' '+person.get('surname','')).strip()
        choices=[(focusru[0].upper()+focusru[1:],focusen[0].upper()+focusen[1:])]
        alternative=[('Охрана объектов архитектуры','Protecting architectural monuments'),('Исследование планет Солнечной системы','Exploring Solar System planets'),('Развитие спортивных соревнований','Developing sports competitions'),('Создание новых сортов растений','Developing new crop varieties'),('Охрана морских млекопитающих','Protecting marine mammals'),('Сохранение исчезающих языков','Preserving endangered languages')]
        choices += [alternative[(i+j)%len(alternative)] for j in (0,2,4)]
        key='nobel_'+str(pid); source(key,f'https://api.nobelprize.org/v1/laureate.json?id={pid}')
        rows('modern_history','§'.join([f'peace_{pid}_{year}','E' if i<8 else 'M' if i<16 else 'H',f'За какую работу организация «{ru}» получила Нобелевскую премию мира {year} года?~For which work was {name} awarded the {year} Nobel Peace Prize?',';'.join(a+'~'+b for a,b in choices),f'Премия {year} года отметила эту область международной работы организации.~The {year} award recognised this area of the organisation\'s international work.',key,f'laureate id={pid}; peace prize {year}; motivation']))
        EVIDENCE[OUT[-1]['id']]['sourceRecord']={'id':pid,'name':name,'award':award}

source('musicgloss','https://www.carnegiehall.org/uploadedFiles/Resources_and_Components/PDF/WMI/OR_Resources.pdf')
source('musicexpress','https://www.carnegiehall.org/Education/Programs/Music-Educators-Toolbox/1-Exploring-Expressive-Qualities')
source('violin','https://philharmonia.co.uk/resources/instruments/violin/')
source('instruments','https://philharmonia.co.uk/resources/instruments/')
source('oboe','https://philharmonia.co.uk/resources/instruments/oboe/')
rows('music','''
tempo§E§Какой музыкальный термин обозначает скорость исполнения?~Which musical term describes the speed of a performance?§Темп~Tempo;Тембр~Timbre;Регистр~Register;Гармония~Harmony§Темп может меняться независимо от громкости музыки.~Tempo can change independently of musical volume.§musicgloss§Tempo and Dynamics
forte§E§Что означает указание forte в музыке?~What does forte indicate in music?§Громко~Loud;Тихо~Soft;Связно~Smoothly connected;Отрывисто~Detached§Это указание динамики, а не скорости исполнения.~It is a dynamic marking rather than a speed instruction.§musicexpress§Dynamics
piano§E§Что означает указание piano, если речь идёт о динамике?~What does piano mean as a dynamic marking?§Тихо~Soft;Быстро~Fast;Отрывисто~Detached;Высоко~High§Музыкальное обозначение динамики следует отличать от названия инструмента.~The dynamic marking should be distinguished from the name of the instrument.§musicexpress§Dynamics
conductor§E§Кто обычно руководит исполнением симфонического оркестра?~Who usually directs a symphony orchestra's performance?§Дирижёр~Conductor;Либреттист~Librettist;Настройщик~Tuner;Переплётчик нот~Score binder§Оркестр объединяет несколько семейств инструментов.~An orchestra brings together several instrument families.§musicgloss§Orchestra
strings§E§К какому семейству оркестровых инструментов относится скрипка?~To which orchestral instrument family does the violin belong?§Струнные~Strings;Медные духовые~Brass;Деревянные духовые~Woodwind;Ударные~Percussion§В стандартной струнной группе скрипка занимает самый высокий регистр.~The violin occupies the highest register of the standard string section.§violin§Opening description
oboe§E§К какому семейству оркестра относится гобой?~To which orchestral family does the oboe belong?§Деревянные духовые~Woodwind;Медные духовые~Brass;Струнные~Strings;Ударные~Percussion§Его регистр немного ниже регистра флейты.~Its register is slightly lower than the flute's.§oboe§Instrument description
rehearsal§E§Как называют совместное занятие музыкантов перед выступлением?~What is a musicians' joint practice session before a performance called?§Репетиция~Rehearsal;Рефрен~Refrain;Каденция~Cadenza;Увертюра~Overture§На репетиции ансамбль готовит согласованное исполнение произведения.~During rehearsal an ensemble prepares a coordinated performance.§musicgloss§Rehearsal
score§E§Как называется запись музыкального произведения, показывающая партии исполнителей?~What is the written musical document showing performers' parts called?§Партитура~Score;Либретто~Libretto;Афиша~Poster;Рецензия~Review§Такая запись указывает, что и когда следует исполнять.~The document indicates what should be played and when.§musicgloss§Score
staccato§M§Какое указание просит исполнять ноты отрывисто?~Which marking calls for detached notes?§Staccato~Staccato;Legato~Legato;Piano~Piano;Largo~Largo§Это характеристика артикуляции — способа соединять или разделять звуки.~This concerns articulation, how sounds are connected or separated.§musicexpress§Articulation
legato§M§Какое указание просит связно соединять звуки?~Which marking calls for smoothly connected notes?§Legato~Legato;Staccato~Staccato;Forte~Forte;Presto~Presto§Связность исполнения не определяет сама по себе его громкость.~Connected playing does not by itself determine volume.§musicexpress§Articulation
presto§M§Какое из этих обозначений относится к быстрому темпу?~Which of these markings denotes a fast tempo?§Presto~Presto;Largo~Largo;Piano~Piano;Legato~Legato§Темп и артикуляция описывают разные стороны исполнения.~Tempo and articulation describe different aspects of performance.§musicexpress§Presto and largo
largo§M§Какое из этих обозначений указывает на медленный темп?~Which of these markings indicates a slow tempo?§Largo~Largo;Presto~Presto;Forte~Forte;Staccato~Staccato§Громкость при медленном исполнении может быть разной.~A slow performance can have different dynamic levels.§musicexpress§Presto and largo
unison§M§Как называют исполнение одной музыкальной линии несколькими музыкантами вместе?~What is it called when several musicians perform the same musical line together?§Унисон~Unison;Канон~Canon;Контрапункт~Counterpoint;Каденция~Cadenza§В унисоне участники исполняют одну линию одновременно.~In unison, performers present the same line at the same time.§musicgloss§Unison
ostinato§M§Как называется короткий многократно повторяющийся музыкальный рисунок?~What is a short musical pattern repeated many times called?§Остинато~Ostinato;Каденция~Cadenza;Увертюра~Overture;Фермата~Fermata§Повторяющийся рисунок может служить основой для других партий.~A repeating pattern can form a foundation for other parts.§musicgloss§Ostinato
refrain§M§Как называют повторяющийся раздел песни, часто именуемый припевом?~What is a repeating song section, often called the chorus, known as?§Рефрен~Refrain;Вступление~Introduction;Кода~Coda;Каденция~Cadenza§Между повторениями припева могут располагаться куплеты.~Verses may appear between repetitions of the chorus.§musicgloss§Refrain and Verse
pitch§M§Какой параметр позволяет различать высокий и низкий музыкальный звук?~Which quality distinguishes high and low musical sounds?§Высота~Pitch;Громкость~Loudness;Длительность~Duration;Пространственное положение~Spatial position§Высота звука и его громкость — разные свойства.~Pitch and loudness are different properties.§musicgloss§Pitch
pulse§H§Как называется ровная повторяющаяся основа музыкального движения?~What is the steady repeating foundation of musical movement called?§Пульс~Pulse;Тембр~Timbre;Кода~Coda;Транспозиция~Transposition§Ритмический рисунок может отличаться от ровного основного пульса.~A rhythmic pattern can differ from the steady underlying pulse.§musicgloss§Pulse and Rhythm
timbre§H§Какое свойство помогает различить голоса инструментов при одинаковой высоте звука?~Which quality helps distinguish instruments playing the same pitch?§Тембр~Timbre;Размер такта~Metre;Темп~Tempo;Длина паузы~Rest length§Тембр часто описывают как окраску звука.~Timbre is often described as tone colour.§musicexpress§Expressive qualities and sound quality
synchronization§H§Как называют согласованное совпадение начала или окончания музыкальных партий?~What is coordinated timing of the start or ending of musical parts called?§Синхронизация~Synchronization;Транспозиция~Transposition;Импровизация~Improvisation;Модуляция~Modulation§Согласованность времени важна даже при исполнении разных партий.~Coordinated timing matters even when the parts differ.§musicgloss§Synchronization
verse§H§Как называется раздел песни, обычно расположенный между припевами?~What is a song section usually found between choruses called?§Куплет~Verse;Увертюра~Overture;Кода~Coda;Каденция~Cadenza§Куплеты чередуются с возвращающимся припевом.~Verses alternate with the returning chorus.§musicgloss§Verse
''')
source('mariochars','https://mario.nintendo.com/ca/characters/')
source('potterhouses','https://www.harrypotter.com/features/hogwarts-house-meanings')
source('potterhogwarts','https://www.harrypotter.com/fact-file/locations/hogwarts')
source('r2d2','https://www.starwars.com/databank/r2-d2')
source('c3po','https://www.starwars.com/databank/c-3po')
source('chewie','https://www.starwars.com/databank/chewbacca')
source('falcon','https://www.starwars.com/databank/millennium-falcon')
source('yoda','https://www.starwars.com/databank/yoda')
source('vader','https://www.starwars.com/databank/darth-vader')
source('tatooine','https://www.starwars.com/databank/tatooine')
source('lightsaber','https://www.starwars.com/databank/lightsaber')
source('hoth','https://www.starwars.com/databank/hoth')
source('deathstar','https://www.starwars.com/databank/death-star')
rows('pop_culture','''
luigi§E§Как зовут брата Марио в играх Nintendo?~What is Mario's brother's name in Nintendo games?§Луиджи~Luigi;Боузер~Bowser;Варио~Wario;Тоад~Toad§Луиджи легко узнать по зелёной кепке и рубашке.~Luigi is recognisable by his green cap and shirt.§mariochars§Luigi
peach§E§Какая принцесса связана с Грибным королевством в мире Марио?~Which princess is associated with the Mushroom Kingdom in Mario's world?§Пич~Peach;Дейзи~Daisy;Розалина~Rosalina;Зельда~Zelda§Её традиционный образ включает розовое платье.~Her familiar appearance includes a pink dress.§mariochars§Princess Peach
bowser§E§Кто считается королём куп в играх о Марио?~Who is the King of the Koopas in Mario games?§Боузер~Bowser;Луиджи~Luigi;Тоад~Toad;Дидди Конг~Diddy Kong§Боузер — постоянный противник Марио.~Bowser is Mario's recurring adversary.§mariochars§Bowser
yoshi§E§Какой спутник Марио известен длинным языком и островом Йоши?~Which Mario companion is known for a long tongue and Yoshi's Island?§Йоши~Yoshi;Варио~Wario;Боузер~Bowser;Валуиджи~Waluigi§Йоши может превращать проглоченных врагов в яйца для броска.~Yoshi can turn swallowed enemies into throwable eggs.§mariochars§Yoshi
daisy§E§Принцессой какой страны Nintendo называет Дейзи?~Of which land does Nintendo describe Daisy as princess?§Сарасаленд~Sarasaland;Хайрул~Hyrule;Грибное королевство~Mushroom Kingdom;Канто~Kanto§Её узнаваемый образ включает жёлтое платье и цветочные украшения.~Her signature appearance includes a yellow dress and flower accessories.§mariochars§Daisy
r2§E§Какой дроид из «Звёздных войн» относится к астромеханикам?~Which Star Wars droid is an astromech?§R2-D2~R2-D2;C-3PO~C-3PO;IG-88~IG-88;K-2SO~K-2SO§R2-D2 помогает обслуживать корабли и сопровождать пилотов.~R2-D2 helps service spacecraft and accompanies pilots.§r2d2§Databank description
c3§E§Какова специализация C-3PO в «Звёздных войнах»?~What is C-3PO's speciality in Star Wars?§Этикет, протокол и перевод~Etiquette, protocol and translation;Только пилотирование истребителей~Fighter piloting only;Только ремонт гипердвигателей~Hyperdrive repair only;Только подводная разведка~Underwater reconnaissance only§Он — протокольный дроид, часто действующий вместе с R2-D2.~He is a protocol droid often working alongside R2-D2.§c3po§Databank description
chewbacca§E§К какому народу относится Чубакка?~To which people does Chewbacca belong?§Вуки~Wookiees;Эвоки~Ewoks;Джавы~Jawas;Гунганы~Gungans§Чубакка — напарник Хана Соло и второй пилот его корабля.~Chewbacca is Han Solo's partner and the ship's co-pilot.§chewie§Databank description
falcon§M§Как называется знаменитый корабль Хана Соло?~What is Han Solo's famous ship called?§Тысячелетний сокол~Millennium Falcon;Звезда Смерти~Death Star;Раб I~Slave I;Призрак~Ghost§Это модифицированный грузовой корабль, а не истребитель.~It is a modified freighter rather than a starfighter.§falcon§Databank description
yoda§M§К какому ордену принадлежит мастер Йода?~To which order does Master Yoda belong?§Джедаи~Jedi;Ситхи~Sith;Мандалорцы~Mandalorians;Гильдия охотников~Bounty Hunters' Guild§Йода обучал джедаев на протяжении многих поколений.~Yoda trained Jedi over many generations.§yoda§Databank description
vader§M§Кем был Дарт Вейдер до перехода на тёмную сторону?~Who was Darth Vader before turning to the dark side?§Энакин Скайуокер~Anakin Skywalker;Оби-Ван Кеноби~Obi-Wan Kenobi;Квай-Гон Джинн~Qui-Gon Jinn;Мейс Винду~Mace Windu§Его прежняя жизнь связана с орденом джедаев.~His earlier life was connected with the Jedi Order.§vader§Databank description
tatooine§M§Какой тип ландшафта характерен для Татуина?~Which landscape is characteristic of Tatooine?§Пустынный~Desert;Ледниковый~Glacial;Тропический лес~Tropical forest;Сплошной океан~Global ocean§Татуин в мире «Звёздных войн» — засушливая планета.~Tatooine is an arid planet in Star Wars.§tatooine§Databank description
lightsaber§M§Какое оружие особенно связано с джедаями и ситхами?~Which weapon is especially associated with Jedi and Sith?§Световой меч~Lightsaber;Лазерная пушка корабля~A ship's laser cannon;Ионная торпеда~Ion torpedo;Электрическая сеть~Electrified net§Клинок светового меча создаётся энергетическим устройством в рукояти.~A lightsaber's blade is produced by an energy device in its hilt.§lightsaber§Databank description
hoth§M§Какой климатический образ характерен для планеты Хот?~Which environment characterises the planet Hoth?§Ледяной~Icy;Пустынный~Desert;Вулканический~Volcanic;Тропический~Tropical§На Хоте повстанцы устроили базу «Эхо».~The Rebels established Echo Base on Hoth.§hoth§Databank description
deathstar§M§Что представляет собой Звезда Смерти в «Звёздных войнах»?~What is the Death Star in Star Wars?§Боевая космическая станция~A battle space station;Естественный спутник~A natural moon;Комета~A comet;Грузовой шаттл~A cargo shuttle§Станция вооружена сверхмощным орудием, способным уничтожать планеты.~The station carries a powerful weapon capable of destroying planets.§deathstar§Databank description
hogwarts§M§Чему учат в Хогвартсе в книгах о Гарри Поттере?~What is taught at Hogwarts in the Harry Potter books?§Колдовству и волшебству~Witchcraft and wizardry;Морской навигации~Sea navigation;Только военному делу~Military subjects only;Только астрономии~Astronomy only§Хогвартс — школа, разделённая на четыре факультета.~Hogwarts is a school divided into four houses.§potterhogwarts§Fact file
gryffindor§H§Какое животное изображено на эмблеме Гриффиндора?~Which animal appears on Gryffindor's emblem?§Лев~Lion;Орёл~Eagle;Барсук~Badger;Змея~Snake§Каждый из четырёх факультетов Хогвартса имеет свой символ.~Each of the four Hogwarts houses has its own symbol.§potterhouses§Gryffindor
slytherin§H§Какое животное изображено на эмблеме Слизерина?~Which animal appears on Slytherin's emblem?§Змея~Snake;Лев~Lion;Орёл~Eagle;Барсук~Badger§Символ Слизерина связан с основателем факультета Салазаром Слизерином.~Slytherin's symbol is associated with its founder, Salazar Slytherin.§potterhouses§Slytherin
ravenclaw§H§Какой символ у Когтеврана в книжной традиции Гарри Поттера?~What is Ravenclaw's symbol in the Harry Potter books?§Орёл~Eagle;Ворон~Raven;Сова~Owl;Сокол~Falcon§Несмотря на английское название факультета, его книжный символ — орёл.~Despite the house's English name, its book symbol is an eagle.§potterhouses§Ravenclaw
hufflepuff§H§Какое животное служит символом Пуффендуя?~Which animal is Hufflepuff's symbol?§Барсук~Badger;Лев~Lion;Орёл~Eagle;Змея~Snake§Пуффендуй — один из четырёх факультетов Хогвартса.~Hufflepuff is one of the four Hogwarts houses.§potterhouses§Hufflepuff
''')

source('carolingian','https://www.metmuseum.org/essays/carolingian-art')
source('hastings','https://www.english-heritage.org.uk/visit/places/1066-battle-of-hastings-abbey-and-battlefield/history-and-stories/what-happened-battle-hastings')
source('gothic','https://www.metmuseum.org/essays/gothic-art')
source('yuan','https://www.metmuseum.org/essays/yuan-dynasty-1271-1368')
rows('middle_ages','''
charlemagne§E§Каким народом правил Карл Великий до императорской коронации?~Which people did Charlemagne rule before his imperial coronation?§Франками~Franks;Ацтеками~Aztecs;Инками~Incas;Японцами~Japanese§Во франкском королевстве его правление началось в 768 году.~His reign in the Frankish kingdom began in 768.§carolingian§Kingship and coronation
coronation§E§В каком году Карл Великий был коронован императором?~In which year was Charlemagne crowned emperor?§800~800;476~476;1066~1066;1453~1453§Коронация состоялась в день Рождества.~The coronation took place on Christmas Day.§carolingian§Opening paragraph
leo§E§Какой папа короновал Карла Великого императором?~Which pope crowned Charlemagne emperor?§Лев III~Leo III;Урбан II~Urban II;Григорий VII~Gregory VII;Иннокентий III~Innocent III§Коронация подчёркивала союз императорской власти и церкви.~The coronation emphasised the alliance between imperial authority and the Church.§carolingian§Opening paragraph
latin§E§Какой язык Карл Великий поддерживал как язык учёности?~Which language did Charlemagne promote as a language of scholarship?§Латынь~Latin;Китайский~Chinese;Санскрит~Sanskrit;Персидский~Persian§Культурное возрождение сопровождалось повышением образовательных стандартов.~The cultural revival also raised educational standards.§carolingian§Cultural revival
revival§E§Что называют Каролингским возрождением?~What is the Carolingian Renaissance?§Культурный подъём эпохи Карла Великого~The cultural revival of Charlemagne's age;Изобретение парового двигателя~The invention of the steam engine;Открытие Америки Колумбом~Columbus' discovery of the Americas;Возникновение кино~The emergence of cinema§Название происходит от латинской формы имени Карл — Carolus.~The name derives from Carolus, the Latin form of Charles.§carolingian§Carolingian Renaissance
hastings_year§E§В каком году произошла битва при Гастингсе?~In which year was the Battle of Hastings fought?§1066~1066;1215~1215;1415~1415;1485~1485§Сражение состоялось 14 октября.~The battle took place on 14 October.§hastings§Opening account
normandy§E§Каким герцогством правил Вильгельм, вторгшийся в Англию в 1066 году?~Which duchy did William rule when he invaded England in 1066?§Нормандия~Normandy;Бургундия~Burgundy;Бретань~Brittany;Аквитания~Aquitaine§После победы его стали знать как Вильгельма Завоевателя.~After his victory he became known as William the Conqueror.§hastings§Duke William of Normandy
harold§E§Какого английского короля победила армия Вильгельма при Гастингсе?~Which English king's army did William defeat at Hastings?§Гарольд II~Harold II;Иоанн Безземельный~King John;Ричард III~Richard III;Генрих VIII~Henry VIII§Гарольд был коронован в январе того же года.~Harold had been crowned in January of the same year.§hastings§Opening account
pointed§M§Какой тип арки особенно характерен для готической архитектуры?~Which arch type is especially characteristic of Gothic architecture?§Стрельчатая~Pointed;Только полуциркульная~Exclusively semicircular;Только плоская перемычка~Exclusively a flat lintel;Только треугольный фронтон~Exclusively a triangular pediment§Стрельчатая арка помогала перекрывать проёмы разной ширины и высоты.~Pointed arches helped span openings of different widths and heights.§gothic§Structural innovations
windows§M§Какую роль играли большие витражи в готическом соборе?~What role did large stained-glass windows play in a Gothic cathedral?§Создавали цветное освещение и передавали сюжеты~Created coloured light and conveyed stories;Служили главным водопроводом~Served as the main water supply;Заменяли весь несущий каркас~Replaced the entire supporting frame;Использовались как отопительные печи~Served as heating stoves§Сюжеты витражей могли рассказывать о библейских событиях и святых.~Window scenes could recount biblical events and saints' lives.§gothic§Stained glass
buttress§M§Какую конструктивную задачу решает аркбутан готического собора?~What structural task does a Gothic flying buttress perform?§Воспринимает боковой распор сводов~Takes the vault's outward thrust;Закрывает вход от дождя~Covers the entrance from rain;Поднимает воду из колодца~Raises water from a well;Служит механизмом часов~Acts as a clock mechanism§Внешние опоры позволяли делать стены тоньше и окна больше.~External supports allowed thinner walls and larger windows.§gothic§Flying buttresses
gothic_birth§M§В каком районе Европы в XII веке сложилась готическая архитектура?~In which European area did Gothic architecture emerge in the twelfth century?§Окрестности Парижа~The area around Paris;Окрестности Афин~The area around Athens;Юг Португалии~Southern Portugal;Север Исландии~Northern Iceland§Затем новый архитектурный язык распространился по Европе.~The new architectural language subsequently spread across Europe.§gothic§Opening definition
mongols§M§Какой народ правил Китаем при династии Юань?~Which people ruled China under the Yuan dynasty?§Монголы~Mongols;Норманны~Normans;Франки~Franks;Ацтеки~Aztecs§Китай стал частью более обширного Монгольского государства.~China became part of a larger Mongol political realm.§yuan§Opening historical paragraphs
dadu§M§Как называется сегодня город Даду, столица императоров Юань?~What is Dadu, the Yuan emperors' capital, called today?§Пекин~Beijing;Шанхай~Shanghai;Киото~Kyoto;Сеул~Seoul§Город также был известен под названием Ханбалык.~The city was also known as Khanbaliq.§yuan§Capital in Dadu
centuries§M§К каким векам относится правление династии Юань в Китае: 1271–1368 годы?~Which centuries span China's Yuan dynasty, dated 1271–1368?§XIII–XIV~Thirteenth–fourteenth;IX–X~Ninth–tenth;XI–XII~Eleventh–twelfth;XV–XVI~Fifteenth–sixteenth§Эта эпоха входит в историю средневековой Восточной Азии.~This period belongs to the history of medieval East Asia.§yuan§Article title dates
literati§M§Что, по описанию искусства Юань, стало важной целью живописи учёных?~According to the account of Yuan art, what became an important aim of scholar-painters?§Самовыражение художника~The artist's self-expression;Только точная военная картография~Only precise military mapping;Только изготовление печатных денег~Only making banknotes;Только копирование иностранных гербов~Only copying foreign coats of arms§Художники использовали возможности кисти не только для внешнего сходства.~Artists used brushwork for more than outward resemblance.§yuan§Literati painting
suger§H§При каком аббате перестройка Сен-Дени стала важным этапом ранней готики?~Under which abbot did the rebuilding of Saint-Denis become a key stage of early Gothic?§Сугерий~Suger;Бернард Клервоский~Bernard of Clairvaux;Алкуин~Alcuin;Беда Достопочтенный~Bede§Перестройка восточной части церкви датируется 1140–1144 годами.~The rebuilding of the church's eastern end dates to 1140–1144.§gothic§Saint-Denis
paiza§H§Для чего предназначалась монгольская пайцза, представленная в статье музея об искусстве Юань?~What was the Mongol paiza shown in the museum's Yuan article intended for?§Подтверждать право на безопасный проезд~To certify safe conduct;Измерять вес серебра~To measure silver weight;Определять время суток~To tell the time of day;Записывать музыкальный строй~To record musical tuning§Музей описывает этот предмет как пропуск с надписью.~The museum describes this object as an inscribed safe-conduct pass.§yuan§Safe Conduct Pass object caption
cobalt§H§Какой пигмент указан для синей росписи фарфоровой тарелки эпохи Юань с рыбами?~Which pigment is listed for the blue decoration of the Yuan porcelain plate with fish?§Кобальт~Cobalt;Киноварь~Cinnabar;Малахит~Malachite;Охра~Ochre§Роспись нанесена под прозрачной глазурью.~The decoration lies beneath a transparent glaze.§yuan§Plate with fish object caption
kesi§H§Что обозначает техника кэсы (kesi) в представленном памятнике искусства Юань?~What does kesi denote in the Yuan artwork presented?§Шёлковое ткачество типа гобелена~Silk tapestry weaving;Резьбу по нефриту~Jade carving;Литьё бронзы~Bronze casting;Письмо маслом на холсте~Oil painting on canvas§Музей приводит в качестве примера тканую мандалу.~The museum presents a woven mandala as an example.§yuan§Cosmological Mandala object caption
''')

OSCAR_LABELS = [
('Титаник','Титаник','Джеймс Кэмерон'),
('Властелин колец: Возвращение короля','Властелин колец: Возвращение короля','Питер Джексон'),
('Форрест Гамп','Форрест Гамп','Роберт Земекис'),
('Гладиатор','Траффик','Стивен Содерберг'),
('Список Шиндлера','Список Шиндлера','Стивен Спилберг'),
('Крёстный отец','Кабаре','Боб Фосс'),
('Касабланка','Касабланка','Майкл Кёртис'),
('Звуки музыки','Звуки музыки','Роберт Уайз'),
('Крамер против Крамера','Крамер против Крамера','Роберт Бентон'),
('Взвод','Взвод','Оливер Стоун'),
('Молчание ягнят','Молчание ягнят','Джонатан Демми'),
('Английский пациент','Английский пациент','Энтони Мингелла'),
('Миллионер из трущоб','Миллионер из трущоб','Дэнни Бойл'),
('Артист','Артист','Мишель Хазанавичус'),
('Бёрдмэн','Бёрдмэн','Алехандро Гонсалес Иньярриту'),
('Лунный свет','Ла-Ла Ленд','Дэмьен Шазелл'),
('Форма воды','Форма воды','Гильермо дель Торо'),
('Зелёная книга','Рома','Альфонсо Куарон'),
('Паразиты','Паразиты','Пон Джун-хо'),
('Король говорит!','Король говорит!','Том Хупер')]

def oscar_drafts():
    records=json.loads((ROOT/'authoring/expansion_20261108.oscar-source-records.json').read_text())
    assert len(records)==len(OSCAR_LABELS)==20
    for i,(record,labels) in enumerate(zip(records,OSCAR_LABELS)):
        year=record['year']; best=record['best']; film=record['directingFilm']; director=record['director']
        bestr,filmr,dr=labels; key='oscar_'+str(year)
        source(key,f'https://www.oscars.org/oscars/ceremonies/{year}')
        if i<10:
            prompt=f'Какой фильм получил «Оскар» за лучший фильм на церемонии {year} года?~Which film won Best Picture at the {year} Academy Awards?'
            choices=[(bestr,best)]+[(OSCAR_LABELS[j][0],records[j]['best']) for j in ((i+3)%20,(i+7)%20,(i+11)%20)]
            explanation=f'Режиссёрскую награду той церемонии получил {dr} за фильм «{filmr}».~The same ceremony\'s Directing award went to {director} for {film}.'
            location='Best Picture / Winner; Directing / Winner'
        else:
            prompt=f'Кто получил режиссёрский «Оскар» за фильм «{filmr}» на церемонии {year} года?~Who won Directing for {film} at the {year} Academy Awards?'
            choices=[(dr,director)]+[(OSCAR_LABELS[j][2],records[j]['director']) for j in ((i+3)%20,(i+7)%20,(i+11)%20)]
            explanation=f'Лучшим фильмом той церемонии стал «{bestr}».~The ceremony\'s Best Picture winner was {best}.'
            location='Directing / Winner; Best Picture / Winner'
        rows('cinema','§'.join([str(year),'E' if i<8 else 'M' if i<16 else 'H',prompt,';'.join(a+'~'+b for a,b in choices),explanation,key,location]))
        EVIDENCE[OUT[-1]['id']]['sourceRecord']=record

def write():
    published={q['id'] for p in (ROOT/'questions').glob('*.json') for q in json.loads(p.read_text())}
    if published.intersection(q['id'] for q in OUT):
        raise SystemExit('This historical batch is already published; refusing duplicate drafts. Work on a fresh batch with new stable IDs.')
    grouped={}
    for q in OUT: grouped.setdefault(q['categoryId'],[]).append(q)
    for category, questions in grouped.items():
        (ROOT/'drafts'/f'{category}.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'authoring/expansion_20261108.evidence.json').write_text(json.dumps(EVIDENCE,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'authoring/expansion_20261108.sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2)+'\n')
    print('Drafts only:',len(OUT),'questions;',len(grouped),'categories')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--cache',type=Path,required=True)
    cache=parser.parse_args().cache
    nobel_drafts(cache)
    nobel_history(cache)
    oscar_drafts()
    exec((ROOT/'authoring/expansion_20261108_extra.py').read_text(), globals())
    write()
