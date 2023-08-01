import psycopg2
import plotly.graph_objects as go


def retrieve_data(db_config, sql_query):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while retrieving data:", error)
        return []


def generate_history_plot(data, plot_title, x_label, y_label, image_path):
    y_data = [row[0] for row in data]

    fig = go.Figure(data=[go.Histogram(x=y_data)])
    fig.update_layout(title=plot_title, xaxis_title=x_label, yaxis_title=y_label)
    fig.write_image(image_path)


def main():
    db_config = {
        "host": "bwlabsrv01",
        "port": 5432,
        "database": "dev_db",
        "user": "dev_user",
        "password": "dev_user_pwd"
    }

    sql_query = "SELECT results->>'sum' FROM dice_roll_2"

    plot_title = "Dice Roll History Plot"
    x_label = "Value"
    y_label = "Frequency"
    image_path = "dice_roll_history_plot.png"

    data = retrieve_data(db_config, sql_query)
    generate_history_plot(data, plot_title, x_label, y_label, image_path)


if __name__ == "__main__":
    main()

