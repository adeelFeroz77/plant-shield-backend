from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shdwnhufnm:xvRNy8ZmuqNfRk$U@w-server.postgres.database.azure.com:5432/w-database?ssl=true'

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
from app.routes import notification_routes
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

engine = create_engine("postgresql://shdwnhufnm:xvRNy8ZmuqNfRk$U@w-server.postgres.database.azure.com:5432/w-database?ssl=true")
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
INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Apple', 
		'Apple, (Malus domestica), domesticated tree and fruit of the rose family (Rosaceae), one of the most widely cultivated tree fruits. Apples are predominantly grown for sale as fresh fruit, though apples are also used commercially for vinegar, juice, jelly, applesauce, and apple butter and are canned as pie stock. A significant portion of the global crop also is used for cider, wine, and brandy. Fresh apples are eaten raw or cooked. There are a variety of ways in which cooked apples are used; frequently, they are used as a pastry filling, apple pie being perhaps the archetypal American dessert. Especially in Europe, fried apples characteristically accompany certain dishes of sausage or pork. Apples provide vitamins A and C, are high in carbohydrates, and are an excellent source of dietary fibre.',
		'Malus domestica', 
		'Malus domestica is the common apple tree, cultivated for its edible fruits. There are over 7,500 known cultivars of apples worldwide, with a vast variety in size, flavor, color, and ripening time.',
		'The lifespan of an apple tree depends on the type of tree, with standard and pear trees living for over 50 years, while dwarf and semi-dwarf trees living for 15–25 years. Dwarf and semi-dwarf trees reach bearing age sooner, but their productive life is also shorter. In ideal conditions, a fruit trees lifespan may be longer',
		'24', 
		'Water young trees regularly, especially those on dwarfing or semi-dwarfing rootstocks, to help establish the root system. When fruiting, apple trees require regular watering or irrigation. The frequency of watering depends on factors such as weather and soil moisture.',
		'6 to 8 hours',
		'Apple trees require ample sunlight for proper growth and fruit production. Ensure that they are planted in a location where they receive adequate sunlight throughout the day.',
		'0 to 35°C', 
		'Apple trees can tolerate a wide range of temperatures, but they thrive in moderate climates with temperatures between 15 to 25°C. Extreme temperatures can affect fruit development and overall tree health.',
		'40-60%', 
		'Apple trees can tolerate a range of humidity levels, but moderate humidity (40-60%) is ideal.  Very high humidity can increase the risk of fungal diseases.',
		false,
	NOW());
	
INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Blueberry', 
		'The plants are deciduous perennial shrubs that range in size from 60 cm (24 inches) tall for lowbush blueberries (Vaccinium angustifolium) up to 4 metres (13 feet) tall for highbush (V. corymbosum) cultivars. They have simple elliptical leaves that are arranged alternately along the dotted stems. The plants produce clusters of small urn-shaped flowers that range in colour from white to pale pink. The fruits are true berries with many small seeds and are a deep indigo to black colour when ripe.',
		'Vaccinium angustifolium', 
		'Vaccinium angustifolium, also known as the lowbush blueberry, is a perennial shrub native to eastern and central Canada and the northeastern United States. It can grow up to 2 feet tall and wide, with multiple stems, twiggy branches, and glossy foliage that changes color with the seasons. The plant has small, white, bell-shaped flowers that are followed by edible blue fruit.',
		'Blueberry plants can live for up to 50 years or more if they are healthy and in ideal conditions. They reach full size around 8–10 years old and can remain productive for 20 years or more if they are properly pruned and the growing conditions are good.',
		'48', 
		'Blueberries prefer consistently moist soil, but not soggy.  Water deeply once a week, allowing the top inch of soil to dry slightly between waterings.  Increase watering frequency during hot or dry weather.',
		'6 to 8 hours',
		'Blueberries require full sun, or at least six hours of direct sunlight per day, to grow well. Plants will grow more slowly and produce less fruit if they are planted in too much shade.',
		'20 to 26°C', 
		'The ideal temperature for blueberry growth is between (20–26°C) during the day, with cooler nights. This range is ideal for photosynthesis and avoids cooking the plant. Nighttime temperatures should be cooler but not frosty, to maintain plant health.',
		'40-60%', 
		'Blueberry plants prefer a consistent humidity level between 40–60%. Too much humidity can create a swampy environment, while too little can make the plant feel like it is in the Sahara.',
		false,
	NOW());
	
INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Cherry', 
		'Cherry, any of various trees belonging to the genus Prunus and their edible fruits. Commercial cherry production includes tart cherries (Prunus cerasus), which are frozen or canned and used in sauces and pastries, and sweet cherries (P. avium), which are usually consumed fresh and are the principal type preserved in true or imitation maraschino liqueur. A number of species, hybrids, and cultivars are grown as ornamentals for their prolific spring flowers, and the dark red wood of some cherry species is especially esteemed for the manufacture of fine furniture. Most cherry species are native to the Northern Hemisphere. Some 10 to 12 species are recognized in North America and a similar number in Europe. The greatest concentration of species, however, appears to be in eastern Asia. The native habitat of the species from which the cultivated cherries came is believed to be in western Asia and eastern Europe from the Caspian Sea to the Balkans. Cherries are grown in all areas of the world where winter temperatures are not too severe and where summer temperatures are moderate. They require winter cold in order to blossom in spring. The trees bloom quite early in the spring, just after peaches and earlier than apples.',
		'Prunus cerasus', 
		'Prunus cerasus, also known as the sour cherry or tart cherry tree, is a deciduous shrub or small tree that is native to Europe, North Africa, and West Asia. It is a member of the rose family and is closely related to the sweet cherry (Prunus avium).',
		'The average lifespan of a cherry tree falls roughly between 30 and 40 years, depending on variety, yet the two trees planted by Taft and Chinda and a handful of other trees are still standing 111 years later.',
		'62', 
		'Cherry trees require regular watering during their first year, especially in early spring, summer, and sometimes early autumn. In the first week after planting, water cherry trees deeply every other day. In the second week, water them deeply two to three times, and after that, water them once a week for the rest of the first season. You should water cherry trees enough to soak the ground around their roots, but not so much that the roots become waterlogged',
		'6 to 8 hours',
		'Cherry trees thrive in full sun, which is at least 6 to 8 hours of sun each day. They also need well-drained, fertile soil with a pH of 6.0-7.0. Cherry trees thrive in a location that gets full sun and has a well-drained, fertile soil. “Full sun” is defined as at least 6 to 8 hours of sun each day. Sunlight is critical to fruit production and quality, and also helps keep fungal issues from getting a foothold.',
		'5 to 35°C', 
		'Cherry trees grow best in temperate climates with distinct seasons, cold winters, and warm, dry summers. Sweet cherry trees (Prunus avium) prefer cooler climates with temperatures between 41–95°F (5–35°C) and can tolerate frost in the winter. In the spring, temperatures between 59–68°F (15–20°C) are ideal for flowering.',
		'40-60%', 
		'The ideal relative humidity (RH) for Yoshino cherry trees is around 40–50%, and for flowering cherry trees have 40–60%. The right humidity level helps the cherry tree flowers be vibrant and contributes to the cherry tree overall vitality. If the humidity level is too low, the blossoms may not look as good, or the tree may develop fungal issues. If the humidity level is too high, the tree may develop fungal issues. A hygrometer can be used to monitor and adjust humidity levels indoors.',
		false,
	NOW());


INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Corn', 
		'The corn plant is a tall annual grass with a stout, erect, solid stem. The large narrow leaves have wavy margins and are spaced alternately on opposite sides of the stem. Staminate (male) flowers are borne on the tassel terminating the main axis of the stem. The pistillate (female) inflorescences, which mature to become the edible ears, are spikes with a thickened axis, bearing paired spikelets in longitudinal rows; each row of paired spikelets normally produces two rows of grain. Varieties of yellow and white corn are the most popular as food, though there are varieties with red, blue, pink, and black kernels, often banded, spotted, or striped. Each ear is enclosed by modified leaves called shucks or husks.',
		'Zea mays', 
		'Zea mays is the scientific name for corn, a member of the grass family that is grown for its cereal grain. It is also known as maize, and Indian corn. Corn is the most produced cereal in the world, grown on every continent except Antarctica. It comes in about 50 species, with different colors, textures, and grain shapes and sizes. The most common cultivated maize types are white, yellow, and red.',
		'The lifespan of a corn plant, also known as dracaena fragrans, is approximately two to three years. However, with proper care, the plant can live for decades.',
		'64', 
		'Corn plants, also known as Dracaena, prefer an environment that is moist but not soggy. A good rule of thumb is to water every 7–10 days, or when the top inch of soil feels dry. During fall and winter, you can reduce watering to when the top two inches of soil feel dry.',
		'6 to 8 hours',
		'A minimum of 6–8 hours of sunlight every day is the common growing corn plant light requirement. It is needed to grow corn away from any large trees that could cast shadows and plant tall varieties to the north or east of your field so that your shorter plants can get enough sun during the day.',
		'18 to 27°C', 
		'Corn plants do best in temperatures from 60°F to 75°F. Avoid exposing them to temperatures in the 50s. If you temporarily moved your corn plants outdoors for the summer, make sure to bring them indoors before temperatures reach this point.',
		'40-50%', 
		'Maintain humidity levels between 40 to 50 percent, which mimics the corn plant native environment. To raise your plant humidity, use a humidifier or place the pot on a tray of water and pebbles.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Grape', 
		'The grape is usually a woody vine, climbing by means of tendrils (modified branches) and when untrained often reaching a length of 17 metres (56 feet) or more. In arid regions it may form an almost erect shrub. The edible leaves are alternate, palmately lobed, and always tooth-edged. Small greenish flowers, in clusters, precede the fruit, which varies in colour from almost black to green, red, and amber. Botanically, the fruit is a berry, more or less globular, within the juicy pulp of which lie the seeds. In many varieties the fruit develops a whitish powdery coating, or bloom.',
		'Vitis vinifera', 
		'Vitis vinifera is the botanical name for grapes, encompassing numerous cultivars with varying characteristics. It is native to Eurasia and has been cultivated for thousands of years for its fruits and for winemaking. Grapevines are perennial plants that produce fruit on new growth each year.',
		'Grapevines have a long lifespan, typically ranging from 30 to 50 years under optimal growing conditions. With proper care and maintenance, some grapevines can live even longer. Pruning, trellising, and disease management are essential for prolonging the lifespan of grapevines and maintaining productivity.',
		'62', 
		'Grapes require regular watering, especially during dry periods, to support their growth and fruit development. Water plants deeply approximately every 168-240 hours, ensuring that the soil is evenly moist but not waterlogged. Avoid overhead watering to prevent fungal diseases. Mulching can help retain soil moisture and reduce weed competition.',
		'6 to 8 hours',
		'Grapes thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or along a trellis or arbor. Adequate sunlight promotes vigorous growth and higher yields.',
		'15 to 25°C', 
		'Grapes prefer moderate temperatures between 15 to 25°C for optimal growth and fruit development. They can tolerate slightly cooler temperatures but may experience slower growth below 15°C. High temperatures above 30°C can inhibit flower and fruit set. Plant grapes in well-drained soil and provide protection from frost during cold periods.',
		'50-70%', 
		'Grapes prefer moderate humidity levels between 50% to 70% during their growing season. Adequate humidity helps maintain soil moisture and promotes healthy foliage growth. However, ensure proper air circulation to prevent fungal diseases, especially in humid conditions.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Orange', 
		'Oranges (Citrus sinensis) are citrus fruits known for their bright orange color, sweet-tart flavor, and juicy pulp. They belong to the Rutaceae family and are widely cultivated in subtropical and tropical regions around the world. Oranges are commonly eaten fresh, juiced, or used in cooking, baking, and making preserves. They are rich in vitamin C, antioxidants, and dietary fiber, making them a nutritious addition to any diet.',
		'Citrus sinensis', 
		'Citrus sinensis is the botanical name for oranges, which belong to the Citrus genus within the Rutaceae family. It is believed to be a hybrid of pomelo (Citrus maxima) and mandarin (Citrus reticulata) species. Oranges come in various varieties with different flavors, sizes, and seediness.',
		'Orange trees have a long lifespan, typically ranging from 50 to 100 years under optimal growing conditions. With proper care and maintenance, some orange trees can live even longer. Pruning, fertilization, and disease management are essential for prolonging the lifespan of orange trees and maintaining fruit production.',
		'168', 
		'Orange trees require regular watering to maintain soil moisture for optimal growth and fruit production. Water trees deeply approximately every 168-336 hours, ensuring that the soil is evenly moist but not waterlogged. Adjust watering frequency based on weather conditions, rainfall, and soil moisture levels. Mulching can help conserve soil moisture and reduce weed competition.',
		'6 to 8 hours',
		'Orange trees thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or orchard. Adequate sunlight promotes vigorous growth and higher yields.',
		'15 to 30°C', 
		'Orange trees prefer moderate temperatures between 15 to 30°C for optimal growth and fruit development. They can tolerate slightly cooler temperatures but may experience slower growth below 10°C. Protect trees from frost during cold periods, as freezing temperatures can damage foliage and fruit.',
		'50-70%', 
		'Orange trees prefer moderate humidity levels between 50% to 70% during their growing season. Adequate humidity helps maintain soil moisture and promotes healthy foliage growth. However, ensure proper air circulation to prevent fungal diseases and improve pollination.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Peach', 
		'Peaches (Prunus persica) are juicy, sweet fruits that belong to the Rosaceae family. They are native to China and have been cultivated for thousands of years for their delicious flavor and nutritional benefits. Peaches come in various colors, including yellow, white, and red, and are commonly eaten fresh, canned, or used in cooking, baking, and making preserves. They are rich in vitamins, minerals, and antioxidants, making them a healthy snack or ingredient.',
		'Prunus persica', 
		'Prunus persica is the botanical name for peaches, which belong to the Prunus genus within the Rosaceae family. It is a deciduous tree that produces delicious fruits in summer. Peaches are classified into clingstone and freestone varieties based on how easily the flesh separates from the pit.',
		'Peach trees have a lifespan of 15 to 20 years under optimal growing conditions. With proper care and maintenance, some peach trees can live longer. Pruning, fertilization, and disease management are essential for prolonging the lifespan of peach trees and maintaining fruit production.',
		'168', 
		'Peach trees require regular watering to maintain soil moisture for optimal growth and fruit production. Water trees deeply approximately every 168-240 hours, ensuring that the soil is evenly moist but not waterlogged. Adjust watering frequency based on weather conditions, rainfall, and soil moisture levels. Mulching can help conserve soil moisture and reduce weed competition.',
		'6 to 8 hours',
		'Peach trees thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or orchard. Adequate sunlight promotes vigorous growth and higher yields.',
		'15 to 30°C', 
		'Peach trees prefer moderate temperatures between 15 to 30°C for optimal growth and fruit development. They can tolerate slightly cooler temperatures but may experience slower growth below 10°C. Protect trees from frost during cold periods, as freezing temperatures can damage foliage and flowers.',
		'50-70%', 
		'Peach trees prefer moderate humidity levels between 50% to 70% during their growing season. Adequate humidity helps maintain soil moisture and promotes healthy foliage growth. However, ensure proper air circulation to prevent fungal diseases and improve pollination.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Pepper Bell', 
		'Bell peppers (Capsicum annuum) are colorful, bell-shaped fruits that belong to the nightshade family (Solanaceae). They come in various colors, including green, red, yellow, and orange, and are prized for their sweet, crisp flesh. Bell peppers are versatile in cooking, commonly used in salads, stir-fries, and stuffed dishes. They are rich in vitamins A and C, as well as antioxidants, making them a nutritious addition to any diet.',
		'Capsicum annuum', 
		'Capsicum annuum is the botanical name for bell peppers, which belong to the Capsicum genus within the Solanaceae family. It is one of the most common and widely cultivated species of peppers, known for its mild flavor and crisp texture.',
		'Bell pepper plants typically have a lifespan of 2 years under optimal growing conditions. However, they are often grown as annuals in temperate climates, replanted each year for the best yields. Proper care, including regular watering, fertilization, and pest management, can help prolong the lifespan of bell pepper plants.',
		'48', 
		'Bell pepper plants require consistent moisture to thrive. Water plants deeply approximately every 48-72 hours, ensuring that the soil is evenly moist but not waterlogged. During hot and dry periods, increase watering frequency as needed to prevent the soil from drying out completely. Mulching can help retain soil moisture and reduce the frequency of watering.',
		'6 to 8 hours',
		'Bell pepper plants thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or container, to promote healthy foliage and abundant fruiting.',
		'18 to 30°C', 
		'Bell pepper plants prefer moderate temperatures between 18 to 30°C. They can tolerate slightly cooler temperatures but may experience slower growth below 18°C. High temperatures above 30°C can inhibit flowering and fruit set, leading to reduced yields. Provide protection during temperature extremes to ensure optimal growth and fruit production.',
		'40-60%', 
		'Bell pepper plants prefer moderate humidity levels between 40% to 60%. Adequate humidity promotes healthy growth and fruit development while reducing the risk of stress-related problems. However, ensure proper air circulation to prevent fungal diseases in humid conditions.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Potato', 
		'Potatoes (Solanum tuberosum) are starchy tuberous vegetables that are widely cultivated for their edible underground tubers. They are one of the most important food crops in world and are consumed in various forms, including boiled, mashed, fried, and baked. Potatoes come in numerous varieties with different skin colors, flesh colors, and textures, offering a wide range of culinary possibilities. They are rich in carbohydrates, vitamins, minerals, and dietary fiber, making them a nutritious staple food.',
		'Solanum tuberosum', 
		'Solanum tuberosum is the botanical name for potatoes, belonging to the Solanaceae family. It is native to the Andes region of South America and has been cultivated for thousands of years. Potatoes are grown worldwide in diverse climates and soil conditions, with numerous cultivars adapted to different growing environments.',
		'Potatoes are typically harvested within 3 to 5 months after planting, depending on the variety and growing conditions. While individual plants have a relatively short lifespan, potatoes can be stored for several months after harvest under proper storage conditions. Early, mid, and late-season varieties allow for staggered harvesting throughout the growing season.',
		'96', 
		'Potatoes require regular watering to maintain soil moisture for tuber development. Water plants deeply approximately every 96-168 hours, ensuring that the soil is evenly moist but not waterlogged. During dry periods, increase watering frequency as needed to prevent the soil from drying out completely. Mulching can help conserve soil moisture and reduce the frequency of watering.',
		'6 to 8 hours',
		'Potatoes thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and tuber production. Plant them in a location with ample sunlight exposure, ensuring that they receive sufficient light throughout the day. Adequate sunlight promotes vigorous foliage growth and higher yields.',
		'15 to 20°C', 
		'Potatoes prefer moderate temperatures between 15 to 20°C for optimal growth and tuber development. They can tolerate cooler temperatures but may experience slower growth below 10°C. High temperatures above 25°C can inhibit tuber formation and lead to heat stress. Plant potatoes in early spring when soil temperatures are suitable for planting.',
		'70-80%', 
		'Potatoes prefer moderate to high humidity levels between 70% to 80% during their growing period. Adequate humidity helps maintain soil moisture and promotes healthy foliage growth. However, ensure proper air circulation to prevent fungal diseases such as late blight, especially in humid conditions.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Raspberry', 
		'Raspberries (Rubus idaeus) are delicious, sweet-tart berries that belong to the Rosaceae family. They are highly prized for their vibrant color, juicy texture, and distinct flavor. Raspberries come in various colors, including red, black, purple, and gold, with each variety offering unique taste characteristics. They are commonly eaten fresh, added to desserts, or used in jams, jellies, and baked goods. Raspberries are rich in vitamins, minerals, and antioxidants, making them a nutritious addition to any diet.',
		'Rubus idaeus', 
		'Rubus idaeus is the botanical name for raspberries, which belong to the Rubus genus within the Rosaceae family. It is native to Europe and Asia and has been cultivated for centuries for its delicious fruits. Raspberries are perennial plants with biennial canes that produce fruit in their second year of growth.',
		'Raspberry plants have a lifespan of 10 to 12 years under optimal growing conditions. While individual canes live for two years, new canes emerge each year to replace older ones, ensuring continuous fruit production. Proper care, including pruning, fertilization, and disease management, can help prolong the lifespan of raspberry plants and maintain productivity.',
		'48', 
		'Raspberries require regular watering to maintain soil moisture for optimal growth and fruit development. Water plants deeply approximately every 48-72 hours, ensuring that the soil is evenly moist but not waterlogged. During dry periods, increase watering frequency as needed to prevent the soil from drying out completely. Mulching can help retain soil moisture and reduce weed competition.',
		'6 to 8 hours',
		'Raspberries thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or along a south-facing fence or wall. Adequate sunlight promotes vigorous growth and higher yields.',
		'18 to 25°C', 
		'Raspberries prefer moderate temperatures between 18 to 25°C for optimal growth and fruit development. They can tolerate slightly cooler temperatures but may experience slower growth below 18°C. High temperatures above 25°C can inhibit flower and fruit set. Plant raspberries in early spring or late autumn when temperatures are suitable for planting.',
		'50-70%', 
		'Raspberries prefer moderate temperatures between 18 to 25°C for optimal growth and fruit development. They can tolerate slightly cooler temperatures but may experience slower growth below 18°C. High temperatures above 25°C can inhibit flower and fruit set. Plant raspberries in early spring or late autumn when temperatures are suitable for planting.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Soybean', 
		'Soybean (Glycine max) is a versatile legume known for its high protein content and oil-rich seeds. It is widely cultivated for various purposes, including human consumption, animal feed, and industrial applications. Soybeans are used to produce products such as soy milk, tofu, soy sauce, and cooking oil. They are also a major source of protein in vegetarian diets and play a crucial role in global food security.',
		'Glycine max', 
		'Glycine max is the scientific name for soybean, belonging to the Fabaceae family. It is native to East Asia and has been domesticated for thousands of years. Soybeans exhibit considerable genetic diversity, with numerous varieties adapted to different growing conditions and uses.',
		'Soybean plants are typically grown as annuals, completing their life cycle within one year. They are sown in spring or early summer, grow throughout the summer months, and are harvested in late summer or autumn. While individual plants have a relatively short lifespan, soybeans are a valuable crop due to their high yield potential and wide range of applications.',
		'72', 
		'Soybeans require regular watering to support their growth and development. Water plants deeply every 72-120 hours, allowing the soil to dry slightly between waterings. Adjust watering frequency based on weather conditions, rainfall, and soil moisture levels to maintain optimal soil moisture for plant growth.',
		'6 to 8 hours',
		'Soybeans thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and yield. Plant them in a location with ample sunlight exposure, ensuring that they receive sufficient light throughout the day. Adequate sunlight promotes photosynthesis, leading to healthy plant growth and higher yields.',
		'20 to 30°C', 
		'Soybeans prefer moderate temperatures between 20 to 30°C for optimal growth and development. They are sensitive to both cold and heat stress, with temperatures below 20°C slowing growth and temperatures above 30°C affecting flowering and pod formation. Plant soybeans after the danger of frost has passed and provide protection during temperature extremes.',
		'50-80%', 
		'Soybeans thrive in moderate to high humidity environments, with relative humidity levels between 50% to 80%. Adequate humidity promotes healthy plant growth and pod development. However, ensure proper air circulation to prevent fungal diseases, particularly during periods of high humidity.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Squash', 
		'Squash refers to several species of trailing or bushy plants belonging to the Cucurbita genus. These plants produce fruits that vary widely in shape, size, color, and flavor. Squash is classified into two main types: summer squash, harvested when immature and eaten fresh, and winter squash, harvested when mature and stored for later consumption. Squash fruits are rich in vitamins, minerals, and dietary fiber, making them a nutritious addition to various dishes.',
		'Cucurbita spp', 
		'Cucurbita spp. encompasses several species of squash, including Cucurbita pepo, Cucurbita moschata, Cucurbita maxima, and Cucurbita mixta. Each species has its own unique characteristics and varieties.',
		'Squash plants typically have a lifespan of 1 to 2 years, with productivity declining after the first year. While some varieties may exhibit longer lifespans under optimal conditions, most squash plants are considered annuals or short-lived perennials. Proper care, including regular watering, fertilization, and pest management, can help prolong the lifespan of squash plants.',
		'48', 
		'Squash plants require consistent moisture throughout their growth cycle. Water plants deeply every 48-72 hours, allowing the soil to dry slightly between waterings. Adjust watering frequency based on weather conditions and soil moisture levels, aiming to keep the soil evenly moist but not waterlogged.',
		'6 to 8 hours',
		'Squash plants thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, ensuring that they receive sufficient light to develop healthy foliage and fruits.',
		'18 to 30°C', 
		'Squash plants prefer moderate temperatures between 18 to 30°C. They can tolerate slightly cooler temperatures but may experience slower growth below 18°C. High temperatures above 30°C can inhibit pollination and fruit set, leading to reduced yields.',
		'50-70%', 
		'Squash plants prefer moderate to high humidity levels between 50% to 70%. Adequate humidity helps promote healthy growth and fruit development while reducing the risk of stress-related problems. However, ensure proper air circulation to prevent fungal diseases in humid conditions.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Strawberry', 
		'Strawberries (Fragaria × ananassa) are popular fruits known for their sweet, juicy flavor and vibrant red color. They are commonly enjoyed fresh, added to desserts, or used in jams, jellies, and sauces. Strawberries are rich in vitamin C, fiber, and antioxidants, making them a nutritious addition to any diet.',
		'Fragaria × ananassa', 
		'Fragaria × ananassa is the hybrid species of cultivated strawberries, originating from the crossbreeding of Fragaria chiloensis and Fragaria virginiana. It belongs to the rose family (Rosaceae) and is widely cultivated for its delicious fruits.',
		'Strawberry plants typically remain productive for 3 to 5 years before their productivity declines, requiring renovation or replanting for continued vigor and yield.',
		'48', 
		'Strawberries require consistent moisture to thrive. Water plants deeply every 48-72 hours, ensuring that the soil is kept evenly moist but not waterlogged. During hot and dry periods, increase watering frequency to prevent the soil from drying out completely. Avoid overhead watering to minimize the risk of fungal diseases. Adjust watering based on weather conditions and soil moisture levels.',
		'6 to 8 hours',
		'Strawberries thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Plant them in a location with ample sunlight exposure, such as a sunny garden bed or a sunny spot in a container.',
		'15 to 25°C', 
		'Strawberries prefer moderate temperatures between 15 to 25°C. They can tolerate slightly cooler temperatures but may experience slower growth below 15°C. High temperatures above 25°C can inhibit flowering and fruiting, leading to reduced yields.',
		'40-60%', 
		'Strawberries prefer moderate humidity levels between 40% to 60%. High humidity can increase the risk of fungal diseases such as botrytis (gray mold) and powdery mildew. Provide adequate air circulation around the plants to reduce humidity levels and minimize disease pressure.',
		false,
	NOW());

INSERT INTO plant(
	plant_name,
	description,
	species,
	species_detail,
	max_life,
	watering_schedule,
	watering_schedule_detail,
	sunlight_requirements,
	sunlight_requirements_detail,
	temperature_requirements,
	temperature_requirements_detail,
	humidity,
	humidity_detail,
	is_favorite,
	created_date)
	VALUES (
		'Tomato', 
		'Tomatoes (Solanum lycopersicum) are a widely cultivated fruit known for their versatility in culinary applications. They are prized for their juicy flesh and sweet-tart flavor, making them a staple in salads, sauces, soups, and sandwiches. Tomatoes come in various sizes, shapes, and colors, including red, yellow, orange, and even purple. They are rich in vitamins A and C, as well as antioxidants like lycopene, which is associated with numerous health benefits.',
		'Solanum lycopersicum', 
		'Solanum lycopersicum is the botanical name for the tomato plant, belonging to the nightshade family (Solanaceae). It is native to western South America and has been cultivated for thousands of years.',
		'Indeterminate varieties of tomato plants can live for several years in optimal conditions, while determinate varieties typically have a lifespan of one growing season.',
		'24', 
		'Tomatoes require consistent moisture throughout their growth cycle. Water young plants every 24-48 hours, aiming to keep the soil consistently moist but not waterlogged. During periods of fruit development, increase watering frequency as needed to ensure proper fruit formation. Adjust watering based on weather conditions such as rainfall and soil moisture levels.',
		'6 to 8 hours',
		'Tomatoes thrive in full sunlight and require at least 6 to 8 hours of direct sunlight daily for optimal growth and fruit production. Ensure they are planted in a location with ample sunlight exposure.',
		'15 to 30°C', 
		'Tomatoes prefer moderate temperatures between 15 to 30°C. They can tolerate slightly cooler temperatures but may experience slower growth below 15°C. High temperatures above 30°C can inhibit fruit set and lead to sunburn on fruits.',
		'40-70%', 
		'Tomatoes can tolerate a wide range of humidity levels, but they perform best in moderate humidity environments. Aim for relative humidity levels between 40% to 70%. High humidity coupled with poor air circulation can increase the risk of fungal diseases like blight and powdery mildew.',
		false,
	NOW());
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
        


scheduler = BackgroundScheduler()
scheduler.add_job(func=notification_routes.schedule_notification, trigger="cron", hour='*')
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))