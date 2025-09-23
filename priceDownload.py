from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
#https://storage.googleapis.com/chrome-for-testing-public/140.0.7339.80/win64/chrome-win64.zip
# Настройка за автоматично сваляне в папка
download_dir = r"C:\Users\user\Desktop\kursovaRabota\static\csvs\raw"  # смени пътя
options = Options()
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get("https://ibex.bg/markets/dam/day-ahead-prices-and-volumes-v2-0-2/")

time.sleep(5)  # изчакваме JS да зареди таблиците

# Извикваме функцията за CSV директно
driver.execute_script("csvFunc()")

time.sleep(10)  # време за сваляне на файла

driver.quit()
print("CSV файлът трябва да е свален в:", download_dir)



import pandas as pd

# Четем оригиналния CSV, като пропускаме първите редове, които не са таблица
df = pd.read_csv("Wed, 09_10 - Thu, 09_04.csv", sep=";", skiprows=10, header=None)

# Първата колона е часът, втората е единицата (EUR/MWh или MWh)
# Вземаме само редовете с EUR/MWh
eur_rows = df[df[1] == "EUR/MWh"]

# Изчистваме колоната с единицата
eur_rows = eur_rows.drop(columns=[1])

# Записваме в нов CSV
eur_rows.to_csv("static\csvs\eur_mwh.csv", index=False, header=False, sep=";")

print("Файлът eur_mwh.csv е създаден.")