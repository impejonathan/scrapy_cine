def temps_en_minutes(temps: str) -> int:
    if temps is None or temps.strip() == '':
        return None
    if 'h' in temps:
        heures = int(temps.split('h')[0])
        if 'm' in temps:
            minutes = int(temps.split('h')[1].split('m')[0])
        else:
            minutes = 0
        temps_en_minutes = (heures*60)+minutes
        return temps_en_minutes
    else:
        minutes = int(temps.split('m')[0])
        return minutes


def drop_back_to_top(x:str) -> list:
    return ", ".join(x.split(',')[:-1]) + ']'

def split_comma(x:str) -> list:
    return x.split(',')