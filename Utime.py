import time


def time_coute(function):
    def surrogate(*args, **kwargs):
        time_start = time.time()
        result = function(*args, **kwargs)
        time_finish = time.time()
        time_estimation_minets = int((time_finish - time_start)//60)
        time_estimation_secund = round((time_finish - time_start)%60, 2)
        print(f'Функция выполнялась {time_estimation_minets} минут и {time_estimation_secund} с')
        return result
    return surrogate