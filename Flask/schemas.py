from marshmallow import Schema, fields


class TweetSchema(Schema):
    tweet_data = fields.String(required=True)
    tweet_media_ids = fields.Dict(required=False)
