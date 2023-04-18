def temps_en_minutes(temps:str) -> int :
    if 'h' in temps:
        heures = int(temps.split('h')[0])
        minutes = int(temps.split('h')[1][0:-1])
        temps_en_minutes = (heures*60)+minutes
        return temps_en_minutes
    else:
        minutes = int(temps.split('m')[0])
        return minutes