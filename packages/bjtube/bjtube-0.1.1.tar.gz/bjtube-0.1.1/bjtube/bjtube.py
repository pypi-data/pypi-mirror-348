import yt_dlp
from datetime import datetime

def main():
    url = input("Enter YouTube video URL: ")

    def get_formats(info):
        formats = info.get('formats', [])
        usable_formats = []

        for fmt in formats:
            has_video = fmt.get('vcodec', 'none') != 'none'
            has_audio = fmt.get('acodec', 'none') != 'none'
            res = fmt.get('resolution') or f"{fmt.get('width')}x{fmt.get('height')}" or "audio only"
            ext = fmt.get('ext')
            format_id = fmt.get('format_id')

            if has_video and has_audio:
                label = '✅ Video+Audio'
            elif has_video and not has_audio:
                label = '🎞️ Video only (will merge)'
            elif has_audio and not has_video:
                label = '🔊 Audio only'
            else:
                label = '❓ Unknown'

            if has_video:
                usable_formats.append({
                    'id': format_id,
                    'ext': ext,
                    'res': res,
                    'label': label,
                    'has_audio': has_audio
                })

        return usable_formats

    def print_formats(formats):
        print("\n🎞️ Available formats with video (merged or direct):\n")
        for f in formats:
            print(f"ID: {f['id']:>4} | Ext: {f['ext']:<5} | Res: {f['res']:<12} | {f['label']}")

    def download_video(format_id, merge_audio=False):
        outtmpl = f"%(title).50s - {datetime.now().strftime('%Y%m%d-%H%M%S')}.%(ext)s"

        if merge_audio:
            format_string = f"{format_id}+bestaudio"
        else:
            format_string = format_id

        ydl_opts = {
            'format': format_string,
            'outtmpl': outtmpl,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        }

        print(f"\n⬇️ Downloading using format: {format_string}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # Fetch info
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = get_formats(info)
    print_formats(formats)

    selected_id = input("\nEnter the format ID to download: ").strip()
    selected = next((f for f in formats if f['id'] == selected_id), None)

    if selected:
        download_video(selected_id, merge_audio=not selected['has_audio'])
    else:
        print("❌ Invalid format ID.")
