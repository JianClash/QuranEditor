from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip,\
        vfx
from quran import Quran


qur = Quran()


def get_meaning_arabic():
    chp = int(input("Enter chapter: "))
    if chp == 0:
        test_mode()

    start = int(input("Enter verse to start from: "))
    num = int(input("No. of verses: "))


    arabic = []
    meaning = []

    for i in range(start, start+num):
        verse = qur.get_verse(chp, i)["verse"]

        arabic.append(verse["text_madani"])
        verse_meaning = ""

        for word in verse["words"]:
            verse_meaning += word["translation"]["text"] + " "
        meaning.append(verse_meaning)

    print(arabic, meaning)
    return arabic, meaning



def create_video(arabic, meaning):
    subs = []
    rec = AudioFileClip("/home/jianclash/Projects/QuranEditor/QuranEditor/assets/recordings/1.acc")
    bgclip = VideoFileClip("/home/jianclash/Projects/QuranEditor/QuranEditor/assets/videos/beach.mp4")


    if rec.duration < bgclip.duration:
        bgclip = bgclip.subclip(rec.duration)
    bgclip = bgclip.fx(vfx.colorx, 0.5).crop(x_center=bgclip.w//2, y_center=bgclip.h//2, width=1080, height=1920)\
            .resize((1080, 1920))
    subs.append(bgclip)


    for i in range(len(arabic)):
        text = TextClip(arabic[i], fontsize=60, size=(1060, None), font="Ubuntu-Arabic",\
            color="white", method='caption', align='center')
        text2 = TextClip(meaning[i], fontsize=60, size=(1060, None), font="UbuntuMono-Nerd-font",\
            color="white", method='caption', align='center')
        subs.append(text.set_position(("center", 0.4), relative=True).set_duration(5).set_start(i*5))
        subs.append(text2.set_position("center", 0.6).set_duration(5).set_start(i*5))


    combined = CompositeVideoClip(subs)
    combined.audio = CompositeAudioClip([rec])
    combined.write_videofile("outputs/out.mp4")



def test_mode():

    print("------ ENTERING TEST MODE ------")

    arabic = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
    meaning = 'In (the) name (of) Allah the Most Gracious the Most Merciful (1)'
    subs = []

    rec = AudioFileClip("/home/jianclash/Projects/QuranEditor/QuranEditor/assets/recordings/1.acc")\
            .subclip(0, 5)
    bgclip = VideoFileClip("/home/jianclash/Projects/QuranEditor/QuranEditor/assets/videos/beach.mp4")
    bgclip = bgclip.subclip(0, 5).fx(vfx.colorx, 0.5)\
            .crop(x_center=bgclip.w//2, y_center=bgclip.h//2, width=1080, height=1920).resize((1080, 1920))


    textArabic = TextClip(arabic, fontsize=60, size=(1060, None), font="Ubuntu-Arabic",\
            color="white", method='caption', align='center')
    textMeaning = TextClip(meaning, fontsize=60, size=(1060, None) ,font="UbuntuMono-Nerd-font",\
            color="white", method='caption', align='center')

    subs.append(bgclip)
    subs.append(textArabic.set_position(("center", 0.4), relative=True).set_duration(5).set_start(0))
    subs.append(textMeaning.set_position("center", 0.6).set_duration(5).set_start(0))

    combined = CompositeVideoClip(subs)
    combined.audio = CompositeAudioClip([rec])
    combined.write_videofile("outputs/out.mp4", audio=False)
    exit(0)



(arabic, meaning) = get_meaning_arabic()
create_video(arabic, meaning)
