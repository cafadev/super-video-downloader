import youtube_dl

def create_dict(url, quality, ext):
    """
    Create a dictionary with Args values
    Args:
        url (str): Video URL for download
        quality (str): Video quality
        ext (str): Video extension

    Returns:
        dict: Dictionary with args values

    """
    return {
        'url': url,
        'quality': quality,
        'ext': ext,
    }

def get_urls(url):
    """
    Create a dictionary with Args values
    Args:
        url (str): URL to track video

    Returns:
        dict: Dictionary with video information: title, thumbnail, formats(list type)
    """
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    response = {
        'title': video['title'],
        'thumbnail': video['thumbnail'],
        'formats':[]
    }

    # Get medium or/and high quality video formats.
    # Also can get video audio
    for fmt in video['formats']:
        if fmt['ext'] == 'mp4':

            if fmt['format_note'] == 'medium':
                response['formats'].append(create_dict(fmt['url'], 'medium', fmt['ext']))

            elif fmt['format_note'] == 'hd720':
                response['formats'].append(create_dict(fmt['url'], 'high', fmt['ext']))
                
            elif fmt['format_note'] == '720p':
                response['formats'].append(create_dict(fmt['url'], 'high', fmt['ext']))
        elif fmt['ext'] == 'm4a':
            response['formats'].append({
                'url': fmt['url'],
                'ext': 'm4a'
            })

    return response
