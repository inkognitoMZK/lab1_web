import matplotlib.pyplot as plt
import numpy as np
import os
import secrets
from flask import Flask
from flask import render_template
from rgb_hist import get_plt_hist
from PIL import Image
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, FloatField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

app = Flask(__name__)

# генерируем csrf токен
SECRET_KEY = secrets.token_hex(16)
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта Google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf72f8jAAAAAI4om06ZZI8WojeeoTjRp8ZATd-p'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf72f8jAAAAAJQswjUhroF3mnCgXOTwmHEHV9hn'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
#для работы со стандартными шаблонами
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения уровня смешивания картинок, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные, если они не введены
 # или неверны
 flotFild = FloatField('Уровень смешивания от 0 до 1', validators=[NumberRange(0, 1, 'Укажите число от 0 до 1 !')])
 # поля загрузки файлов
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
  FileRequired(),
  FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 upload2 = FileField('Load image № 2', validators=[
     FileRequired(),
     FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('Начать')
# функция обработки запросов на адрес 127.0.0.1:5000
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
# метод обработки запроса GET и POST от клиента
@app.route("/",methods=['GET', 'POST'])
def start():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные, передаваемые в форму
 filename = None
 filename2 = None
 imgs = None
 level_mixing = None
 resimage_ = None
 new_image = None
 resim_ = None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  filename2 = os.path.join('./static', secure_filename(form.upload2.data.filename))
  # сохраняем загруженный файл
  form.upload.data.save(filename)
  form.upload2.data.save(filename2)
  # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
  # сети, если был нажат сабмит, либо передадим falsy значения
  img1 = Image.open(filename)
  img2 = Image.open(filename2)
  imgs = [np.array(i.resize((224, 224))) / 255.0 for i in [img1, img2]]
  # изменяем размер входных изображений на стандартный
  new_image = img1.resize((224, 224))
  new_image_2 = img2.resize((224, 224))
  # в качестве значения для смешивания берем значение из формы flotFild
  level_mixing = form.flotFild.data
  # смешиваем 2 изображения для получения результирующего изображения
  resimage_ = imgs[0] * level_mixing + imgs[1] * (1 - level_mixing)
  # переводим массив resimage_ в изображение чтобы с ним могла работать функция get_plt_hist
  resimage11 = Image.fromarray(resimage_, "RGB")
  # Создаем плот с введенными картинками, результатом смешивания и цветовыми гистограммами этих изображений
  plt.figure(figsize=(15, 15))
  plt.subplot(2, 3, 1)
  plt.imshow(img1)
  plt.subplot(2, 3, 2)
  plt.imshow(img2)
  plt.subplot(2, 3, 3)
  plt.imshow(resimage_)
  plt.subplot(2, 3, 4)
  get_plt_hist(new_image)
  plt.subplot(2, 3, 5)
  get_plt_hist(new_image_2)
  plt.subplot(2, 3, 6)
  get_plt_hist(resimage11)
  # Сохраняем результат в папку static
  plt.savefig(os.path.join('./static', '1.jpg'))
  resim_ = os.path.join('./static', '1.jpg')
  # передаем плот на отображение в html
 return render_template('start.html',form=form, image_name=resim_)

if __name__ == "__main__":
    app.run()
