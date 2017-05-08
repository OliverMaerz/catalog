# Catalog App

Very simple Catalog App written in python for a Udacity course. 

The required libraries are listed in the requirements.txt file.

The app is currently setup for postgress. Setup an empty database on your postgress an configure db name, credentials etc. in config.py ``SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/catalog'``. The tables will be automatically created the first time the app is run (see below.)

The app uses Google Oauth 2.0 for authentication. You can setup Google Oauth by configuring the client ID in app/google_auth/controller.py ``googleauth_id = '< YOUR GOOGLE OAUTH ID >'`` and then by copying the client secret to app/config/client_secret.json. For more info and details on how to generate the credentials please visit: https://developers.google.com/identity/protocols/OAuth2

To start the app run 'run.py'. 

The first time you run 'run.py' the database tables will be setup automatically and you are ready to go. Once the website is running create some categories by logging in and then selecting the "Edit Categories" menu. Next create some items via the "Add Item" menu (requires at least one category).

If using Udacity's vagrant virtual machine then the default url should be http://localhost:8000/ and the JSON endpoint should be at http://localhost:8000/catalog/json/ 

You can also load some sample categories directly on your postgres server with the following sql:

```
INSERT INTO "public"."category"("id","date_created","date_modified","name")
VALUES
(13,E'2017-05-08 01:46:20.378092',E'2017-05-08 01:46:20.378092',E'Frisbee'),
(12,E'2017-05-08 01:45:53.910956',E'2017-05-08 01:45:53.910956',E'Snowboarding'),
(11,E'2017-05-08 01:45:37.750502',E'2017-05-08 01:45:37.750502',E'Hockey'),
(10,E'2017-05-08 01:45:06.759074',E'2017-05-08 01:45:06.759074',E'Skating'),
(9,E'2017-05-08 01:44:54.150976',E'2017-05-08 01:44:54.150976',E'Rock Climbing'),
(8,E'2017-05-08 01:44:42.572014',E'2017-05-08 01:44:42.572014',E'Basketball'),
(7,E'2017-05-08 01:44:35.451474',E'2017-05-08 01:44:35.451474',E'Baseball'),
(6,E'2017-05-08 01:44:12.793999',E'2017-05-08 01:44:12.793999',E'Skiing'),
(3,E'2017-05-08 01:43:55.012303',E'2017-05-08 01:43:55.012303',E'Soccer');
```

You can also load some sample items directly on your postgres db with the sql below. But make sure you log into the website at least once first - so the user with the user.id '1' is created.  

```
INSERT INTO "public"."item"("id","date_created","date_modified","title","description","category_id","user_id")
VALUES
(2,E'2017-05-08 01:51:15.476859',E'2017-05-08 03:21:51.329975',E'Bat',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',7,1),
(4,E'2017-05-08 03:22:07.191742',E'2017-05-08 03:22:07.191742',E'Goggles',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',12,1),
(5,E'2017-05-08 03:22:41.848914',E'2017-05-08 03:22:41.848914',E'Snowboard',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',12,1),
(6,E'2017-05-08 03:23:06.089494',E'2017-05-08 03:23:06.089494',E'Two shinguards',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',3,1),
(7,E'2017-05-08 03:23:24.259928',E'2017-05-08 03:23:24.259928',E'Shinguards',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',3,1),
(8,E'2017-05-08 03:23:37.766098',E'2017-05-08 03:23:37.766098',E'Frisbee',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',13,1),
(9,E'2017-05-08 03:24:01.770587',E'2017-05-08 03:24:01.770587',E'Jersey',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',3,1),
(10,E'2017-05-08 03:24:18.221624',E'2017-05-08 03:24:18.221624',E'Soccer Cleats',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',3,1),
(11,E'2017-05-08 03:24:37.552713',E'2017-05-08 03:24:37.552713',E'Ball',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',7,1),
(12,E'2017-05-08 03:24:47.589723',E'2017-05-08 03:24:47.589723',E'Ball',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',3,1),
(13,E'2017-05-08 03:25:10.583954',E'2017-05-08 03:25:10.583954',E'Ball',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',8,1),
(14,E'2017-05-08 03:25:54.063606',E'2017-05-08 03:25:54.063606',E'Stick',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',11,1),
(15,E'2017-05-08 03:26:23.657435',E'2017-05-08 03:26:23.657435',E'Skates',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',10,1),
(16,E'2017-05-08 03:26:34.940043',E'2017-05-08 03:26:34.940043',E'Boots',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',6,1),
(17,E'2017-05-08 03:26:50.61632',E'2017-05-08 03:26:50.61632',E'Skis',E'Lorem ipsum dolor sit amet, at natum cotidieque neglegentur sed, falli reprehendunt at vis. Nec id aperiam nusquam singulis, per te brute mucius appellantur, vis solet menandri id. Et eos errem apeirian, quo no tibique appetere salutatus. Cibo modus neglegentur et pri, mel essent aliquando ad, an sit quis dolor. Scripta iuvaret no pri, cu sapientem temporibus vel. Enim nonumes ponderum mel ex.',6,1);
```

