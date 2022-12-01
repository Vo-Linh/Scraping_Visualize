import base64
from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns


def statisticsWeather(df, date, name):

    # Generate the figure **without using pyplot**.
    fig = plt.Figure(figsize=(8, 5))
    ax = fig.subplots()
    ax.plot(df[name])
    ax.set_xticks(date, rotation=55)
    ax.set_xticklabels(date, rotation=45, fontsize=10)
    ax.set_title(name, fontsize=14)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    img_path = f'data:image/png;base64,{img_data}'

    return img_path

def correlationWeather(df, cols, rows):


    # Generate the figure **without using pyplot**.
    fig = plt.Figure(figsize=(4, 4))
    ax = fig.subplots()
    sns.regplot(x=cols, 
               y=rows, 
               data=df, 
               ax = ax)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    img_path = f'data:image/png;base64,{img_data}'

    return img_path

# https://gist.github.com/mjanv/90d4ef43edbff3f3b0fc
