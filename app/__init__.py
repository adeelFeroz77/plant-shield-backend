from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/plantshield'

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "fa20bscs0031@maju.edu.pk"
app.config['MAIL_PASSWORD'] = "orty ksag ufjm xtnp"
app.config['MAIL_DEFAULT_SENDER'] = "fa20bscs0031@maju.edu.pk"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from app.routes import *
from app.models import *
from app.static import *
from app.detection_model import *
from app.service import *

with app.app_context():
    # db.drop_all()
    db.create_all()

    # Add data to ImageEntityType
    dummy_entity_names = ['PROFILE', 'PLANT', 'USER_PLANT']

    for entity_name in dummy_entity_names:
        existing_entity = ImageEntityType.query.filter_by(entity_name=entity_name).first()

        if not existing_entity:
            new_entity = ImageEntityType(entity_name=entity_name)
            db.session.add(new_entity)
    db.session.commit()

# MIGRATION_SCRIPT

engine = create_engine("postgresql://postgres:root@localhost/plantshield")
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'pictures'))
pictures = os.listdir(directory)

image_insertion_query = '''
	INSERT INTO image(data, image_name, image_extension, entity_id, entity_type_id) VALUES(
		pg_read_binary_file(:absolute_path),
        :image_name,
        :image_extension,
        :entity_id,
        :entity_type_id
	);
'''

with engine.connect() as connection:
    result = connection.execute(text("Select * from plant;"))
    print(result.rowcount)
    if result.rowcount == 0:
        connection.execute(text(
            '''
INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Apple',
	'Apple, (Malus domestica), domesticated tree and fruit of the rose family (Rosaceae), one of the most widely cultivated tree fruits. Apples are predominantly grown for sale as fresh fruit, though apples are also used commercially for vinegar, juice, jelly, applesauce, and apple butter and are canned as pie stock. A significant portion of the global crop also is used for cider, wine, and brandy. Fresh apples are eaten raw or cooked. There are a variety of ways in which cooked apples are used; frequently, they are used as a pastry filling, apple pie being perhaps the archetypal American dessert. Especially in Europe, fried apples characteristically accompany certain dishes of sausage or pork. Apples provide vitamins A and C, are high in carbohydrates, and are an excellent source of dietary fibre.',
	'Malus domestica',
	'Atleast 6 to 8 Hours',
	'0 to 35 degree Celcius',
	'24',
	false,
	false,
	'Apple trees prefer full sun, well-drained soil, and protection from high winds. They can grow in a variety of soils, but fertile sandy soils and loams produce the best crops.
Water young trees regularly, especially those on dwarfing or semi-dwarfing rootstocks, to help establish the root system. When fruiting, apple trees require regular watering or irrigation.
In early spring, feed apple trees with a high potassium fertilizer, such as blood, fish, and bonemeal, or Vitax Q4. Scatter one handful per square meter around trees growing in bare soil, and one and a half around those growing in grass. After the tree starts producing fruit, provide it with a nitrogen-heavy fertilizer. Fertilize during the growing season, starting in early spring and finishing by July. Fertilizing too late in the season can cause trees to grow when they should be shutting down for the winter.
Prune apple trees in the fall after producing fruit.
Protect the tree from frost damage and pests and diseases. Apple trees are one of the most pest-susceptible fruits, but it is possible to avoid pesticides.
Refresh mulch periodically, but pull it away from the trunk so that it doesn''t rot. This also helps to prevent rodents from nesting in it over the winter and chewing on the tree''s bark.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Blueberry', 
	'The plants are deciduous perennial shrubs that range in size from 60 cm (24 inches) tall for lowbush blueberries (Vaccinium angustifolium) up to 4 metres (13 feet) tall for highbush (V. corymbosum) cultivars. They have simple elliptical leaves that are arranged alternately along the dotted stems. The plants produce clusters of small urn-shaped flowers that range in colour from white to pale pink. The fruits are true berries with many small seeds and are a deep indigo to black colour when ripe.', 
	'Vaccinium angustifolium',
	'Atleast 6 to 8 Hours', 
	'20 to 26 degree Celcius', 
	'48', 
	false, 
	false, 
	'Watering
Water blueberry plants during the day to keep the soil moist but not soggy. During the growing season, water them with at least 1 inch of water per week, and up to 4 inches per week when the fruit is ripening. Water evenly on all sides of the plant. Underwatered plants may produce smaller berries, while overwatered plants may produce large, bland fruit.
Soil
Blueberries prefer acidic, well-drained soil with a pH between 4.5 and 5.5. If you have heavy clay soil, you can improve drainage by amending it with organic matter like compost. You can also use sulfur to amend the pH in the fall before planting.
Sunlight
Blueberries should be planted in full sun, but they can tolerate some shade.
Spacing
Depending on the variety, blueberry bushes should be spaced 3–4 feet apart to allow for proper growth and air circulation.
Feeding
Blueberry bushes can be fed with a high potash fertilizer, such as liquid tomato feed, throughout the growing season. Container plants should be fed once a month with a liquid fertilizer specifically for ericaceous plants.
Pruning
Blueberry bushes don''t require much maintenance, but you should prune them in winter after leaf-fall, when the plant is dormant. You can prune off branches that contain disease, low hanging branches, and ones that cross over in the middle.
Repotting
Young plants that are initially in a 30 cm (1 ft) wide container should be repotted into a larger, 45–50 cm (18–20 in) pot once roots start to appear through the drainage hole in the base.
Mulching
Container plants will need regular feeding using a liquid fertilizer specially formulated for acid loving plants. Plants in the ground simply need mulching topping up using an acidic organic material such as leaf mold, bark chippings, pine needles, or composted sawdust. Do not use manure, which is both too rich and too alkaline for blueberries.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Cherry',
	'Cherry, any of various trees belonging to the genus Prunus and their edible fruits. Commercial cherry production includes tart cherries (Prunus cerasus), which are frozen or canned and used in sauces and pastries, and sweet cherries (P. avium), which are usually consumed fresh and are the principal type preserved in true or imitation maraschino liqueur. A number of species, hybrids, and cultivars are grown as ornamentals for their prolific spring flowers, and the dark red wood of some cherry species is especially esteemed for the manufacture of fine furniture.

Most cherry species are native to the Northern Hemisphere. Some 10 to 12 species are recognized in North America and a similar number in Europe. The greatest concentration of species, however, appears to be in eastern Asia. The native habitat of the species from which the cultivated cherries came is believed to be in western Asia and eastern Europe from the Caspian Sea to the Balkans. Cherries are grown in all areas of the world where winter temperatures are not too severe and where summer temperatures are moderate. They require winter cold in order to blossom in spring. The trees bloom quite early in the spring, just after peaches and earlier than apples.',
	'Prunus cerasus',
	'Atleast 6 to 8 Hours',
	'5 to 35 degree Celcius',
	'62',
	false,
	false,
	'Location
Plant cherry trees in an open area with full sun exposure and in a protected area, such as a flat or sloped area. Avoid areas that may experience late spring frosts and areas near trees or bushes that may compete for water.
Soil
Test your soil before planting to determine its structure and acidity. Plant in rich, well-draining soil that can retain some moisture.
Watering
Water new trees weekly and potted trees twice a week. In winter, water once a week. During hot and dry months, provide supplemental irrigation. Infrequent, shallow watering can cause the fruit to dry up and drop.
Fertilizing
Fertilize in early spring and regularly throughout the growing season with a tree-specific fertilizer to encourage healthy growth.
Pruning
Prune in mid-summer when conditions are dry, but never in winter.
Mulching
Spread mulch to help retain moisture and limit weed growth. In February, give the roots a good mulch with well-rotted manure or garden compost.
Protecting from birds
Secure netting over the plant to protect the fruits from birds in the summer.
Protecting from frost
If frost is forecast, protect any early blossom with horticultural fleece.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Corn',
	'The corn plant is a tall annual grass with a stout, erect, solid stem. The large narrow leaves have wavy margins and are spaced alternately on opposite sides of the stem. Staminate (male) flowers are borne on the tassel terminating the main axis of the stem. The pistillate (female) inflorescences, which mature to become the edible ears, are spikes with a thickened axis, bearing paired spikelets in longitudinal rows; each row of paired spikelets normally produces two rows of grain. Varieties of yellow and white corn are the most popular as food, though there are varieties with red, blue, pink, and black kernels, often banded, spotted, or striped. Each ear is enclosed by modified leaves called shucks or husks.',
	'Zea mays',
	'Atleast 6 to 8 Hours',
	'18 to 27 degree Celcius',
	'64',
	false,
	false,
	'Light
Corn plants prefer bright, indirect light, but can tolerate low light. Place them near an east-facing window, or filter bright sunlight through a sheer curtain if your window faces south or west. Avoid direct sunlight and harsh sunlight to avoid sunburn.
Water
Water corn plants when the top inch of soil feels dry in spring and summer, and when the top two inches of soil feel dry in fall and winter. Pour off any excess water that collects in the saucer.
Humidity
Corn plants prefer a humid environment. Spray with a mister every few days, or group the plant with other plants or set the pot on a gravel tray to increase humidity. You can also use a humidifier or place a water tray near the plant.
Temperature
Corn plants prefer temperatures between 65-80°F (18-27°C). Avoid exposing them to drafts or extreme temperature fluctuations.
Fertilizer
Feed with liquid fertilizer once a month in spring and summer. Use a balanced, water-soluble fertilizer during the growing season to provide essential nutrients.
Repotting
Repot every couple of years to help your plant grow.
Location
Protect corn plants from drafts and heat by moving them away from cold or drafty windows, air conditioners, and heating vents.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Grape',
	'The grape is usually a woody vine, climbing by means of tendrils (modified branches) and when untrained often reaching a length of 17 metres (56 feet) or more. In arid regions it may form an almost erect shrub. The edible leaves are alternate, palmately lobed, and always tooth-edged. Small greenish flowers, in clusters, precede the fruit, which varies in colour from almost black to green, red, and amber. Botanically, the fruit is a berry, more or less globular, within the juicy pulp of which lie the seeds. In many varieties the fruit develops a whitish powdery coating, or bloom.',
	'Genus Vitis',
	'Atleast 7 to 8 Hours',
	'25 to 32 degree Celcius',
	'62',
	false,
	false,
	'Sunlight
Grape plants need full sun all day, so plant them in a sunny location, preferably south-facing, to maximize ripening.
Soil
Grape plants need deep, well-draining soil that''s free of weeds and grass. The soil pH should be slightly acidic to neutral.
Watering
Water young grape plants regularly during their first two years, about 1 inch per week. After the vines are established, they seldom need watering, and overwatering can cause leaves to drop. Water deeply and regularly in spring and summer, but don''t water erratically, as this may cause the fruit to split.
Temperature
The best temperature for growing grapes is 77ºF to 90ºF.
Pruning
In the first couple of years, don''t allow the vine to produce fruit, as its roots need to be strong enough to bear the weight. Prune in March or April, removing at least 90 percent of the previous season''s growth. In the first year, cut the buds except for 2 or 3, then select healthy canes and cut back the rest. In the second year, prune back all the canes, leaving a couple of buds on each arm.
Fertilizing
The fertilizer requirements of bunch grapes can vary widely depending on vine vigor and crop size. You can use urea (46-0-0) at 2 to 3 ounces (1/2 cup) or bloodmeal (12-0-0) at 8 ounces (1 ½ cups) per vine to supply the desired amounts of nitrogen.
Mulching
Mulching is not usually recommended for grapes because mulch will keep the soil temperature too cool. However, you can use mulch to maintain the moisture around the vines.
Birds
Use a mesh to keep the birds away from budding fruit.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Orange',
	'Orange, any of several species of small trees or shrubs of the genus Citrus of the family Rutaceae and their nearly round fruits, which have leathery and oily rinds and edible, juicy inner flesh. A number of species and varieties of orange are economically important, namely the China orange, also called the sweet, or common, orange (Citrus ×sinensis); the mandarin orange (C. reticulata), some varieties of which are called tangerines; and the sour, or Seville, orange (C. ×aurantium), which is less extensively grown. Common varieties of the sweet orange include the Jaffa, from Israel, the seedless navel, and the Maltese, or blood, orange.',
	'Citrus × sinensis',
	'Atleast 6 to 8 Hours',
	'18 to 29 degree Celcius',
	'8',
	false,
	false,
	'Light: Orange trees need 6–8 hours of direct sunlight daily.
Water: Water when the top two inches of soil are dry, but don''t overwater, as this can damage the roots. Established trees need about one inch of water per week, but the amount depends on rainfall.
Soil: Orange trees prefer slightly acidic to neutral soil with a pH of 6.0–7.0. They also need well-draining soil, so you can build up a small mound at the bottom of the planting hole to improve drainage.
Fertilizer: Fertilize your tree weekly in spring and summer, or three times a year, to encourage more fruit and prettier flowers.
Pruning: Trim your tree regularly and prune away sprouts as they appear.
Temperature: Orange trees thrive in subtropical regions with warm temperatures and moderate humidity. They can be grown outdoors in USDA hardiness zones 9–11, but begin to go dormant when temperatures drop below 50°F.
Pests: Protect your tree from pests like aphids and scale.
Planting: The best time to plant an orange tree is in spring or early autumn. In spring, the soil is warming but still mild, and in autumn, the tree can establish itself before the cold winter. Dig a hole that''s twice as wide and just as deep as the root ball.
Harvesting: Ripe citrus fruit can stay on the tree until late winter, but you should harvest it all before the tree blooms in spring, and before any significant freeze.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Peach',
	'Small to medium-sized, peach trees seldom reach 6.5 meters (21 feet) in height. Under cultivation, however, they are usually kept between 3 and 4 meters (10 and 13 feet) by pruning. The leaves are glossy green, lance-shaped, and long pointed; they usually have glands at their bases that secrete a fluid to attract ants and other insects. The flowers, borne in the leaf axils, are arranged singly or in groups of two or three at nodes along the shoots of the previous season’s growth. The five petals, usually pink but occasionally white, five sepals, and three whorls of stamens are borne on the outer rim of the short tube, known as the hypanthium, that forms the base of the flower.',
	'Prunus persica',
	'Atleast 6 to 8 Hours',
	'5 to 35 degree Celcius',
	'12',
	false,
	false,
	'Sunlight
Peach trees need full sun, at least eight hours a day in the summer. Avoid planting them in shady areas or where other trees may compete for roots.
Soil
Peach trees prefer well-drained, moderately fertile soil with a pH of 6–6.5. The best soil is a humus-rich, sandy loam. Avoid low-lying areas where drainage may be poor, as even a short period of soggy soil can kill a peach tree.
Watering
Water new trees deeply two to three times a week, and keep the soil moist throughout the growing season. Water more generously during hot, sunny weather.
Fertilizing
In late winter, feed peach trees with a continuous release feed, followed by a mulch of well-rotted manure. In early spring, fertilize with a slow-release fertilizer that''s high in phosphorus and low in nitrogen. Six weeks after planting, spread one pound of a balanced 10-10-10 fertilizer around the root zone.
Pruning
Prune annually in the spring when the buds start to swell, or in late summer after fruiting. Pruning increases fruit production, as peaches bear fruit on second-year wood. In the tree''s first, second, and third years, prune in early summer. After the third year, prune in late April, and maintain the tree''s shape by cutting shoots growing from the center of the tree.
Mulching
Mulch annually to feed the soil and suppress weeds.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Pepper Bell',
	'Bell pepper, (Capsicum annuum), pepper cultivar in the nightshade family (Solanaceae), grown for its thick, mild fruits. Bell peppers are used in salads and in cooked dishes and are high in vitamin A and vitamin C. The large furrowed fruits are technically berries and can be green, red, yellow, or orange. Bell pepper plants are grown as annuals, and the green varieties are harvested before the appearance of red or yellow pigment—generally about 60–80 days after transplanting.',
	'Capsicum annuum',
	'Atleast 6 to 8 Hours',
	'20 to 28 degree Celcius',
	'48',
	false,
	false,
	'Sunlight
Bell peppers need at least 6–8 hours of direct sunlight per day. Avoid planting them near taller crops that block the sun. If you live in a hot climate, you can use shade cloth or nearby plants to manage temperatures.
Soil
Bell peppers grow best in nutrient-rich, well-drained, loamy soil with a balanced pH level of 6.5–7. When planting, mix compost or other organic matter into the soil.
Water
Water bell peppers regularly to moisten the soil about 6 inches deep, then let it dry slightly. Aim for 1–2 inches of water per week, but more when it''s hotter. Drip irrigation works best, and soaker hoses provide the deep watering needed. Watering is especially important during fruit set and as the bells mature.
Fertilizer
Mix a continuous-release fertilizer into the soil at planting and replenish as directed during the growing season. Switch to a high potash feed when the first fruit has set.
Support
Support bell pepper plants with bamboo canes or similar and tie them in as they grow.
Pinch out growing tip
When plants reach about 8 inches high, pinch out the growing tip to encourage bushy growth and better cropping.
Prune early flowers and fruits
Remove early flowers and fruits from smaller seedlings so the plant can grow larger before setting fruit.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Potato',
	'The potato is one of some 150 tuber-bearing species of the genus Solanum (a tuber is the swollen end of an underground stem). The compound leaves are spirally arranged; each leaf is 20–30 cm (about 8–12 inches) long and consists of a terminal leaflet and two to four pairs of leaflets. The white, lavender, or purple flowers have five fused petals and yellow stamens. The fruit is a small poisonous berry with numerous seeds.',
	'Solanum tuberosum',
	'Atleast 6 to 10 Hours',
	'7 to 21 degree Celcius',
	'24',
	false,
	false,
	'Sunlight
Potato plants need full sun to produce the best yields, but may need some afternoon shade in hot summers.
Soil
Potato plants prefer well-drained soil that''s high in organic matter. Loosen the soil regularly to prevent compaction and encourage root development. Deep soils with good water retention and aeration give best growth and yields.
Water
Water potatoes regularly, especially during warm, dry spells. Potato plants absorb a lot of water, so be prepared to water them frequently, daily if necessary, in hot conditions. The taller the plants become the more water they will need.
Fertilizer
Feed potatoes every three to four weeks during key growth periods with a specialty fertilizer that contains high levels of phosphorus and potassium.
Earthing up
As the plants grow, use a spade or hoe to cover the shoots with soil to stop the developing tubers becoming green and inedible. This is called "earthing up" and increases eventual yield and protects from late frosts. Leave the top few centimeters poking out the top.
Harvesting
Once the plants have died back and the leaves have turned yellow, it is time to harvest the potatoes. Carefully dig the tubers out of the ground and store them in a dry, dark and cool place. Let the potatoes dry there for about two weeks before processing or storing them.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Raspberry',
	'Raspberries are perennial plants with canes that live two years each. The canes are either armed with prickles or smooth, and many only produce fruit in their second year. Often reaching more than 1.8 metres (6 feet) in height, the canes bear compound leaves with three or more toothed leaflets, depending on the species or cultivar. The leaf undersides are characteristically white to gray in colour and often hairy. The white to pink flowers have five petals and produce juicy red, purple, or black (rarely orange, amber, or pale yellow) fruit. The core of the delicate fruit remains on the plant when picked, unlike that of the blackberry. Though they are commonly called “berries,” the fruit is technically an aggregate of drupelets (small drupes), each of which contains a single seed.',
	'Rubus idaeus',
	'Atleast 6 to 8 Hours',
	'10 to 32 degree Celcius',
	'24',
	false,
	false,
	'Sunlight
Raspberry plants need at least six hours of full sun each day.
Watering
Water raspberry plants during the day, giving them about 1–2 inches per week during the growing season and up to 4 inches per week during harvest. Keep the soil around the roots moist for at least one week.
Fertilizing
In the first year, add nitrogen or a 10-10-10 nitrogen fertilizer after planting and the soil has settled, keeping about 3–4 inches away from the base of the plant. In subsequent years, add a higher amount of nitrogen fertilizer.
Mulching
Spread mulch over the soil in a layer 7.5 cm (3 in) deep to help maintain moisture and control weeds. Garden compost is ideal, but avoid alkaline mushroom compost.
Pruning
Most raspberries should be pruned straight after planting, cutting the stems down to 25 cm (10 in) tall. However, don''t prune summer-fruiting raspberries bought as "long canes".
Support
Most raspberries will benefit from a trellis system, especially trailing varieties. Use steel posts about 7 ft high and 8 ft apart and buried at least one ft into the ground with two to three horizontal guide wires.
Spacing
Space plants 45–60 cm (18–24 in) apart, with 1.8 m (6 ft) between rows.
Planting
Dig a hole slightly larger than the container and work the soil at the bottom of the hole so that it''s loose and aerated. The first roots should be no more than 5 cm (2 in) below the soil surface.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Soybean',
	'The soybean is an erect branching plant and can reach more than 2 metres (6.5 feet) in height. The self-fertilizing flowers are white or a shade of purple. Seeds can be yellow, green, brown, black, or bicoloured, though most commercial varieties have brown or tan seeds, with one to four seeds per pod.',
	'Glycine max',
	'Atleast 6 to 8 Hours',
	'15 to 25 degree Celcius',
	'24',
	false,
	false,
	'Soybean plants are best grown in full sun. Choose a location that will receive at least 6 hours of full sun each day.Soybean plants need a well drained soil enriched with plenty of organic matter. Prepare soil by weeding it thoroughly, digging it over to loosen it and adding aged animal manure or compost. Keep the area free of weeds until planting.');
	
INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Squash',
	'Squash, (genus Cucurbita), genus of flowering plants in the gourd family (Cucurbitaceae), many of which are widely cultivated as vegetables and for livestock feed. Squashes are native to the New World, where they were cultivated by indigenous peoples before European settlement. The fruit of edible species is usually served as a cooked vegetable, and the seeds and blossoms may also be cooked and eaten.',
	'Genus Cucurbita',
	'Atleast 6 to 8 Hours',
	'20 to 38 degree Celcius',
	'24',
	false,
	false,
	'Watering
Squash plants need a lot of water, especially when they are fruiting. Water them early in the morning, and try to give them at least 1 inch of water per week. Avoid getting the leaves wet, as this can lead to fungal diseases. For containers, keep an eye on the soil as it will dry out faster than soil in the ground.
Soil
Squash plants grow best in rich, well-drained soil with a pH of 6.0 to 6.7. You can improve your soil by mixing in compost or other organic matter.
Sunlight
Squash plants grow best in full sun, so try to plant them on a south or southeast facing slope.
Feeding
Once the first fruits start to swell, feed your squash plants every 10 to 14 days with a high potassium liquid fertilizer. You can also use a continuous-release plant food.
Mulching
After planting, cover the soil with a thick layer of mulch, such as garden compost, to help retain moisture. However, leave a gap around the base of the plant stem to prevent dampness and rotting.
Spacing
Give squash plants room to sprawl by planting them 3 to 6 feet apart.
Support
Winter squash and pumpkins need space to climb and scramble, so provide them with strong supports, such as a trellis or arch.
Diseases
If your squash plants are affected by common diseases like powdery mildew or downy mildew, treat them at the first sign. You can use a fungicide like Daconil to treat squash plants up until the day of harvest');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Strawberry',
	'Strawberries are low-growing herbaceous plants with a fibrous root system and a crown from which arise basal leaves. The leaves are compound, typically with three leaflets, sawtooth-edged, and usually hairy. The flowers, generally white, rarely reddish, are borne in small clusters on slender stalks arising, like the surface-creeping stems, from the axils of the leaves. As a plant ages, the root system becomes woody, and the “mother” crown sends out runners (e.g., stolons) that touch ground and root, thus enlarging the plant vegetatively. Botanically, the strawberry fruit is considered an “accessory fruit” and is not a true berry. The flesh consists of the greatly enlarged flower receptacle and is embedded with the many true fruits, or achenes, which are popularly called seeds.',
	'Genus Fragaria',
	'Atleast 6 to 8 Hours',
	'10 to 27 degree Celcius',
	'48',
	false,
	false,
	'Planting: Plant in spring or fall, depending on your growing zone. Space plants 18 inches apart, with 4 feet between rows. Strawberry plants prefer moist soil with a pH of 5.8 to 6.2. You can add compost or other organic matter to improve your soil.
Watering: Water plants once a week, or when the top inch of soil is dry. Water from the bottom to avoid getting leaves wet. Overwatering can cause root rot and powdery mildew.
Sunlight: Strawberries need plenty of sunlight, so choose a sunny location. Avoid overhead watering, which can keep leaves wet for too long.
Fertilizing: Use a continuous-release fertilizer to promote fruit production.
Mulching: Mulch can reduce water needs and weed invasion.
Harvesting: Harvest ripe strawberries in the morning and refrigerate immediately.');

INSERT INTO plant(plant_name, description, species, sunlight_requirements, temperature_requirements, watering_schedule, is_favorite, is_blooming, care_instructions) values (
	'Tomato',
	'Tomato plants are generally much branched, spreading 60–180 cm (24–72 inches) and somewhat trailing when fruiting, but a few forms are compact and upright. Leaves are more or less hairy, strongly odorous, pinnately compound, and up to 45 cm (18 inches) long. The five-petaled flowers are yellow, 2 cm (0.8 inch) across, pendant, and clustered. Fruits are berries that vary in diameter from 1.5 to 7.5 cm (0.6 to 3 inches) or more. They are usually red, scarlet, or yellow, though green and purple varieties do exist, and they vary in shape from almost spherical to oval and elongate to pear-shaped. Each fruit contains at least two cells of small seeds surrounded by jellylike pulp.',
	'Solanum lycopersicum',
	'Atleast 6 to 8 Hours',
	'15 to 35 degree Celcius',
	'24',
	false,
	false,
	'Sunlight
Tomatoes need warmth, not light, to ripen, so keep them out of direct sunlight in a spot with a temperature of 65–70°F.
Soil
Tomatoes grow best in warm, well-drained soil. You can use a lightweight potting mix that drains well, as regular soil may not drain fast enough.
Watering
Water the soil, not the foliage or stems, consistently and generously to keep tomatoes evenly moist and prevent blossom end rot. Don''t let pots stand in water, allow water to drain out through drainage holes.
Support
Most varieties of tomato plants grow along the ground, so you may need to provide support with a cage, trellis, or stake.
Pruning
Regular pruning helps tomato plants grow stronger and healthier, and produce more vegetables. Pruning also helps with pest control.
Fertilizer
Provide a side dressing of tomato fertilizer for the best-looking fruit.
Seedlings
Handle tomato seedlings with care, and never touch the main stem, as the juicy tissues bruise easily and can allow fungi to enter and cause the seedlings to rot.
Containers
If reusing plastic module trays, wash them well in warm, soapy water to remove old soil and accumulated salts. Small paper cups with holes punched in the bottoms can also be used.');

            '''
        ))
        connection.commit()
        entity_id_counter = 1
        for filename in pictures:
            absolute_path = os.path.join(directory,filename)
            image_name, image_extension = os.path.splitext(filename)
            connection.execute(
                text(image_insertion_query),
                {
					'absolute_path' : absolute_path,
					'image_name' : image_name,
					'image_extension' : image_extension[1:],
					'entity_id' : entity_id_counter,
					'entity_type_id': 2
				}
			)
            entity_id_counter+=1

    result = connection.execute(text("Select * from disease_info;"))
    if result.rowcount == 0:
        connection.execute(text(
            '''
INSERT INTO disease_info(name, description, possible_steps) values(
	'Scab',
	'Scab is the most common disease of apple and crabapple trees in Minnesota.
Scab is caused by a fungus that infects both leaves and fruit.
Scabby fruit are often unfit for eating.
Infected leaves have olive green to brown spots.
Leaves with many leaf spots turn yellow and fall off early.
Leaf loss weakens the tree when it occurs many years in a row.
Planting disease resistant varieties is the best way to manage scab.',
	'Choose resistant varieties when possible.
Rake under trees and destroy infected leaves to reduce the number of fungal spores available to start the disease cycle over again next spring.
Water in the evening or early morning hours (avoid overhead irrigation) to give the leaves time to dry out before infection can occur.
Spread a 3- to 6-inch layer of compost under trees, keeping it away from the trunk, to cover soil and prevent splash dispersal of the fungal spores.
For best control, spray liquid copper soap early, two weeks before symptoms normally appear. Alternatively, begin applications when disease first appears, and repeat at 7 to 10 day intervals up to blossom drop.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Black Rot',
	'Leaf symptoms first occur early in the spring when the leaves are unfolding.
They appear as small, purple specks on the upper surface of the leaves that enlarge into circular lesions 1/8 to 1/4 inch (3-6 mm) in diameter.
The margin of the lesions remains purple, while the center turns tan to brown. In a few weeks, secondary enlargement of these leaf spots occurs.
Heavily infected leaves become chlorotic and defoliation occurs.
As the rotted area enlarges, a series of concentric bands of uniform width form which alternate in color from black to brown. The flesh of the rotted area remains firm and leathery. Black pycnidia are often seen on the surface of the infected fruit.',
	'Remove the cankers by pruning at least 15 inches below the end and burn or bury them. Also take preventative care with new season prunings and burn them, too.You are better off pruning during the dormant season. This will minimize the odds that fire blight will infect your tree and produce dead tissue that can easily be infected by Botryosphaeria.You should also take precautions if the bark is damaged by hail, or branches break during a windstorm. Using a copper-based fungicide will protect against both black rot and fire blight.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Cedar rust',
	'Cedar apple rust (Gymnosporangium juniperi-virginianae) is a fungal disease that requires juniper plants to complete its complicated two year life-cycle. Spores overwinter as a reddish-brown gall on young twigs of various juniper species. In early spring, during wet weather, these galls swell and bright orange masses of spores are blown by the wind where they infect susceptible apple and crab-apple trees. The spores that develop on these trees will only infect junipers the following year. From year to year, the disease must pass from junipers to apples to junipers again; it cannot spread between apple trees.',
	'Choose resistant cultivars when available.
Rake up and dispose of fallen leaves and other debris from under trees.
Remove galls from infected junipers. In some cases, juniper plants should be removed entirely.
Apply preventative, disease-fighting fungicides labeled for use on apples weekly, starting with bud break, to protect trees from spores being released by the juniper host. This occurs only once per year, so additional applications after this springtime spread are not necessary.
On juniper, rust can be controlled by spraying plants with a copper solution (0.5 to 2.0 oz/ gallon of water) at least four times between late August and late October.
Safely treat most fungal and bacterial diseases with SERENADE Garden. This broad spectrum bio-fungicide uses a patented strain of Bacillus subtilis that is registered for organic use. Best of all, SERENADE is completely non-toxic to honey bees and beneficial insects.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Healthy',
	'Nothing to worry about! Your plant is Healthy',
	'Keep following the care instructions to maintain your plant''s health'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Powdery Mildew',
	'Initial symptoms, often occurring 7 to 10 days after the onset of the first irrigation, are light roughly-circular, powdery looking patches on young, susceptible leaves (newly unfolded, and light green expanding leaves). Older leaves develop an age-related (ontogenic) resistance to powdery mildew and are naturally more resistant to infection than younger leaves. Look for early leaf infections on root suckers, the interior of the canopy or the crotch of the tree where humidity is high. In contrast to other fungi, powdery mildews do not need free water to germinate but germination and fungal growth are favored by high humidity. The disease is more likely to initiate on the undersides (abaxial) of leaves but will occur on both sides at later stages. As the season progresses and infection is spread by wind, leaves may become distorted, curling upward. Severe infections may cause leaves to pucker and twist. Newly developed leaves on new shoots become progressively smaller, are often pale and may be distorted.',
	'Disinfect the cutting edges, then prune out and discard the diseased portions of the plant immediately. At the same time, apply fungicides to protect the remaining leaves on the fruit tree. You''ll need to repeat the fungicide applications according to label instructions to protect the trees over the entire season.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Cercospora Leaf Spot | Gray Leaf Spot',
	'Gray leaf spot on corn, caused by the fungus Cercospora zeae-maydis, is a peren- nial and economically damaging disease in the United States. Since the mid-1990s, the disease has increased in importance in Indiana, and now is the one of the most important foliar diseases of corn in the state.Gray leaf spot disease is caused by the fungus Pyricularia grisea, also referred to as Magnaporthe grisea. The frequent warm rainy periods common in Florida create favorable conditions for this fungal disease. This fungus slows grow-in, thins established stands and can kill large areas of St.',
	'Irrigate deeply, but infrequently.
Avoid using post-emergent weed killers on the lawn while the disease is active.
Avoid medium to high nitrogen fertilizer levels.
Improve air circulation and light level on lawn.
Mow at the proper height and only mow when the grass is dry.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Common Rust',
	'Although a few rust pustules can always be found in corn fields throughout the growing season, symptoms generally do not appear until after tasseling. These can be easily recognized and distinguished from other diseases by the development of dark, reddish-brown pustules (uredinia) scattered over both the upper and lower surfaces of the corn leaves. These pustules may appear on any above ground part of the plant, but are most abundant on the leaves. Pustules appear oval to elongate in shape, are generally small, less than 1/4 inch long, and are surrounded by the leaf epidermal layer, where it has broken through. ',
	'To reduce the incidence of corn rust, plant only corn that has resistance to the fungus. Resistance is either in the form of race-specific resistance or partial rust resistance. In either case, no sweet corn is completely resistant. If the corn begins to show symptoms of infection, immediately spray with a fungicide.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Northern Leaf Blight',
	'Northern corn leaf blight (NCLB) is caused by the fungus Setosphaeria turcica. Symptoms usually appear first on the lower leaves. Leaf lesions are long (1 to 6 inches) and elliptical, gray-green at first but then turn pale gray or tan. Under moist conditions, dark gray spores are produced, usually on the lower leaf surface, which give lesions a "dirty" gray appearance. Entire leaves on severely blighted plants can die, so individual lesions are not visible. Lesions may occur on the outer husk of ears, but the kernels are not infected. On hybrids that contain an Ht gene for resistance to the fungus, lesions are smaller, chlorotic, and may develop into linear streaks. These lesions rarely produce spores.',
	'Fungicide applications reduced Northern Corn Leaf Blight damage and protected yield. Fungicide value was higher in reducing yield in susceptible corn hybrids. Fungicide were most effective if they were applied at disease onset. Disease onset varied in growth stages, and so the best stage to apply fungicides.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Esca | Black Measles',
	'Grapevine measles, also called esca, black measles or Spanish measles, has long plagued grape growers with its cryptic expression of symptoms and, for a long time, a lack of identifiable causal organism(s). The name ‘measles’ refers to the superficial spots found on the fruit (Fig. 1). During the season, the spots may coalesce over the skin surface, making berries black in appearance. Spotting can develop anytime between fruit set and a few days prior to harvest. Berries affected at fruit set tend not to mature and will shrivel and dry up. In addition to spotting, fruit affected later in the season will also have an acrid taste.Leaf symptoms are characterized by a ‘tiger stripe’ pattern (Fig 2-bottom leaf) when infections are severe from year to year. Mild infections can produce leaf symptoms (Fig. 2-upper leaf) that can be confused with other diseases or nutritional deficiencies. White cultivars will display areas of chlorosis followed by necrosis, while red cultivars are characterized by red areas followed by necrosis. Early spring symptoms include shoot tip dieback, leaf discoloration and complete defoliation in severe cases.',
	'Till date there is no effective method to control this disease. Remove the infected berries, leaves and trunk and destroy them. Protect the prune wounds to minimize fungal infection using wound sealant (5% boric acid in acrylic paint) or essential oil or suitable fungicides.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Leaf Blight | Isariopsis Leaf Spot',
	'The fungus is an obligate pathogen which can attack all green parts of the vine.
Symptoms of this disease are frequently confused with those of powdery mildew. Infected leaves develop pale yellow-green lesions which gradually turn brown. Severely infected leaves often drop prematurely.Infected petioles, tendrils, and shoots often curl, develop a shepherd''s crook, and eventually turn brown and die.
Young berries are highly susceptible to infection and are often covered with white fruiting structures of the fungus. Infected older berries of white cultivars may turn dull gray-green, whereas those of black cultivars turn pinkish red.',
	'Apply dormant sprays to reduce inoculum levels.
Cut it out. 
Open up that canopy.
Don''t let down your defenses.
Scout early, scout often.
Use protectant and systemic fungicides.
Consider fungicide resistance.
Watch the weather.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Haunglongbing | Citrus Greening',
	'Citrus greening disease is a disease of citrus caused by a vector-transmitted pathogen. HLB is distinguished by the common symptoms of yellowing of the veins and adjacent tissues; followed by splotchy mottling of the entire leaf, premature defoliation, dieback of twigs, decay of feeder rootlets and lateral roots, and decline in vigor, ultimately followed by the death of the entire plant. Affected trees have stunted growth, bear multiple off-season flowers (most of which fall off), and produce small, irregularly shaped fruit with a thick, pale peel that remains green at the bottom and tastes very bitter. Common symptoms can often be mistaken for nutrient deficiencies; however, the distinguishing factor between nutrient deficiencies is the pattern of symmetry. Nutrient deficiencies tend to be symmetrical along the leaf vein margin, while HLB has an asymmetrical yellowing around the vein. The most noticeable symptom of HLB is greening and stunting of the fruit, especially after ripening',
	'The only way to prevent the spread of Citrus Greening Disease is to control ACP(Asian Citrus Psyllid). Since citrus is such a popular and widely-planted garden tree, homeowners are on the front lines of this important battle.Spray the lemon tree with Neem oil insecticide, both the top and undersides of the foliage. You may need to repeat in 10-14 days, depending upon the extent of the infestation. Follow up by treating the mold growth with liquid copper fungicide.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Bacterial Spot',
	'Bacterial spot is an important disease of peaches, nectarines, apricots, and plums caused by Xanthomonas campestris pv. pruni. Symptoms of this disease include fruit spots, leaf spots, and twig cankers. Fruit symptoms include pitting, cracking, gumming, and watersoaked tissue, which can make the fruit more susceptible to brown rot, rhizopus, and other fungal infections. Severe leaf spot infections can cause early defoliation. Severe defoliation can result in reduced fruit size, and sunburn and cracking of fruit. Early defoliated trees are reduced in vigor and winter hardiness.',
	'Fruit symptoms of bacterial spot may be confused with peach scab, caused by the fungus Cladosporium carpophyllium, however scab spots are more circular, have a dark brown/greenish, fuzzy appearance, and do not pit the fruit surface, although skin cracking can occur. Scab does not cause leaf symptoms but can cause spots on twigs. Initial fruit spots of bacterial spot may be superficial but develop into craters.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Early Blight',
	'In most production areas, early blight occurs annually to some degree. The severity of early blight is dependent upon the frequency of foliar wetness from rain, dew, or irrigation; the nutritional status of the foliage; and cultivar susceptibility.The first symptoms of early blight appear as small, circular or irregular, dark-brown to black spots on the older (lower) leaves. These spots enlarge up to 3/8 inch in diameter and gradually may become angular-shaped.Initial lesions on young, fully expanded leaves may be confused with brown spot lesions. These first lesions appear about two to three days after infection, with further sporulation on the surface of these lesions occurring three to five days later.',
	'Treatment of early blight includes prevention by planting potato varieties that are resistant to the disease; late maturing are more resistant than early maturing varieties. Avoid overhead irrigation and allow for sufficient aeration between plants to allow the foliage to dry as quickly as possible.
	'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Late Blight',
	'The primary host is potato, but P. infestans also can infect other solanaceous plants, including tomatoes, petunias and hairy nightshade, that can act as source of inoculum to potato.The first symptoms of late blight in the field are small, light to dark green, circular to irregular-shaped water-soaked spots. These lesions usually appear first on the lower leaves. Lesions often begin to develop near the leaf tips or edges, where dew is retained the longest.During cool, moist weather, these lesions expand rapidly into large, dark brown or black lesions, often appearing greasy. Leaf lesions also frequently are surrounded by a yellow chlorotic halo',
	'The severe late blight can be effectively managed with prophylactic spray of mancozeb at 0.25% followed by cymoxanil+mancozeb or dimethomorph+mancozeb at 0.3% at the onset of disease and one more spray of mancozeb at 0.25% seven days after application of systemic fungicides in West Bengal'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Powdery Mildew',
	'White powdery spots can form on both upper and lower leaf surfaces, and quickly expand into large blotches.
Powdery mildew weakens the plant and the fruit ripens prematurely. Fewer and smaller fruit grow on infected plants.
In warm, dry conditions, new spores form and easily spread the disease.
Symptoms of powdery mildew first appear mid to late summer in Minnesota.
Provide good air movement around plants through proper spacing, staking of plants and weed control.
If susceptible varieties are growing in an area where powdery mildew has resulted in yield loss in the past, fungicide may be necessary.',
	'Combine one tablespoon baking soda and one-half teaspoon of liquid, non-detergent soap with one gallon of water, and spray the mixture liberally on the plants. Mouthwash. The mouthwash you may use on a daily basis for killing the germs in your mouth can also be effective at killing powdery mildew spores.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Leaf Scorch',
	'Leaf scorch symptoms are very similar to the early stages of common (Mycosphaerella) leaf spot, with irregular dark purple spots being scattered over the upper leaf surface. As the spots enlarge, they begin to look like drops of tar, and are actually the accumulations of black fruiting bodies (acervuli) of the fungus. The centers of the spots remain purple (in Mycosphaerella leaf spot they are white) and there is no well-defined lesion border. In heavy infections, these regions coalesce and the tissue between the lesions often takes on a purplish to bright red color that is dependent on cultivar, temperature, or other factors. The leaves eventually turn brown, dry up, and curl at the margins giving the leaf a scorched appearance. Examination of the acervuli and conidial morphology can help to distinguish between leaf spot and leaf scorch at this advanced stage of disease. On the upper leaf surfaces of leaf scorch lesions, the acervuli are dark with glistening spore masses and dark apothecia. Petiole lesions are elongate, sunken, with a purplish to brown color and can kill the leaf by girdling the petiole. Runners, fruit stalks, fruit and caps can also become infected. Plants may become weakened and the number and vigor of crowns reduced. Infection predisposes the plants to winter and drought stress. In severe infestations, flowers and fruit may die.',
	'While leaf scorch on strawberry plants can be frustrating, there are some strategies which home gardeners may employ to help prevent its spread in the garden. The primary means of strawberry leaf scorch control should always be prevention. Since this fungal pathogen overwinters on the fallen leaves of infected plants, proper garden sanitation is key. This includes the removal of infected garden debris from the strawberry patch, as well as the frequent establishment of new strawberry transplants. The creation of new plantings and strawberry patches is key to maintaining a consistent strawberry harvest, as older plants are more likely to show signs of severe infection.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Leaf Mold',
	'Tomato leaf mold is a fungal disease that can develop when there are extended periods of leaf wetness and the relative humidity is high (greater than 85 percent). Due to this moisture requirement, the disease is seen primarily in hoophouses and greenhouses. Tomato leaf mold can develop during early spring temperatures (50.9 degrees Fahrenheit) or those characteristic of summer (90 F). The optimal temperature tomato leaf mold is in the low 70s.

Symptoms of disease include yellow spots on the upper leaf surface. Discrete masses of olive-green spores can be seen on the underside of the affected leaves.',
	'When treating tomato plants with fungicide, be sure to cover all areas of the plant that are above the soil, especially the underside of leaves, where the disease often forms. Calcium chloride-based sprays are recommended for treating leaf mold issues. Organic fungicide options are also available.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Septoria Leaf Spot',
	'Septoria leaf spot is caused by a fungus, Septoria lycopersici. It is one of the most destructive diseases of tomato foliage and is particularly severe in areas where wet, humid weather persists for extended periods.Septoria leaf spot usually appears on the lower leaves after the first fruit sets. Spots are circular, about 1/16 to 1/4 inch in diameter with dark brown margins and tan to gray centers with small black fruiting structures. Characteristically, there are many spots per leaf. This disease spreads upwards from oldest to youngest growth. If leaf lesions are numerous, the leaves turn slightly yellow, then brown, and then wither. Fruit infection is rare.',
	'Remove diseased leaves. 
Improve air circulation around the plants.
Mulch around the base of the plants. Mulching will reduce splashing soil, which may contain fungal spores associated with debris. Apply mulch after the soil has warmed.
Do not use overhead watering. Overhead watering facilitates infection and spreads the disease. Use a soaker hose at the base of the plant to keep the foliage dry. Water early in the day.
Control weeds. Nightshade and horsenettle are frequently hosts of Septoria leaf spot and should be eradicated around the garden site.
Use crop rotation. Next year do not plant tomatoes back in the same location where diseased tomatoes grew. Wait 1–2 years before replanting tomatoes in these areas.
Use fungicidal sprays.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Spider Mites | Two-Spotted Spider Mite',
	'The two-spotted spider mite is the most common mite species that attacks vegetable and fruit crops in New England. Spider mites can occur in tomato, eggplant, potato, vine crops such as melons, cucumbers, and other crops. Two-spotted spider mites are one of the most important pests of eggplant. They have up to 20 generations per year and are favored by excess nitrogen and dry and dusty conditions. Outbreaks are often caused by the use of broad-spectrum insecticides which interfere with the numerous natural enemies that help to manage mite populations. As with most pests, catching the problem early will mean easier control.',
	'Avoid weedy fields and do not plant eggplant adjacent to legume forage crops.
Avoid early season, broad-spectrum insecticide applications for other pests.
Do not over-fertilize.
Overhead irrigation or prolonged periods of rain can help reduce populations.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Target Spot',
	'The disease starts on the older leaves and spreads upwards. The first signs are irregular-shaped spots (less than 1 mm) with a yellow margin . Some of the spots enlarge up to 10 mm and show characteristics rings, hence the name of "target spot" . Spread to all leaflets and to other leaves is rapid , causing the leaves to turn yellow, collapse and die . Spots also occur on the stems. They are long and thin. Small light brown spots with dark margins may also occur on the fruit.
The spores are spread by wind-blown rain, and if windy wet weather continues for a few days, spread is fast and plants lose their leaves quickly.',
	'Cultural control is important. The following should be done:
Do not plant new crops next to older ones that have the disease.
Plant as far as possible from papaya, especially if leaves have small angular spots (Photo 5).
Check all seedlings in the nursery, and throw away any with leaf spots.
Remove a few branches from the lower part of the plants to allow better airflow at the base
Remove and burn the lower leaves as soon as the disease is seen, especially after the lower fruit trusses have been picked.
Keep plots free from weeds, as some may be hosts of the fungus.
Do not use overhead irrigation; otherwise, it will create conditions for spore production and infection.
Collect and burn as much of the crop as possible when the harvest is complete.
Practise crop rotation, leaving 3 years before replanting tomato on the same land.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Yellow Leaf Curl Virus',
	'Tomato yellow leaf curl virus is a species in the genus Begomovirus and family Geminiviridae. Tomato yellow leaf curl virus (TYLCV) infection induces severe symptoms on tomato plants and causes serious yield losses worldwide. TYLCV is persistently transmitted by the sweetpotato whitefly, Bemisia tabaci (Gennadius). Cultivars and hybrids with a single or few genes conferring resistance against TYLCV are often planted to mitigate TYLCV-induced losses. These resistant genotypes (cultivars or hybrids) are not immune to TYLCV. They typically develop systemic infection, display mild symptoms, and produce more marketable tomatoes than susceptible genotypes under TYLCV pressure.In several pathosystems, extensive use of resistant cultivars with single dominant resistance-conferring gene has led to intense selection pressure on the virus, development of highly virulent strains, and resistance breakdown.',
	'Use only virus-and whitefly-free tomato and pepper transplants. Transplants should be treated with Capture (bifenthrin) or Venom (dinotefuran) for whitefly adults and Oberon for eggs and nymphs. Imidacloprid or thiamethoxam should be used in transplant houses at least seven days before shipping. Imidacloprid should be sprayed on the entire plant and below the leaves; eggs and flies are often found below the leaves. Spray every 14-21 days and rotate on a monthly basis with Abamectin so that the whiteflies do not build-up resistance to chemicals.'
);

INSERT INTO disease_info(name, description, possible_steps) values(
	'Mosaic Virus',
	'Tomato mosaic virus (ToMV) and  Tobacco mosaic virus (TMV) are hard to distinguish.
Tomato mosaic virus (ToMV) can cause yellowing and stunting of tomato plants resulting in loss of stand and reduced yield.
ToMV may cause uneven ripening of fruit, further reducing yield.
Tobacco mosaic virus (TMV) was once thought to be more common on tomato. 
TMV is usually more of a tobacco pathogen than a tomato pathogen.Mottled light and dark green on leaves.
Young tomato leaf that is mottled light and dark green, stunted growth, curled and malformed leaves.
Tobacco Mosaic virus symptoms on a tomato seedling
If plants are infected early, they may appear yellow and stunted overall.
Leaves may be curled, malformed, or reduced in size.',
	'Use certified disease-free seed or treat your own seed.
Soak seeds in a 10% solution of trisodium phosphate (Na3PO4) for at least 15 minutes.
Or heat dry seeds to 158 °F and hold them at that temperature for two to four days.
Purchase transplants only from reputable sources. Ask about the sanitation procedures they use to prevent disease.
Inspect transplants prior to purchase. Choose only transplants showing no clear symptoms.
Avoid planting in fields where tomato root debris is present, as the virus can survive long-term in roots.
Wash hands with soap and water before and during the handling of plants to reduce potential spread between plants.'
);
            '''
        ))
        connection.commit()