from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class User(db.Model):
    """Users of WanderList."""

    __tablename__ = "users"

    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User username: {}, name: {}{}>".format(self.username, self.first_name,
                                                        self.last_name)


class BucketList(db.Model):
    """Bucket lists of travel items."""

    __tablename__ = "bucket_lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(32), db.ForeignKey('users.username'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Bucket List list_id: {}, title: {}, username: {}>".format(
                                                                          self.list_id, 
                                                                          self.title, 
                                                                          self.username)

    user = db.relationship("User",
                            backref=db.backref("bucket_lists",
                                               order_by=username))

class PublicItem(db.Model):
    """Public bucket list items."""

    __tablename__ = "public_items"

    public_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.LatLon, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Public Item public_item_id: {} title: {}>".format(self.public_item_id, self.title)

class PrivateItem(db.Model):
    """Private bucket list items."""

    __tablename__ = "private_items"

    priv_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    public_item_id = db.Column(db.Integer, db.ForeignKey("PublicItem.public_item_id"))
    list_id = db.Column(db.Integer, db.ForeignKey("BucketList.list_id"))
    tour_link = db.Column(db.String(200), nullable=True)
    checked_off = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=DateTime.now, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)

    public_item = db.relationship("PublicItem",
                                    backref=db.backref("priv_items",
                                               order_by=public_item_id))

    bucket_list = db.relationship("BucketList",
                                backref=db.backref("priv_items",
                                           order_by=list_id))

    def __repr__(self):
        """Private bucket list items."""

        return "<PrivateItem priv_item_id: {} list_id: {}>".format(self.priv_item_id,
                                                                   self.list_id)

    



