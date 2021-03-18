#!/usr/bin/python3
import pika
import sys
import os
from config import mq_server, queue_name, db_name, db_user, db_host, db_password
import psycopg2
import json


# noinspection SqlNoDataSourceInspection
def db_insert_results(result: bytes):
    conn = psycopg2.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}')
    cur = conn.cursor()

    results = convert_byte_results_to_dict(result)

    # sql = f"""INSERT INTO pi_data.metrics (hostname, os, ip_address, cpu_usage_percent, cpu_frequency,
    # cpu_temperature, memory_usage_percent, memory_usage, swap_usage_percent, pi_timestamp)
    # VALUES ('{results.get('hostname')}', '{results.get('os')}', '{results.get('ip_address')}',
    #     {results.get('cpu_usage_percent')}, {results.get('cpu_frequency')}, {results.get('cpu_temperature')},
    #     {results.get('memory_usage_percent')}, {results.get('memory_usage')}, {results.get('swap_usage_percent')},
    #     '{results.get('timestamp')}')"""

    # print(sql)
    # cur.execute(sql)

    sql = """INSERT INTO pi_data.metrics (hostname, os, ip_address, cpu_usage_percent, cpu_frequency, 
    cpu_temperature, memory_usage_percent, memory_usage, swap_usage_percent, pi_timestamp) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""

    cur.execute(sql, (results.get('hostname'), results.get('os'), results.get('ip_address'),
                      results.get('cpu_usage_percent'), results.get('cpu_frequency'), results.get('cpu_temperature'),
                      results.get('memory_usage_percent'), results.get('memory_usage'), results.get('swap_usage_percent'),
                      results.get('timestamp')
                      ))

    new_rec_id: int = cur.fetchone()[0]
    if new_rec_id is not None:
        print(f"Record written successfully with ID: {new_rec_id}")
    conn.commit()

    # Close the connections out
    cur.close()
    conn.close()


def convert_byte_results_to_dict(results: bytes):
    import ast
    new_result = ast.literal_eval(results.decode('utf-8'))
    return new_result


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_server))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        db_insert_results(body)
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
