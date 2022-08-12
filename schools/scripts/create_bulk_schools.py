from time import sleep
import requests

school_codes = [
    7451111, 7831028, 7841023, 7862015, 7862006, 7031215, 8222012, 7010186, 
    8750210, 7380030, 9290049, 7569072, 7091368, 7010125, 7061094, 7010170, 
    7130181, 7010227, 7130203, 7361037, 7321066, 7010132, 7031180, 7061058, 
    7181084, 7150396, 7310057, 7061067, 9051124, 7061079, 7191038, 7061064,
    7061088, 7541096, 7351007, 7031125, 7831015, 7821049, 8011200, 7561038, 
    8681015, 8681015, 7391067, 8151067, 8331045, 7010203, 7031198, 9101008, 
    9091015, 7150097, 7679016, 7010171, 7061102, 7271108, 7010278, 7010536, 
    7061105, 7611066, 7441046, 7821041, 7081463, 7631052, 7631069, 8320095, 
    8331117, 7341065, 8320109, 8331037, 7010059, 7061057, 7251055, 7430067,
    7351026, 9022059, 7530335, 7530497, 7541059, 7761038, 7240218, 8320093, 
    7631029, 7931023, 7530336, 7541025, 8490085, 8501016, 8501014, 7010204, 
    7132148, 7171051, 8921018, 8011204, 8061020, 8801122, 8222024, 8021071, 
    7010208, 7081522, 8391019, 7011488, 7031197, 7681063, 8051025, 8071028, 
    7281023, 8561021, 7132151, 7010244, 7010268, 7091457, 8341074, 8571012, 
    7010238, 7091455, 7010201, 7091453, 8111021, 8371081, 8761130, 8331075, 
    8531038
]
url = 'http://127.0.0.1:8000/api/v1/schools/'


# request post schoools for each school_code
for school_code in school_codes:
    response = requests.post(url data={'school_code': school_code})
    print(response.status_code)
    sleep(0.1)
