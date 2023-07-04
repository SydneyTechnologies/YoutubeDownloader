from enum import Enum


class FormatCategory(Enum):
    BEST = 'bestvideo+bestaudio/best'
    BEST_MP4 = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    MAX_1080P = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    WORST = 'worstvideo+worstaudio/worst'


def resolveQuality(quality: str):
    return FormatCategory.BEST.value