-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: geo
-- ------------------------------------------------------
-- Server version	5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `border_info`
--

DROP TABLE IF EXISTS `border_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `border_info` (
  `state_name` text,
  `border` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `border_info`
--

LOCK TABLES `border_info` WRITE;
/*!40000 ALTER TABLE `border_info` DISABLE KEYS */;
INSERT INTO `border_info` VALUES ('alabama','tennessee'),('alabama','georgia'),('alabama','florida'),('alabama','mississippi'),('arizona','utah'),('arizona','colorado'),('arizona','new mexico'),('arizona','california'),('arizona','nevada'),('arkansas','missouri'),('arkansas','tennessee'),('arkansas','mississippi'),('arkansas','louisiana'),('arkansas','texas'),('arkansas','oklahoma'),('california','oregon'),('california','nevada'),('california','arizona'),('colorado','nebraska'),('colorado','kansas'),('colorado','oklahoma'),('colorado','new mexico'),('colorado','arizona'),('colorado','utah'),('colorado','wyoming'),('connecticut','massachusetts'),('connecticut','rhode island'),('connecticut','new york'),('delaware','pennsylvania'),('delaware','new jersey'),('delaware','maryland'),('district of columbia','maryland'),('district of columbia','virginia'),('florida','georgia'),('florida','alabama'),('georgia','north carolina'),('georgia','south carolina'),('georgia','florida'),('georgia','alabama'),('georgia','tennessee'),('idaho','montana'),('idaho','wyoming'),('idaho','utah'),('idaho','nevada'),('idaho','oregon'),('idaho','washington'),('illinois','wisconsin'),('illinois','indiana'),('illinois','kentucky'),('illinois','missouri'),('illinois','iowa'),('indiana','michigan'),('indiana','ohio'),('indiana','kentucky'),('indiana','illinois'),('iowa','minnesota'),('iowa','wisconsin'),('iowa','illinois'),('iowa','missouri'),('iowa','nebraska'),('iowa','south dakota'),('kansas','nebraska'),('kansas','missouri'),('kansas','oklahoma'),('kansas','colorado'),('kentucky','indiana'),('kentucky','ohio'),('kentucky','west virginia'),('kentucky','virginia'),('kentucky','tennessee'),('kentucky','missouri'),('kentucky','illinois'),('louisiana','arkansas'),('louisiana','mississippi'),('louisiana','texas'),('maine','new hampshire'),('maryland','pennsylvania'),('maryland','delaware'),('maryland','virginia'),('maryland','district of columbia'),('maryland','west virginia'),('massachusetts','new hampshire'),('massachusetts','rhode island'),('massachusetts','connecticut'),('massachusetts','new york'),('massachusetts','vermont'),('michigan','ohio'),('michigan','indiana'),('michigan','wisconsin'),('minnesota','wisconsin'),('minnesota','iowa'),('minnesota','south dakota'),('minnesota','north dakota'),('mississippi','tennessee'),('mississippi','alabama'),('mississippi','louisiana'),('mississippi','arkansas'),('missouri','iowa'),('missouri','illinois'),('missouri','kentucky'),('missouri','tennessee'),('missouri','arkansas'),('missouri','oklahoma'),('missouri','kansas'),('missouri','nebraska'),('montana','north dakota'),('montana','south dakota'),('montana','wyoming'),('montana','idaho'),('nebraska','south dakota'),('nebraska','iowa'),('nebraska','missouri'),('nebraska','kansas'),('nebraska','colorado'),('nebraska','wyoming'),('nevada','idaho'),('nevada','utah'),('nevada','arizona'),('nevada','california'),('nevada','oregon'),('new hampshire','maine'),('new hampshire','massachusetts'),('new hampshire','vermont'),('new jersey','new york'),('new jersey','delaware'),('new jersey','pennsylvania'),('new mexico','colorado'),('new mexico','oklahoma'),('new mexico','texas'),('new mexico','arizona'),('new mexico','utah'),('new york','vermont'),('new york','massachusetts'),('new york','connecticut'),('new york','new jersey'),('new york','pennsylvania'),('north carolina','virginia'),('north carolina','south carolina'),('north carolina','georgia'),('north carolina','tennessee'),('north dakota','minnesota'),('north dakota','south dakota'),('north dakota','montana'),('ohio','michigan'),('ohio','pennsylvania'),('ohio','west virginia'),('ohio','kentucky'),('ohio','indiana'),('oklahoma','kansas'),('oklahoma','missouri'),('oklahoma','arkansas'),('oklahoma','texas'),('oklahoma','new mexico'),('oklahoma','colorado'),('oregon','washington'),('oregon','idaho'),('oregon','nevada'),('oregon','california'),('pennsylvania','new york'),('pennsylvania','new jersey'),('pennsylvania','delaware'),('pennsylvania','maryland'),('pennsylvania','west virginia'),('pennsylvania','ohio'),('rhode island','massachusetts'),('rhode island','connecticut'),('south carolina','north carolina'),('south carolina','georgia'),('south dakota','north dakota'),('south dakota','minnesota'),('south dakota','iowa'),('south dakota','nebraska'),('south dakota','wyoming'),('south dakota','montana'),('tennessee','kentucky'),('tennessee','virginia'),('tennessee','north carolina'),('tennessee','georgia'),('tennessee','alabama'),('tennessee','mississippi'),('tennessee','arkansas'),('tennessee','missouri'),('texas','oklahoma'),('texas','arkansas'),('texas','louisiana'),('texas','new mexico'),('utah','wyoming'),('utah','colorado'),('utah','new mexico'),('utah','arizona'),('utah','nevada'),('utah','idaho'),('vermont','new hampshire'),('vermont','massachusetts'),('vermont','new york'),('virginia','maryland'),('virginia','district of columbia'),('virginia','north carolina'),('virginia','tennessee'),('virginia','kentucky'),('virginia','west virginia'),('washington','idaho'),('washington','oregon'),('west virginia','pennsylvania'),('west virginia','maryland'),('west virginia','virginia'),('west virginia','kentucky'),('west virginia','ohio'),('wisconsin','michigan'),('wisconsin','illinois'),('wisconsin','iowa'),('wisconsin','minnesota'),('wyoming','montana'),('wyoming','south dakota'),('wyoming','nebraska'),('wyoming','colorado'),('wyoming','utah'),('wyoming','idaho');
/*!40000 ALTER TABLE `border_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `city_name` text,
  `population` int(11) DEFAULT NULL,
  `country_name` varchar(3) NOT NULL DEFAULT '',
  `state_name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES ('birmingham',284413,'usa','alabama'),('mobile',200452,'usa','alabama'),('montgomery',177857,'usa','alabama'),('huntsville',142513,'usa','alabama'),('tuscaloosa',75143,'usa','alabama'),('anchorage',174431,'usa','alaska'),('phoenix',789704,'usa','arizona'),('tucson',330537,'usa','arizona'),('mesa',152453,'usa','arizona'),('tempe',106919,'usa','arizona'),('glendale',96988,'usa','arizona'),('scottsdale',88622,'usa','arizona'),('little rock',158915,'usa','arkansas'),('fort smith',71384,'usa','arkansas'),('north little rock',64388,'usa','arkansas'),('los angeles',2966850,'usa','california'),('san diego',875538,'usa','california'),('san francisco',678974,'usa','california'),('san jose',629442,'usa','california'),('long beach',361334,'usa','california'),('oakland',339337,'usa','california'),('sacramento',275741,'usa','california'),('anaheim',219311,'usa','california'),('fresno',218202,'usa','california'),('santa ana',203713,'usa','california'),('riverside',170876,'usa','california'),('huntington beach',170505,'usa','california'),('stockton',149779,'usa','california'),('glendale',139060,'usa','california'),('fremont',131945,'usa','california'),('torrance',131497,'usa','california'),('garden grove',123351,'usa','california'),('san bernardino',118794,'usa','california'),('pasadena',118072,'usa','california'),('east los angeles',110017,'usa','california'),('oxnard',108195,'usa','california'),('modesto',106963,'usa','california'),('sunnyvale',106618,'usa','california'),('bakersfield',105611,'usa','california'),('concord',103763,'usa','california'),('berkeley',103328,'usa','california'),('fullerton',102246,'usa','california'),('inglewood',94162,'usa','california'),('hayward',93585,'usa','california'),('pomona',92742,'usa','california'),('orange',91450,'usa','california'),('ontario',88820,'usa','california'),('santa monica',88314,'usa','california'),('santa clara',87700,'usa','california'),('citrus heights',85911,'usa','california'),('norwalk',84901,'usa','california'),('burbank',84625,'usa','california'),('chula vista',83927,'usa','california'),('santa rosa',83205,'usa','california'),('downey',82602,'usa','california'),('costa mesa',82291,'usa','california'),('compton',81230,'usa','california'),('carson',81221,'usa','california'),('salinas',80479,'usa','california'),('west covina',80292,'usa','california'),('vallejo',80188,'usa','california'),('el monte',79494,'usa','california'),('daly city',78519,'usa','california'),('thousand oaks',77797,'usa','california'),('san mateo',77640,'usa','california'),('simi valley',77500,'usa','california'),('oceanside',76698,'usa','california'),('richmond',74676,'usa','california'),('lakewood',74654,'usa','california'),('santa barbara',74542,'usa','california'),('el cajon',73892,'usa','california'),('ventura',73774,'usa','california'),('westminster',71133,'usa','california'),('whittier',68558,'usa','california'),('south gate',66784,'usa','california'),('alhambra',64767,'usa','california'),('buena park',64165,'usa','california'),('san leandro',63952,'usa','california'),('alameda',63852,'usa','california'),('newport beach',63475,'usa','california'),('escondido',62480,'usa','california'),('irvine',62134,'usa','california'),('mountain view',58655,'usa','california'),('fairfield',58099,'usa','california'),('redondo beach',57102,'usa','california'),('scotts valley',6037,'usa','california'),('denver',492365,'usa','colorado'),('colorado springs',215150,'usa','colorado'),('aurora',158588,'usa','colorado'),('lakewood',113808,'usa','colorado'),('pueblo',101686,'usa','colorado'),('arvada',84576,'usa','colorado'),('boulder',76685,'usa','colorado'),('fort collins',64632,'usa','colorado'),('bridgeport',142546,'usa','connecticut'),('hartford',136392,'usa','connecticut'),('new haven',126089,'usa','connecticut'),('waterbury',103266,'usa','connecticut'),('stamford',102466,'usa','connecticut'),('norwalk',77767,'usa','connecticut'),('new britain',73840,'usa','connecticut'),('west hartford',61301,'usa','connecticut'),('danbury',60470,'usa','connecticut'),('greenwich',59578,'usa','connecticut'),('bristol',57370,'usa','connecticut'),('meriden',57118,'usa','connecticut'),('wilmington',70195,'usa','delaware'),('washington',638333,'usa','district of columbia'),('jacksonville',540920,'usa','florida'),('miami',346865,'usa','florida'),('tampa',271523,'usa','florida'),('st. petersburg',238647,'usa','florida'),('fort lauderdale',153256,'usa','florida'),('orlando',128394,'usa','florida'),('hollywood',117188,'usa','florida'),('miami beach',96298,'usa','florida'),('clearwater',85450,'usa','florida'),('tallahassee',81548,'usa','florida'),('gainesville',81371,'usa','florida'),('kendall',73758,'usa','florida'),('west palm beach',62530,'usa','florida'),('largo',58977,'usa','florida'),('pensacola',57619,'usa','florida'),('atlanta',425022,'usa','georgia'),('columbus',169441,'usa','georgia'),('savannah',141654,'usa','georgia'),('macon',116860,'usa','georgia'),('albany',74425,'usa','georgia'),('honolulu',762874,'usa','hawaii'),('ewa',190037,'usa','hawaii'),('koolaupoko',109373,'usa','hawaii'),('boise',102249,'usa','idaho'),('chicago',3005172,'usa','illinois'),('rockford',139712,'usa','illinois'),('peoria',124160,'usa','illinois'),('springfield',100054,'usa','illinois'),('decatur',93939,'usa','illinois'),('aurora',81293,'usa','illinois'),('joliet',77956,'usa','illinois'),('evanston',73706,'usa','illinois'),('waukegan',67653,'usa','illinois'),('arlington heights',66116,'usa','illinois'),('elgin',63668,'usa','illinois'),('cicero',61232,'usa','illinois'),('oak lawn',60590,'usa','illinois'),('skokie',60278,'usa','illinois'),('champaign',58267,'usa','illinois'),('indianapolis',700807,'usa','indiana'),('fort wayne',172196,'usa','indiana'),('gary',151968,'usa','indiana'),('evansville',130496,'usa','indiana'),('south bend',109727,'usa','indiana'),('hammond',93714,'usa','indiana'),('muncie',77216,'usa','indiana'),('anderson',64695,'usa','indiana'),('terre haute',61125,'usa','indiana'),('des moines',191003,'usa','iowa'),('cedar rapids',110243,'usa','iowa'),('davenport',103254,'usa','iowa'),('sioux city',82003,'usa','iowa'),('waterloo',75985,'usa','iowa'),('dubuque',62321,'usa','iowa'),('wichita',279212,'usa','kansas'),('kansas city',161148,'usa','kansas'),('topeka',118690,'usa','kansas'),('overland park',81784,'usa','kansas'),('louisville',298451,'usa','kentucky'),('lexington',204165,'usa','kentucky'),('new orleans',557515,'usa','louisiana'),('baton rouge',219419,'usa','louisiana'),('shreveport',205820,'usa','louisiana'),('metairie',164160,'usa','louisiana'),('lafayette',80584,'usa','louisiana'),('lake charles',75051,'usa','louisiana'),('kenner',66382,'usa','louisiana'),('monroe',57597,'usa','louisiana'),('portland',61572,'usa','maine'),('baltimore',786775,'usa','maryland'),('silver spring',72893,'usa','maryland'),('dundalk',71293,'usa','maryland'),('bethesda',63022,'usa','maryland'),('boston',562994,'usa','massachusetts'),('worcester',161799,'usa','massachusetts'),('springfield',152319,'usa','massachusetts'),('new bedford',98478,'usa','massachusetts'),('cambridge',95322,'usa','massachusetts'),('brockton',95172,'usa','massachusetts'),('fall river',92574,'usa','massachusetts'),('lowell',92418,'usa','massachusetts'),('quincy',84743,'usa','massachusetts'),('newton',83622,'usa','massachusetts'),('lynn',78471,'usa','massachusetts'),('somerville',77372,'usa','massachusetts'),('framingham',65113,'usa','massachusetts'),('lawrence',63175,'usa','massachusetts'),('waltham',58200,'usa','massachusetts'),('medford',58076,'usa','massachusetts'),('detroit',1203339,'usa','michigan'),('grand rapids',181843,'usa','michigan'),('warren',161134,'usa','michigan'),('flint',159611,'usa','michigan'),('lansing',130414,'usa','michigan'),('sterling heights',108999,'usa','michigan'),('ann arbor',107969,'usa','michigan'),('livonia',104814,'usa','michigan'),('dearborn',90660,'usa','michigan'),('westland',84603,'usa','michigan'),('kalamazoo',79722,'usa','michigan'),('taylor',77568,'usa','michigan'),('saginaw',77508,'usa','michigan'),('pontiac',76715,'usa','michigan'),('st. clair shores',76210,'usa','michigan'),('southfield',75568,'usa','michigan'),('clinton',72400,'usa','michigan'),('royal oak',70893,'usa','michigan'),('dearborn heights',67706,'usa','michigan'),('troy',67102,'usa','michigan'),('waterford',64250,'usa','michigan'),('wyoming',59616,'usa','michigan'),('redford',58441,'usa','michigan'),('farmington hills',58056,'usa','michigan'),('minneapolis',370951,'usa','minnesota'),('st. paul',270230,'usa','minnesota'),('duluth',92811,'usa','minnesota'),('bloomington',81831,'usa','minnesota'),('rochester',57906,'usa','minnesota'),('jackson',202895,'usa','mississippi'),('st. louis',453085,'usa','missouri'),('kansas city',448159,'usa','missouri'),('springfield',133116,'usa','missouri'),('independence',111797,'usa','missouri'),('st. joseph',76691,'usa','missouri'),('columbia',62061,'usa','missouri'),('billings',66842,'usa','montana'),('great falls',56725,'usa','montana'),('omaha',314255,'usa','nebraska'),('lincoln',171932,'usa','nebraska'),('las vegas',164674,'usa','nevada'),('reno',100756,'usa','nevada'),('manchester',90936,'usa','new hampshire'),('nashua',67865,'usa','new hampshire'),('newark',329248,'usa','new jersey'),('jersey city',223532,'usa','new jersey'),('paterson',137970,'usa','new jersey'),('elizabeth',106201,'usa','new jersey'),('trenton',92124,'usa','new jersey'),('woodbridge',90074,'usa','new jersey'),('camden',84910,'usa','new jersey'),('east orange',77878,'usa','new jersey'),('clifton',74388,'usa','new jersey'),('edison',70193,'usa','new jersey'),('cherry hill',68785,'usa','new jersey'),('bayonne',65047,'usa','new jersey'),('middletown',61615,'usa','new jersey'),('irvington',61493,'usa','new jersey'),('albuquerque',331767,'usa','new mexico'),('new york',7071639,'usa','new york'),('buffalo',357870,'usa','new york'),('rochester',241741,'usa','new york'),('yonkers',195351,'usa','new york'),('syracuse',170105,'usa','new york'),('albany',101727,'usa','new york'),('cheektowaga',92145,'usa','new york'),('utica',75632,'usa','new york'),('niagara falls',71384,'usa','new york'),('new rochelle',70794,'usa','new york'),('schenectady',67972,'usa','new york'),('mount vernon',66713,'usa','new york'),('irondequoit',57648,'usa','new york'),('levittown',57045,'usa','new york'),('charlotte',314447,'usa','north carolina'),('greensboro',155642,'usa','north carolina'),('raleigh',149771,'usa','north carolina'),('winston-salem',131885,'usa','north carolina'),('durham',100538,'usa','north carolina'),('high point',64107,'usa','north carolina'),('fayetteville',59507,'usa','north carolina'),('fargo',61308,'usa','north dakota'),('cleveland',573822,'usa','ohio'),('columbus',564871,'usa','ohio'),('cincinnati',385457,'usa','ohio'),('toledo',354635,'usa','ohio'),('akron',237177,'usa','ohio'),('dayton',203371,'usa','ohio'),('youngstown',115436,'usa','ohio'),('canton',93077,'usa','ohio'),('parma',92548,'usa','ohio'),('lorain',75416,'usa','ohio'),('springfield',72563,'usa','ohio'),('hamilton',63189,'usa','ohio'),('lakewood',61963,'usa','ohio'),('kettering',61186,'usa','ohio'),('euclid',59999,'usa','ohio'),('elyria',57504,'usa','ohio'),('oklahoma city',403213,'usa','oklahoma'),('tulsa',360919,'usa','oklahoma'),('lawton',80054,'usa','oklahoma'),('norman',68020,'usa','oklahoma'),('portland',366383,'usa','oregon'),('eugene',105664,'usa','oregon'),('salem',89233,'usa','oregon'),('philadelphia',1688210,'usa','pennsylvania'),('pittsburgh',423938,'usa','pennsylvania'),('erie',119123,'usa','pennsylvania'),('allentown',103758,'usa','pennsylvania'),('scranton',88117,'usa','pennsylvania'),('upper darby',84054,'usa','pennsylvania'),('reading',78686,'usa','pennsylvania'),('bethlehem',70419,'usa','pennsylvania'),('lower merion',59651,'usa','pennsylvania'),('abingdon',59084,'usa','pennsylvania'),('bristol township',58733,'usa','pennsylvania'),('penn hills',57632,'usa','pennsylvania'),('altoona',57078,'usa','pennsylvania'),('providence',156804,'usa','rhode island'),('warwick',87123,'usa','rhode island'),('cranston',71992,'usa','rhode island'),('pawtucket',71204,'usa','rhode island'),('columbia',101229,'usa','south carolina'),('charleston',69855,'usa','south carolina'),('north charleston',62504,'usa','south carolina'),('greenville',58242,'usa','south carolina'),('sioux falls',81343,'usa','south dakota'),('memphis',646356,'usa','tennessee'),('nashville',455651,'usa','tennessee'),('knoxville',175030,'usa','tennessee'),('chattanooga',169728,'usa','tennessee'),('houston',1595138,'usa','texas'),('dallas',904078,'usa','texas'),('san antonio',785880,'usa','texas'),('el paso',425259,'usa','texas'),('fort worth',385164,'usa','texas'),('austin',345496,'usa','texas'),('corpus christi',231999,'usa','texas'),('lubbock',173979,'usa','texas'),('arlington',160123,'usa','texas'),('amarillo',149230,'usa','texas'),('garland',138857,'usa','texas'),('beaumont',118102,'usa','texas'),('pasadena',112560,'usa','texas'),('irving',109943,'usa','texas'),('waco',101261,'usa','texas'),('abilene',98315,'usa','texas'),('wichita falls',94201,'usa','texas'),('laredo',91449,'usa','texas'),('odessa',90027,'usa','texas'),('brownsville',84997,'usa','texas'),('san angelo',73240,'usa','texas'),('richardson',72496,'usa','texas'),('plano',72331,'usa','texas'),('grand prairie',71462,'usa','texas'),('midland',70525,'usa','texas'),('tyler',70508,'usa','texas'),('mesquite',67053,'usa','texas'),('mcallen',67042,'usa','texas'),('longview',62762,'usa','texas'),('port arthur',61195,'usa','texas'),('salt lake city',163034,'usa','utah'),('provo',74111,'usa','utah'),('west valley',72299,'usa','utah'),('ogden',64407,'usa','utah'),('norfolk',266979,'usa','virginia'),('virginia beach',262199,'usa','virginia'),('richmond',219214,'usa','virginia'),('arlington',152599,'usa','virginia'),('newport news',144903,'usa','virginia'),('hampton',122617,'usa','virginia'),('chesapeake',114226,'usa','virginia'),('portsmouth',104577,'usa','virginia'),('alexandria',103217,'usa','virginia'),('roanoke',100427,'usa','virginia'),('lynchburg',66743,'usa','virginia'),('seattle',493846,'usa','washington'),('spokane',171300,'usa','washington'),('tacoma',158501,'usa','washington'),('bellevue',73903,'usa','washington'),('charleston',63968,'usa','west virginia'),('huntington',63684,'usa','west virginia'),('milwaukee',636212,'usa','wisconsin'),('madison',170616,'usa','wisconsin'),('green bay',87899,'usa','wisconsin'),('racine',85725,'usa','wisconsin'),('kenosha',77685,'usa','wisconsin'),('west allis',63982,'usa','wisconsin'),('appleton',58913,'usa','wisconsin'),('casper',51016,'usa','wyoming');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `highlow`
--

DROP TABLE IF EXISTS `highlow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `highlow` (
  `state_name` text,
  `highest_elevation` int(11),
  `lowest_point` text,
  `highest_point` text,
  `lowest_elevation` int(11)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `highlow`
--

LOCK TABLES `highlow` WRITE;
/*!40000 ALTER TABLE `highlow` DISABLE KEYS */;
INSERT INTO `highlow` VALUES ('alabama',734,'gulf of mexico','cheaha mountain',0),('alaska',6194,'pacific ocean','mount mckinley',0),('arizona',3851,'colorado river','humphreys peak',21),('arkansas',839,'ouachita river','magazine mountain',17),('california',4418,'death valley','mount whitney',-85),('colorado',4399,'arkansas river','mount elbert',1021),('connecticut',725,'long island sound','mount frissell',0),('delaware',135,'atlantic ocean','centerville',0),('district of columbia',125,'potomac river','tenleytown',0),('florida',105,'atlantic ocean','walton county',0),('georgia',1458,'atlantic ocean','brasstown bald',0),('hawaii',4205,'pacific ocean','mauna kea',0),('idaho',3859,'snake river','borah peak',216),('illinois',376,'mississippi river','charles mound',85),('indiana',383,'ohio river','franklin township',98),('iowa',511,'mississippi river','ocheyedan mound',146),('kansas',1231,'verdigris river','mount sunflower',207),('kentucky',1263,'mississippi river','black mountain',78),('louisiana',163,'new orleans','driskill mountain',-1),('maine',1606,'atlantic ocean','mount katahdin',0),('maryland',1024,'atlantic ocean','backbone mountain',0),('massachusetts',1064,'atlantic ocean','mount greylock',0),('michigan',604,'lake erie','mount curwood',174),('minnesota',701,'lake superior','eagle mountain',183),('mississippi',246,'gulf of mexico','woodall mountain',0),('missouri',540,'st. francis river','taum sauk mountain',70),('montana',3901,'kootenai river','granite peak',549),('nebraska',1654,'southeast corner','johnson township',256),('nevada',4005,'colorado river','boundary peak',143),('new hampshire',1917,'atlantic ocean','mount washington',0),('new jersey',550,'atlantic ocean','high point',0),('new mexico',4011,'red bluff reservoir','wheeler peak',859),('new york',1629,'atlantic ocean','mount marcy',0),('north carolina',2037,'atlantic ocean','mount mitchell',0),('north dakota',1069,'red river','white butte',229),('ohio',472,'ohio river','campbell hill',132),('oklahoma',1516,'little river','black mesa',87),('oregon',3424,'pacific ocean','mount hood',0),('pennsylvania',979,'delaware river','mount davis',0),('rhode island',247,'atlantic ocean','jerimoth hill',0),('south carolina',1085,'atlantic ocean','sassafras mountain',0),('south dakota',2207,'big stone lake','harney peak',284),('tennessee',2025,'mississippi river','clingmans dome',55),('texas',2667,'gulf of mexico','guadalupe peak',0),('utah',4123,'beaver dam creek','kings peak',610),('vermont',1339,'lake champlain','mount mansfield',29),('virginia',1746,'atlantic ocean','mount rogers',0),('washington',4392,'pacific ocean','mount rainier',0),('west virginia',1482,'potomac river','spruce knob',73),('wisconsin',595,'lake michigan','timms hill',177),('wyoming',4202,'belle fourche river','gannett peak',945);
/*!40000 ALTER TABLE `highlow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lake`
--

DROP TABLE IF EXISTS `lake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lake` (
  `lake_name` text,
  `area` double DEFAULT NULL,
  `country_name` varchar(3) NOT NULL DEFAULT '',
  `state_name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lake`
--

LOCK TABLES `lake` WRITE;
/*!40000 ALTER TABLE `lake` DISABLE KEYS */;
INSERT INTO `lake` VALUES ('iliamna',2675,'usa','alaska'),('becharof',1186,'usa','alaska'),('teshekpuk',816,'usa','alaska'),('naknek',630,'usa','alaska'),('salton sea',932,'usa','california'),('tahoe',497,'usa','california'),('okeechobee',1810,'usa','florida'),('michigan',58016,'usa','illinois'),('michigan',58016,'usa','indiana'),('pontchartrain',1632,'usa','louisiana'),('superior',82362,'usa','michigan'),('huron',59570,'usa','michigan'),('michigan',58016,'usa','michigan'),('erie',25667,'usa','michigan'),('st. clair',1119,'usa','michigan'),('superior',82362,'usa','minnesota'),('lake of the woods',4391,'usa','minnesota'),('red',1169,'usa','minnesota'),('rainy',932,'usa','minnesota'),('mille lacs',536,'usa','minnesota'),('flathead',510,'usa','montana'),('tahoe',497,'usa','nevada'),('erie',25667,'usa','new york'),('ontario',19684,'usa','new york'),('champlain',1114,'usa','new york'),('erie',25667,'usa','ohio'),('erie',25667,'usa','pennsylvania'),('great salt lake',5180,'usa','utah'),('champlain',1114,'usa','vermont'),('superior',82362,'usa','wisconsin'),('michigan',58016,'usa','wisconsin'),('winnebago',557,'usa','wisconsin');
/*!40000 ALTER TABLE `lake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mountain`
--

DROP TABLE IF EXISTS `mountain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mountain` (
  `mountain_name` text,
  `mountain_altitude` int(11) DEFAULT NULL,
  `country_name` varchar(3) NOT NULL DEFAULT '',
  `state_name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mountain`
--

LOCK TABLES `mountain` WRITE;
/*!40000 ALTER TABLE `mountain` DISABLE KEYS */;
INSERT INTO `mountain` VALUES ('mckinley',6194,'usa','alaska'),('st. elias',5489,'usa','alaska'),('foraker',5304,'usa','alaska'),('bona',5044,'usa','alaska'),('blackburn',4996,'usa','alaska'),('kennedy',4964,'usa','alaska'),('sanford',4949,'usa','alaska'),('south buttress',4842,'usa','alaska'),('vancouver',4785,'usa','alaska'),('churchill',4766,'usa','alaska'),('fairweather',4663,'usa','alaska'),('hubbard',4577,'usa','alaska'),('bear',4520,'usa','alaska'),('east buttress',4490,'usa','alaska'),('hunter',4442,'usa','alaska'),('alverstone',4439,'usa','alaska'),('browne tower',4429,'usa','alaska'),('wrangell',4317,'usa','alaska'),('whitney',4418,'usa','california'),('williamson',4382,'usa','california'),('white',4342,'usa','california'),('north palisade',4341,'usa','california'),('shasta',4317,'usa','california'),('sill',4317,'usa','california'),('elbert',4399,'usa','colorado'),('massive',4396,'usa','colorado'),('harvard',4395,'usa','colorado'),('bianca',4372,'usa','colorado'),('la plata',4370,'usa','colorado'),('uncompahgre',4361,'usa','colorado'),('crestone',4357,'usa','colorado'),('lincoln',4354,'usa','colorado'),('grays',4349,'usa','colorado'),('antero',4349,'usa','colorado'),('torreys',4349,'usa','colorado'),('castle',4348,'usa','colorado'),('quandary',4348,'usa','colorado'),('evans',4348,'usa','colorado'),('longs',4345,'usa','colorado'),('wilson',4342,'usa','colorado'),('shavano',4337,'usa','colorado'),('belford',4327,'usa','colorado'),('princeton',4327,'usa','colorado'),('crestone needle',4327,'usa','colorado'),('yale',4327,'usa','colorado'),('bross',4320,'usa','colorado'),('kit carson',4317,'usa','colorado'),('el diente',4316,'usa','colorado'),('maroon',4315,'usa','colorado'),('rainier',4392,'usa','washington');
/*!40000 ALTER TABLE `mountain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `river`
--

DROP TABLE IF EXISTS `river`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `river` (
  `river_name` text,
  `length` int(11) DEFAULT NULL,
  `country_name` varchar(3) NOT NULL DEFAULT '',
  `traverse` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `river`
--

LOCK TABLES `river` WRITE;
/*!40000 ALTER TABLE `river` DISABLE KEYS */;
INSERT INTO `river` VALUES ('mississippi',3778,'usa','minnesota'),('mississippi',3778,'usa','wisconsin'),('mississippi',3778,'usa','iowa'),('mississippi',3778,'usa','illinois'),('mississippi',3778,'usa','missouri'),('mississippi',3778,'usa','kentucky'),('mississippi',3778,'usa','tennessee'),('mississippi',3778,'usa','arkansas'),('mississippi',3778,'usa','mississippi'),('mississippi',3778,'usa','louisiana'),('missouri',3968,'usa','montana'),('missouri',3968,'usa','north dakota'),('missouri',3968,'usa','south dakota'),('missouri',3968,'usa','iowa'),('missouri',3968,'usa','nebraska'),('missouri',3968,'usa','missouri'),('colorado',2333,'usa','colorado'),('colorado',2333,'usa','utah'),('colorado',2333,'usa','arizona'),('colorado',2333,'usa','nevada'),('colorado',2333,'usa','california'),('ohio',1569,'usa','pennsylvania'),('ohio',1569,'usa','west virginia'),('ohio',1569,'usa','kentucky'),('ohio',1569,'usa','indiana'),('ohio',1569,'usa','illinois'),('ohio',1569,'usa','ohio'),('red',1638,'usa','new mexico'),('red',1638,'usa','texas'),('red',1638,'usa','oklahoma'),('red',1638,'usa','arkansas'),('red',1638,'usa','louisiana'),('arkansas',2333,'usa','colorado'),('arkansas',2333,'usa','kansas'),('arkansas',2333,'usa','oklahoma'),('arkansas',2333,'usa','arkansas'),('canadian',1458,'usa','colorado'),('canadian',1458,'usa','new mexico'),('canadian',1458,'usa','texas'),('canadian',1458,'usa','oklahoma'),('connecticut',655,'usa','new hampshire'),('connecticut',655,'usa','vermont'),('connecticut',655,'usa','massachusetts'),('connecticut',655,'usa','connecticut'),('delaware',451,'usa','new york'),('delaware',451,'usa','pennsylvania'),('delaware',451,'usa','new jersey'),('delaware',451,'usa','delaware'),('little missouri',901,'usa','wyoming'),('little missouri',901,'usa','montana'),('little missouri',901,'usa','south dakota'),('little missouri',901,'usa','north dakota'),('snake',1670,'usa','wyoming'),('snake',1670,'usa','idaho'),('snake',1670,'usa','oregon'),('snake',1670,'usa','washington'),('chattahoochee',702,'usa','georgia'),('chattahoochee',702,'usa','florida'),('cimarron',965,'usa','new mexico'),('cimarron',965,'usa','kansas'),('cimarron',965,'usa','oklahoma'),('green',1175,'usa','wyoming'),('green',1175,'usa','utah'),('green',1175,'usa','colorado'),('north platte',1094,'usa','colorado'),('north platte',1094,'usa','wyoming'),('north platte',1094,'usa','nebraska'),('potomac',462,'usa','west virginia'),('potomac',462,'usa','maryland'),('potomac',462,'usa','virginia'),('potomac',462,'usa','district of columbia'),('republican',679,'usa','colorado'),('republican',679,'usa','nebraska'),('republican',679,'usa','kansas'),('rio grande',3033,'usa','colorado'),('rio grande',3033,'usa','new mexico'),('rio grande',3033,'usa','texas'),('san juan',579,'usa','colorado'),('san juan',579,'usa','new mexico'),('san juan',579,'usa','utah'),('tennessee',1049,'usa','tennessee'),('tennessee',1049,'usa','alabama'),('tennessee',1049,'usa','kentucky'),('wabash',764,'usa','ohio'),('wabash',764,'usa','indiana'),('wabash',764,'usa','illinois'),('yellowstone',1080,'usa','wyoming'),('yellowstone',1080,'usa','montana'),('yellowstone',1080,'usa','north dakota'),('allegheny',523,'usa','pennsylvania'),('allegheny',523,'usa','new york'),('bighorn',541,'usa','wyoming'),('bighorn',541,'usa','montana'),('cheyenne',848,'usa','wyoming'),('cheyenne',848,'usa','north dakota'),('clark fork',483,'usa','montana'),('clark fork',483,'usa','idaho'),('columbia',1953,'usa','washington'),('columbia',1953,'usa','oregon'),('cumberland',1105,'usa','kentucky'),('cumberland',1105,'usa','tennessee'),('dakota',1142,'usa','north dakota'),('dakota',1142,'usa','south dakota'),('gila',805,'usa','new mexico'),('gila',805,'usa','arizona'),('hudson',492,'usa','new york'),('hudson',492,'usa','new jersey'),('neosho',740,'usa','kansas'),('neosho',740,'usa','oklahoma'),('niobrara',693,'usa','wyoming'),('niobrara',693,'usa','nebraska'),('ouachita',973,'usa','arkansas'),('ouachita',973,'usa','louisiana'),('pearl',788,'usa','michigan'),('pearl',788,'usa','louisiana'),('pecos',805,'usa','new mexico'),('pecos',805,'usa','texas'),('powder',603,'usa','wyoming'),('powder',603,'usa','montana'),('roanoke',660,'usa','virginia'),('roanoke',660,'usa','north carolina'),('rock',459,'usa','wisconsin'),('rock',459,'usa','illinois'),('smoky hill',869,'usa','colorado'),('smoky hill',869,'usa','kansas'),('south platte',682,'usa','colorado'),('south platte',682,'usa','nebraska'),('st. francis',684,'usa','missouri'),('st. francis',684,'usa','arkansas'),('tombigbee',658,'usa','mississippi'),('tombigbee',658,'usa','alabama'),('washita',805,'usa','texas'),('washita',805,'usa','oklahoma'),('wateree catawba',636,'usa','north carolina'),('wateree catawba',636,'usa','south carolina'),('white',1110,'usa','arkansas'),('white',1110,'usa','missouri');
/*!40000 ALTER TABLE `river` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state` (
  `state_name` text,
  `population` int(11) DEFAULT NULL,
  `area` double DEFAULT NULL,
  `country_name` varchar(3) NOT NULL DEFAULT '',
  `capital` text,
  `density` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state`
--

LOCK TABLES `state` WRITE;
/*!40000 ALTER TABLE `state` DISABLE KEYS */;
INSERT INTO `state` VALUES ('alabama',3894000,51700,'usa','montgomery',75.31914893617021),('alaska',401800,591000,'usa','juneau',0.6798646362098139),('arizona',2718000,114000,'usa','phoenix',23.842105263157894),('arkansas',2286000,53200,'usa','little rock',42.96992481203007),('california',23670000,158000,'usa','sacramento',149.81012658227849),('colorado',2889000,104000,'usa','denver',27.778846153846153),('connecticut',3107000,5020,'usa','hartford',618.9243027888447),('delaware',594000,2044,'usa','dover',290.60665362035223),('district of columbia',638000,1100,'usa','washington',580),('florida',9746000,68664,'usa','tallahassee',141.9375509728533),('georgia',5463000,58900,'usa','atlanta',92.75042444821732),('hawaii',964000,6471,'usa','honolulu',148.97233812393756),('idaho',944000,83000,'usa','boise',11.373493975903614),('illinois',11400000,56300,'usa','springfield',202.4866785079929),('indiana',5490000,36200,'usa','indianapolis',151.65745856353593),('iowa',2913000,56300,'usa','des moines',51.740674955595026),('kansas',2364000,82300,'usa','topeka',28.724179829890645),('kentucky',2364000,82300,'usa','frankfort',28.724179829890645),('louisiana',4206000,47700,'usa','baton rouge',88.17610062893081),('maine',1125000,33265,'usa','augusta',33.81932962573275),('maryland',4217000,10460,'usa','annapolis',403.1548757170172),('massachusetts',5737000,8284,'usa','boston',692.5398358281024),('michigan',9262000,58500,'usa','lansing',158.32478632478632),('minnesota',4076000,84400,'usa','st. paul',48.29383886255924),('mississippi',2520000,47700,'usa','jackson',52.83018867924528),('missouri',4916000,69700,'usa','jefferson city',70.53084648493544),('montana',786700,147000,'usa','helena',5.351700680272109),('nebraska',1569000,77300,'usa','lincoln',20.297542043984475),('nevada',800500,110500,'usa','carson city',7.244343891402715),('new hampshire',920600,9279,'usa','concord',99.21327729281172),('new jersey',7365000,7787,'usa','trenton',945.8071144214717),('new mexico',1303000,121600,'usa','santa fe',10.71546052631579),('new york',17558000,49100,'usa','albany',357.5967413441955),('north carolina',5882000,52670,'usa','raleigh',111.67647617239415),('north dakota',652700,70700,'usa','bismarck',9.231966053748232),('ohio',10800000,41300,'usa','columbus',261.50121065375305),('oklahoma',3025000,69950,'usa','oklahoma city',43.24517512508935),('oregon',2633000,97073,'usa','salem',27.12391705211542),('pennsylvania',11863000,45308,'usa','harrisburg',261.8301403725611),('rhode island',947200,1212,'usa','providence',781.5181518151816),('south carolina',3121800,31113,'usa','columbia',100.3374795101726),('south dakota',690767,77116,'usa','pierre',8.957505576015354),('tennessee',4591000,42140,'usa','nashville',108.94636924537257),('texas',14229000,266807,'usa','austin',53.33068472716233),('utah',1461000,84900,'usa','salt lake city',17.208480565371026),('vermont',511500,9614,'usa','montpelier',53.203661327231124),('virginia',5346800,40760,'usa','richmond',131.1776251226693),('washington',4113200,68139,'usa','olympia',60.36484245439469),('west virginia',1950000,24200,'usa','charleston',80.57851239669421),('wisconsin',4700000,56153,'usa','madison',83.69989136822609),('wyoming',469557,97809,'usa','cheyenne',4.8007545317915525);
/*!40000 ALTER TABLE `state` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-12 17:54:35
