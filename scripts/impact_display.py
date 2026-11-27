"""Static rendering counterpart of src/js/impact-display.js; never edits source scores."""
EMPTY = {
    'en': 'No scored impact entries have been recorded. This does not establish zero real-world impact or a completed impact audit.',
    'zhHans': '尚未录入可计分的影响条目；不表示实测影响为零，也不表示已经完成影响审计。',
}


def impact_index_label(event, language='en'):
    if event.get('impacts') == []:
        return '尚无已记录影响' if language == 'zhHans' else 'No impacts recorded'
    return str(event['impactIndex']) + '/10'
