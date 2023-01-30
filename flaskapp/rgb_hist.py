import matplotlib.pyplot as plt

def get_plt_hist (image):
    rgb_im = image.convert('RGB') # Конвертируем в RGB

    # Создаем массивы для распределения цветов
    red = []
    green = []
    blue = []

    # Для каждой точки получаем значения цветов и добавляем их в массивы
    for x in range(image.size[0]):
      for y in range(image.size[0]):
        r, g, b = rgb_im.getpixel((x, y))
        red.append(r)
        green.append(g)
        blue.append(b)

    # Строим гистограммы для каждого цвета
    return plt.hist(red, bins=255, color='red'), plt.hist(green, bins=255, color='green'), plt.hist(blue, bins=255, color='blue'), plt.legend(['Red_Channel', 'Green_Channel', 'Blue_Channel'])
