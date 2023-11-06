import sqlite3


def is_student_linked_to_another_trainer(student_id, trainer_id):
    conn = sqlite3.connect('gym_helper.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relations WHERE student_id=? AND trainer_id!=?", (student_id, trainer_id))
    existing_relation = cursor.fetchone()
    conn.close()
    return existing_relation is not None
