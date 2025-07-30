# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2019 Tobias Gruetzmacher
# SPDX-FileCopyrightText: © 2019 Daniel Ring
import logging

from ..scraper import ParserScraper

logger = logging.getLogger(__name__)


class Tapas(ParserScraper):
    baseUrl = 'https://tapas.io/'
    imageSearch = '//article[contains(@class, "js-episode-article")]//img/@data-src'
    prevSearch = '//a[contains(@class, "js-prev-ep-btn")]'
    latestSearch = '//ul[contains(@class, "js-episode-list")]//a'
    multipleImagesPerStrip = True

    def __init__(self, name, url):
        super().__init__('Tapas/' + name)
        self.url = self.baseUrl + 'series/' + url + '/info'
        self.stripUrl = self.baseUrl + 'episode/%s'

    def starter(self):
        # Retrieve comic metadata from info page
        info = self.getPage(self.url)
        series = self.match(info, '//@data-series-id')[0]
        # Retrieve comic metadata from API
        data = self.session.get(self.baseUrl + 'series/' + series + '/episodes?sort=NEWEST')
        data.raise_for_status()
        episodes = data.json()['data']['body']
        return self.stripUrl % episodes.split('data-id="')[1].split('"')[0]

    def getPrevUrl(self, url, data):
        # Retrieve comic metadata from API
        data = self.session.get(url + '/info')
        data.raise_for_status()
        apiData = data.json()['data']
        if apiData['scene'] == 2:
            self.firstStripUrl = self.stripUrl % apiData['prev_ep_id']
        return self.stripUrl % apiData['prev_ep_id']

    def extract_image_urls(self, url, data):
        # Save link order for position-based filenames
        self._cached_image_urls = super().extract_image_urls(url, data)
        return self._cached_image_urls

    def shouldSkipUrl(self, url, data):
        if self.match(data, '//button[d:class("js-have-to-sign")]'):
            logger.warning('Nothing to download on %r, because a login is required.', url)
            return True
        return False

    def namer(self, imageUrl, pageUrl):
        # Construct filename from episode number and image position on page
        episodeNum = pageUrl.rsplit('/', 1)[-1]
        imageNum = self._cached_image_urls.index(imageUrl)
        imageExt = pageUrl.rsplit('.', 1)[-1]
        if len(self._cached_image_urls) > 1:
            filename = "%s-%d.%s" % (episodeNum, imageNum, imageExt)
        else:
            filename = "%s.%s" % (episodeNum, imageExt)
        return filename

    @classmethod
    def getmodules(cls):
        return (
            # Manually-added comics
            cls('AmpleTime', 'Ample-Time'),
            cls('FANGS', 'fangscomic'),
            cls('FishNuggets', 'Fish-Nuggets'),
            cls('Ginpu', 'Ginpu-Studios-Comics'),
            cls('InsignificantOtters', 'IOtters'),
            cls('MagicalBoy', 'magicalboy'),
            cls('NoFuture', 'NoFuture'),
            cls('OrensForge', 'OrensForge'),
            cls('RadioactivePanda', 'Radioactive-Panda'),
            cls('RavenWolf', 'RavenWolf'),
            cls('SyntheticInstinct', 'Synthetic-Instinct'),
            cls('TheCatTheVineAndTheVictory', 'The-Cat-The-Vine-and-The-Victory'),
            cls('TheInkApprentice', 'The-Ink-Apprentice'),
            cls('TheSeaInYou', 'theseainyou'),
            cls('TheSelkiesSkin', 'theselkiesskincomic'),
            cls('TheWitchsThrone', 'thewitchsthrone'),
            cls('VenturaCityDrifters', 'Ventura-City-Drifters'),

            # START AUTOUPDATE
            # END AUTOUPDATE
        )
