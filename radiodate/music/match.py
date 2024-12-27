from yandex_music import Client


class MatchMan:

    def __init__(self, first_token: str, second_token: str):
        self.first_client = Client(first_token).init()
        self.second_client = Client(second_token).init()

    @staticmethod
    def __get_all_albums_title(all_albums_obj: list):
        data = []
        for album_obj in all_albums_obj:
            data.append((album_obj.album["title"], album_obj.album.get_cover_url()))
        return data

    @staticmethod
    def __get_all_tracks_data(all_tracks_objs):
        data = []
        for track_obj in all_tracks_objs:
            if track_obj["id"] is None:
                continue
            data.append(track_obj["id"])

        return data

    def get_prepared_albums(self, client: Client):
        all_albums_objs1 = client.users_likes_albums()
        return self.__get_all_albums_title(all_albums_objs1)

    def get_prepared_tracks(self, client: Client):
        all_tracks_objs1 = client.users_likes_tracks()
        return self.__get_all_tracks_data(all_tracks_objs1)

    @staticmethod
    def get_match_album(
        first_album_prepared_data: list, second_album_prepared_data: list
    ):
        return list(set(first_album_prepared_data) & set(second_album_prepared_data))

    @staticmethod
    def get_match_percent(
        first_tracks_prepared_data: list, second_tracks_prepared_data: list
    ):
        union_tracks = set(first_tracks_prepared_data) & set(
            second_tracks_prepared_data
        )

        # Общее количество уникальных треков, лайкнутых обоими пользователями
        total_tracks = set(first_tracks_prepared_data) | set(
            second_tracks_prepared_data
        )

        # Процент совпадения
        percent_match = (
            (len(union_tracks) / len(total_tracks)) * 100 if total_tracks else 0
        )

        return percent_match

    def get_data(self):
        first_album_prepared_data = self.get_prepared_albums(self.first_client)
        second_album_prepared_data = self.get_prepared_albums(self.second_client)

        album_cover_url = self.get_match_album(
            first_album_prepared_data, second_album_prepared_data
        )
        if not album_cover_url:
            album_cover_url = "https://sun9-21.userapi.com/impg/h6NPKOhgyhA6bWylUSHQyYK7oniE_hxvYtkSkA/EULx8fU8Nos.jpg?size=736x721&quality=95&sign=3e99fe41a4b996cdf72fc6a2d3c34910&type=album"
        else:
            album_cover_url = album_cover_url[-1][-1]

        first_tracks_prepared_data = self.get_prepared_tracks(self.first_client)
        second_tracks_prepared_data = self.get_prepared_tracks(self.second_client)

        match_percent = self.get_match_percent(
            first_tracks_prepared_data, second_tracks_prepared_data
        )
        return {
            "album_cover_url": album_cover_url,
            "match_percent": match_percent,
        }
