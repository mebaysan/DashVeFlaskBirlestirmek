# Languages
- [Türkçe](#dash-ve-flask-birleştirmek)
- [English](#combining-dash-and-flask)


# Dash ve Flask Birleştirmek
[PDF Linki](https://drive.google.com/file/d/1jy65z91ytZShthRkem8gx2qZvGSUQcf4/view?usp=sharing)
## Kullanılan Teknolojiler (Requirements)
- Flask
- Dash & Dash Bootstrap Components
- Plotly
- Pandas
- Tüm paketler için **req.txt** dosyasına bakabilirsiniz
## Proje Yapısı (Structure)
### Structure
- Proje **wsgi.py** dosyasından ayağa kalkar
- Kök dizindeki **fetch_all.py** dosyası sayesinde (sisteme eklenmiş cronjob bu dosyayı çalıştırır) tüm dash uygulama dizinlerinin altındaki fetch_data.py dosyası çalıştırılır.
    - Bu sayede her gece 00 00'da veri ambarından güncel veriler çekilir ve 03 00'da python projemiz yeniden başlatılır ve güncel veriler dashboard'lara dahil edilmiş olur.
- **__init__.py** ana FLASK uygulamamızı oluşturur
- **app.py** ana FLASK uygulamamıza ait bileşenleri barındırır (blueprints, routes, handlers vb)
- Ana dizindeki **myconfig.py** dosyası Flask uygulamasına ait ayarları tutmaktadır (static path, development mode vb.)
- Proje ile ilgili bütün fonksiyonlar, modüller, paketler vb **flaskapp** klasörü altında toplanmıştır
- **flaskapp/dashboard** klasörü altından DASH uygulamalarına erişebiliriz
- **flaskapp/dashboard/utilites/database_config.py** dosyası ambara bağlanılacak olan pymssql config bilgilerini içerir
- **flaskapp/dashboard/utilities** klasörü altında işimizi kolaylaştıracak fonksiyonlar bulunmaktadır, varsa kendi yazdığımız componentler vb, veya dash uygulamalarının uyumluluğu için CSS sabitleri
- **flaskapp/static** klasörü altında FLASK uygulamasına ait static dosyalar (bootstrap, jquery vb) tutulmaktadır
- **flaskapp/templates** klasörü altında FLASK uygulamasına ait route'ların döndürdüğü template (jinja2, html vb) dosyaları tutulmaktadır
- **flaskapp/dashboard/apps** klasörü altında **her bir** dash uygulamasına ait klasörler bulunmaktadır
    -  **app.py** altında DASH uygulaması ayağa kalkar
        - **BASE_URL** sabitleri iframe olarak kullanılacak linki bize vermektedir. -> ÖR: www.xyz.com/BASE_URL
        - **APP_NAME** sabitleri DASH uygulamasını FLASK'a gönderirken (navbar, context processors vb) hangi isimle anılacağını belirler
    - **data.py** altında DASH uygulamasına gönderilecek olan veri hazırlanır/çekilir
    - **fetch_data.py** altında veri ambarından veriler çekilir, işlenir ve bulunduğu dizine csv olarak export edilir
    - **\*.xlsx/\*.csv** dosyaları eğer veri seti SQL'den çekilmeyecekse aynı dizin altına eklenir

### Dizin Yapısı
```
.
├── README.md
├── config.py 
├── flaskapp 
│   ├── __init__.py 
│   ├── dashboard
│   │   ├── apps 
│   │   │   ├── dash_uygulamasi_1
│   │   │   │   ├── veriseti.csv 
│   │   │   │   ├── app.py 
│   │   │   │   └── data.py 
│   │   │   │   └── fetch_data 
│   │   ├── layout.py 
│   │   ├── urls.py 
│   │   └── utilities
│   │       ├── style.py
│   │       └── tables.py
│   ├── app.py 
│   ├── db.py 
│   ├── login.py 
│   ├── template_filters.py 
│   ├── context_processors.py 
│   ├── static 
│   ├── admin
│   │    ├── app.py
│   └── templates
│       │── dashboard_basic.jinja2
│       ├── index.jinja2
│       ├── layout.jinja2
│       └── admin
│           ├── index.jinja2
│           └── user_detail.jinja2
├── req.txt 
└── wsgi.py
└── fetch_all.py

```

### Çalışma Mantığı
**__init__.py** altında bir FLASK uygulaması oluştururuz. 

**app.py** altında çekirdek FLASK uygulamamıza ait bileşenleri tanımlarız.

Ardından oluşturduğumuz her DASH uygulamasını initialize ederken server parametresini oluşturduğumuz FLASK uygulaması olarak set ederiz. 

Bu sayede Tüm DASH uygulamalarımız ve FLASK uygulamamız aynı server üzerinde çalışır.

FLASK uygulaması ayağa kalkarken ona bind ettiğimiz DASH uygulamaları da ayağa kalkar. urls.py içerisinde tanımlanmış iframe url'leri sayesinde FLASK uygulamamız içerisinde DASH uygulamalarımızı kullanabiliriz.

/dashboard/urls.py altında her app'imizin kendine ait olan CONFIG sabitlerini ekleriz. Bu sayede bu sabitler üzerinden route işlemlerimizi gerçekleştirebiliriz.

**wsgi.py** dosyasından FLASK uygulamamızı çağırırız (haliyle ona bind edilmiş tüm DASH'ler) ve sunucuda serve ederiz.

**fetch_all.py** dosyası altında tüm dash uygulamalarına ait olan fetch_data modülleri çağrılır ve fetch_data fonksiyonları çalıştırılır. Bu satede cronjob gece önce bu dosyayı çalıştıracak ve uzun süren bir vakit alacak. Bu işlem tamamlandıktan sonra ise flask uygulamamızı yeniden başlatacak. Bu sayede çekilen yeni veriler projeye dahil edilmiş olacak.

### Örnek Bir CONFIG Sabiti
```
CONFIG = {
    'BASE_URL': '/pure/dashboard-adi/', # iframe adresi
    'APP_URL': 'dashboard-adi', # navbar'da listelenen ve route işlemini gerçekleştirmemizi sağlayan key ('/' kullanılmamalıdır) aynı zamanda bu sabit sayesinde yetkilendirme işlemini de yapabiliriz
    'APP_NAME': 'Dashboard Adı', # template'de gözükecek isim
    'MIN_HEIGHT': 1500 # iframe için gerekli olan minimum yükseklik
}
```


# Combining Dash and Flask
[Turkish PDF Link where each code is explained in detail](https://drive.google.com/file/d/1jy65z91ytZShthRkem8gx2qZvGSUQcf4/view?usp=sharing)
## Technologies Used (Requirements)
- Flask
- Dash & Dash Bootstrap Components
- Plotly
- Pandas
- You can check the **req.txt** file for all packages.
## Project Structure
### Structure
- Project stands up from **wsgi.py** file
- Thanks to the **fetch_all.py** file in the root directory (cronjob attached to the system runs this file) fetch_data.py under all dash application directories is run.
    - In this way, updated data is taken from the data warehouse every night at 00:00 and our python project is restarted at 03:00 and the current data is included in the dashboards.
- **__init.py__** creates our main FLASK application
- **app.py** contains components of our main FLASK application (blueprints, routes, handlers etc)
- The **myconfig.py** file in the main directory holds the settings of the Flask application (static path, development mode etc.).
- All functions, modules, packages etc. related to the project are collected under the **flaskapp** folder.
- We can access DASH applications under the **flaskapp/dashboard** folder.
- **flaskapp/dashboard/utilites/database_config.py** file contains pymssql config information to connect to the warehouse
- There are functions to make our work easier under the **flaskapp/dashboard/utilities** folder, if any, components etc.
- Under the **flaskapp/static** folder, static files (bootstrap, jquery etc.) of the FLASK application are kept.
- Under the **flaskapp/templates** folder, the template files (jinja2, html etc.) returned by the routes belonging to the FLASK application are kept.
- Under the **flaskapp/dashboard/apps** folder, there are folders **for each dash** application.
    -  Under **app.py** DASH app stands up
        - **BASE_URL** constants give us the link to be used as an iframe. -> EX: www.xyz.com/BASE_URL
        - **APP_NAME** constants determine the name of the DASH application when sending it to FLASK (navbar, context processors, etc.)
    - The data to be sent to the DASH application under **data.py** is prepared / pulled
    - Under **fetch_data.py** data is extracted from the data warehouse, processed and exported as csv to the directory where it is located.
    - **\*.xlsx/\*.csv** files are added under the same directory if the data set is not extracted from SQL

### Directory Structure
```
.
├── README.md
├── config.py 
├── flaskapp 
│   ├── __init__.py 
│   ├── dashboard
│   │   ├── apps 
│   │   │   ├── dash_uygulamasi_1
│   │   │   │   ├── veriseti.csv 
│   │   │   │   ├── app.py 
│   │   │   │   └── data.py 
│   │   │   │   └── fetch_data 
│   │   ├── layout.py 
│   │   ├── urls.py 
│   │   └── utilities
│   │       ├── style.py
│   │       └── tables.py
│   ├── app.py 
│   ├── db.py 
│   ├── login.py 
│   ├── template_filters.py 
│   ├── context_processors.py 
│   ├── static 
│   ├── admin
│   │    ├── app.py
│   └── templates
│       │── dashboard_basic.jinja2
│       ├── index.jinja2
│       ├── layout.jinja2
│       └── admin
│           ├── index.jinja2
│           └── user_detail.jinja2
├── req.txt 
└── wsgi.py
└── fetch_all.py

```

### Working logic
We create a FLASK application under **__init__.py**.

Under **app.py** we define components of our core FLASK application.

Then, while initializing each DASH application we create, we set the server parameter as the FLASK application we created. 

In this way, all our DASH applications and our FLASK application run on the same server.

While the FLASK application stands up, the DASH applications we mount on it also stand up. Thanks to the iframe urls defined in urls.py, we can use our DASH applications in our FLASK application.

Under /dashboard/urls.py, we add the CONFIG constants for each app. In this way, we can perform our route operations through these constants.

We call our FLASK application from **wsgi.py** file (naturally all DASHs binded to it) and serve on the server.

Under the **fetch_all.py** file, fetch_data modules belonging to all dash applications are called and fetch_data functions are executed. In this satte the cronjob will run this file the night before and it will take a long time. After this process is completed, it will restart our flask application. In this way, the new data captured will be included in the project.

### An Example CONFIG Constant
```
CONFIG = {
    'BASE_URL': '/pure/dashboard-name/', # iframe address (url)
    'APP_URL': 'dashboard-name', # The key ('/' should not be used), which is listed on the navbar and enables us to perform the route operation, at the same time we can do the authorization process thanks to this constant.
    'APP_NAME': 'Dashboard Name', # name to appear in template (Flask)
    'MIN_HEIGHT': 1500 # Minimum height required for iframe
}
```