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
    - Bu sayede her gece 00 00'da veri ambarından güncel veriler çekilir ve 03 00'da python projemiz yeniden başlatılır ve güncel veriler dahsboard'lara dahil edilmiş olur.
- **__init__.py** ana FLASK uygulamamızı oluşturur
- **app.py** ana FLASK uygulamamıza ait bileşenleri barındırır (blueprints, routes, handlers vb)
- Ana dizindeki **myconfig.py** dosyası Flask uygulamasına ait ayarları tutmaktadır (static path, development mode vb.)
- Proje ile ilgili bütün fonksiyonlar, modüller, paketler vb **flaskapp** klasörü altında toplanmıştır
- **flaskapp/dashboard** klasörü altından DASH uygulamalarına erişebiliriz
- **flaskapp/dashboard/utilites/database_config.py** dosyası ambara bağlanılacak olan pymssql config bilgilerini içerir
- **flaskapp/dahsboard/utilities** klasörü altında işimizi kolaylaştıracak fonksiyonlar bulunmaktadır, varsa kendi yazdığımız componentler vb, veya dash uygulamalarının uyumluluğu için CSS sabitleri
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