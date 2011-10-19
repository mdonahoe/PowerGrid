import powerplant

powerplants = [
    (3,1,'oil',2),
    (4,1,'coal',2),
    (5,1,'oil/coal',2),
    (6,1,'garbage',1),
    (7,2,'oil',3),
    (8,2,'coal',3),
    (9,1,'oil',1),
    (10,2,'coal',2),
    (11,2,'uranium',1),
    (12,2,'oil/coal',2),
    (13,1,'eco',0),
    (14,2,'garbage',2),
    (15,3,'coal',2),
    (16,3,'oil',2),
    (17,2,'uranium',1),
    (18,2,'eco',0),
    (19,3,'garbage',2),
    (20,5,'coal',3),
    (21,4,'oil/coal',2),
    (22,2,'eco',0),
    (23,3,'uranium',1),
    (24,4,'garbage',2),
    (25,5,'coal',2),
    (26,5,'oil',2),
    (27,3,'eco',0),
    (28,4,'uranium',1),
    (29,4,'oil/coal',1),
    (30,6,'garbage',3),
    (31,6,'coal',3),
    (32,6,'oil',3),
    (33,4,'eco',0),
    (34,5,'uranium',1),
    (35,5,'oil',1),
    (36,7,'coal',3),
    (37,4,'eco',0),
    (38,7,'garbage',3),
    (39,6,'uranium',1),
    (40,6,'oil',2),
    (42,6,'coal',2),
    (44,5,'eco',0),
    (46,7,'oil/coal',3),
    (50,6,'fusion',0)
]

payments = [10,22,33,44,54,64,73,82,90,98,105,112,118,124,129,134,138,142,145,148,150]

resource_sub_markets = [
    ('coal', 24, 3, range(1,9)),
    ('oil', 18, 3, range(1,9)),
    ('garbage', 6, 3, range(1,9)),
    ('uranium', 2, 1, range(1,9)+[10,12,14,16])
]

network = {
    #purple
    'passau':{'regensburg':12,'muenchen':14},
    'regensburg':{'nuernberg':12,'augsburg':13,'muenchen':10},
    'augsburg':{'muenchen':6,'nuernberg':18,'wuerzburg':19,'stuttgart':15,'konstanz':17},
    'konstanz':{'stuttgart':16,'freiburg':14},
    'stuttgart':{'freiburg':16,'saarbruecken':17,'mannheim':6,'wuerzburg':12},
    #yellow
    'nuernberg':{'erfurt':21,'wuerzburg':8},
    'wuerzburg':{'mannheim':10,'frankfurt-m':13,'fulda':11},
    'fulda':{'frankfurt-m':8,'kassel':8,'erfurt':13},
    'erfurt':{'kassel':15,'hannover':19,'halle':6,'dresden':19},
    'halle':{'magdeburg':11,'berlin':17,'leipzig':0},
    'leipzig':{'frankfurt-d':21,'dresden':13},
    'dresden':{'frankfurt-d':16},
    #blue,
    'mannheim':{'wiesbaden':11,'saarbruecken':11},
    'saarbruecken':{'wiesbaden':10,'trier':11},
    'trier':{'aachen':19,'koeln':20,'wiesbaden':18},
    'wiesbaden':{'koeln':21,'frankfurt-m':0},
    'frankfurt-m':{'dortmund':20,'kassel':13},
    'aachen':{'duesseldorf':9,'koeln':7},
    'koeln':{'duesseldorf':4,'dortmund':10},
    #red
    'duesseldorf':{'essen':2},
    'essen':{'duisburg':0,'muenster':6,'dortmund':4},
    'kassel':{'osnabrueck':20,'hannover':15},
    'osnabrueck':{'muenster':7,'wilhelmshaven':14,'bremen':11,'hannover':16},
    'muenster':{'dortmund':2},
    #teal
    'bremen':{'wilhelmshaven':11,'cuxhaven':8,'hamburg':11,'hannover':10},
    'hannover':{'hamburg':17,'schwerin':19,'magdeburg':15},
    'hamburg':{'cuxhaven':11,'kiel':8,'luebeck':6,'schwerin':8},
    'kiel':{'flensburg':4,'luebeck':4},
    #brown
    'schwerin':{'luebeck':6,'rostock':6,'torgelow':19,'berlin':18,'magdeburg':16},
    'berlin':{'magdeburg':10,'torgelow':15,'frankfurt-d':6},
    'torgelow':{'rostock':19}
}

colors = {
    'purple':['passau','regensburg','augsburg','konstanz','stuttgart','freiburg','muenchen'],
    'yellow':['nuernberg','wuerzburg','fulda','erfurt','halle','leipzig','dresden'],
    'blue':['mannheim','saarbruecken','trier', 'wiesbaden','frankfurt-m','aachen','koeln'],
    'red':['duesseldorf','essen','kassel','osnabrueck','muenster','duisburg','dortmund'],
    'teal':['bremen','hannover','hamburg','kiel','cuxhaven','flensburg','wilhelmshaven'],
    'brown':['schwerin','berlin','torgelow','luebeck','rostock','frankfurt-d','magdeburg'],
}
