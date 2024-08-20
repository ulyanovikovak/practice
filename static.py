import pandas as pd

def complex_distance(a, b):
    return a - b

def main():
    name = 'en_r1'
    # Чтение данных из CSV файла
    limits = [0.07, 0.08, 0.09, 0.1, 0.15, 0.2]
    for limit in limits:
        input_file = f'eigvals_with_limits_{name}_{limit}.csv'
        output_file = f'z_statistics_with_limits_{name}_{limit}.csv'

        # Чтение данных без заголовков
        data = pd.read_csv(input_file, header=None)

        # Проверка, что данные не пустые
        if data.empty:
            raise ValueError("CSV файл пуст или данные не были прочитаны.")

        # Преобразование строковых значений в комплексные числа
        data[0] = data[0].apply(lambda x: complex(x.replace('(', '').replace(')', '')))

        # Вычисление z-статистики
        z_statistics = []
        eigenvalues = data[0].values

        for i in range(len(eigenvalues)):
            distances = [complex_distance(eigenvalues[i], eigenvalues[j]) for j in range(len(eigenvalues)) if i != j]

            if len(distances) < 2:
                z_statistics.append(None)  # Недостаточно данных для вычисления z-статистики
                continue

            closest_distance = min(distances, key=abs)
            second_closest_distance = sorted(distances, key=abs)[1]

            z_stat = closest_distance / second_closest_distance
            z_statistics.append(z_stat)

        # Создание DataFrame для z-статистики
        z_statistics_df = pd.DataFrame({
            'z_statistic': z_statistics
        })

        # Запись результатов в новый CSV файл
        z_statistics_df.to_csv(output_file, index=False)

        print(f"Z-статистика записана в файл {output_file}")


if __name__ == '__main__':
    main()
