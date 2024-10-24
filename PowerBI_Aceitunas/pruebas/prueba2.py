def process_page(year = 0, month = 1, mes = 1, taric = 0):
    url = 'http://aduanas.camaras.org/index.phpc?impexp=E&anno={year}&mes={month}&22tipo=ORGDES&meses=%2201%22&producto=TA&codprod={taric}&areanacional=PR&codareanac=&areainternac=PS&codareainter=400&result=PR&orden=LOCAL&tipo=ORGDES'.format(year=year, month=month, mes=mes, taric=taric)
    for year in range(15, 23):
        for month in range(1, 13):
            if month <= 1 and month <= 9:
                month = '0' + str(month)
                for mes in range(1,13):
                    if mes <= 1 and mes <= 9:
                        mes = '0' + str(month)
                    process_page(str(year), str(month), str(mes), taric='20057000')
                    break
    
    print(url)