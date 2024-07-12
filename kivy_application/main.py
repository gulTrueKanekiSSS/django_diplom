import subprocess
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import requests
import cv2
import torch

django_project_path = '/Users/dmitrijzaharov/PycharmProjects/SmartInventory'
kivy_app_path = '/Users/dmitrijzaharov/PycharmProjects/SmartInventory/main.py'


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        btn_show_inventory = Button(text='Мои запасы')
        btn_show_inventory.bind(on_press=self.show_inventory)
        layout.add_widget(btn_show_inventory)

        btn_add_inventory = Button(text='Пополнить запасы')
        btn_add_inventory.bind(on_press=self.add_inventory)
        layout.add_widget(btn_add_inventory)

        Clock.schedule_once(self.start_django_server, 1)

        return layout

    def start_django_server(self, dt):
        os.chdir(django_project_path)
        self.process = subprocess.Popen(['python3', 'manage.py', 'runserver'])

    def stop_django_server(self):
        if self.process:
            self.process.terminate()

    def show_inventory(self, instance):
        try:
            response = requests.get('http://127.0.0.1/api/stocks/')
            products = response.json()
            content = '\n'.join([f"{product['name']}: {product['amount']}" for product in products])
        except Exception as e:
            content = f"Ошибка: {e}"

        popup = Popup(title='Мои запасы', content=Label(text=content), size_hint=(0.8, 0.8))
        popup.open()

    def add_inventory(self, instance):
        image_path, error = self.img_from_cam()
        if error:
            self.show_popup('Ошибка камеры', error)
            return

        products = self.process_image(image_path)
        for product in products:
            self.save_inventory_to_db(product)

    def save_inventory_to_db(self, product):
        try:
            response = requests.post('http://127.0.0.1/api/stocks/', json=product)
            if response.status_code == 201:
                content = "Запасы успешно пополнены!"
            else:
                content = f"Ошибка: {response.status_code}"
        except Exception as e:
            content = f"Ошибка: {e}"

        self.show_popup('Пополнение запасов', content)

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(0.8, 0.8))
        popup.open()

    def img_from_cam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None, "Не удалось открыть камеру"

        ret, frame = cap.read()
        if not ret:
            return None, "Не удалось захватить изображение"

        captured_image_path = 'images/captured_image.jpg'
        os.makedirs(os.path.dirname(captured_image_path), exist_ok=True)
        cv2.imwrite(captured_image_path, frame)
        cap.release()
        return captured_image_path, None

    def process_image(self, image_path):
        try:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            results = model(image_path)
            products = self.extract_products(results)
            return products
        except Exception as e:
            self.show_popup('Ошибка обработки изображения', str(e))
            return []

    def extract_products(self, results):
        class_names = results.names  # Имена классов
        product_counts = {}

        for result in results.xyxy[0]:
            cls = int(result[5])
            product_name = class_names[cls]
            if product_name in product_counts:
                product_counts[product_name] += 1
            else:
                product_counts[product_name] = 1

        products = [{'name': name, 'amount': quantity} for name, quantity in product_counts.items()]
        return products

    def on_stop(self):
        self.stop_django_server()


if __name__ == '__main__':
    MyApp().run()

