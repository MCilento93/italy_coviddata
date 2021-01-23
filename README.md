# italy_coviddata
This repository is based on python scripts for compute and promptly analyse COVID cases data.

### module 'italy_coviddata_curvefit'
The module 'italy_coviddata_curvefit', by mean of pandas and the class CovidCurveFit is able to manage statistics and predictions on user-defined label from italy-official database from [github](https://github.com/pcm-dpc/COVID-19/blob/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv).
![data](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_curvefit%20data.png)
![fitting](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_curvefit%20fitting.png)
![integration](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_curvefit%20integration.png)
![summary_italy](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_curvefit%20summary%20plot.png)

### module 'italy_coviddata_regions'
Like for provinces, this module shows daily updates of italian regions. Once again there is a class to instance for each region. Same story already told. The official source is again the pcm-dpc github profile [here](https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni)
![daily](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_regions%20nuovi_positivi%20Campania.png)

### module 'italy_coviddata_provinces'
This module elaborates the data of italian provinces. You can instance a CovidItalyProvince object to print/plot/save relevant values for a chosen italian-province (included daily-cases!). Once again the data are retrived from official pcm-dpc github profile [here](https://github.com/pcm-dpc/COVID-19/tree/master/dati-province).
</br>![tot_cases](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_provinces%20totale_casi%20Salerno.png)
![summary_salerno](https://github.com/MCilento93/italy_coviddata/blob/master/images/italy_coviddata_provinces%20summary%20plot%20Salerno.png)

### module 'italy_coviddata_cities'
This module searches on google-news feeds about the desired city. Will it manage to prompt, among the rest of locals facts, the correct number of positive cases?

### module 'world_coviddata'
A flash rapid-API will give you brief data on covid-19 for the desired foreign coutry.

### @italycoviddataBot the telegram-bot [ᴛʀʏ ɪᴛ ᴏᴜᴛ](https://t.me/italycoviddataBot)
Very intuitive commands allow you to use the above mentioned modules directly on telegram. Have a look at @italycoviddataBot.
![telegram_screen](https://github.com/MCilento93/italy_coviddata/blob/master/images/telegram%20screenshot.png)
</br>New feature: custom-keyboards ⌨️ are arrived!

## License
This repository is licensed under [GNU](LICENSE) (c) 2019 GitHub, Inc.
