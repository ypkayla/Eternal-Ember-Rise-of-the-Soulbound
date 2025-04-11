# quest_templates.py
def create_quests_from_data(data):
    # Implementierung der Funktion basierend auf deinen Anforderungen
    quests = []
    for item in data:
        quests.append(Quest(item['id'], item['name'], item['description']))
    return quests
