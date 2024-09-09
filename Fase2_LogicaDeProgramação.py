import csv
from collections import defaultdict
import matplotlib.pyplot as plt


def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'data': row['data'],
                'precipitacao': float(row['precip']) if row['precip'] else None,
                'temp_max': float(row['maxima']) if row['maxima'] else None,
                'temp_min': float(row['minima']) if row['minima'] else None,
                'umidade': float(row['um_relativa']) if row['um_relativa'] else None,
                'vento': float(row['vel_vento']) if row['vel_vento'] else None
            })
    return data


def filter_and_display_data(data, start_month, start_year, end_month, end_year, data_type):
    filtered_data = [row for row in data if start_year <= int(row['data'][6:]) <= end_year and
                     (start_month <= int(row['data'][3:5]) if int(row['data'][6:]) == start_year else True) and
                     (int(row['data'][3:5]) <= end_month if int(row['data'][6:]) == end_year else True)]
    
    print("\nDados filtrados:")
    if data_type == 'precipitacao':
        print("Data | Precipitação (mm)")
        for row in filtered_data:
            print(f"{row['data']} | {row['precipitacao']}")
    elif data_type == 'temperatura':
        print("Data | Temp. Máx (°C) | Temp. Mín (°C)")
        for row in filtered_data:
            print(f"{row['data']} | {row['temp_max']} | {row['temp_min']}")
    elif data_type == 'umidade_vento':
        print("Data | Umidade (%) | Vento (m/s)")
        for row in filtered_data:
            print(f"{row['data']} | {row['umidade']} | {row['vento']}")
    else:
        print("Data | Precipitação (mm) | Temp. Máx (°C) | Temp. Mín (°C) | Umidade (%) | Vento (m/s)")
        for row in filtered_data:
            print(f"{row['data']} | {row['precipitacao']} | {row['temp_max']} | {row['temp_min']} | {row['umidade']} | {row['vento']}")


def most_rainy_month(data):
    monthly_precipitation = defaultdict(float)
    
    for row in data:
        year_month = row['data'][3:7]  
        if row['precipitacao'] is not None:
            monthly_precipitation[year_month] += row['precipitacao']
    
    max_month = max(monthly_precipitation, key=monthly_precipitation.get)
    print(f"Mês mais chuvoso: {max_month} com {monthly_precipitation[max_month]:.2f} mm")


def avg_min_temp_last_11_years(data, target_month):
    temp_min_data = defaultdict(list)
    
    for row in data:
        year = int(row['data'][6:])
        month = int(row['data'][3:5])
        if 2006 <= year <= 2016 and month == target_month and row['temp_min'] is not None:
            temp_min_data[f"{year}-{month:02}"].append(row['temp_min'])
    
    avg_temp_min = {key: sum(values) / len(values) for key, values in temp_min_data.items()}
    
    print(f"\nMédias de temperatura mínima em {target_month:02} nos últimos 11 anos:")
    for year_month, avg in avg_temp_min.items():
        print(f"{year_month}: {avg:.2f}°C")
    
    return avg_temp_min

def plot_min_temp(avg_temp_min):
    years = list(avg_temp_min.keys())
    temps = list(avg_temp_min.values())
    
    plt.bar(years, temps, color='blue')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Média de Temperatura Mínima (°C)')
    plt.title('Médias de Temperatura Mínima dos Últimos 11 Anos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def overall_avg_min_temp(avg_temp_min):
    overall_avg = sum(avg_temp_min.values()) / len(avg_temp_min)
    print(f"\nMédia geral da temperatura mínima: {overall_avg:.2f}°C")

def main():
    data = read_csv_file('dados.csv')
    

    start_month, start_year = 1, 2006
    end_month, end_year = 12, 2016
    filter_and_display_data(data, start_month, start_year, end_month, end_year, 'temperatura')
    

    most_rainy_month(data)
    

    target_month = 8  
    avg_temp_min = avg_min_temp_last_11_years(data, target_month)
    

    plot_min_temp(avg_temp_min)
    

    overall_avg_min_temp(avg_temp_min)

if __name__ == '__main__':
    main()
