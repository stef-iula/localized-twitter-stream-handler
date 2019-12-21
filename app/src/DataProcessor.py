import datetime
from psycopg2 import sql


class DataProcessor:

    def __init__(self, connection):
        self.connection = connection

    def process(self, data):
        user_row = self.make_user_row(data=data)
        tweet_row = self.make_tweet_row(data=data)
        self.write_user_row(row=user_row)
        self.write_tweet_row(row=tweet_row)
        self.write_hashtags(data=data)

    def get_user(self, id):
        cursor = self.connection.cursor()
        print('checking..')
        q = sql.SQL("""select id from twitter_user where id = %s""")
        try:
            cursor.execute(q, [id])
            user = cursor.fetchall()
            cursor.close()
            return user
        except Exception as error:
            raise Exception(error)

    def write_tweet_row(self, row):
        cursor = self.connection.cursor()
        print('writing tweet to db..')
        q = sql.SQL("""INSERT INTO tweet(id,
                    user_id,
                    created_at_utc,
                    location,
                    replied_to_user_id,
                    replied_to_tweet_id,
                    num_hashtags,
                    has_media,
                    text)
                VALUES
                   (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING""")
        try:
            cursor.execute(q, [row['tweet_id'],
                               row['user_id'],
                               datetime.datetime.strftime(row['created_at_utc'], "%Y-%m-%d %H:%M:%S%z")[:-2],
                               row['location'],
                               row['replied_to_user_id'],
                               row['replied_to_tweet_id'],
                               row['num_hashtags'],
                               row['has_media'],
                               row['text']])
            self.connection.commit()
            print('tweet {id} successfully written to db'.format(id=row['tweet_id']))
            cursor.close()
        except Exception as error:
            raise Exception(error)

    def write_user_row(self, row):
        cursor = self.connection.cursor()
        print('writing user to db..')
        q = sql.SQL("""INSERT INTO twitter_user(id,
                            screen_name,
                            description,
                            is_verified,
                            followers_count,
                            statuses_count)
                        VALUES
                            (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO
                            UPDATE
                            SET screen_name =  EXCLUDED.screen_name,
                                description =  EXCLUDED.description,
                                is_verified =  EXCLUDED.is_verified,
                                followers_count =  EXCLUDED.followers_count,
                                statuses_count =  EXCLUDED.statuses_count
                    """)

        try:
            cursor.execute(q, [row.get('user_id'),
                               row.get('screen_name'),
                               row.get('description'),
                               row.get('is_verified'),
                               row.get('followers_count'),
                               row.get('statuses_count')])
            self.connection.commit()
            print('user {id} successfully written to db'.format(id=row['user_id']))
            cursor.close()
        except Exception as error:
            raise Exception(error)

    def write_hashtags(self, data):
        is_truncated = data['truncated']
        if is_truncated:
            hashtags = data['extended_tweet']['entities']['hashtags']
        else:
            hashtags = data['entities']['hashtags']

        if len(hashtags) > 0:
            for hashtag in hashtags:
                cursor = self.connection.cursor()
                row = self.make_hashtag_row(data=data, hashtag=hashtag)
                print('writing hashtag to db..')
                q = sql.SQL("""INSERT INTO hashtag(tweet_id,
                                    user_id,
                                    tag,
                                    indices)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT DO NOTHING
                            """)
                try:
                    cursor.execute(q, [row.get('tweet_id'),
                                       row.get('user_id'),
                                       row.get('hashtag'),
                                       row.get('indices')])
                    self.connection.commit()
                    print('hashtag {tag} successfully written to db'.format(tag=row['hashtag']))
                    cursor.close()
                except Exception as error:
                    raise Exception(error)

    @staticmethod
    def make_user_row(data):
        user = data.get('user')

        user_id = user.get('id')
        screen_name = user.get('screen_name')
        description = user.get('description')
        is_verified = user.get('verified')
        followers_count = user.get('followers_count')
        statuses_count = user.get('statuses_count') 

        row = {
            'user_id': user_id,
            'screen_name': screen_name,
            'description': description,
            'is_verified': is_verified,
            'followers_count': followers_count,
            'statuses_count': statuses_count
        }

        return row

    @staticmethod
    def make_hashtag_row(data, hashtag):
        tweet_id = data['id']
        user_id = data['user']['id']
        tag = hashtag['text']
        indices = hashtag['indices']

        row = {
            'tweet_id': tweet_id,
            'user_id': user_id,
            'hashtag': tag,
            'indices': indices
        }

        return row

    def make_tweet_row(self, data):
        user_id = data['user']['id']
        tweet_id = data['id']
        created_at = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S %z %Y')
        location = data['location']
        replied_to_user_id = data['in_reply_to_user_id']
        replied_to_tweet_id = data['in_reply_to_status_id']
        is_truncated = data['truncated']
        extended_entities = data.get('extended_entities')
        if extended_entities is not None:
            media = data.get('extended_entities').get('media')
            has_media = True if media is not None else False
        else:
            has_media = False

        if is_truncated:
            num_hashtags = len(data['extended_tweet']['entities']['hashtags'])
            text = data['extended_tweet']['full_text']
        else:
            num_hashtags = len(data['entities']['hashtags'])
            text = data['text']

        row = {
            'user_id': user_id,
            'tweet_id': tweet_id,
            'created_at_utc': created_at,
            'location': location,
            'replied_to_user_id': replied_to_user_id,
            'replied_to_tweet_id': replied_to_tweet_id,
            'num_hashtags': num_hashtags,
            'has_media': has_media,
            'text': text
        }

        return row
