def delete_record(record_id, del_query):
    print(f'Delete record id={record_id}.')


def delete_position(position_id):
    delete_record(position_id, 'DELETE')

