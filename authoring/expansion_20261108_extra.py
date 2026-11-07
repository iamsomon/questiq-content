"""Additional authored drafts. Executed in the draft author's namespace."""
source('tv_tardis','https://www.doctorwho.tv/characters/the-tardis')
source('tv_sesame','https://sesameworkshop.org/our-work/shows/sesame-street/sesame-street-characters/')
source('tv_wednesday','https://www.netflix.com/tudum/videos/wednesday-welcomes-you-to-nevermore-academy')
source('tv_simpsons','https://www.disneyplus.com/explore/articles/the-simpsons-collection-guide')
rows('television','''
tardis_shape§E§Как обычно выглядит ТАРДИС снаружи в сериале «Доктор Кто»?~What does the TARDIS usually look like from outside in Doctor Who?§Синяя полицейская будка~A blue police box;Красная телефонная будка~A red telephone box;Серебристая ракета~A silver rocket;Жёлтый автобус~A yellow bus§Маскировочная система корабля застряла в этом облике.~The ship's disguise system became stuck in this form.§tv_tardis§Description: chameleon circuit
wednesday_school§E§В какой академии учится Уэнсдей Аддамс в сериале Netflix?~Which academy does Wednesday Addams attend in the Netflix series?§Невермор~Nevermore;Ривердейл~Riverdale;Хокинс~Hawkins;Саннидейл~Sunnydale§Школьная жизнь Уэнсдей переплетается с расследованием загадочных событий.~Wednesday's school life becomes entangled with a mystery investigation.§tv_wednesday§Video introduction
simpsons_town§E§В каком вымышленном городе живёт семья Симпсонов?~In which fictional town does the Simpson family live?§Спрингфилд~Springfield;Куахог~Quahog;Саут-Парк~South Park;Арлен~Arlen§Гомер работает на местной атомной электростанции.~Homer works at the local nuclear power plant.§tv_simpsons§What is The Simpsons about?
sesame_cookies§E§Кто из героев «Улицы Сезам» особенно любит печенье?~Which Sesame Street character is particularly fond of cookies?§Коржик~Cookie Monster;Элмо~Elmo;Гровер~Grover;Берт~Bert§В описании героя его постоянный поиск еды особенно связан с печеньем.~The character's search for food particularly centres on cookies.§tv_sesame§Cookie Monster character card
tardis_builders§M§Кто создал ТАРДИС во вселенной «Доктора Кто»?~Who created the TARDIS in the Doctor Who universe?§Повелители Времени~Time Lords;Далеки~Daleks;Киберлюди~Cybermen;Сонтаранцы~Sontarans§Корабль Доктора относится к капсулам типа 40.~The Doctor's ship is a Type 40 capsule.§tv_tardis§Type 40 capsule
sesame_count§M§Какое занятие особенно любит граф фон Знак из «Улицы Сезам»?~Which activity does Sesame Street's Count von Count especially enjoy?§Считать предметы~Counting things;Печь хлеб~Baking bread;Чинить автомобили~Repairing cars;Выращивать цветы~Growing flowers§Герой помогает знакомить зрителей с числами через своё любимое занятие.~His favourite activity helps introduce viewers to numbers.§tv_sesame§Count Von Count character card
sesame_friends§M§Кто назван лучшим другом Эрни в официальном описании «Улицы Сезам»?~Who is named as Ernie's best friend in the official Sesame Street description?§Берт~Bert;Гровер~Grover;Элмо~Elmo;Оскар~Oscar§Эрни часто подшучивает над своим приятелем.~Ernie frequently plays practical jokes on his friend.§tv_sesame§Bert and Ernie character cards
simpsons_creator§M§Кто создал сериал «Симпсоны»?~Who created The Simpsons?§Мэтт Грейнинг~Matt Groening;Сет Макфарлейн~Seth MacFarlane;Майк Джадж~Mike Judge;Стивен Хилленберг~Stephen Hillenburg§Над разработкой получасового сериала также работали Джеймс Брукс и Сэм Саймон.~James L. Brooks and Sam Simon also helped develop the half-hour series.§tv_simpsons§Who created The Simpsons?
tardis_acronym§H§Какие английские слова раскрывают название TARDIS?~Which English words expand the name TARDIS?§Time and Relative Dimension in Space~Time and Relative Dimension in Space;Temporal Andromeda Research Device in Space~Temporal Andromeda Research Device in Space;Time and Radiation Detection in Space~Time and Radiation Detection in Space;Transport and Remote Discovery in Space~Transport and Remote Discovery in Space§Сокращение придумала Сьюзен, внучка Доктора.~The acronym was coined by Susan, the Doctor's granddaughter.§tv_tardis§Acronym and Susan
simpsons_shorts§H§В каком телешоу впервые появились короткометражки о Симпсонах в 1987 году?~In which TV show did The Simpsons first appear as shorts in 1987?§Шоу Трейси Ульман~The Tracey Ullman Show;Субботним вечером в прямом эфире~Saturday Night Live;Шоу Кэрол Бёрнетт~The Carol Burnett Show;Маппет-шоу~The Muppet Show§Самостоятельный сериал вышел в 1989 году.~The standalone series premiered in 1989.§tv_simpsons§Fun Fact 1
''')
source('food_bread','https://annex.exploratorium.edu/cooking/bread/bread_science.html')
source('food_ferment','https://annex.exploratorium.edu/cooking/pickles/fermentation.html')
source('food_eggs','https://annex.exploratorium.edu/cooking/eggs/eggscience.html')
source('food_sugar','https://annex.exploratorium.edu/cooking/candy/sugar.html')
rows('food','''
yeast§E§К какой группе организмов относятся пекарские дрожжи?~To which group of organisms does baker's yeast belong?§Грибы~Fungi;Бактерии~Bacteria;Водоросли~Algae;Простейшие~Protozoa§Пекарские дрожжи — одноклеточные организмы, питающиеся сахарами.~Baker's yeast consists of single-celled organisms that feed on sugars.§food_bread§Yeast paragraph
bread_gas§E§Какой газ помогает дрожжевому тесту подниматься?~Which gas helps yeast dough rise?§Углекислый газ~Carbon dioxide;Кислород~Oxygen;Азот~Nitrogen;Водород~Hydrogen§Пузырьки газа формируются, пока дрожжи перерабатывают сахара.~Gas bubbles form as yeast processes sugars.§food_bread§Yeast and carbon dioxide
lavash§E§К какому виду выпечки относится лаваш?~What type of baked food is lavash?§Тонкий хлеб~Thin flatbread;Слоёное печенье~Puff-pastry biscuit;Сладкий кекс~Sweet sponge cake;Песочный пирог~Shortcrust pie§Хлеб может иметь очень разную толщину и структуру: от плоских лепёшек до пышной бриоши.~Bread ranges widely in thickness and texture, from flatbreads to airy brioche.§food_bread§Opening examples
sucrose§E§Как называется вещество, из которого состоит обычный столовый сахар?~What substance makes up ordinary table sugar?§Сахароза~Sucrose;Лактоза~Lactose;Крахмал~Starch;Целлюлоза~Cellulose§Её получают, в частности, из сахарного тростника и сахарной свёклы.~Sugarcane and sugar beet are major sources of it.§food_sugar§Opening paragraph
leavener§M§Чем действие пищевой соды и разрыхлителя отличается от действия дрожжей?~How does the action of baking soda and baking powder differ from that of yeast?§Газ образуется в химической реакции~Gas is produced by a chemical reaction;Растут колонии живых грибов~Colonies of living fungi grow;Тесто поднимают волокна муки без газа~Flour fibres lift dough without gas;Объём увеличивают кристаллы соли~Salt crystals expand the volume§Такие разрыхлители обычно действуют быстрее дрожжевого брожения.~These leaveners generally work faster than yeast fermentation.§food_bread§Baking powder or baking soda
lactic§M§Какая кислота придаёт характерную кислинку овощам при молочнокислом брожении?~Which acid gives vegetables their characteristic sourness during lactic fermentation?§Молочная~Lactic;Лимонная~Citric;Яблочная~Malic;Винная~Tartaric§Её образуют бактерии, перерабатывающие сахара овощей.~Bacteria produce it by processing sugars in the vegetables.§food_ferment§Pickled Vegetables
whey§M§Какую жидкость отделяют от сгустка при изготовлении сыра?~Which liquid is drained from curds during cheese-making?§Сыворотку~Whey;Сливки~Cream;Масло~Butter;Сироп~Syrup§После отделения жидкости сырный сгусток уплотняют и могут отправлять на созревание.~After drainage, the curds are compacted and may be ripened.§food_ferment§Cheeses
cooked_white§M§Почему яичный белок при нагревании становится плотнее?~Why does egg white become firm when heated?§Белковые молекулы разворачиваются и связываются в сеть~Protein molecules unfold and link into a network;Сахара образуют крупные кристаллы~Sugars form large crystals;Вода превращается в крахмал~Water changes into starch;Жиры превращаются в клетчатку~Fats change into fibre§Образовавшаяся белковая сеть удерживает воду.~The resulting protein network traps water.§food_eggs§Heat them
meringue§H§Что взбивание добавляет в яичные белки для безе?~What does beating incorporate into egg whites for meringue?§Пузырьки воздуха~Air bubbles;Кристаллы соли~Salt crystals;Зёрна крахмала~Starch granules;Капли масла~Oil droplets§Взбивание также меняет форму белковых молекул.~Beating also changes the shape of protein molecules.§food_eggs§Beat them
sugar_units§H§Какие два простых сахара входят в молекулу сахарозы?~Which two simple sugars make up a sucrose molecule?§Глюкоза и фруктоза~Glucose and fructose;Глюкоза и галактоза~Glucose and galactose;Две молекулы глюкозы~Two glucose molecules;Фруктоза и галактоза~Fructose and galactose§Небольшое количество кислоты помогает расщепить сахарозу на эти части.~A little acid can help split sucrose into these components.§food_sugar§Opening two paragraphs
''')
source('olyrings','https://www.olympics.com/ioc/olympic-rings')
for key,slug in [('olyfounder','who-was-pierre-de-coubertin'),('olyorigin','what-is-the-origin-of-the-olympic-games'),('olywomen','when-did-women-first-compete-in-the-olympic-games'),('olywinter','when-were-the-first-olympic-winter-games-held'),('olycycle','since-when-have-the-summer-and-winter-games-no-longer-been-held-in-the-same-year')]:
    source(key,'https://www.olympics.com/ioc/faq/history-and-origin-of-the-games/'+slug)
rows('olympics','''
athens§E§Где состоялись первые Олимпийские игры современности в 1896 году?~Where were the first modern Olympic Games held in 1896?§Афины~Athens;Париж~Paris;Рим~Rome;Лондон~London§Проект возрождения Игр Пьер де Кубертен представил в 1894 году.~Pierre de Coubertin launched his revival project in 1894.§olyorigin§Final answer paragraph
rings§E§Сколько переплетённых колец в олимпийском символе?~How many interlaced rings form the Olympic symbol?§Пять~Five;Четыре~Four;Шесть~Six;Семь~Seven§Символ выражает встречу спортсменов и единство пяти частей света.~The symbol represents athletes meeting and the union of five parts of the world.§olyrings§Definition and meaning
women§E§В каком городе женщины впервые участвовали в современных Олимпийских играх в 1900 году?~In which city did women first compete in the modern Olympic Games in 1900?§Париж~Paris;Афины~Athens;Стокгольм~Stockholm;Антверпен~Antwerp§Они участвовали в теннисе, парусном спорте, крокете, конном спорте и гольфе.~They competed in tennis, sailing, croquet, equestrian events and golf.§olywomen§First answer paragraph
winter§E§Какой город принял первые зимние Олимпийские игры в 1924 году?~Which town hosted the first Olympic Winter Games in 1924?§Шамони~Chamonix;Санкт-Мориц~St Moritz;Инсбрук~Innsbruck;Гармиш-Партенкирхен~Garmisch-Partenkirchen§Сначала соревнования называли Международной неделей зимних видов спорта.~The event was initially called International Winter Sports Week.§olywinter§First answer paragraph
flag§M§Какого цвета фон классического олимпийского флага?~What is the background colour of the classic Olympic flag?§Белый~White;Синий~Blue;Жёлтый~Yellow;Зелёный~Green§Флаг создали к Олимпийскому конгрессу 1914 года в Париже.~The flag was created for the 1914 Olympic Congress in Paris.§olyrings§History: 1914
ringdesigner§M§Кто разработал олимпийский символ из пяти колец?~Who designed the five-ring Olympic symbol?§Пьер де Кубертен~Pierre de Coubertin;Анри Дидон~Henri Didon;Анри де Байе-Латур~Henri de Baillet-Latour;Деметриус Викелас~Demetrius Vikelas§Символ впервые публично представили в 1913 году.~The symbol was first publicly presented in 1913.§olyrings§History: 1913
olympiad§M§Какой период называли олимпиадой в Древней Греции?~What period was called an Olympiad in Ancient Greece?§Четыре года~Four years;Один год~One year;Два года~Two years;Десять лет~Ten years§Этот интервал между Играми использовали для летосчисления.~This interval between the Games was used for dating events.§olyorigin§Olympiad paragraph
lastsame§M§В каком году летние и зимние Олимпийские игры в последний раз планово прошли в одном году?~In which year were the Summer and Winter Olympics last regularly held in the same year?§1992~1992;1984~1984;1988~1988;1996~1996§Тогда летние Игры приняла Барселона, а зимние — Альбервиль.~Barcelona hosted the Summer Games and Albertville the Winter Games that year.§olycycle§First answer paragraph
antwerp§H§На каких Играх олимпийский флаг впервые появился на стадионе в 1920 году?~At which Games did the Olympic flag first appear in the stadium in 1920?§Антверпен~Antwerp;Париж~Paris;Стокгольм~Stockholm;Амстердам~Amsterdam§Белое полотнище с кольцами создали ещё в 1914 году.~The white flag bearing the rings had been created in 1914.§olyrings§History: 1920
founderioc§H§Какую международную организацию Пьер де Кубертен основал в 1894 году?~Which international organisation did Pierre de Coubertin found in 1894?§Международный олимпийский комитет~International Olympic Committee;Международную федерацию футбола~International Federation of Association Football;Международный паралимпийский комитет~International Paralympic Committee;Всемирное антидопинговое агентство~World Anti-Doping Agency§Он связывал развитие спорта с образованием и мирным сотрудничеством.~He connected sport with education and peaceful cooperation.§olyfounder§First answer paragraph
''')
source('record_montreal','https://www.olympics.com/ioc/news/montreal-celebrates-30th-anniversary-of-1976-olympic-games')
source('record_helsinki','https://www.olympics.com/ioc/news/from-major-sports-events-to-rock-concerts-the-legacy-of-helsinki-1952-lives-on')
source('record_rome','https://www.olympics.com/ioc/news/sporting-highlights-x2424')
source('record_bolt','https://worldathletics.org/competition/calendar-results/results/6998524?eventId=10229630')
source('record_jumps','https://worldathletics.org/competitions/world-athletics-championships/world-athletics-championships-oregon-2022-7137279/news/feature/track-and-field-basics')
rows('sports_records','''
comaneci§E§Кто получил первую олимпийскую оценку 10,0 в спортивной гимнастике в Монреале в 1976 году?~Who earned the first Olympic perfect 10.0 in artistic gymnastics at Montreal 1976?§Надя Комэнеч~Nadia Comaneci;Ольга Корбут~Olga Korbut;Лариса Латынина~Larisa Latynina;Нелли Ким~Nellie Kim§Первую такую оценку она получила на разновысоких брусьях.~Her first perfect score came on the uneven bars.§record_montreal§Nadia Comaneci star of the Games
bolt§E§Какое время показал Усэйн Болт в финале 100 метров на чемпионате мира 2009 года в Берлине?~What time did Usain Bolt run in the 100m final at the 2009 World Championships in Berlin?§9,58 с~9.58 s;9,69 с~9.69 s;9,72 с~9.72 s;9,77 с~9.77 s§Тайсон Гэй стал вторым с результатом 9,71 секунды.~Tyson Gay finished second in 9.71 seconds.§record_bolt§Men 100 Metres final table
bikila§E§Кто выиграл марафон Олимпиады 1960 года в Риме босиком?~Who won the Rome 1960 Olympic marathon barefoot?§Абебе Бикила~Abebe Bikila;Эмиль Затопек~Emil Zatopek;Ален Мимун~Alain Mimoun;Фрэнк Шортер~Frank Shorter§В 1964 году в Токио он защитил олимпийский титул.~He defended his Olympic title in Tokyo in 1964.§record_rome§Abebe Bikila paragraph
zatopek§E§Кто в Хельсинки в 1952 году выиграл 5000 метров, 10 000 метров и марафон?~Who won the 5000m, 10,000m and marathon at Helsinki 1952?§Эмиль Затопек~Emil Zatopek;Пааво Нурми~Paavo Nurmi;Лассе Вирен~Lasse Viren;Ханнес Колехмайнен~Hannes Kolehmainen§Марафон стал для этого бегуна дебютом на данной дистанции.~The marathon was his debut at that distance.§record_helsinki§Opening sporting highlights
powell§M§Какую длину показал прыжок Майка Пауэлла на чемпионате мира 1991 года в Токио?~How far did Mike Powell jump at the 1991 World Championships in Tokyo?§8,95 м~8.95 m;8,90 м~8.90 m;8,84 м~8.84 m;8,79 м~8.79 m§Он превзошёл результат Боба Бимона 1968 года — 8,90 метра.~He surpassed Bob Beamon's 1968 mark of 8.90 metres.§record_jumps§Long Jump
edwards§M§В каком виде Джонатан Эдвардс показал 18,29 метра на чемпионате мира 1995 года?~In which event did Jonathan Edwards achieve 18.29 metres at the 1995 World Championships?§Тройной прыжок~Triple jump;Прыжок в длину~Long jump;Толкание ядра~Shot put;Метание молота~Hammer throw§Эти соревнования проходили в шведском Гётеборге.~The championships took place in Gothenburg, Sweden.§record_jumps§Triple Jump
rudolph§M§Кто выиграл женские 100 метров, 200 метров и эстафету 4 × 100 на Играх в Риме в 1960 году?~Who won the women's 100m, 200m and 4 × 100m relay at Rome 1960?§Вильма Рудольф~Wilma Rudolph;Бетти Катберт~Betty Cuthbert;Вайомия Тайес~Wyomia Tyus;Фанни Бланкерс-Кун~Fanny Blankers-Koen§Она стала первой американкой с тремя золотыми медалями на одной Олимпиаде.~She became the first US woman to win three golds at one Olympics.§record_rome§Wilma Rudolph paragraph
ali§M§Под каким именем будущий Мухаммед Али выиграл олимпийское золото в боксе в 1960 году?~Under which name did the future Muhammad Ali win Olympic boxing gold in 1960?§Кассиус Клей~Cassius Clay;Джо Фрейзер~Joe Frazier;Джордж Форман~George Foreman;Флойд Паттерсон~Floyd Patterson§Он выступал в полутяжёлом весе.~He competed in the light-heavyweight division.§record_rome§Cassius Clay paragraph
sotomayor§H§Кто в 1993 году установил результат 2,45 метра в прыжках в высоту?~Who achieved a 2.45m high jump in 1993?§Хавьер Сотомайор~Javier Sotomayor;Патрик Шёберг~Patrik Sjoberg;Стефан Хольм~Stefan Holm;Богдан Бондаренко~Bohdan Bondarenko§Сотомайор представлял Кубу.~Sotomayor represented Cuba.§record_jumps§High Jump historical mark 1993
jackson§H§Какая австралийская бегунья выиграла 100 и 200 метров на Играх 1952 года?~Which Australian sprinter won the 100m and 200m at the 1952 Games?§Марджори Джексон~Marjorie Jackson;Бетти Катберт~Betty Cuthbert;Ширли Стрикленд~Shirley Strickland;Джойс Кинг~Joyce King§Игры в Хельсинки стали важным этапом её спортивной карьеры.~The Helsinki Games were a major milestone in her athletics career.§record_helsinki§Marjorie Jackson paragraph
''')

# Explicit editorial changes after reading the source pages and both locales.
def edit(category, slug, *, prompt=None, choices=None, explanation=None, url=None, location=None):
    q=next(q for q in OUT if q['id']==f'{category}_nov08_{slug}')
    if prompt:
        for lang,value in zip(('ru','en'),prompt.split('~')): q['localizations'][lang]['question']=value
    if choices:
        pairs=[s.split('~') for s in choices.split(';')]
        assert len(pairs)==4 and all(len(p)==2 for p in pairs)
        q['options']=[{'id':f'o{i}','ru':p[0],'en':p[1]} for i,p in enumerate(pairs)]
    if explanation:
        for lang,value in zip(('ru','en'),explanation.split('~')): q['localizations'][lang]['explanation']=value
    if url: q['sources']=[url]; EVIDENCE[q['id']]['url']=url
    if location: EVIDENCE[q['id']]['location']=location
    EVIDENCE[q['id']]['claim']=q['localizations']['en']['question']+' Answer: '+q['options'][0]['en']+'. '+q['localizations']['en']['explanation']

for slug,url,location in [
('synagogue','https://pluralism.org/the-synagogue','Main text: prayer, study and community'),
('sabbath','https://pluralism.org/keeping-shabbat','Main text: weekly rest'),
('gurdwara','https://pluralism.org/the-gurdwara','Main text: meeting place and scripture'),
('granth','https://pluralism.org/the-guru-granth-sahib','Main text: successor to Gobind Singh'),
('langar','https://pluralism.org/langar-the-communal-meal','Main text: meal and equality'),
('nanak','https://pluralism.org/sikhism','Timeline: 1469 Guru Nanak'),
('khalsa','https://pluralism.org/sikhism','Timeline: 1699 Khalsa'),
('puja','https://pluralism.org/puja','Glossary: offerings in Hindu worship'),
('shinto_japan','https://www.meijijingu.or.jp/en/about/aboutshinto/','About Shinto: Japanese roots'),
('kami','https://www.meijijingu.or.jp/en/about/aboutshinto/','About Shinto: Kami'),
('zoroaster','https://pluralism.org/ancient-faith-in-the-modern-world','Opening text: Zarathushtra and Zoroaster'),
('avesta','https://pluralism.org/avesta','Glossary: scripture collection and Gathas')]:
    edit('world_religions',slug,url=url,location=location)
edit('world_religions','puja',explanation='Во время пуджи божеству предлагают, например, воду, плоды и благовония.~Offerings in a puja may include water, fruit and incense.')
edit('world_religions','langar',choices='Общая бесплатная трапеза~A free communal meal;Чтение писания без перерыва~An unbroken reading of scripture;Совместное пение гимнов~Singing hymns together;Торжественная процессия~A ceremonial procession')
edit('christianity','visitation',prompt='Какую родственницу Мария посещает после Благовещения в евангельском повествовании?~Which relative does Mary visit after the Annunciation in the Gospel narrative?')
edit('islam','five',prompt='Сколько установленных ежедневных молитв совершают в исламской традиции?~How many prescribed daily prayers are performed in Islamic tradition?')
edit('islam','surah',explanation='Коран разделён на 114 сур.~The Qur\'an is divided into 114 suras.')
edit('pop_culture','yoshi',prompt='Как зовут зелёного спутника Марио с длинным языком, который умеет откладывать яйца?~What is the name of Mario\'s green companion with a long tongue who can lay eggs?')
edit('pop_culture','c3',choices='Этикет, протокол и перевод~Etiquette, protocol and translation;Обслуживание кораблей~Spacecraft maintenance;Медицинская помощь~Medical assistance;Военная разведка~Military reconnaissance')
edit('pop_culture','hogwarts',choices='Колдовству и волшебству~Witchcraft and wizardry;Морской навигации~Sea navigation;Офицерскому делу~Officer training;Классическому балету~Classical ballet',explanation='Школа находится в замке в Шотландском нагорье.~The school occupies a castle in the Scottish Highlands.')
edit('pop_culture','gryffindor',explanation='Цвета факультета — алый и золотой.~The house colours are scarlet and gold.')
edit('pop_culture','slytherin',explanation='Цвета факультета — серебряный и изумрудно-зелёный.~The house colours are silver and emerald green.')
edit('pop_culture','hufflepuff',explanation='Цвета факультета — жёлтый и чёрный.~The house colours are yellow and black.')
# The original pitch/timbre/verse references did not substantiate the whole claim.
# Replace those draft facts, rather than approving an unsupported source match.
edit('music','pitch',prompt='Как называют создание и исполнение музыки без заранее записанной партии?~What is creating and performing music without a previously written part called?',choices='Импровизация~Improvisation;Транскрипция~Transcription;Транспозиция~Transposition;Оркестровка~Orchestration',explanation='Так могут возникать музыкальные идеи прямо во время исполнения.~Musical ideas can emerge during the performance itself.',location='PDF printed page 88: Improvisation')
edit('music','timbre',prompt='В честь какого композитора назван сузафон?~After which composer is the sousaphone named?',choices='Джон Филип Суза~John Philip Sousa;Джордж Гершвин~George Gershwin;Аарон Копленд~Aaron Copland;Чарльз Айвз~Charles Ives',explanation='Суза написал марш «Звёзды и полосы навсегда» в 1897 году.~Sousa wrote Stars and Stripes Forever in 1897.',url=SOURCES['musicgloss'],location='PDF printed page 87: John Philip Sousa')
edit('music','verse',prompt='По произведению какого писателя Шостакович написал оперу «Нос»?~Whose story inspired Shostakovich\'s opera The Nose?',choices='Николай Гоголь~Nikolai Gogol;Антон Чехов~Anton Chekhov;Иван Тургенев~Ivan Turgenev;Михаил Булгаков~Mikhail Bulgakov',explanation='Помимо опер, Шостакович написал пятнадцать симфоний.~As well as operas, Shostakovich wrote fifteen symphonies.',location='PDF printed page 87: Dmitri Shostakovich')
edit('music','unison',explanation='При таком исполнении голоса не разделяются на самостоятельные мелодические линии.~In this kind of performance, the voices do not split into independent melodic lines.')

# Plausible alternatives in the same subject area; none is a second correct answer.
for slug,choices in {
'soap':'Мыло~Soap;Увлажняющий крем~Moisturising cream;Защитный воск~Protective wax;Тальк~Talc',
'hygiene':'Помогает уменьшить распространение~Helps reduce transmission;Уничтожает все микробы навсегда~Eliminates all germs permanently;Обеззараживает предметы без их мытья~Disinfects objects without washing them;Меняет генетический код микробов~Changes the genetic code of germs',
'sleepmemory':'Обучение и запоминание~Learning and memory;Формирование новой группы крови~Formation of a new blood group;Увеличение числа хромосом~An increase in chromosome number;Образование витамина C~Production of vitamin C',
'sleeprem':'Быстрые движения глаз~Rapid eye movements;Глубокое медленное дыхание~Deep slow breathing;Регулярные движения конечностей~Regular limb movements;Расслабление мышц спины~Relaxation of back muscles',
'deep':'Третью~Stage three;Первую~Stage one;Вторую~Stage two;Фазу REM~The REM phase',
'antigen':'Антиген~Antigen;Антитело~Antibody;Гормон~Hormone;Нейромедиатор~Neurotransmitter',
'vaccine':'Иммунную память~Immune memory;Прямую устойчивость к любому яду~Direct resistance to every poison;Постоянное отсутствие воспаления~Permanent absence of inflammation;Полную защиту от всех инфекций~Complete protection from all infections',
'remsignals':'Электрическую активность мозга~Electrical brain activity;Химический состав волос~Chemical composition of hair;Минеральную плотность костей~Bone mineral density;Пигментацию кожи~Skin pigmentation',
'memorycells':'Клетки памяти~Memory cells;Запас готовых антибиотиков~A stock of ready-made antibiotics;Новую группу крови~A new blood group;Запас кислорода в лимфоузлах~Oxygen stored in lymph nodes',
'percentdv':'Долю установленной суточной величины нутриента~The fraction of a nutrient\'s established Daily Value;Долю усвоенных организмом веществ~The fraction of substances absorbed by the body;Долю продукта от суточной массы пищи~The food\'s fraction of daily food mass;Изменение нутриентов при готовке~The change in nutrients during cooking',
}.items(): edit('health',slug,choices=choices)
edit('health','sodium',prompt='В каких единицах приведено количество натрия на примере этикетки FDA?~In which units is sodium shown on the FDA sample label?',choices='Миллиграммы~Milligrams;Граммы~Grams;Микрограммы~Micrograms;Килокалории~Kilocalories',explanation='Количество указывают для одной порции продукта.~The amount refers to one serving of the food.',location='Sample label: Sodium 850mg')
edit('health','remsignals',prompt='Какой сигнал от головного мозга помогает различать стадии сна?~Which signal from the brain helps distinguish sleep stages?')
edit('health','totalsugar',choices='Да, это часть общего количества~Yes, they are part of the total;Нет, эти две величины нужно складывать~No, the two values must be added;Только сахар, добавленный перед продажей~Only sugar added just before sale;Только сахар, добавленный перед упаковкой~Only sugar added just before packaging')

for slug,choices in {
'traction':'Тяговый электромотор~Electric traction motor;Бортовое зарядное устройство~Onboard charger;Преобразователь DC/DC~DC/DC converter;Вспомогательная батарея~Auxiliary battery',
'battery':'В тяговой батарее~In the traction battery;В бортовом зарядном устройстве~In the onboard charger;В преобразователе DC/DC~In the DC/DC converter;В контроллере силовой электроники~In the power electronics controller',
'hybrid':'ДВС и электромотор~Combustion engine and electric motor;Дизельный и бензиновый ДВС~Diesel and petrol combustion engines;Газовую турбину и дизель~Gas turbine and diesel engine;Два бензиновых ДВС~Two petrol combustion engines',
'phev':'Возможность зарядки от внешней сети~It can be charged from an external supply;Отсутствие ДВС~It has no combustion engine;Отсутствие тяговой батареи~It has no traction battery;Зарядка только при торможении~It can charge only while braking',
'regen':'Возвращает часть энергии в батарею~Returns some energy to the battery;Превращает всю энергию в нагрев дисков~Converts all energy into brake-disc heat;Увеличивает обороты мотора без выработки тока~Increases motor speed without generating electricity;Разряжает батарею для работы тормозных колодок~Discharges the battery to operate brake pads',
'airbag':'Ремень безопасности~Seat belt;Антиблокировочную систему~Anti-lock braking;Контроль тяги~Traction control;Контроль давления в шинах~Tyre-pressure monitoring',
'auxbattery':'Вспомогательные электрические устройства~Electrical accessories;Основной ток тягового двигателя~The main traction motor current;Постоянное питание внешней зарядной станции~Continuous power to the external charging station;Высоковольтный вход быстрого зарядного устройства~The high-voltage input of a rapid charger',
'dcdc':'Понижает постоянное напряжение для вспомогательных систем~Reduces DC voltage for auxiliary systems;Преобразует сетевой переменный ток для зарядки~Converts grid AC for charging;Распределяет крутящий момент между колёсами~Distributes torque between wheels;Поддерживает давление тормозной жидкости~Maintains brake-fluid pressure',
'onboard':'Бортовое зарядное устройство~Onboard charger;Преобразователь DC/DC~DC/DC converter;Дифференциал~Differential;Контроллер тягового мотора~Traction motor controller',
 'thermal':'Поддерживает подходящую температуру компонентов~Maintains suitable component temperatures;Преобразует сетевой ток в постоянный~Converts grid AC into DC;Распределяет крутящий момент~Distributes torque;Понижает напряжение для аксессуаров~Reduces voltage for accessories',
'controller':'Управление потоком энергии и работой мотора~Managing energy flow and motor operation;Хранение основной энергии для движения~Storing the main driving energy;Преобразование сетевого тока при зарядке~Converting grid AC during charging;Передача механической энергии колёсам~Transferring mechanical power to the wheels',
'hevcharge':'Работой двигателя и рекуперацией~Through the engine and regenerative braking;Только внешней зарядной станцией~Only through an external charging station;Только заменой модулей батареи~Only through replacement battery modules;Только встроенной солнечной панелью~Only through an integrated solar panel',
'bev':'Батарейный электромобиль~Battery electric vehicle;Подключаемый гибрид~Plug-in hybrid electric vehicle;Обычный гибрид~Conventional hybrid electric vehicle;Электромобиль на топливных элементах~Fuel-cell electric vehicle',
'motor_generator':'Мотор-генератор~Motor-generator;Преобразователь DC/DC~DC/DC converter;Бортовое зарядное устройство~Onboard charger;Вспомогательная батарея~Auxiliary battery',
'charger_monitor':'Напряжение, ток и температуру~Voltage, current and temperature;Давление, вязкость и объём~Pressure, viscosity and volume;Ускорение, скорость и путь~Acceleration, speed and distance;Мощность звука, яркость и частоту~Sound power, brightness and frequency',
'fuelparts':'Топливный насос~Fuel pump;Насос охлаждения~Coolant pump;Тормозной насос~Brake pump;Насос омывателя~Washer pump',
}.items(): edit('cars',slug,choices=choices)
edit('cars','cooling',choices='У него есть система охлаждения электрических компонентов~It has a cooling system for electrical components;Ему обязательно нужен выхлопной коллектор~It must have an exhaust manifold;Ему обязательно нужен бензиновый бак~It must have a petrol tank;Его мотор не выделяет тепла~Its motor produces no heat')
edit('cars','hevcharge',explanation='Батарея получает энергию при торможении и от двигателя.~The battery receives energy during braking and from the engine.')

for slug,choices in {
'charlemagne':'Франками~Franks;Лангобардами~Lombards;Вестготами~Visigoths;Остготами~Ostrogoths',
'latin':'Латынь~Latin;Греческий~Greek;Древнеанглийский~Old English;Арабский~Arabic',
'revival':'Культурный подъём эпохи Карла Великого~The cultural revival of Charlemagne\'s age;Культурный подъём Византии при Македонской династии~Byzantium\'s cultural revival under the Macedonian dynasty;Расцвет итальянских городов XV века~The flourishing of Italian cities in the fifteenth century;Распространение печатных книг XVI века~The spread of printed books in the sixteenth century',
'pointed':'Стрельчатая~Pointed;Подковообразная~Horseshoe;Полуциркульная~Semicircular;Килевидная~Ogee',
'windows':'Создавали цветное освещение и передавали сюжеты~Created coloured light and conveyed stories;Передавали распор сводов наружным опорам~Transferred vault thrust to external supports;Усиливали фундамент под колоннами~Strengthened the foundation below columns;Поддерживали каменные рёбра сводов~Supported the stone ribs of vaults',
'buttress':'Воспринимает боковой распор сводов~Takes the vault\'s outward thrust;Несёт перемычку входного портала~Carries the entrance portal lintel;Соединяет края витражных стёкол~Joins the edges of stained-glass panes;Укрепляет подземный свод крипты~Reinforces the underground crypt vault',
'mongols':'Монголы~Mongols;Маньчжуры~Manchus;Кидани~Khitans;Чжурчжэни~Jurchens',
'literati':'Самовыражение художника~The artist\'s self-expression;Точная копия архитектурного плана~An exact copy of an architectural plan;Строгое воспроизведение внешнего сходства~Strict reproduction of outward likeness;Стандартизация орнамента керамики~Standardisation of ceramic decoration',
}.items():edit('middle_ages',slug,choices=choices)

# Laureate award-category and co-award facts provide actual additional context.
people={int(p['id']):p for p in json.loads((cache/'nobel-laureates.json').read_text())['laureates']}
for q in OUT:
    if q['categoryId']=='historical_figures':
        ev=EVIDENCE[q['id']]; award=ev['sourceRecord']['award']; p=people[int(ev['sourceRecord']['id'])]
        category={'physics':('физике','Physics'),'chemistry':('химии','Chemistry'),'medicine':('физиологии или медицине','Physiology or Medicine'),'peace':('мира','Peace'),'economics':('экономическим наукам','Economic Sciences')}[award['category']]
        if len(p['prizes'])>1:
            more=[x for x in p['prizes'] if x['year']!=award['year']]
            if more:
                extra=more[0]; ex=f"Этот лауреат также получил премию в {extra['year']} году.~The same laureate also received a prize in {extra['year']}."
            else: ex=f"Награда относится к премии по {category[0]}.~The award belongs to the {category[1]} category."
        else:
            # Full name, date of birth and award category are separately checked metadata.
            year=p.get('born','')[:4]
            ex=f"Год рождения лауреата — {year}; награда относится к премии по {category[0]}.~The laureate was born in {year}; the award category was {category[1]}." if category[1]!='Peace' else f"Лауреат родился в {year} году.~The laureate was born in {year}."
        edit('historical_figures',q['id'].split('_nov08_')[1],explanation=ex,location=ev['location']+'; born; prizes/category')
    elif q['categoryId']=='modern_history':
        ev=EVIDENCE[q['id']]; pid=ev['sourceRecord']['id']; p=people[pid]
        if pid==881: ex='Награда отметила более шести десятилетий европейского сотрудничества.~The award recognised more than six decades of European cooperation.'
        elif pid==503: ex='Организация продолжала помощь беженцам, начатую Фритьофом Нансеном.~The organisation continued refugee assistance begun by Fridtjof Nansen.'
        elif pid==482: ex='Комитет также получил Нобелевскую премию мира в 1944 и 1963 годах.~The committee also received the Nobel Peace Prize in 1944 and 1963.'
        else:
            year=p['born'][:4]; ex=f'Начало работы этой организации относится к {year} году.~This organisation began its work in {year}.'
        edit('modern_history',q['id'].split('_nov08_')[1],explanation=ex,location=ev['location']+'; founding year (born) or other prizes')
# No unused guessed URLs are exported as a source inventory.
SOURCES={k:v for k,v in SOURCES.items() if any(v in q['sources'] for q in OUT)}
for q in OUT:
    ev=EVIDENCE[q['id']]
    ev['claim']=q['localizations']['en']['question']+' Answer: '+q['options'][0]['en']+'. '+q['localizations']['en']['explanation']
edit('middle_ages','charlemagne',prompt='Королём какого народа Карл Великий стал в 768 году?~Of which people did Charlemagne become king in 768?',explanation='В 800 году он также получил императорскую корону.~In 800 he also received an imperial crown.')
for pid,name in [(670,'Тони Моррисон'),(615,'Габриэла Мистраль'),(673,'Вислава Шимборская')]:
    q=next(q for q in OUT if q['id']==f'celebrities_nov08_birth_{pid}')
    q['localizations']['ru']['question']=f'На территории какой современной страны родилась {name}?'
# Export every actually used URL, including corrected canonical references.
for q in OUT:
    u=q['sources'][0]
    if u not in SOURCES.values():
        import hashlib
        SOURCES['checked_'+hashlib.sha256(u.encode()).hexdigest()[:12]]=u
edit('buddhism','meditation',prompt='Какую практику обозначает поза Будды с обращёнными вверх ладонями, лежащими одна на другой на коленях?~Which practice is indicated by a Buddha with upward-facing palms resting one on top of the other in the lap?',choices='Медитация~Meditation;Наставление~Teaching;Защита~Protection;Дарование~Bestowing')
edit('buddhism','karma',choices='Поступки и их последствия~Actions and their consequences;Только судьба, заданная при рождении~Only destiny fixed at birth;Независимые от поступков случайности~Chance events independent of actions;Только принадлежность к общине~Only membership of a community')
edit('buddhism','jataka',choices='О прежних жизнях Будды~The Buddha\'s previous lives;О воплощениях Вишну~Vishnu\'s incarnations;О деяниях Гуру Нанака~Guru Nanak\'s deeds;О путешествиях Махавиры~Mahavira\'s journeys')
edit('buddhism','sanchi',choices='Санчи~Sanchi;Аджанта~Ajanta;Эллора~Ellora;Бадами~Badami')
edit('buddhism','aniconic',choices='Отпечатками стоп~Footprints;Профильным портретом царя~A king\'s portrait in profile;Царской погребальной маской~A royal funerary mask;Головой слона с короной~A crowned elephant head')
edit('world_religions','gurdwara',choices='Гурдвара~Gurdwara;Синагога~Synagogue;Собор~Cathedral;Вихара~Vihara')
edit('islam','hadith',choices='Хадисы~Hadith;Суры~Surahs;Тафсиры~Tafsirs;Дуа~Duas')
edit('christianity','christ_title',choices='Помазанник~Anointed one;Учитель~Teacher;Законодатель~Lawgiver;Посланник~Messenger')
edit('christianity','apostles',explanation='К этому кругу принадлежали Пётр, Иаков и Иоанн.~Peter, James and John belonged to this circle.')
edit('christianity','jordan',explanation='В этом эпизоде крещение совершает Иоанн Креститель.~John the Baptist performs the baptism in this episode.')
# Remove repetitive source-process language from explanations shown to players.
places=['Дулуте','Калькутте','Аракатаке','Оук-Парке','Вудстоке','Мондови','Париже','Салинасе','Нью-Олбани','Москве','Дублине','Сент-Луисе','Кисловодске','Абеокуте','Мехико','Лорейне','Бомбее','Викунье','Кастри','Бнине']
for i,q in enumerate([q for q in OUT if q['categoryId']=='celebrities']):
    female=q['id'].endswith(('_670','_615','_673'))
    city=EVIDENCE[q['id']]['sourceRecord']['bornCity']
    edit('celebrities',q['id'].split('_nov08_')[1],explanation=('Она родилась в ' if female else 'Он родился в ')+places[i]+'.~'+('She' if female else 'He')+' was born in '+city+'.')
edit('cars','exhaust',prompt='Чего из перечисленного полностью электрический автомобиль не выделяет при движении?~Which of these does an all-electric car not emit while driving?',choices='Выхлопные газы~Tailpipe exhaust gases;Шум шин~Tyre noise;Тепло от компонентов~Heat from components;Звук электромотора~Motor noise')
# Use actual fellow nominees, not films that had not been released at the time.
nominee_ru=[
['Лучше не бывает','Мужской стриптиз','Умница Уилл Хантинг'],
['Трудности перевода','Хозяин морей: На краю Земли','Таинственная река'],
['Четыре свадьбы и одни похороны','Криминальное чтиво','Телевикторина'],
['Шоколад','Крадущийся тигр, затаившийся дракон','Эрин Брокович'],
['Беглец','Во имя отца','Пианино'],
['Кабаре','Избавление','Эмигранты'],
['По ком звонит колокол','Небеса могут подождать','Человеческая комедия'],
['Дорогая','Доктор Живаго','Корабль дураков'],
['Весь этот джаз','Апокалипсис сегодня','Уходя в отрыв'],
['Дети меньшего бога','Ханна и её сёстры','Миссия'],
['Джон Синглтон','Барри Левинсон','Оливер Стоун'],
['Джоэл Коэн','Милош Форман','Майк Ли'],
['Дэвид Финчер','Рон Ховард','Гас Ван Сент'],
['Александр Пэйн','Мартин Скорсезе','Вуди Аллен'],
['Ричард Линклейтер','Беннетт Миллер','Уэс Андерсон'],
['Дени Вильнёв','Мел Гибсон','Кеннет Лонерган'],
['Кристофер Нолан','Джордан Пил','Грета Гервиг'],
['Спайк Ли','Павел Павликовский','Йоргос Лантимос'],
['Мартин Скорсезе','Тодд Филлипс','Сэм Мендес'],
['Даррен Аронофски','Дэвид О. Расселл','Дэвид Финчер']]
nominees=json.loads((ROOT/'authoring/expansion_20261108.oscar-nominees.json').read_text())
for item,ru in zip(nominees,nominee_ru):
    q=next(q for q in OUT if q['id']==f"cinema_nov08_{item['year']}")
    first=q['options'][0]
    choices=first['ru']+'~'+first['en']+';'+(';'.join(r+'~'+e for r,e in zip(ru,item['distractors'])))
    edit('cinema',str(item['year']),choices=choices,location=item['category']+' / Winner and Nominees; Directing / Winner; Best Picture / Winner')
    EVIDENCE[q['id']]['nomineeRecord']=item
for old,new in [('pitch','improvisation'),('timbre','sousaphone'),('verse','shostakovich')]:
    oldid='music_nov08_'+old; newid='music_nov08_'+new
    next(q for q in OUT if q['id']==oldid)['id']=newid
    EVIDENCE[newid]=EVIDENCE.pop(oldid)
edit('food','cooked_white',choices='Белковые молекулы разворачиваются и связываются в сеть~Protein molecules unfold and link into a network;Кристаллизуются растворённые соли~Dissolved salts crystallise;Происходит клейстеризация крахмала~Starch undergoes gelatinisation;Кристаллизуются жиры~Fats crystallise')
edit('food','leavener',choices='Газ образуется в химической реакции~Gas is produced by a chemical reaction;Газ образуют молочнокислые бактерии~Lactic acid bacteria produce the gas;Пузырьки появляются только при кипении воды~Bubbles appear only as water boils;Расширяется только воздух, внесённый при замешивании~Only air incorporated during mixing expands')
edit('television','sesame_count',prompt='Какое занятие особенно любит Граф из «Улицы Сезам»?~Which activity does Sesame Street\'s Count von Count especially enjoy?')
