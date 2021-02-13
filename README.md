#  🇮🇹 italy_coviddata
This repository is based on python scripts for compute and promptly analyse COVID cases data.

### Installation
For now, you can only clone the repository and enjoy its features.
```
$ git clone https://github.com/MCilento93/italy_coviddata.git
```

### Module /coviddata/italy_coviddata_curvefit
The module 'italy_coviddata_curvefit', by mean of pandas and the class CovidCurveFit is able to manage statistics and predictions on user-defined label from italy-official database from [github](https://github.com/pcm-dpc/COVID-19/blob/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv).
<p align="center">
  <img src="https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_curvefit.png" width="600px">
</p>

### Module /coviddata/italy_coviddata_regions
Like for provinces, this module shows daily updates of italian regions. Once again there is a class to instance for each region. Same story already told. The official source is again the pcm-dpc github profile [here](https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni)
<p align="center">
  <img src="https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_regions%20nuovi_positivi%20Campania.png" width="450px">
</p>

### Module /coviddata/italy_coviddata_provinces
This module elaborates the data of italian provinces. You can instance a CovidItalyProvince object to print/plot/save relevant values for a chosen italian-province (included daily-cases!). Once again the data are retrieved from official pcm-dpc github profile [here](https://github.com/pcm-dpc/COVID-19/tree/master/dati-province).
<p align="center">
  <img src="https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_provinces%20summary%20plot%20Salerno.png" width="450px">
</p>

### Module /coviddata/italy_coviddata_cities
This module searches on google-news feeds about the desired city. Will it manage to prompt, among the rest of locals facts, the correct number of positive cases?

### Module /coviddata/world_coviddata
A flash rapid-API will give you brief data on covid-19 for the desired foreign coutry.

### Module /coviddata/italy_coviddata_vaccines
Parser of vaccines data from open repository of [italia/covid19-opendata-vaccini](https://github.com/italia/covid19-opendata-vaccini)

### @italycoviddataBot the telegram-bot [ᴛʀʏ ɪᴛ ᴏᴜᴛ](https://t.me/italycoviddataBot)
Very intuitive commands allow you to use the above mentioned modules directly on telegram. Have a look at @italycoviddataBot.
<p align="center">
  <img src="https://github.com/MCilento93/italy_coviddata/blob/master/images/telegram%20screenshot.png" width="450px">
</p>

### Acknowledgments
* **[Dipartimento della Protezione Civile](https://github.com/pcm-dpc/COVID-19)** for the repository with open data on Covid19
* **[Governo Italiano website](http://www.governo.it/it/articolo/domande-frequenti-sulle-misure-adottate-dal-governo/15638?gclid=CjwKCAiAwrf-BRA9EiwAUWwKXicC1bzopYynHP9pvRxHUza7Ar4dte9hWHi55Uj4xfuAHanOCf7a1BoCTggQAvD_BwE)** for the content on the current color-status of italian regions
* **[italia/covid19-opendata-vaccini](https://github.com/italia/covid19-opendata-vaccini)** for maintaining the repository with open data on vaccines for italian regions and provinces
* **[RapidAPI/Gramzivi](https://rapidapi.com/Gramzivi/api/covid-19-data)** for the freemium and powerful API for world Covid19-data
* **[Iceloof](https://github.com/Iceloof/GoogleNews)** for the GoogleNews scraper, used for city data

### License
This repository is licensed under [GNU](LICENSE) (c) 2019 GitHub, Inc.
