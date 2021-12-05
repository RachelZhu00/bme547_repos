import base64
import io
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def plot_data(file_path):
    dataset = pd.read_csv(file_path)  # Read data from CSV datafile
    x, y = dataset.values[::50, 0], dataset.values[::50, 1]
    plt.plot(x, y)  # Draw the plot object
    plt.savefig('image/fig.png')


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def view_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return


def save_b64_image(base64_string, filename):
    image_bytes = base64.b64decode(base64_string)
    filepath = "image/"+filename+".jpg"
    with open(filepath, "wb") as out_file:
        out_file.write(image_bytes)
    return