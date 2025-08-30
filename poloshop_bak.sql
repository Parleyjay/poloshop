BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "authtoken_token" ("key" varchar(40) NOT NULL PRIMARY KEY, "created" datetime NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_api" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "key" varchar(200) NULL, "date_added" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_brand" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "date_created" datetime NULL);
CREATE TABLE IF NOT EXISTS "backend_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "complete" bool NOT NULL, "customer_id" bigint NULL REFERENCES "backend_customer" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer NULL, "cart_id" bigint NULL REFERENCES "backend_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NULL REFERENCES "backend_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "date_created" datetime NULL);
CREATE TABLE IF NOT EXISTS "backend_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NULL, "email" varchar(200) NOT NULL, "user_type" varchar(10) NOT NULL, "user_id" integer NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_delivery" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "delivery_method_id" bigint NULL REFERENCES "backend_deliverymethod" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "backend_deliverystatus" ("id") DEFERRABLE INITIALLY DEFERRED, "order_id" bigint NULL REFERENCES "backend_order" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_deliverymethod" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "mode" varchar(100) NULL, "created_at" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_deliverystatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(100) NULL, "created_at" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_inventory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "created_date" datetime NOT NULL, "modified_date" datetime NOT NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "modified_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "backend_inventorystatus" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "backend_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_inventorystatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL, "created_date" datetime NOT NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "cart_id" bigint NOT NULL UNIQUE REFERENCES "backend_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "customer_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "backend_orderstatus" ("id") DEFERRABLE INITIALLY DEFERRED, "shipping_address_id" bigint NULL REFERENCES "backend_shippingaddress" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_id" bigint NULL REFERENCES "backend_transaction" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_orderstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL UNIQUE, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_paymentmethod" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "method" varchar(100) NULL, "date_added" datetime NOT NULL, "APIkey_id" bigint NULL REFERENCES "backend_api" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "description" text NULL, "image" varchar(100) NULL, "price" decimal NULL, "date_created" datetime NULL, "brand_id" bigint NULL REFERENCES "backend_brand" ("id") DEFERRABLE INITIALLY DEFERRED, "category_id" bigint NULL REFERENCES "backend_category" ("id") DEFERRABLE INITIALLY DEFERRED, "creator_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "product_document_id" bigint NULL REFERENCES "backend_productdocument" ("id") DEFERRABLE INITIALLY DEFERRED, "product_status_id" bigint NULL REFERENCES "backend_productstatus" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_productdocument" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "file_path" varchar(255) NOT NULL, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_productstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "backend_review" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "title" varchar(255) NOT NULL, "message" text NOT NULL, "created_date" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "backend_product" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_savedproducts" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_date" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "backend_product" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_shippingaddress" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address" varchar(200) NOT NULL, "city" varchar(200) NOT NULL, "region" varchar(200) NOT NULL, "phone" varchar(200) NOT NULL, "date_added" datetime NOT NULL, "cart_id" bigint NULL REFERENCES "backend_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "customer_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "backend_transaction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "amount" integer NOT NULL, "reference" varchar(100) NOT NULL UNIQUE, "verified" bool NOT NULL, "date_added" datetime NOT NULL, "customer_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "store_brand" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "date_created" datetime NULL);
CREATE TABLE IF NOT EXISTS "store_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "complete" bool NOT NULL, "customer_id" bigint NULL REFERENCES "store_customer" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer NULL, "cart_id" bigint NULL REFERENCES "store_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NULL REFERENCES "store_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "date_created" datetime NULL);
CREATE TABLE IF NOT EXISTS "store_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NULL, "email" varchar(200) NOT NULL, "user_type" varchar(10) NOT NULL, "user_id" integer NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_inventory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "created_date" datetime NOT NULL, "modified_date" datetime NOT NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "modified_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "store_product" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "store_inventorystatus" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_inventorystatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL, "created_date" datetime NOT NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "payment_id" varchar(255) NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "cart_id" bigint NOT NULL UNIQUE REFERENCES "store_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "customer_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "shipping_address_id" bigint NULL REFERENCES "store_shippingaddress" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "store_orderstatus" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_orderstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL UNIQUE, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "store_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NULL, "description" text NULL, "price" decimal NULL, "date_created" datetime NULL, "brand_id" bigint NULL REFERENCES "store_brand" ("id") DEFERRABLE INITIALLY DEFERRED, "category_id" bigint NULL REFERENCES "store_category" ("id") DEFERRABLE INITIALLY DEFERRED, "creator_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "product_status_id" bigint NULL REFERENCES "store_productstatus" ("id") DEFERRABLE INITIALLY DEFERRED, "product_document_id" bigint NULL REFERENCES "store_productdocument" ("id") DEFERRABLE INITIALLY DEFERRED, "image" varchar(100) NULL);
CREATE TABLE IF NOT EXISTS "store_productdocument" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "file_path" varchar(255) NOT NULL, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "store_productstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NOT NULL, "created_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "store_review" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "title" varchar(255) NOT NULL, "message" text NOT NULL, "created_date" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "store_product" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_savedproducts" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_date" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "store_product" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "store_shippingaddress" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address" varchar(200) NOT NULL, "city" varchar(200) NOT NULL, "region" varchar(200) NOT NULL, "phone" varchar(200) NOT NULL, "date_added" datetime NOT NULL, "cart_id" bigint NULL REFERENCES "store_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "customer_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_brand','Can add brand'),
 (2,1,'change_brand','Can change brand'),
 (3,1,'delete_brand','Can delete brand'),
 (4,1,'view_brand','Can view brand'),
 (5,2,'add_productstatus','Can add product status'),
 (6,2,'change_productstatus','Can change product status'),
 (7,2,'delete_productstatus','Can delete product status'),
 (8,2,'view_productstatus','Can view product status'),
 (9,3,'add_category','Can add category'),
 (10,3,'change_category','Can change category'),
 (11,3,'delete_category','Can delete category'),
 (12,3,'view_category','Can view category'),
 (13,4,'add_customer','Can add customer'),
 (14,4,'change_customer','Can change customer'),
 (15,4,'delete_customer','Can delete customer'),
 (16,4,'view_customer','Can view customer'),
 (17,5,'add_cart','Can add cart'),
 (18,5,'change_cart','Can change cart'),
 (19,5,'delete_cart','Can delete cart'),
 (20,5,'view_cart','Can view cart'),
 (21,6,'add_product','Can add product'),
 (22,6,'change_product','Can change product'),
 (23,6,'delete_product','Can delete product'),
 (24,6,'view_product','Can view product'),
 (25,7,'add_cartitem','Can add cart item'),
 (26,7,'change_cartitem','Can change cart item'),
 (27,7,'delete_cartitem','Can delete cart item'),
 (28,7,'view_cartitem','Can view cart item'),
 (29,8,'add_shippingaddress','Can add shipping address'),
 (30,8,'change_shippingaddress','Can change shipping address'),
 (31,8,'delete_shippingaddress','Can delete shipping address'),
 (32,8,'view_shippingaddress','Can view shipping address'),
 (33,9,'add_token','Can add Token'),
 (34,9,'change_token','Can change Token'),
 (35,9,'delete_token','Can delete Token'),
 (36,9,'view_token','Can view Token'),
 (37,10,'add_tokenproxy','Can add Token'),
 (38,10,'change_tokenproxy','Can change Token'),
 (39,10,'delete_tokenproxy','Can delete Token'),
 (40,10,'view_tokenproxy','Can view Token'),
 (41,11,'add_logentry','Can add log entry'),
 (42,11,'change_logentry','Can change log entry'),
 (43,11,'delete_logentry','Can delete log entry'),
 (44,11,'view_logentry','Can view log entry'),
 (45,12,'add_permission','Can add permission'),
 (46,12,'change_permission','Can change permission'),
 (47,12,'delete_permission','Can delete permission'),
 (48,12,'view_permission','Can view permission'),
 (49,13,'add_group','Can add group'),
 (50,13,'change_group','Can change group'),
 (51,13,'delete_group','Can delete group'),
 (52,13,'view_group','Can view group'),
 (53,14,'add_user','Can add user'),
 (54,14,'change_user','Can change user'),
 (55,14,'delete_user','Can delete user'),
 (56,14,'view_user','Can view user'),
 (57,15,'add_contenttype','Can add content type'),
 (58,15,'change_contenttype','Can change content type'),
 (59,15,'delete_contenttype','Can delete content type'),
 (60,15,'view_contenttype','Can view content type'),
 (61,16,'add_session','Can add session'),
 (62,16,'change_session','Can change session'),
 (63,16,'delete_session','Can delete session'),
 (64,16,'view_session','Can view session'),
 (65,17,'add_productdocument','Can add product document'),
 (66,17,'change_productdocument','Can change product document'),
 (67,17,'delete_productdocument','Can delete product document'),
 (68,17,'view_productdocument','Can view product document'),
 (69,18,'add_inventorystatus','Can add inventory status'),
 (70,18,'change_inventorystatus','Can change inventory status'),
 (71,18,'delete_inventorystatus','Can delete inventory status'),
 (72,18,'view_inventorystatus','Can view inventory status'),
 (73,19,'add_inventory','Can add inventory'),
 (74,19,'change_inventory','Can change inventory'),
 (75,19,'delete_inventory','Can delete inventory'),
 (76,19,'view_inventory','Can view inventory'),
 (77,20,'add_savedproducts','Can add saved products'),
 (78,20,'change_savedproducts','Can change saved products'),
 (79,20,'delete_savedproducts','Can delete saved products'),
 (80,20,'view_savedproducts','Can view saved products'),
 (81,21,'add_review','Can add review'),
 (82,21,'change_review','Can change review'),
 (83,21,'delete_review','Can delete review'),
 (84,21,'view_review','Can view review'),
 (85,22,'add_orderstatus','Can add order status'),
 (86,22,'change_orderstatus','Can change order status'),
 (87,22,'delete_orderstatus','Can delete order status'),
 (88,22,'view_orderstatus','Can view order status'),
 (89,23,'add_order','Can add order'),
 (90,23,'change_order','Can change order'),
 (91,23,'delete_order','Can delete order'),
 (92,23,'view_order','Can view order'),
 (93,24,'add_api','Can add api'),
 (94,24,'change_api','Can change api'),
 (95,24,'delete_api','Can delete api'),
 (96,24,'view_api','Can view api'),
 (97,25,'add_paymentmethod','Can add payment method'),
 (98,25,'change_paymentmethod','Can change payment method'),
 (99,25,'delete_paymentmethod','Can delete payment method'),
 (100,25,'view_paymentmethod','Can view payment method'),
 (101,26,'add_inventory','Can add inventory'),
 (102,26,'change_inventory','Can change inventory'),
 (103,26,'delete_inventory','Can delete inventory'),
 (104,26,'view_inventory','Can view inventory'),
 (105,27,'add_review','Can add review'),
 (106,27,'change_review','Can change review'),
 (107,27,'delete_review','Can delete review'),
 (108,27,'view_review','Can view review'),
 (109,28,'add_customer','Can add customer'),
 (110,28,'change_customer','Can change customer'),
 (111,28,'delete_customer','Can delete customer'),
 (112,28,'view_customer','Can view customer'),
 (113,29,'add_productstatus','Can add product status'),
 (114,29,'change_productstatus','Can change product status'),
 (115,29,'delete_productstatus','Can delete product status'),
 (116,29,'view_productstatus','Can view product status'),
 (117,30,'add_shippingaddress','Can add shipping address'),
 (118,30,'change_shippingaddress','Can change shipping address'),
 (119,30,'delete_shippingaddress','Can delete shipping address'),
 (120,30,'view_shippingaddress','Can view shipping address'),
 (121,31,'add_brand','Can add brand'),
 (122,31,'change_brand','Can change brand'),
 (123,31,'delete_brand','Can delete brand'),
 (124,31,'view_brand','Can view brand'),
 (125,32,'add_deliverymethod','Can add delivery method'),
 (126,32,'change_deliverymethod','Can change delivery method'),
 (127,32,'delete_deliverymethod','Can delete delivery method'),
 (128,32,'view_deliverymethod','Can view delivery method'),
 (129,33,'add_product','Can add product'),
 (130,33,'change_product','Can change product'),
 (131,33,'delete_product','Can delete product'),
 (132,33,'view_product','Can view product'),
 (133,34,'add_inventorystatus','Can add inventory status'),
 (134,34,'change_inventorystatus','Can change inventory status'),
 (135,34,'delete_inventorystatus','Can delete inventory status'),
 (136,34,'view_inventorystatus','Can view inventory status'),
 (137,35,'add_category','Can add category'),
 (138,35,'change_category','Can change category'),
 (139,35,'delete_category','Can delete category'),
 (140,35,'view_category','Can view category'),
 (141,36,'add_transaction','Can add transaction'),
 (142,36,'change_transaction','Can change transaction'),
 (143,36,'delete_transaction','Can delete transaction'),
 (144,36,'view_transaction','Can view transaction'),
 (145,37,'add_savedproducts','Can add saved products'),
 (146,37,'change_savedproducts','Can change saved products'),
 (147,37,'delete_savedproducts','Can delete saved products'),
 (148,37,'view_savedproducts','Can view saved products'),
 (149,38,'add_orderstatus','Can add order status'),
 (150,38,'change_orderstatus','Can change order status'),
 (151,38,'delete_orderstatus','Can delete order status'),
 (152,38,'view_orderstatus','Can view order status'),
 (153,39,'add_order','Can add order'),
 (154,39,'change_order','Can change order'),
 (155,39,'delete_order','Can delete order'),
 (156,39,'view_order','Can view order'),
 (157,40,'add_delivery','Can add delivery'),
 (158,40,'change_delivery','Can change delivery'),
 (159,40,'delete_delivery','Can delete delivery'),
 (160,40,'view_delivery','Can view delivery'),
 (161,41,'add_deliverystatus','Can add delivery status'),
 (162,41,'change_deliverystatus','Can change delivery status'),
 (163,41,'delete_deliverystatus','Can delete delivery status'),
 (164,41,'view_deliverystatus','Can view delivery status'),
 (165,42,'add_cart','Can add cart'),
 (166,42,'change_cart','Can change cart'),
 (167,42,'delete_cart','Can delete cart'),
 (168,42,'view_cart','Can view cart'),
 (169,43,'add_productdocument','Can add product document'),
 (170,43,'change_productdocument','Can change product document'),
 (171,43,'delete_productdocument','Can delete product document'),
 (172,43,'view_productdocument','Can view product document'),
 (173,44,'add_cartitem','Can add cart item'),
 (174,44,'change_cartitem','Can change cart item'),
 (175,44,'delete_cartitem','Can delete cart item'),
 (176,44,'view_cartitem','Can view cart item');
INSERT INTO "auth_user" ("id","password","last_login","is_superuser","username","last_name","email","is_staff","is_active","date_joined","first_name") VALUES (1,'pbkdf2_sha256$1000000$b8WAdOD8UWF3Gs4B07Ju9C$AIRH94jjLG9ZcYHLdWDLPMnbZ9BNNNDxPM8ef5Xaiek=','2025-08-09 19:27:50.041885',1,'admin','','parleystanley8@gmail.com',1,1,'2025-07-21 13:57:30.227622',''),
 (2,'pbkdf2_sha256$1000000$5ysUQleODIc2qRhLCqH2re$VR/7weBhwG7reDGM5Ie49s18EIHEmJ1xv8COLY9AMj0=','2025-08-30 01:45:14.368948',0,'Felix','Gyakari','felix@gmail.com',0,1,'2025-07-21 14:04:40.152317','Felix'),
 (3,'pbkdf2_sha256$1000000$gi5iic4UkJMfm76o7i64HJ$xYNB+jzugR4nPIV/Xtv+52yCN5A1WoUgMZ8ak5jiBPA=','2025-08-07 11:25:15.709109',0,'Jack','','jackson@gmail.com',0,1,'2025-07-22 17:17:25.302341',''),
 (4,'pbkdf2_sha256$1000000$5aQB2SccySaQrKckhVk5R9$ULW3uNK2gH8iNFUjXG1aPcQc3xonARRrI3TAEgpCfYA=','2025-08-07 12:02:16.259514',0,'James','','james@bond.com',0,1,'2025-08-07 12:02:00.766543','');
INSERT INTO "backend_product" ("id","name","description","image","price","date_created","brand_id","category_id","creator_id","product_document_id","product_status_id") VALUES (1,'Dunks','Sneakers that will leave you in awe. Comfortable piece','products/nightpaint.jpeg',300,NULL,1,1,3,NULL,1),
 (2,'Track Pants','Street wear for gym and casual comfort.','products/Iceland.jpeg',80,NULL,2,1,1,NULL,1),
 (3,'School bag','Pack all your school essentials in one place and carry with ease','products/Halloween.jpeg',45,NULL,1,1,1,NULL,1),
 (5,'Rolex','A timeless piece worn by the most classy','products/watch.jpg',250,NULL,3,1,1,NULL,1),
 (6,'Code base','Guide to building your own projects','products/sourcecode.jpg',120,NULL,3,2,3,NULL,1),
 (7,'Headphones','Hear every sound like a pro','products/headphones.jpg',240,NULL,1,2,1,NULL,1),
 (8,'Book','Read to your heart desires','products/book.jpg',20,NULL,1,1,1,NULL,1),
 (9,'Shirt','Nice to wear','products/shirt.jpg',70,NULL,2,1,1,NULL,1),
 (10,'Shoes','Comfortable','products/shoes.jpg',500,NULL,2,1,1,NULL,1);
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (1,'1','Fashion category',1,'[{"added": {}}]',3,1,'2025-07-21 14:00:26.343887'),
 (2,'1','Nike brand',1,'[{"added": {}}]',1,1,'2025-07-21 14:00:48.592489'),
 (3,'1','In stock',1,'[{"added": {}}]',2,1,'2025-07-21 14:01:38.171030'),
 (4,'2','Out of stock',1,'[{"added": {}}]',2,1,'2025-07-21 14:12:07.543305'),
 (5,'3','Discontinued',1,'[{"added": {}}]',2,1,'2025-07-21 14:12:16.016375'),
 (6,'1','Active',2,'[{"changed": {"fields": ["Status"]}}]',2,1,'2025-07-21 14:14:12.758818'),
 (7,'1','Dunks',2,'[{"changed": {"fields": ["Product status"]}}]',6,1,'2025-07-21 14:16:52.003890'),
 (8,'1','Dunks',2,'[{"changed": {"fields": ["Product status"]}}]',6,1,'2025-07-21 14:17:27.328182'),
 (9,'1','In Stock',1,'[{"added": {}}]',18,1,'2025-07-21 14:38:45.903107'),
 (10,'2','Reserved',1,'[{"added": {}}]',18,1,'2025-07-21 14:39:05.963414'),
 (11,'3','Sold',1,'[{"added": {}}]',18,1,'2025-07-21 14:39:20.528825'),
 (12,'4','Damaged',1,'[{"added": {}}]',18,1,'2025-07-21 14:39:35.796248'),
 (13,'5','Returned',1,'[{"added": {}}]',18,1,'2025-07-21 14:39:55.920778'),
 (14,'6','Out of Stock',1,'[{"added": {}}]',18,1,'2025-07-21 14:40:12.140286'),
 (15,'1','Inventory object (1)',1,'[{"added": {}}]',19,1,'2025-07-21 14:46:22.481421'),
 (16,'1','Inventory object (1)',2,'[{"changed": {"fields": ["Status"]}}]',19,1,'2025-07-21 14:48:14.573493'),
 (17,'1','Available',2,'[{"changed": {"fields": ["Status"]}}]',2,1,'2025-07-21 15:11:04.653247'),
 (18,'1','Dunks',2,'[{"changed": {"fields": ["Product status"]}}]',6,1,'2025-07-21 15:11:55.143859'),
 (19,'1','Good - Dunks',1,'[{"added": {}}]',21,1,'2025-07-21 15:18:54.648832'),
 (20,'2','Jack',2,'[{"changed": {"fields": ["User type"]}}]',4,1,'2025-07-22 17:18:30.792521'),
 (21,'3','Inventory object (3)',3,'',19,1,'2025-07-23 10:25:18.233445'),
 (22,'4','School bag',3,'',6,1,'2025-07-23 10:28:15.802328'),
 (23,'3','Felix - School bag (2 stars)',3,'',21,1,'2025-07-25 18:11:32.158096'),
 (24,'2','Felix - Track Pants (5 stars)',3,'',21,1,'2025-07-25 18:11:37.268053'),
 (25,'1','Felix - Dunks (4 stars)',3,'',21,1,'2025-07-25 18:11:42.036862'),
 (26,'3','School bag',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-07-27 09:01:16.640617'),
 (27,'2','Track Pants',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-07-27 09:09:46.518021'),
 (28,'1','Dunks',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-07-27 09:09:59.635824'),
 (29,'5','Rolex',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-07-27 09:30:34.684033'),
 (30,'1','Dunks',2,'[{"changed": {"fields": ["Creator"]}}]',6,1,'2025-07-28 07:56:06.108202'),
 (31,'6','Code base',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-08-04 19:11:02.699580'),
 (32,'7','Headphones',1,'[{"added": {}}]',6,1,'2025-08-04 19:12:43.506544'),
 (33,'7','Headphones',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-08-04 19:13:06.024953'),
 (34,'8','Book',1,'[{"added": {}}]',6,1,'2025-08-04 19:14:21.946284'),
 (35,'8','Book',2,'[{"changed": {"fields": ["Image"]}}]',6,1,'2025-08-04 19:14:42.224383'),
 (36,'9','Shirt',1,'[{"added": {}}]',6,1,'2025-08-04 19:15:31.606998'),
 (37,'10','Shoes',1,'[{"added": {}}]',6,1,'2025-08-04 19:16:45.294722'),
 (38,'1','Pending',1,'[{"added": {}}]',22,1,'2025-08-09 19:16:18.395523'),
 (39,'2','Processing',1,'[{"added": {}}]',22,1,'2025-08-09 19:16:25.348231'),
 (40,'3','Shipped',1,'[{"added": {}}]',22,1,'2025-08-09 19:16:30.823431'),
 (41,'4','Cancelled',1,'[{"added": {}}]',22,1,'2025-08-09 19:16:34.779060'),
 (42,'5','Delivered',1,'[{"added": {}}]',22,1,'2025-08-09 19:17:16.934213'),
 (43,'1','Order 1 - Felix (Pending)',1,'[{"added": {}}]',23,1,'2025-08-09 19:17:38.819579'),
 (44,'2','Order 2 - Jack (Pending)',1,'[{"added": {}}]',23,1,'2025-08-09 19:17:54.066225'),
 (45,'3','Order 3 - James (Pending)',1,'[{"added": {}}]',23,1,'2025-08-09 19:18:13.420568'),
 (46,'4','Order 4 - James (Processing)',1,'[{"added": {}}]',23,1,'2025-08-09 19:18:37.182111'),
 (47,'9','CartItem for Cart 4 - Customer: James',1,'[{"added": {}}]',7,1,'2025-08-09 19:22:02.549643');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'store','brand'),
 (2,'store','productstatus'),
 (3,'store','category'),
 (4,'store','customer'),
 (5,'store','cart'),
 (6,'store','product'),
 (7,'store','cartitem'),
 (8,'store','shippingaddress'),
 (9,'authtoken','token'),
 (10,'authtoken','tokenproxy'),
 (11,'admin','logentry'),
 (12,'auth','permission'),
 (13,'auth','group'),
 (14,'auth','user'),
 (15,'contenttypes','contenttype'),
 (16,'sessions','session'),
 (17,'store','productdocument'),
 (18,'store','inventorystatus'),
 (19,'store','inventory'),
 (20,'store','savedproducts'),
 (21,'store','review'),
 (22,'store','orderstatus'),
 (23,'store','order'),
 (24,'backend','api'),
 (25,'backend','paymentmethod'),
 (26,'backend','inventory'),
 (27,'backend','review'),
 (28,'backend','customer'),
 (29,'backend','productstatus'),
 (30,'backend','shippingaddress'),
 (31,'backend','brand'),
 (32,'backend','deliverymethod'),
 (33,'backend','product'),
 (34,'backend','inventorystatus'),
 (35,'backend','category'),
 (36,'backend','transaction'),
 (37,'backend','savedproducts'),
 (38,'backend','orderstatus'),
 (39,'backend','order'),
 (40,'backend','delivery'),
 (41,'backend','deliverystatus'),
 (42,'backend','cart'),
 (43,'backend','productdocument'),
 (44,'backend','cartitem');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2025-07-21 13:55:26.521026'),
 (2,'auth','0001_initial','2025-07-21 13:55:26.824119'),
 (3,'admin','0001_initial','2025-07-21 13:55:27.059875'),
 (4,'admin','0002_logentry_remove_auto_add','2025-07-21 13:55:27.231320'),
 (5,'admin','0003_logentry_add_action_flag_choices','2025-07-21 13:55:27.357569'),
 (6,'contenttypes','0002_remove_content_type_name','2025-07-21 13:55:27.588819'),
 (7,'auth','0002_alter_permission_name_max_length','2025-07-21 13:55:27.726586'),
 (8,'auth','0003_alter_user_email_max_length','2025-07-21 13:55:27.855304'),
 (9,'auth','0004_alter_user_username_opts','2025-07-21 13:55:27.979691'),
 (10,'auth','0005_alter_user_last_login_null','2025-07-21 13:55:28.126367'),
 (11,'auth','0006_require_contenttypes_0002','2025-07-21 13:55:28.256205'),
 (12,'auth','0007_alter_validators_add_error_messages','2025-07-21 13:55:28.387739'),
 (13,'auth','0008_alter_user_username_max_length','2025-07-21 13:55:28.554472'),
 (14,'auth','0009_alter_user_last_name_max_length','2025-07-21 13:55:28.712423'),
 (15,'auth','0010_alter_group_name_max_length','2025-07-21 13:55:28.889166'),
 (16,'auth','0011_update_proxy_permissions','2025-07-21 13:55:29.142075'),
 (17,'auth','0012_alter_user_first_name_max_length','2025-07-21 13:55:29.298775'),
 (18,'authtoken','0001_initial','2025-07-21 13:55:29.454256'),
 (19,'authtoken','0002_auto_20160226_1747','2025-07-21 13:55:29.638713'),
 (20,'authtoken','0003_tokenproxy','2025-07-21 13:55:29.780652'),
 (21,'authtoken','0004_alter_tokenproxy_options','2025-07-21 13:55:29.924442'),
 (22,'sessions','0001_initial','2025-07-21 13:55:30.184786'),
 (23,'store','0001_initial','2025-07-21 13:55:30.566352'),
 (24,'store','0002_alter_product_brand','2025-07-21 13:55:30.723572'),
 (25,'store','0003_productdocument_remove_category_creator_and_more','2025-07-21 14:25:23.472585'),
 (26,'store','0004_inventorystatus','2025-07-21 14:27:08.957786'),
 (27,'store','0005_inventory','2025-07-21 14:28:33.582789'),
 (28,'store','0006_savedproducts','2025-07-21 14:31:35.944619'),
 (29,'store','0007_alter_inventory_modified_by_and_more','2025-07-21 15:17:49.894033'),
 (30,'store','0008_remove_review_created_by_product_image_and_more','2025-07-27 09:00:36.628645'),
 (31,'store','0009_orderstatus_order','2025-08-09 19:15:06.745312'),
 (32,'store','0010_remove_order_total_price','2025-08-09 19:15:06.782523'),
 (33,'backend','0001_initial','2025-08-30 01:06:37.613150');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('l2emaqsakozaypgb3d09ki7gm1miw225','.eJxVjDsOwjAQBe_iGlmxvf5R0nMGa9fe4ABypDipEHeHSCmgfTPzXiLhtta0dV7SVMRZKHH63Qjzg9sOyh3bbZZ5busykdwVedAur3Ph5-Vw_w4q9vqtQQM6BCZtRl0yF_baoQrWeQ84qBAUGqOiATc6skOEDC7EiOQpWp_F-wPSEzce:1uj0a6:YprY7qXOTYxB4CJvq2wHDbcweZrUHqp4-zPxFIfIpcI','2025-08-18 19:10:46.949052'),
 ('8gnxy7yl51nu56z1ubhanyas782l33xr','.eJxVjDsOwjAQBe_iGlmxvf5R0nMGa9fe4ABypDipEHeHSCmgfTPzXiLhtta0dV7SVMRZKHH63Qjzg9sOyh3bbZZ5busykdwVedAur3Ph5-Vw_w4q9vqtQQM6BCZtRl0yF_baoQrWeQ84qBAUGqOiATc6skOEDC7EiOQpWp_F-wPSEzce:1ujzIl:NtvSQFU8ISxM9qiAi22SIPnRR-bKBqg3hEeDEi1Y-UE','2025-08-21 12:00:55.954087'),
 ('7lvo2abypbfefnn3h4j4ecgvdr5mophf','.eJxVjMsOwiAQAP-FsyHL0-LRu99AdhcqVQNJaU_GfzckPeh1ZjJvEXHfStx7XuOSxEVYcfplhPzMdYj0wHpvklvd1oXkSORhu7y1lF_Xo_0bFOxlbNlbH2zWSaNVnjyBR6XdmZwx4Ay77AjIqzCzNWCYOUwQXAae0MAsPl_CsDct:1ujzK4:Rn9z1qde9YD8NNeOmVVxJh1IOs4D_s53glt-LBAbqyM','2025-08-21 12:02:16.269719'),
 ('21ilx1dey4cgw4n9bxb18dvcjsicvgjj','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1ukrbJ:sxpM0KQTxUnrVE2uTHMbVSKKmGC9XuBIu2ANhRDKAYE','2025-08-23 21:59:41.083268'),
 ('jlc7l7gj97bah0j7d7jbjnyxl3s4ux6n','.eJxVjDsOwjAQBe_iGlmxvf5R0nMGa9fe4ABypDipEHeHSCmgfTPzXiLhtta0dV7SVMRZKHH63Qjzg9sOyh3bbZZ5busykdwVedAur3Ph5-Vw_w4q9vqtQQM6BCZtRl0yF_baoQrWeQ84qBAUGqOiATc6skOEDC7EiOQpWp_F-wPSEzce:1ukpEM:XjATzuLmWQ2MhJo5p8Luk27MzTv0GPuhmMi7hxJb3Bk','2025-08-23 19:27:50.046889'),
 ('xqq8bouroa0jpq5xd10qc9xqf760rsxy','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1ukvXd:oNafszY5i78XFJlJ9dpOjW_EheG96A0LG7bbXDyOoMM','2025-08-24 02:12:09.363277'),
 ('7igu19sie31ke6j9cr56mm7bwnppi9db','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1ukwuF:ZRzGKmdVXlUcL0vZWjD95mQX6w_q0XkTf7S6Uf3gT0k','2025-08-24 03:39:35.752052'),
 ('jmc64d3guhkwcoapa92ixszj9y74kh8k','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1ukwuG:mjnUz1SlQp6b6l4DHKx-76bTuFdnsK44L5SbHEOAj2w','2025-08-24 03:39:36.841281'),
 ('wc5bx0g014e79uabq5yxzk29v3ymw90h','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1ul4sR:WJ999JuIaCxEjDZOSvzVa56N4cj0uDt58-ZdATuYFmo','2025-08-24 12:10:15.835671'),
 ('rxv02w04jzlrym82hw7zbjf5tsboaxvy','.eJxVjEEOwiAQRe_C2hCEgYJL956BwMxUqgaS0q6Md7dNutDtf-_9t4hpXUpcO89xInERWpx-t5zwyXUH9Ej13iS2usxTlrsiD9rlrRG_rof7d1BSL1uNyiiHwNqAs5y9pTOFQY_KO2eUDwlIQwCjCAbryCBnJNhgBuARjfh8Ab-wN0s:1usAeY:Insu2XZ4qLSOKe6wseGDBsA3eXlKdQJQ4Dl2REjlIJw','2025-09-13 01:45:14.377259');
INSERT INTO "store_brand" ("id","name","date_created") VALUES (1,'Nike','2025-07-21 14:00:48.585277'),
 (2,'Addidas','2025-07-22 17:12:41.414956'),
 (3,'Rolex','2025-07-27 09:26:46.854890');
INSERT INTO "store_cart" ("id","created_at","complete","customer_id") VALUES (1,'2025-07-21 14:05:08.212255',0,1),
 (2,'2025-07-27 18:08:55.113673',0,2),
 (3,'2025-08-07 12:02:18.927285',1,3),
 (4,'2025-08-07 12:04:29.378692',0,3);
INSERT INTO "store_cartitem" ("id","quantity","cart_id","product_id") VALUES (1,1,1,1),
 (2,2,1,3),
 (5,1,2,5),
 (6,1,2,3),
 (7,1,3,7),
 (8,1,3,8),
 (9,1,4,7),
 (10,2,1,7);
INSERT INTO "store_category" ("id","name","date_created") VALUES (1,'Fashion','2025-07-21 14:00:26.342336'),
 (2,'Tech','2025-08-04 19:09:30.129350');
INSERT INTO "store_customer" ("id","name","email","user_type","user_id") VALUES (1,'Felix','felix@gmail.com','buyer',2),
 (2,'Jack','jackson@gmail.com','seller',3),
 (3,'James','james@bond.com','buyer',4);
INSERT INTO "store_inventory" ("id","quantity","created_date","modified_date","created_by_id","modified_by_id","product_id","status_id") VALUES (1,5,'2025-07-21 14:46:22.475694','2025-07-21 14:48:14.573493',1,NULL,1,1),
 (2,2,'2025-07-23 10:17:10.559946','2025-07-23 10:17:10.559946',1,NULL,2,1),
 (4,10,'2025-07-23 10:28:35.254239','2025-07-23 10:28:35.254239',NULL,NULL,3,1);
INSERT INTO "store_inventorystatus" ("id","status","created_date","created_by_id") VALUES (1,'In Stock','2025-07-21 14:38:45.899392',1),
 (2,'Reserved','2025-07-21 14:39:05.955273',1),
 (3,'Sold','2025-07-21 14:39:20.522400',1),
 (4,'Damaged','2025-07-21 14:39:35.791829',1),
 (5,'Returned','2025-07-21 14:39:55.913105',1),
 (6,'Out of Stock','2025-07-21 14:40:12.138105',1);
INSERT INTO "store_order" ("id","payment_id","created_at","updated_at","cart_id","customer_id","shipping_address_id","status_id") VALUES (1,'1','2025-08-09 19:17:38.819579','2025-08-09 19:17:38.819579',1,2,1,1),
 (2,'2','2025-08-09 19:17:54.066225','2025-08-09 19:17:54.066225',2,3,2,1),
 (3,'3','2025-08-09 19:18:13.419063','2025-08-09 19:18:13.419063',3,4,3,1),
 (4,'4','2025-08-09 19:18:37.179660','2025-08-09 19:18:37.180658',4,4,3,2);
INSERT INTO "store_orderstatus" ("id","status","created_date") VALUES (1,'Pending','2025-08-09 19:16:18.393521'),
 (2,'Processing','2025-08-09 19:16:25.345924'),
 (3,'Shipped','2025-08-09 19:16:30.821427'),
 (4,'Cancelled','2025-08-09 19:16:34.776215'),
 (5,'Delivered','2025-08-09 19:17:16.932201');
INSERT INTO "store_product" ("id","name","description","price","date_created","brand_id","category_id","creator_id","product_status_id","product_document_id","image") VALUES (1,'Dunks','Sneakers that will leave you in awe. Comfortable piece',300,'2025-07-21 14:03:44.158777',1,1,3,1,NULL,'products/nightpaint.jpeg'),
 (2,'Track Pants','Street wear for gym and casual comfort.',80,'2025-07-22 17:36:18.916999',2,1,1,1,NULL,'products/Iceland.jpeg'),
 (3,'School bag','Pack all your school essentials in one place and carry with ease',45,'2025-07-23 10:27:29.259020',1,1,1,1,NULL,'products/Halloween.jpeg'),
 (5,'Rolex','A timeless piece worn by the most classy',250,'2025-07-27 09:30:04.129896',3,1,1,1,NULL,'products/watch.jpg'),
 (6,'Code base','Guide to building your own projects',120,'2025-08-04 19:10:27.226270',3,2,3,1,NULL,'products/sourcecode.jpg'),
 (7,'Headphones','Hear every sound like a pro',240,'2025-08-04 19:12:43.504538',1,2,1,1,NULL,'products/headphones.jpg'),
 (8,'Book','Read to your heart desires',20,'2025-08-04 19:14:21.940742',1,1,1,1,NULL,'products/book.jpg'),
 (9,'Shirt','Nice to wear',70,'2025-08-04 19:15:31.603986',2,1,1,1,NULL,'products/shirt.jpg'),
 (10,'Shoes','Comfortable',500,'2025-08-04 19:16:45.292179',2,1,1,1,NULL,'products/shoes.jpg');
INSERT INTO "store_productstatus" ("id","status","created_date") VALUES (1,'Available','2025-07-21 14:01:38.168522'),
 (2,'Out of stock','2025-07-21 14:12:07.541209'),
 (3,'Discontinued','2025-07-21 14:12:16.012017');
INSERT INTO "store_review" ("id","rating","title","message","created_date","product_id","user_id") VALUES (4,4,'Excellent','Convenient for carrying all my school essentials','2025-07-25 18:14:16.718975',3,2),
 (6,4,'Good','very quality','2025-07-27 18:00:55.307728',5,3),
 (7,4,'Awesome','Very comfortable to wear','2025-07-27 18:06:40.772124',2,3),
 (8,3,'Excellent','This is cool','2025-07-27 18:54:50.813244',5,2),
 (9,5,'Awesome','easy to carry around','2025-07-28 07:52:57.011218',3,3),
 (10,5,'Good','Just do it alright','2025-07-28 07:55:27.870838',1,3);
INSERT INTO "store_savedproducts" ("id","created_date","product_id","user_id") VALUES (8,'2025-07-24 17:32:29.211882',2,2),
 (9,'2025-07-25 17:29:05.096905',3,2),
 (10,'2025-07-27 17:52:36.283655',5,2),
 (11,'2025-07-27 18:10:15.010694',1,3);
INSERT INTO "store_shippingaddress" ("id","address","city","region","phone","date_added","cart_id","customer_id") VALUES (1,'Lakeside University Avenue','Accra','Greater Accra','0554706223','2025-07-27 08:31:33.247827',1,2),
 (2,'P.O. Box 331','Kumasi','Ashanti Region','0554706225','2025-08-07 11:34:00.909949',2,3),
 (3,'P.O. Box 331','Kumasi','Ashanti Region','0554706225','2025-08-07 12:03:25.062369',3,4);
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "backend_cart_customer_id_c15bcdfe" ON "backend_cart" ("customer_id");
CREATE INDEX "backend_cartitem_cart_id_643117c5" ON "backend_cartitem" ("cart_id");
CREATE INDEX "backend_cartitem_product_id_452696cb" ON "backend_cartitem" ("product_id");
CREATE INDEX "backend_delivery_delivery_method_id_0c28de97" ON "backend_delivery" ("delivery_method_id");
CREATE INDEX "backend_delivery_order_id_ed26665a" ON "backend_delivery" ("order_id");
CREATE INDEX "backend_delivery_status_id_8f89178a" ON "backend_delivery" ("status_id");
CREATE INDEX "backend_inventory_created_by_id_21f9924d" ON "backend_inventory" ("created_by_id");
CREATE INDEX "backend_inventory_modified_by_id_72db11d0" ON "backend_inventory" ("modified_by_id");
CREATE INDEX "backend_inventory_product_id_78f42578" ON "backend_inventory" ("product_id");
CREATE INDEX "backend_inventory_status_id_ae2dd6dd" ON "backend_inventory" ("status_id");
CREATE INDEX "backend_inventorystatus_created_by_id_97ee1a5f" ON "backend_inventorystatus" ("created_by_id");
CREATE INDEX "backend_order_customer_id_bbb93e8b" ON "backend_order" ("customer_id");
CREATE INDEX "backend_order_payment_id_ba3b3c49" ON "backend_order" ("payment_id");
CREATE INDEX "backend_order_shipping_address_id_bc9f9e5b" ON "backend_order" ("shipping_address_id");
CREATE INDEX "backend_order_status_id_2c5c8019" ON "backend_order" ("status_id");
CREATE INDEX "backend_paymentmethod_APIkey_id_0d4c1551" ON "backend_paymentmethod" ("APIkey_id");
CREATE INDEX "backend_product_brand_id_156bbfc9" ON "backend_product" ("brand_id");
CREATE INDEX "backend_product_category_id_d4f6d780" ON "backend_product" ("category_id");
CREATE INDEX "backend_product_creator_id_fca799c4" ON "backend_product" ("creator_id");
CREATE INDEX "backend_product_product_document_id_6fec926f" ON "backend_product" ("product_document_id");
CREATE INDEX "backend_product_product_status_id_2f181e74" ON "backend_product" ("product_status_id");
CREATE INDEX "backend_review_product_id_242faefe" ON "backend_review" ("product_id");
CREATE INDEX "backend_review_user_id_ee348b0d" ON "backend_review" ("user_id");
CREATE INDEX "backend_sav_user_id_1cb619_idx" ON "backend_savedproducts" ("user_id", "product_id");
CREATE INDEX "backend_savedproducts_product_id_c450c162" ON "backend_savedproducts" ("product_id");
CREATE INDEX "backend_savedproducts_user_id_05ce05a3" ON "backend_savedproducts" ("user_id");
CREATE UNIQUE INDEX "backend_savedproducts_user_id_product_id_8af7973d_uniq" ON "backend_savedproducts" ("user_id", "product_id");
CREATE INDEX "backend_shippingaddress_cart_id_83df4cfc" ON "backend_shippingaddress" ("cart_id");
CREATE INDEX "backend_shippingaddress_customer_id_7cd464cc" ON "backend_shippingaddress" ("customer_id");
CREATE INDEX "backend_transaction_customer_id_bbb8ebe0" ON "backend_transaction" ("customer_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "store_cart_customer_id_e7ee89e3" ON "store_cart" ("customer_id");
CREATE INDEX "store_cartitem_cart_id_4f60ac05" ON "store_cartitem" ("cart_id");
CREATE INDEX "store_cartitem_product_id_4238d443" ON "store_cartitem" ("product_id");
CREATE INDEX "store_inventory_created_by_id_c6fbbc6f" ON "store_inventory" ("created_by_id");
CREATE INDEX "store_inventory_modified_by_id_96f1cdbc" ON "store_inventory" ("modified_by_id");
CREATE INDEX "store_inventory_product_id_07402474" ON "store_inventory" ("product_id");
CREATE INDEX "store_inventory_status_id_6627fd8f" ON "store_inventory" ("status_id");
CREATE INDEX "store_inventorystatus_created_by_id_f6e0fbb4" ON "store_inventorystatus" ("created_by_id");
CREATE INDEX "store_order_customer_id_13d6d43e" ON "store_order" ("customer_id");
CREATE INDEX "store_order_shipping_address_id_9d19a8a7" ON "store_order" ("shipping_address_id");
CREATE INDEX "store_order_status_id_4789c92a" ON "store_order" ("status_id");
CREATE INDEX "store_product_brand_id_ec9e66ab" ON "store_product" ("brand_id");
CREATE INDEX "store_product_category_id_574bae65" ON "store_product" ("category_id");
CREATE INDEX "store_product_creator_id_2641f1d4" ON "store_product" ("creator_id");
CREATE INDEX "store_product_product_document_id_c19a2195" ON "store_product" ("product_document_id");
CREATE INDEX "store_product_product_status_id_03b4d7e5" ON "store_product" ("product_status_id");
CREATE INDEX "store_review_product_id_abc413b2" ON "store_review" ("product_id");
CREATE INDEX "store_review_user_id_cc54d86d" ON "store_review" ("user_id");
CREATE INDEX "store_saved_user_id_d238f7_idx" ON "store_savedproducts" ("user_id", "product_id");
CREATE INDEX "store_savedproducts_product_id_5d4ff3b1" ON "store_savedproducts" ("product_id");
CREATE INDEX "store_savedproducts_user_id_c0fa040a" ON "store_savedproducts" ("user_id");
CREATE UNIQUE INDEX "store_savedproducts_user_id_product_id_4f9ff574_uniq" ON "store_savedproducts" ("user_id", "product_id");
CREATE INDEX "store_shippingaddress_cart_id_0bb1f686" ON "store_shippingaddress" ("cart_id");
CREATE INDEX "store_shippingaddress_customer_id_66e362a6" ON "store_shippingaddress" ("customer_id");
COMMIT;
